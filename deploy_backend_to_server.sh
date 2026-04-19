#!/bin/bash
# 上传最新 backend 到服务器并重启、测试
# 请在 Mac 自带的「终端」或 iTerm 中执行（不要用 Cursor 内置终端）:
#   cd /Users/yy/Documents/GitHub/eceshi && ./deploy_backend_to_server.sh
#
# 服务器: 8.148.188.85  root  Ceshi@123  后台目录: /www/wwwroot/ceshi/backend  端口: 3001
#
# 上传方式：使用 rsync，只会传输有改动的文件（按大小/修改时间），未改动的不会重传，速度更快。

set -e
SERVER="8.148.188.85"
USER="root"
REMOTE_DIR="/www/wwwroot/ceshi/backend"
LOCAL_DIR="$(cd "$(dirname "$0")/backend" && pwd)"
SSHPASS_PWD="Ceshi@123"
BACKEND_PORT="3001"
PUBLIC_URL="https://www.keyanbaice.com"

echo "========== 1. 上传 backend 到服务器（仅传输有改动的文件）=========="
sshpass -p "$SSHPASS_PWD" rsync -avz --delete \
  --exclude '.env' \
  --exclude '__pycache__' \
  --exclude '*.pyc' \
  --exclude '.git' \
  --exclude 'venv' \
  --exclude '*.pid' \
  --exclude '.env.backup*' \
  -e "ssh -o StrictHostKeyChecking=accept-new" \
  "$LOCAL_DIR/" "$USER@$SERVER:$REMOTE_DIR/"

echo ""
echo "========== 2. 服务器上安装依赖并重启服务 =========="
sshpass -p "$SSHPASS_PWD" ssh -o StrictHostKeyChecking=accept-new "$USER@$SERVER" "cd $REMOTE_DIR && (command -v pip3 >/dev/null && pip3 install -r requirements.txt -q -i https://pypi.tuna.tsinghua.edu.cn/simple || pip install -r requirements.txt -q) 2>/dev/null; (supervisorctl restart eceshi 2>/dev/null) || (supervisorctl restart ceshi 2>/dev/null) || true; (systemctl restart eceshi 2>/dev/null) || (systemctl restart ceshi 2>/dev/null) || true; sleep 3"

echo ""
echo "========== 3. 测试 API =========="

# 先从服务器本机检查服务是否真正启动
HTTP_CODE_LOCAL=$(sshpass -p "$SSHPASS_PWD" ssh -o StrictHostKeyChecking=accept-new "$USER@$SERVER" \
  "curl -s -o /dev/null -w \"%{http_code}\" --connect-timeout 5 http://127.0.0.1:$BACKEND_PORT/health 2>/dev/null || echo 000")
if [ "$HTTP_CODE_LOCAL" = "200" ]; then
  echo "服务器本机健康检查通过 (http://127.0.0.1:$BACKEND_PORT/health) HTTP $HTTP_CODE_LOCAL"
else
  echo "服务器本机健康检查失败 HTTP $HTTP_CODE_LOCAL"
fi

# 再测外网 IP 直连端口
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "http://$SERVER:$BACKEND_PORT/api/v1/projects/categories" 2>/dev/null || echo "000")
if [ "$HTTP_CODE" = "200" ]; then
  echo "外网端口测试通过 (http://$SERVER:$BACKEND_PORT) HTTP $HTTP_CODE"
  curl -s "http://$SERVER:$BACKEND_PORT/api/v1/projects/categories" | head -c 200
  echo ""
else
  echo "外网端口测试未通过 (http://$SERVER:$BACKEND_PORT) HTTP $HTTP_CODE"
fi

# 兼容仅开放 80 的情况
HTTP_CODE80=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "http://$SERVER/api/v1/projects/categories" 2>/dev/null || echo "000")
if [ "$HTTP_CODE80" = "200" ]; then
  echo "外网 80 端口测试通过 (http://$SERVER) HTTP $HTTP_CODE80"
  curl -s "http://$SERVER/api/v1/projects/categories" | head -c 200
  echo ""
else
  echo "外网 80 端口测试未通过 (http://$SERVER) HTTP $HTTP_CODE80"
fi

# 如果服务器 .env 配置了站点域名，优先用 .env；否则回退到当前项目默认域名
ENV_PUBLIC_URL=$(sshpass -p "$SSHPASS_PWD" ssh -o StrictHostKeyChecking=accept-new "$USER@$SERVER" \
  "cd $REMOTE_DIR && grep -E '^SITE_BASE_URL=' .env 2>/dev/null | tail -n1 | cut -d= -f2-" | tr -d '\r')
if [ -n "$ENV_PUBLIC_URL" ]; then
  PUBLIC_URL="$ENV_PUBLIC_URL"
fi

if [ -n "$PUBLIC_URL" ]; then
  DOMAIN_API_URL="${PUBLIC_URL%/}/api/v1/projects/categories"
  HTTP_CODE_DOMAIN=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 8 "$DOMAIN_API_URL" 2>/dev/null || echo "000")
  if [ "$HTTP_CODE_DOMAIN" = "200" ]; then
    echo "域名业务接口检查通过 ($DOMAIN_API_URL) HTTP $HTTP_CODE_DOMAIN"
    curl -s "$DOMAIN_API_URL" | head -c 200
    echo ""
  else
    echo "域名业务接口检查未通过 ($DOMAIN_API_URL) HTTP $HTTP_CODE_DOMAIN"
  fi
fi

if [ "$HTTP_CODE_LOCAL" != "200" ] && [ "$HTTP_CODE" != "200" ] && [ "$HTTP_CODE80" != "200" ]; then
  echo "请检查: 1) 服务是否成功启动 2) 服务器防火墙是否放行 $BACKEND_PORT 或 80 3) 宝塔/Nginx 反向代理是否指向 localhost:$BACKEND_PORT"
  echo "可先 SSH 登录检查: ssh $USER@$SERVER"
fi

echo ""
echo "========== 部署完成 =========="
