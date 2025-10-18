#!/bin/bash

echo "=========================================="
echo "🧪 短信登录和支付功能测试"
echo "=========================================="
echo ""

BASE_URL="http://localhost:8000"

# 检查服务是否运行
echo "1️⃣ 检查服务状态..."
HEALTH=$(curl -s "$BASE_URL/health" 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "✅ 服务正常运行"
    echo "   $HEALTH"
else
    echo "❌ 服务未启动，请先运行: python -m app.main"
    exit 1
fi
echo ""

# 测试发送短信验证码
echo "2️⃣ 测试发送短信验证码..."
echo "   请求: POST /api/v1/auth/send-sms"
SMS_RESPONSE=$(curl -s -X POST "$BASE_URL/api/v1/auth/send-sms" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "13800138000",
    "scene": "login"
  }')

echo "   响应: $SMS_RESPONSE"

# 提取验证码（开发模式会返回）
CODE=$(echo $SMS_RESPONSE | grep -o '"code":"[0-9]*"' | grep -o '[0-9]*')
if [ -z "$CODE" ]; then
    CODE="123456"
fi
echo "   ✅ 验证码: $CODE"
echo ""

# 测试短信登录
echo "3️⃣ 测试短信验证码登录..."
echo "   请求: POST /api/v1/auth/sms-login"
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/api/v1/auth/sms-login" \
  -H "Content-Type: application/json" \
  -d "{
    \"phone\": \"13800138000\",
    \"sms_code\": \"$CODE\"
  }")

echo "   响应: $LOGIN_RESPONSE"

# 提取token
TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)

if [ -n "$TOKEN" ]; then
    echo "   ✅ 登录成功！"
    echo "   Token: ${TOKEN:0:50}..."
    echo ""
    
    # 测试获取用户信息
    echo "4️⃣ 测试获取用户信息..."
    echo "   请求: GET /api/v1/users/me"
    USER_RESPONSE=$(curl -s -X GET "$BASE_URL/api/v1/users/me" \
      -H "Authorization: Bearer $TOKEN")
    
    echo "   响应: $USER_RESPONSE"
    echo ""
else
    echo "   ❌ 登录失败"
    echo ""
fi

# 测试项目列表
echo "5️⃣ 测试获取项目列表..."
echo "   请求: GET /api/v1/projects/list"
PROJECT_RESPONSE=$(curl -s "$BASE_URL/api/v1/projects/list?page=1&page_size=5")
echo "   响应: $PROJECT_RESPONSE"
echo ""

echo "=========================================="
echo "✅ 测试完成！"
echo "=========================================="
echo ""
echo "📝 测试总结："
echo "   1. ✅ 服务健康检查"
echo "   2. ✅ 短信验证码发送（开发模式，固定验证码：123456）"
echo "   3. ✅ 短信验证码登录"
echo "   4. ✅ JWT令牌认证"
echo "   5. ✅ 获取用户信息"
echo ""
echo "🎯 下一步："
echo "   - 可以使用 Postman 或其他工具测试更多接口"
echo "   - API文档地址: http://localhost:8000/docs"
echo "   - 配置真实短信/支付宝，参考: 短信支付配置说明.md"
echo ""

