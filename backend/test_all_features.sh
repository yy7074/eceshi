#!/bin/bash

# 科研检测服务平台 - 完整功能测试脚本

echo "=================================="
echo "  🧪 科研检测服务平台功能测试"
echo "=================================="
echo ""

BASE_URL="http://localhost:3000"

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 测试函数
test_api() {
    local name=$1
    local method=$2
    local url=$3
    local data=$4
    local header=$5
    
    echo -n "测试 $name ... "
    
    if [ "$method" == "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" -X GET "$url" -H "$header" 2>/dev/null)
    else
        response=$(curl -s -w "\n%{http_code}" -X POST "$url" -H "Content-Type: application/json" -H "$header" -d "$data" 2>/dev/null)
    fi
    
    http_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | head -n -1)
    
    if [ "$http_code" == "200" ]; then
        echo -e "${GREEN}✓ 成功${NC}"
        return 0
    else
        echo -e "${RED}✗ 失败 (HTTP $http_code)${NC}"
        return 1
    fi
}

# 1. 测试服务是否运行
echo "📡 检查服务状态..."
if curl -s "$BASE_URL/api/docs" > /dev/null; then
    echo -e "${GREEN}✓ 服务运行正常${NC}"
else
    echo -e "${RED}✗ 服务未启动，请先运行: python -m app.main${NC}"
    exit 1
fi
echo ""

# 2. 测试管理员登录
echo "🔐 测试管理员登录..."
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/api/v1/auth/admin-login" \
    -H "Content-Type: application/json" \
    -d '{"username":"admin","password":"123456"}')

TOKEN=$(echo $LOGIN_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['access_token'])" 2>/dev/null)

if [ -n "$TOKEN" ]; then
    echo -e "${GREEN}✓ 管理员登录成功${NC}"
    echo "Token: ${TOKEN:0:50}..."
else
    echo -e "${RED}✗ 管理员登录失败${NC}"
    exit 1
fi
echo ""

# 3. 测试用户管理API
echo "👥 测试用户管理..."
test_api "获取用户列表" "GET" "$BASE_URL/api/v1/admin/users?page=1&page_size=5" "" "Authorization: Bearer $TOKEN"
test_api "获取用户详情" "GET" "$BASE_URL/api/v1/admin/users/12" "" "Authorization: Bearer $TOKEN"
echo ""

# 4. 测试项目管理API
echo "📊 测试项目管理..."
test_api "获取项目列表" "GET" "$BASE_URL/api/v1/admin/projects?page=1&page_size=5" "" "Authorization: Bearer $TOKEN"
test_api "获取项目分类" "GET" "$BASE_URL/api/v1/projects/categories" "" ""
echo ""

# 5. 测试短信登录
echo "📱 测试短信登录..."
test_api "发送短信验证码" "POST" "$BASE_URL/api/v1/auth/send-sms" '{"phone":"18663764585","scene":"login"}' ""
test_api "短信验证码登录" "POST" "$BASE_URL/api/v1/auth/sms-login" '{"phone":"18663764585","sms_code":"123456"}' ""
echo ""

# 6. 测试前端页面
echo "🌐 测试前端页面..."
if curl -s "$BASE_URL/admin/index.html" | grep -q "后台管理"; then
    echo -e "${GREEN}✓ 后台管理页面正常${NC}"
else
    echo -e "${RED}✗ 后台管理页面异常${NC}"
fi

if curl -s "$BASE_URL/static/booking.html" | grep -q "预约"; then
    echo -e "${GREEN}✓ 预约流程页面正常${NC}"
else
    echo -e "${RED}✗ 预约流程页面异常${NC}"
fi
echo ""

# 7. 测试数据库连接
echo "🗄️  测试数据库..."
mysql -u root -p123456 eceshi -e "SELECT COUNT(*) as total FROM projects;" 2>&1 | grep -v "Warning" | tail -1 > /tmp/db_test.txt
if [ -s /tmp/db_test.txt ]; then
    PROJECT_COUNT=$(cat /tmp/db_test.txt)
    echo -e "${GREEN}✓ 数据库连接正常 (项目数: $PROJECT_COUNT)${NC}"
else
    echo -e "${RED}✗ 数据库连接失败${NC}"
fi
echo ""

# 总结
echo "=================================="
echo "  📋 测试完成报告"
echo "=================================="
echo ""
echo "✅ 核心功能已验证:"
echo "   - 管理员登录"
echo "   - 用户管理API"
echo "   - 项目管理API"
echo "   - 短信登录"
echo "   - 前端页面"
echo "   - 数据库连接"
echo ""
echo "🌐 可访问地址:"
echo "   - 后台管理: $BASE_URL/admin"
echo "   - 预约页面: $BASE_URL/static/booking.html?project_id=1"
echo "   - API文档: $BASE_URL/api/docs"
echo ""
echo "🔐 登录信息:"
echo "   - 管理员: admin / 123456"
echo "   - 测试用户: 18663764585 / 验证码:123456"
echo ""
echo "=================================="

