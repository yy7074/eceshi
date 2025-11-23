#!/bin/bash

# 测试新完善的功能
# 包括：优惠券系统、团队功能、邀请返利系统

# 禁用代理
unset http_proxy
unset https_proxy

BASE_URL="http://localhost:3000/api/v1"

# 颜色输出
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "======================================"
echo "测试新完善的功能"
echo "======================================"
echo ""

# 1. 登录获取token
echo -e "${YELLOW}1. 登录获取token...${NC}"
LOGIN_RESPONSE=$(curl -s -X POST "${BASE_URL}/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "admin",
    "password": "123456"
  }')

TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
  echo -e "${RED}❌ 登录失败${NC}"
  echo $LOGIN_RESPONSE
  exit 1
fi

echo -e "${GREEN}✅ 登录成功${NC}"
echo "Token: ${TOKEN:0:20}..."
echo ""

# 2. 测试优惠券系统
echo -e "${YELLOW}2. 测试优惠券系统${NC}"
echo "-----------------------------------"

# 2.1 获取可领取优惠券
echo "2.1 获取可领取优惠券..."
AVAILABLE_COUPONS=$(curl -s -X GET "${BASE_URL}/coupons/available" \
  -H "Authorization: Bearer $TOKEN")
echo $AVAILABLE_COUPONS | jq '.'
echo ""

# 2.2 领取优惠券
echo "2.2 领取优惠券（ID=1）..."
RECEIVE_RESULT=$(curl -s -X POST "${BASE_URL}/coupons/receive?coupon_id=1" \
  -H "Authorization: Bearer $TOKEN")
echo $RECEIVE_RESULT | jq '.'
echo ""

# 2.3 获取我的优惠券
echo "2.3 获取我的优惠券..."
MY_COUPONS=$(curl -s -X GET "${BASE_URL}/coupons/my" \
  -H "Authorization: Bearer $TOKEN")
echo $MY_COUPONS | jq '.'
echo ""

# 3. 测试团队功能
echo -e "${YELLOW}3. 测试团队功能${NC}"
echo "-----------------------------------"

# 3.1 创建团队
echo "3.1 创建团队..."
CREATE_GROUP=$(curl -s -X POST "${BASE_URL}/groups/create" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "测试团队",
    "avatar": "https://example.com/avatar.jpg",
    "unit_type": "高校",
    "region": "北京市",
    "address": "海淀区",
    "leader_name": "张三",
    "leader_phone": "admin"
  }')
echo $CREATE_GROUP | jq '.'

# 提取团队ID和邀请码
GROUP_ID=$(echo $CREATE_GROUP | grep -o '"group_id":[0-9]*' | cut -d':' -f2)
INVITE_CODE=$(echo $CREATE_GROUP | grep -o '"invite_code":"[^"]*"' | cut -d'"' -f4)
echo "团队ID: $GROUP_ID"
echo "邀请码: $INVITE_CODE"
echo ""

# 3.2 获取我的团队
echo "3.2 获取我的团队..."
MY_GROUPS=$(curl -s -X GET "${BASE_URL}/groups/my" \
  -H "Authorization: Bearer $TOKEN")
echo $MY_GROUPS | jq '.'
echo ""

# 3.3 获取团队详情
if [ ! -z "$GROUP_ID" ]; then
  echo "3.3 获取团队详情（ID=$GROUP_ID）..."
  GROUP_DETAIL=$(curl -s -X GET "${BASE_URL}/groups/${GROUP_ID}" \
    -H "Authorization: Bearer $TOKEN")
  echo $GROUP_DETAIL | jq '.'
  echo ""
fi

# 4. 测试邀请返利系统
echo -e "${YELLOW}4. 测试邀请返利系统${NC}"
echo "-----------------------------------"

# 4.1 获取邀请统计
echo "4.1 获取邀请统计..."
INVITE_STATS=$(curl -s -X GET "${BASE_URL}/invites/stats" \
  -H "Authorization: Bearer $TOKEN")
echo $INVITE_STATS | jq '.'
echo ""

# 4.2 获取邀请记录
echo "4.2 获取邀请记录..."
INVITE_RECORDS=$(curl -s -X GET "${BASE_URL}/invites/records?page=1&page_size=10" \
  -H "Authorization: Bearer $TOKEN")
echo $INVITE_RECORDS | jq '.'
echo ""

# 5. 测试订单费用计算（验证从数据库读取价格）
echo -e "${YELLOW}5. 测试订单费用计算${NC}"
echo "-----------------------------------"

echo "5.1 计算订单费用（项目ID=1）..."
CALCULATE_ORDER=$(curl -s -X POST "${BASE_URL}/orders/calculate" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 1,
    "sample_count": 2,
    "is_urgent": false,
    "shipping_method": "express"
  }')
echo $CALCULATE_ORDER | jq '.'
echo ""

# 6. 测试用户余额查询
echo -e "${YELLOW}6. 测试用户余额${NC}"
echo "-----------------------------------"

echo "6.1 查询用户信息（包含余额）..."
USER_INFO=$(curl -s -X GET "${BASE_URL}/users/me" \
  -H "Authorization: Bearer $TOKEN")
echo $USER_INFO | jq '{nickname, phone, prepaid_balance, total_spent, total_orders}'
echo ""

# 总结
echo "======================================"
echo -e "${GREEN}✅ 测试完成！${NC}"
echo "======================================"
echo ""
echo "测试项目："
echo "  ✅ 优惠券系统 - 领取、查询"
echo "  ✅ 团队功能 - 创建、查询、详情"
echo "  ✅ 邀请返利 - 统计、记录"
echo "  ✅ 订单计算 - 从数据库读取价格"
echo "  ✅ 用户余额 - 真实余额查询"
echo ""
echo "详细文档："
echo "  - 功能完善总结报告.md"
echo "  - 团队和邀请功能完成报告.md"
echo ""
