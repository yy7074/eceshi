#!/bin/bash

echo "🧪 Web网站测试脚本"
echo "===================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. 检查文件是否存在
echo "📁 1. 检查Web网站文件..."
if [ -f "backend/static/web/index.html" ]; then
    echo -e "${GREEN}✅ index.html 存在${NC}"
else
    echo -e "${RED}❌ index.html 不存在${NC}"
fi

if [ -f "backend/static/web/assets/css/style.css" ]; then
    echo -e "${GREEN}✅ style.css 存在${NC}"
else
    echo -e "${RED}❌ style.css 不存在${NC}"
fi

if [ -f "backend/static/web/assets/js/app.js" ]; then
    echo -e "${GREEN}✅ app.js 存在${NC}"
else
    echo -e "${RED}❌ app.js 不存在${NC}"
fi

echo ""

# 2. 检查文件大小
echo "📊 2. 检查文件大小..."
echo "总大小: $(du -sh backend/static/web/ 2>/dev/null | cut -f1)"
echo "index.html: $(ls -lh backend/static/web/index.html 2>/dev/null | awk '{print $5}')"
echo "style.css: $(ls -lh backend/static/web/assets/css/style.css 2>/dev/null | awk '{print $5}')"
echo "app.js: $(ls -lh backend/static/web/assets/js/app.js 2>/dev/null | awk '{print $5}')"
echo ""

# 3. 检查后端服务
echo "🔌 3. 检查后端服务..."
if curl -s http://localhost:3000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ 后端服务运行中${NC}"
    echo "健康检查: $(curl -s http://localhost:3000/health)"
else
    echo -e "${YELLOW}⚠️  后端服务未运行${NC}"
    echo "请先启动后端服务："
    echo "  cd backend"
    echo "  python -m app.main"
fi
echo ""

# 4. 测试API接口
echo "🌐 4. 测试API接口..."
BASE_URL="https://catdog.dachaonet.com"

# 测试分类接口
echo -n "测试分类接口... "
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/v1/projects/categories")
if [ "$STATUS" = "200" ]; then
    echo -e "${GREEN}✅ 200 OK${NC}"
else
    echo -e "${RED}❌ $STATUS${NC}"
fi

# 测试项目列表
echo -n "测试项目列表... "
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/v1/projects/list")
if [ "$STATUS" = "200" ]; then
    echo -e "${GREEN}✅ 200 OK${NC}"
else
    echo -e "${RED}❌ $STATUS${NC}"
fi

# 测试项目详情
echo -n "测试项目详情... "
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/v1/projects/1")
if [ "$STATUS" = "200" ]; then
    echo -e "${GREEN}✅ 200 OK${NC}"
else
    echo -e "${YELLOW}⚠️  $STATUS (项目可能不存在)${NC}"
fi

echo ""

# 5. 访问地址
echo "🌐 5. 访问地址："
echo "Web网站:      https://catdog.dachaonet.com/web"
echo "后台管理:     https://catdog.dachaonet.com/admin"
echo "API文档:      https://catdog.dachaonet.com/api/docs"
echo ""
echo "本地访问:"
echo "Web网站:      http://localhost:3000/web"
echo "后台管理:     http://localhost:3000/admin"
echo "API文档:      http://localhost:3000/api/docs"
echo ""

# 6. 浏览器测试建议
echo "🧪 6. 浏览器测试步骤："
echo "1. 打开浏览器访问: https://catdog.dachaonet.com/web"
echo "2. 按 F12 打开开发者工具"
echo "3. 查看 Console 和 Network 标签"
echo "4. 测试以下功能："
echo "   - 首页加载"
echo "   - 项目列表"
echo "   - 项目详情"
echo "   - 用户登录（手机验证码）"
echo "   - 我的订单（需先登录）"
echo "   - 个人中心（需先登录）"
echo ""

# 7. 响应式测试
echo "📱 7. 响应式测试："
echo "PC端:   调整浏览器窗口到 1920x1080"
echo "平板端: 调整浏览器窗口到 900x768"
echo "手机端: 调整浏览器窗口到 375x667"
echo "或使用: F12 → 切换设备工具栏"
echo ""

# 8. 快速打开网站
echo "🚀 8. 快速打开网站..."
echo "执行以下命令打开浏览器："
echo ""
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "  open https://catdog.dachaonet.com/web"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "  xdg-open https://catdog.dachaonet.com/web"
else
    echo "  start https://catdog.dachaonet.com/web"
fi
echo ""

echo "===================="
echo "✅ 测试完成！"
echo ""
echo "💡 提示："
echo "- 如果API测试失败，请检查网络连接"
echo "- 如果后端服务未运行，请先启动后端"
echo "- 详细测试步骤请查看: Web网站测试指南.md"

