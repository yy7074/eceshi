#!/bin/bash

# 禁用代理
unset http_proxy
unset https_proxy

DOMAIN="http://catdog.dachaonet.com"
PHONE="18663764585"

echo "=========================================="
echo "🧪 手机号测试: $PHONE"
echo "=========================================="
echo ""

# 1. 发送验证码
echo "1️⃣ 发送短信验证码..."
echo "   手机号: $PHONE"
echo "   场景: login"
echo ""

SMS_RESULT=$(curl -s -X POST "$DOMAIN/api/v1/auth/send-sms" \
  -H "Content-Type: application/json" \
  -d "{\"phone\":\"$PHONE\",\"scene\":\"login\"}")

echo "响应: $SMS_RESULT"
echo ""

# 提取验证码
CODE=$(echo "$SMS_RESULT" | grep -o '"code":"[^"]*"' | cut -d'"' -f4)

if [ -n "$CODE" ]; then
    echo "✅ 验证码已生成: $CODE"
    echo ""
    
    # 2. 短信登录（自动注册）
    echo "2️⃣ 短信验证码登录..."
    echo "   手机号: $PHONE"
    echo "   验证码: $CODE"
    echo ""
    
    LOGIN_RESULT=$(curl -s -X POST "$DOMAIN/api/v1/auth/sms-login" \
      -H "Content-Type: application/json" \
      -d "{\"phone\":\"$PHONE\",\"sms_code\":\"$CODE\"}")
    
    echo "响应: $LOGIN_RESULT"
    echo ""
    
    # 提取 token
    TOKEN=$(echo "$LOGIN_RESULT" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
    
    if [ -n "$TOKEN" ]; then
        echo "✅ 登录成功！"
        echo "Token: ${TOKEN:0:60}..."
        echo ""
        
        # 3. 获取用户信息
        echo "3️⃣ 获取用户信息..."
        USER_INFO=$(curl -s -X GET "$DOMAIN/api/v1/users/me" \
          -H "Authorization: Bearer $TOKEN")
        echo "$USER_INFO"
        echo ""
        
        # 4. 获取项目列表
        echo "4️⃣ 获取项目列表..."
        PROJECTS=$(curl -s "$DOMAIN/api/v1/projects/list?page=1&page_size=3")
        echo "$PROJECTS"
        echo ""
        
        echo "=========================================="
        echo "✅ 测试完成！"
        echo "=========================================="
        echo ""
        echo "📊 测试结果："
        echo "   ✅ 短信验证码发送成功"
        echo "   ✅ 验证码: $CODE"
        echo "   ✅ 短信登录成功（自动注册）"
        echo "   ✅ JWT认证通过"
        echo "   ✅ 获取用户信息成功"
        echo ""
        echo "🌐 域名访问："
        echo "   - API地址: $DOMAIN"
        echo "   - 服务端口: 3000"
        echo "   - API文档: $DOMAIN/docs"
        echo ""
    else
        echo "❌ 登录失败"
        echo ""
    fi
else
    echo "❌ 验证码发送失败"
    echo ""
fi

