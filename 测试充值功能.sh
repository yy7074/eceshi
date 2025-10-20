#!/bin/bash

echo "========================================"
echo "  测试钱包充值功能"
echo "========================================"
echo ""

# 1. 测试充值规则接口
echo "1. 测试充值赠送规则接口..."
curl -s http://localhost:3000/api/v1/recharge/bonus/rules | python3 -c "import sys, json; print(json.dumps(json.load(sys.stdin), indent=2, ensure_ascii=False))" 2>/dev/null || echo "❌ 接口调用失败（后端可能未启动）"

echo ""
echo "========================================"
echo ""

# 2. 提示如何测试充值
echo "2. 测试充值流程（需要登录token）："
echo ""
echo "步骤："
echo "  (1) 先在小程序中微信登录"
echo "  (2) 打开浏览器开发者工具"
echo "  (3) 复制localStorage中的token"
echo "  (4) 运行以下命令测试："
echo ""
echo "  curl -X POST http://localhost:3000/api/v1/recharge/create \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -H 'Authorization: Bearer YOUR_TOKEN' \\"
echo "    -d '{\"amount\": 100, \"payment_method\": \"wechat\"}'"
echo ""

echo "========================================"
echo ""

# 3. 查看后端日志
echo "3. 后端日志要点："
echo ""
echo "  当你点击充值时，后端应该输出："
echo "  [充值] 创建微信支付订单:"
echo "    - 充值单号: RC..."
echo "    - 充值金额: 100.0元 (10000分)"
echo "    - 用户OpenID: ..."
echo "    - 商户号: 10026954"
echo "  [充值] 统一下单参数: {'total_fee': '10000', ...}"
echo ""
echo "  如果看到 'total_fee'，说明参数已传递"
echo "  如果没有这个字段，说明有问题"
echo ""

echo "========================================"
echo ""

# 4. 前端测试步骤
echo "4. 前端测试步骤："
echo ""
echo "  (1) 打开微信开发者工具"
echo "  (2) 导入项目"
echo "  (3) 使用微信登录"
echo "  (4) 进入充值页面（我的 → 我的钱包 → 充值）"
echo "  (5) 选择100元"
echo "  (6) 点击'立即充值'"
echo "  (7) 查看控制台输出："
echo "      - 充值金额: 100"
echo "      - 后端返回: {appId, timeStamp, nonceStr, package, signType, paySign}"
echo "  (8) 查看微信支付是否调起"
echo ""

echo "========================================"
echo ""

# 5. 常见问题
echo "5. 如果报错'缺少total_fee'："
echo ""
echo "  原因1: 后端未正确构建支付参数"
echo "    解决: 查看后端日志，确认 total_fee 是否在参数中"
echo ""
echo "  原因2: 微信支付API调用失败"
echo "    解决: 检查商户号和密钥配置"
echo ""
echo "  原因3: 金额计算错误（为0）"
echo "    解决: 确认前端传递的金额正确"
echo ""

echo "========================================"
echo ""

echo "✅ 测试准备完成！"
echo ""
echo "下一步: 启动后端并在小程序中测试"
echo "后端启动: cd backend && python -m app.main"
echo ""

