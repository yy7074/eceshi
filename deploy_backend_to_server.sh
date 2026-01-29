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
echo "========== 3. 测试 API（后台端口 $BACKEND_PORT）=========="
# 先测后台端口 3001
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "http://$SERVER:$BACKEND_PORT/api/v1/projects/categories" 2>/dev/null || echo "000")
if [ "$HTTP_CODE" = "200" ]; then
  echo "API 测试通过 (http://$SERVER:$BACKEND_PORT) HTTP $HTTP_CODE"
  curl -s "http://$SERVER:$BACKEND_PORT/api/v1/projects/categories" | head -c 200
  echo ""
else
  # 可能只对外暴露 80（域名），用 80 测
  HTTP_CODE80=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "http://$SERVER/api/v1/projects/categories" 2>/dev/null || echo "000")
  if [ "$HTTP_CODE80" = "200" ]; then
    echo "API 测试通过 (http://$SERVER) HTTP $HTTP_CODE80"
    curl -s "http://$SERVER/api/v1/projects/categories" | head -c 200
    echo ""
  else
    echo "请检查: 1) 服务器防火墙是否放行 $BACKEND_PORT 或 80  2) 宝塔 Python 项目管理器中是否已启动/重启 eceshi"
    echo "本地可 SSH 登录后手动重启: ssh $USER@$SERVER -> 宝塔面板重启项目 或 supervisorctl restart eceshi"
  fi
fi

echo ""
echo "========== 部署完成 =========="
