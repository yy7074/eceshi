#!/bin/bash
# 部署后冒烟测试脚本
#
# 用法:
#   ./deploy_smoke_test.sh https://www.keyanbaice.com
#   BASE_URL=https://www.keyanbaice.com ./deploy_smoke_test.sh
#   REMOTE_HOST=8.148.188.85 REMOTE_USER=root SSHPASS_PWD='***' BACKEND_PORT=3001 ./deploy_smoke_test.sh
#
# 可选环境变量:
#   BASE_URL              公网访问地址，脚本参数优先
#   BACKEND_PORT          服务器后端端口，默认 3001
#   REMOTE_HOST           服务器 IP/域名；设置后会通过 SSH 检查 127.0.0.1:$BACKEND_PORT/health
#   REMOTE_USER           SSH 用户，默认 root
#   REMOTE_DIR            后端部署目录；设置后会读取 .env 中的 SITE_BASE_URL
#   SSHPASS_PWD           sshpass 密码；不设置则跳过远程本机检查
#   CHECK_TIMEOUT         curl 超时时间，默认 8 秒
#   CHECK_WEB             是否检查 /web，默认 1
#   CHECK_ADMIN_PAGE      是否检查 /admin，默认 1
#   CHECK_DIRECT_IP       设置 REMOTE_HOST 后是否探测 IP 直连端口和 80 端口，默认 1
#   CHECK_DOCS            是否检查 /api/docs，默认 0
#   ADMIN_USERNAME        设置后会测试管理员登录
#   ADMIN_PASSWORD        管理员密码；和 ADMIN_USERNAME 同时设置才生效
#   CURL_INSECURE         设置为 1 时跳过 HTTPS 证书校验

set -u

BASE_URL="${1:-${BASE_URL:-https://www.keyanbaice.com}}"
BACKEND_PORT="${BACKEND_PORT:-3001}"
REMOTE_HOST="${REMOTE_HOST:-}"
REMOTE_USER="${REMOTE_USER:-root}"
REMOTE_DIR="${REMOTE_DIR:-}"
SSHPASS_PWD="${SSHPASS_PWD:-}"
CHECK_TIMEOUT="${CHECK_TIMEOUT:-8}"
CHECK_WEB="${CHECK_WEB:-1}"
CHECK_ADMIN_PAGE="${CHECK_ADMIN_PAGE:-1}"
CHECK_DIRECT_IP="${CHECK_DIRECT_IP:-1}"
CHECK_DOCS="${CHECK_DOCS:-0}"
ADMIN_USERNAME="${ADMIN_USERNAME:-}"
ADMIN_PASSWORD="${ADMIN_PASSWORD:-}"
CURL_INSECURE="${CURL_INSECURE:-0}"

BASE_URL="${BASE_URL%/}"

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'
if [ ! -t 1 ]; then
    GREEN=''
    RED=''
    YELLOW=''
    NC=''
fi

TMP_FILES=()
TMP_FILES_SET=0
PASS_COUNT=0
WARN_COUNT=0
FAIL_COUNT=0

cleanup() {
    local file
    if [ "$TMP_FILES_SET" != "1" ]; then
        return 0
    fi
    for file in "${TMP_FILES[@]}"; do
        [ -f "$file" ] && rm -f "$file"
        [ -f "$file.err" ] && rm -f "$file.err"
    done
}
trap cleanup EXIT

make_tmp() {
    local file
    file="$(mktemp)"
    TMP_FILES+=("$file")
    TMP_FILES_SET=1
    printf '%s' "$file"
}

log_pass() {
    PASS_COUNT=$((PASS_COUNT + 1))
    echo -e "${GREEN}✓${NC} $1"
}

log_warn() {
    WARN_COUNT=$((WARN_COUNT + 1))
    echo -e "${YELLOW}!${NC} $1"
}

log_skip() {
    echo "- $1"
}

log_fail() {
    FAIL_COUNT=$((FAIL_COUNT + 1))
    echo -e "${RED}✗${NC} $1"
}

require_command() {
    if ! command -v "$1" >/dev/null 2>&1; then
        log_fail "缺少命令: $1"
        return 1
    fi
    return 0
}

curl_code() {
    local url=$1
    local output_file=$2
    local code
    local args=(-sS -L --connect-timeout "$CHECK_TIMEOUT" --max-time "$CHECK_TIMEOUT" --noproxy '*' -o "$output_file" -w "%{http_code}")
    if [ "$CURL_INSECURE" = "1" ]; then
        args=(-k "${args[@]}")
    fi
    code="$(curl "${args[@]}" "$url" 2>"$output_file.err" || true)"
    if [ -z "$code" ]; then
        code="000"
    fi
    printf '%s' "$code"
}

body_has_text() {
    local body_file=$1
    local pattern=$2
    grep -Eiq "$pattern" "$body_file"
}

json_field_in() {
    local body_file=$1
    local field=$2
    local expected_values=$3
    python3 - "$body_file" "$field" "$expected_values" <<'PY'
import json
import sys

path, field, expected_values = sys.argv[1:4]
try:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
except Exception:
    sys.exit(1)

value = data
for part in field.split("."):
    if isinstance(value, dict) and part in value:
        value = value[part]
    else:
        sys.exit(1)

if str(value) in expected_values.split():
    sys.exit(0)
sys.exit(1)
PY
}

short_body() {
    local body_file=$1
    python3 - "$body_file" <<'PY'
import re
import sys

path = sys.argv[1]
try:
    text = open(path, "r", encoding="utf-8", errors="replace").read()
except Exception:
    sys.exit(0)

text = re.sub(r"\s+", " ", text).strip()
print(text[:220])
PY
}

check_http() {
    local name=$1
    local url=$2
    local expected_codes=$3
    local body_pattern=${4:-}
    local required=${5:-1}
    local body
    local code
    body="$(make_tmp)"
    code="$(curl_code "$url" "$body")"

    if [[ " $expected_codes " == *" $code "* ]]; then
        if [ -n "$body_pattern" ] && ! body_has_text "$body" "$body_pattern"; then
            if [ "$required" = "1" ]; then
                log_fail "$name HTTP $code 但响应内容不符合预期: $(short_body "$body")"
            else
                log_warn "$name HTTP $code 但响应内容不符合预期"
            fi
            return 1
        fi
        log_pass "$name HTTP $code"
        return 0
    fi

    if [ "$required" = "1" ]; then
        log_fail "$name HTTP ${code}，地址: ${url}，响应: $(short_body "$body")"
    else
        log_warn "$name HTTP ${code}，地址: ${url}"
    fi
    return 1
}

check_json_api() {
    local name=$1
    local url=$2
    local required=${3:-1}
    local success_codes=${4:-200}
    local body
    local code
    body="$(make_tmp)"
    code="$(curl_code "$url" "$body")"

    if [ "$code" != "200" ]; then
        if [ "$required" = "1" ]; then
            log_fail "$name HTTP ${code}，地址: ${url}，响应: $(short_body "$body")"
        else
            log_warn "$name HTTP ${code}，地址: ${url}"
        fi
        return 1
    fi

    if json_field_in "$body" "code" "$success_codes"; then
        log_pass "$name HTTP 200 且 code 在 [$success_codes]"
        return 0
    fi

    if [ "$required" = "1" ]; then
        log_fail "$name HTTP 200 但 JSON code 不在 [$success_codes]，响应: $(short_body "$body")"
    else
        log_warn "$name HTTP 200 但 JSON code 不在 [$success_codes]"
    fi
    return 1
}

remote_ssh() {
    local command=$1
    sshpass -p "$SSHPASS_PWD" ssh -o StrictHostKeyChecking=accept-new "$REMOTE_USER@$REMOTE_HOST" "$command"
}

detect_remote_public_url() {
    if [ -z "$REMOTE_HOST" ] || [ -z "$REMOTE_DIR" ] || [ -z "$SSHPASS_PWD" ]; then
        return 0
    fi

    local url
    url="$(remote_ssh "cd '$REMOTE_DIR' && grep -E '^SITE_BASE_URL=' .env 2>/dev/null | tail -n1 | cut -d= -f2-" 2>/dev/null | tr -d '\r')"
    if [ -n "$url" ]; then
        BASE_URL="${url%/}"
    fi
}

check_remote_local_health() {
    if [ -z "$REMOTE_HOST" ] || [ -z "$SSHPASS_PWD" ]; then
        log_skip "未配置 REMOTE_HOST/SSHPASS_PWD，跳过服务器本机健康检查"
        return 0
    fi

    if ! require_command sshpass; then
        return 1
    fi

    local command
    local code
    command="curl -s -o /dev/null -w '%{http_code}' --connect-timeout 5 --max-time 8 http://127.0.0.1:$BACKEND_PORT/health 2>/dev/null || echo 000"
    code="$(remote_ssh "$command" 2>/dev/null | tail -n1 | tr -d '\r')"
    if [ "$code" = "200" ]; then
        log_pass "服务器本机健康检查 HTTP 200"
        return 0
    fi

    log_fail "服务器本机健康检查失败 HTTP ${code:-000}，请检查 127.0.0.1:$BACKEND_PORT"
    return 1
}

check_direct_ip_access() {
    if [ "$CHECK_DIRECT_IP" != "1" ]; then
        log_skip "CHECK_DIRECT_IP=0，跳过外网 IP 直连检查"
        return 0
    fi

    if [ -z "$REMOTE_HOST" ]; then
        log_skip "未配置 REMOTE_HOST，跳过外网 IP 直连检查"
        return 0
    fi

    check_json_api "外网 IP 直连后端端口" "http://$REMOTE_HOST:$BACKEND_PORT/api/v1/projects/categories" 0
    check_json_api "外网 IP 80 端口" "http://$REMOTE_HOST/api/v1/projects/categories" 0
}

check_admin_login() {
    if [ -z "$ADMIN_USERNAME" ] || [ -z "$ADMIN_PASSWORD" ]; then
        log_skip "未配置 ADMIN_USERNAME/ADMIN_PASSWORD，跳过管理员登录检查"
        return 0
    fi

    local body
    local code
    body="$(make_tmp)"
    code="$(curl -sS -L --connect-timeout "$CHECK_TIMEOUT" --max-time "$CHECK_TIMEOUT" --noproxy '*' \
        -H "Content-Type: application/json" \
        -d "{\"username\":\"$ADMIN_USERNAME\",\"password\":\"$ADMIN_PASSWORD\"}" \
        -o "$body" -w "%{http_code}" \
        "$BASE_URL/api/v1/auth/admin-login" 2>"$body.err" || true)"
    if [ -z "$code" ]; then
        code="000"
    fi

    if [ "$code" != "200" ]; then
        log_fail "管理员登录 HTTP ${code}，响应: $(short_body "$body")"
        return 1
    fi

    if python3 - "$body" <<'PY'
import json
import sys

try:
    data = json.load(open(sys.argv[1], encoding="utf-8"))
except Exception:
    sys.exit(1)

token = ((data.get("data") or {}).get("access_token"))
sys.exit(0 if data.get("code") == 200 and token else 1)
PY
    then
        log_pass "管理员登录接口可用"
        return 0
    fi

    log_fail "管理员登录返回结构异常，响应: $(short_body "$body")"
    return 1
}

main() {
    echo "========== 部署冒烟测试 =========="

    require_command curl
    require_command grep
    require_command python3

    detect_remote_public_url
    echo "公网地址: $BASE_URL"
    echo "后端端口: $BACKEND_PORT"
    echo ""

    check_remote_local_health
    check_direct_ip_access

    check_http "公网健康检查" "$BASE_URL/health" "200" '"status"[[:space:]]*:[[:space:]]*"healthy"'
    check_http "公网根路由" "$BASE_URL/" "200" '"status"[[:space:]]*:[[:space:]]*"running"'
    check_json_api "项目分类接口" "$BASE_URL/api/v1/projects/categories"
    check_json_api "项目列表接口" "$BASE_URL/api/v1/projects/list?page=1&page_size=2"
    check_json_api "轮播图接口" "$BASE_URL/api/v1/banners/list" 0 "0 200"
    check_json_api "帮助分类接口" "$BASE_URL/api/v1/help/categories" 0 "0 200"
    check_json_api "充值规则接口" "$BASE_URL/api/v1/recharge/bonus/rules" 0

    if [ "$CHECK_WEB" = "1" ]; then
        check_http "Web 网站页面" "$BASE_URL/web" "200" '<html|科研|检测|百测'
        check_http "Web 静态资源" "$BASE_URL/static/web/assets/js/app.js" "200" 'axios|createApp|api'
    else
        log_skip "CHECK_WEB=0，跳过 Web 网站页面检查"
    fi

    if [ "$CHECK_ADMIN_PAGE" = "1" ]; then
        check_http "后台管理页面" "$BASE_URL/admin" "200" '<html|后台|管理|Element'
    else
        log_skip "CHECK_ADMIN_PAGE=0，跳过后台管理页面检查"
    fi

    if [ "$CHECK_DOCS" = "1" ]; then
        check_http "API 文档页面" "$BASE_URL/api/docs" "200" 'Swagger|openapi|docs' 0
    fi

    check_admin_login

    echo ""
    echo "========== 测试结果 =========="
    echo "通过: $PASS_COUNT"
    echo "警告: $WARN_COUNT"
    echo "失败: $FAIL_COUNT"

    if [ "$FAIL_COUNT" -gt 0 ]; then
        echo -e "${RED}部署冒烟测试未通过。${NC}"
        return 1
    fi

    echo -e "${GREEN}部署冒烟测试通过。${NC}"
    return 0
}

main "$@"
