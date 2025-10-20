#!/bin/bash

# 微信支付快速配置脚本

echo "========================================"
echo "  微信支付配置工具"
echo "========================================"
echo ""

# 进入backend目录
cd backend

# 检查.env文件是否存在
if [ -f ".env" ]; then
    echo "✅ 发现现有.env文件"
    echo "📝 将更新微信支付配置..."
    
    # 备份现有文件
    cp .env .env.backup.$(date +%Y%m%d_%H%M%S)
    echo "✅ 已备份现有配置"
else
    echo "📝 创建新的.env文件..."
fi

# 添加或更新微信支付配置
cat >> .env << 'ENVEOF'

# ========== 微信支付配置 ==========
# 商户号
WECHAT_MCH_ID=10026954

# APIv2密钥
WECHAT_PAY_KEY=fr54thyu78kijfsqv46mkl956edfg3ed

# 支付回调URL
WECHAT_PAY_NOTIFY_URL=https://catdog.dachaonet.com/api/v1/payments/wechat/notify

ENVEOF

echo ""
echo "========================================"
echo "  ✅ 配置完成！"
echo "========================================"
echo ""
echo "已配置的信息："
echo "  商户号: 10026954"
echo "  API密钥: fr54t***（已隐藏）"
echo "  回调URL: https://catdog.dachaonet.com/api/v1/payments/wechat/notify"
echo ""
echo "⚠️  重要提示："
echo "  1. .env文件包含敏感信息，请勿提交到Git"
echo "  2. 请重启后端服务使配置生效"
echo "  3. 需在微信商户平台配置支付授权目录"
echo ""
echo "下一步操作："
echo "  1. 重启后端: cd backend && python -m app.main"
echo "  2. 访问文档: http://localhost:3000/docs"
echo "  3. 测试支付: 使用小程序测试支付流程"
echo ""
echo "📖 详细说明请查看: backend/微信支付配置说明.md"
echo ""
