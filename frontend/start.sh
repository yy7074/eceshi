#!/bin/bash

echo "================================"
echo "  科研检测服务平台 - 小程序启动"
echo "================================"
echo ""

# 检查是否在frontend目录
if [ ! -f "package.json" ]; then
    echo "❌ 错误：请在frontend目录下运行此脚本"
    exit 1
fi

# 检查node_modules是否存在
if [ ! -d "node_modules" ]; then
    echo "📦 首次运行，正在安装依赖..."
    npm install
    echo ""
fi

echo "🚀 启动选项："
echo "1. H5开发模式（浏览器，推荐测试）"
echo "2. 微信小程序编译"
echo ""
read -p "请选择启动方式 (1/2): " choice

case $choice in
    1)
        echo ""
        echo "🌐 启动H5开发服务器..."
        echo "📍 后端API地址: https://catdog.dachaonet.com ✅ HTTPS"
        echo "📱 前端访问地址: http://localhost:5173"
        echo ""
        echo "💡 提示："
        echo "  - 测试手机号: 18663764585"
        echo "  - 验证码: 123456 (开发模式)"
        echo "  - 新手机号会自动注册"
        echo ""
        npm run dev:h5
        ;;
    2)
        echo ""
        echo "📱 编译微信小程序..."
        echo "📍 输出目录: unpackage/dist/dev/mp-weixin"
        echo ""
        echo "💡 提示："
        echo "  - 编译完成后，使用微信开发者工具打开 unpackage/dist/dev/mp-weixin 目录"
        echo ""
        npm run dev:mp-weixin
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac

