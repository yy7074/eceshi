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
WEB_STATIC_DIR="/www/wwwroot/eceshi/backend/static/web"
ADMIN_STATIC_DIR="/www/wwwroot/eceshi/backend/admin"
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
  --exclude 'static/uploads' \
  -e "ssh -o StrictHostKeyChecking=accept-new" \
  "$LOCAL_DIR/" "$USER@$SERVER:$REMOTE_DIR/"

echo ""
echo "========== 1.1 同步网站静态目录 =========="
sshpass -p "$SSHPASS_PWD" ssh -o StrictHostKeyChecking=accept-new "$USER@$SERVER" \
  "if [ -d \"$(dirname "$WEB_STATIC_DIR")\" ]; then mkdir -p \"$WEB_STATIC_DIR\" && rsync -a --delete \"$REMOTE_DIR/static/web/\" \"$WEB_STATIC_DIR/\"; fi"

echo ""
echo "========== 1.2 同步后台管理静态目录 =========="
sshpass -p "$SSHPASS_PWD" ssh -o StrictHostKeyChecking=accept-new "$USER@$SERVER" \
  "if [ -d \"$(dirname "$ADMIN_STATIC_DIR")\" ]; then mkdir -p \"$ADMIN_STATIC_DIR\" && rsync -a --delete \"$REMOTE_DIR/admin/\" \"$ADMIN_STATIC_DIR/\"; fi"

echo ""
echo "========== 2. 服务器上安装依赖并重启服务 =========="
sshpass -p "$SSHPASS_PWD" ssh -o StrictHostKeyChecking=accept-new "$USER@$SERVER" "cd $REMOTE_DIR && (command -v pip3 >/dev/null && pip3 install -r requirements.txt -q -i https://pypi.tuna.tsinghua.edu.cn/simple || pip install -r requirements.txt -q) 2>/dev/null; (supervisorctl restart eceshi 2>/dev/null) || (supervisorctl restart ceshi 2>/dev/null) || true; (systemctl restart eceshi 2>/dev/null) || (systemctl restart ceshi 2>/dev/null) || true; sleep 3"

echo ""
echo "========== 3. 部署冒烟测试 =========="

# 如果服务器 .env 配置了站点域名，优先用 .env；否则回退到当前项目默认域名
ENV_PUBLIC_URL=$(sshpass -p "$SSHPASS_PWD" ssh -o StrictHostKeyChecking=accept-new "$USER@$SERVER" \
  "cd $REMOTE_DIR && grep -E '^SITE_BASE_URL=' .env 2>/dev/null | tail -n1 | cut -d= -f2-" | tr -d '\r')
if [ -n "$ENV_PUBLIC_URL" ]; then
  PUBLIC_URL="$ENV_PUBLIC_URL"
fi

REMOTE_HOST="$SERVER" \
REMOTE_USER="$USER" \
REMOTE_DIR="$REMOTE_DIR" \
SSHPASS_PWD="$SSHPASS_PWD" \
BACKEND_PORT="$BACKEND_PORT" \
BASE_URL="$PUBLIC_URL" \
"$(cd "$(dirname "$0")" && pwd)/deploy_smoke_test.sh"

echo ""
echo "========== 部署完成 =========="
