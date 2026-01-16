#!/usr/bin/env python3
"""
检查支付宝配置状态
"""
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app.core.config import settings
    from app.services.alipay_service import alipay_service
    
    print("=" * 50)
    print("支付宝配置检查")
    print("=" * 50)
    
    # 检查配置项
    print("\n📋 配置项检查:")
    print(f"  ALIPAY_APP_ID: {'✅ 已配置' if settings.ALIPAY_APP_ID else '❌ 未配置'}")
    if settings.ALIPAY_APP_ID:
        app_id_preview = settings.ALIPAY_APP_ID[:10] + "..." if len(settings.ALIPAY_APP_ID) > 10 else settings.ALIPAY_APP_ID
        print(f"    值: {app_id_preview}")
    
    print(f"  ALIPAY_PRIVATE_KEY: {'✅ 已配置' if settings.ALIPAY_PRIVATE_KEY else '❌ 未配置'}")
    if settings.ALIPAY_PRIVATE_KEY:
        key_preview = settings.ALIPAY_PRIVATE_KEY[:50] + "..." if len(settings.ALIPAY_PRIVATE_KEY) > 50 else settings.ALIPAY_PRIVATE_KEY
        print(f"    预览: {key_preview}")
        # 检查格式
        if "BEGIN RSA PRIVATE KEY" in settings.ALIPAY_PRIVATE_KEY:
            print("    格式: ✅ 正确（包含BEGIN/END标记）")
        else:
            print("    格式: ⚠️  可能不正确（缺少BEGIN/END标记）")
    
    print(f"  ALIPAY_PUBLIC_KEY: {'✅ 已配置' if settings.ALIPAY_PUBLIC_KEY else '❌ 未配置'}")
    if settings.ALIPAY_PUBLIC_KEY:
        pub_key_preview = settings.ALIPAY_PUBLIC_KEY[:50] + "..." if len(settings.ALIPAY_PUBLIC_KEY) > 50 else settings.ALIPAY_PUBLIC_KEY
        print(f"    预览: {pub_key_preview}")
        # 检查格式
        if "BEGIN PUBLIC KEY" in settings.ALIPAY_PUBLIC_KEY:
            print("    格式: ✅ 正确（包含BEGIN/END标记）")
        else:
            print("    格式: ⚠️  可能不正确（缺少BEGIN/END标记）")
    
    print(f"  ALIPAY_GATEWAY: {settings.ALIPAY_GATEWAY}")
    if "alipaydev.com" in settings.ALIPAY_GATEWAY:
        print("    环境: 🧪 沙箱环境（测试）")
    elif "alipay.com" in settings.ALIPAY_GATEWAY:
        print("    环境: 🏭 正式环境")
    else:
        print("    环境: ⚠️  未知环境")
    
    # 检查服务初始化状态
    print("\n🔧 服务初始化状态:")
    if alipay_service.alipay_client:
        print("  ✅ 支付宝客户端已初始化")
        print("  ✅ 支付功能可用")
    else:
        print("  ❌ 支付宝客户端未初始化")
        print("  ❌ 支付功能不可用")
        print("\n💡 可能的原因:")
        if not settings.ALIPAY_APP_ID:
            print("    - ALIPAY_APP_ID 未配置")
        if not settings.ALIPAY_PRIVATE_KEY:
            print("    - ALIPAY_PRIVATE_KEY 未配置")
        if settings.ALIPAY_APP_ID and settings.ALIPAY_PRIVATE_KEY:
            print("    - 配置格式可能有问题，请检查密钥格式")
            print("    - 查看 backend.log 获取详细错误信息")
    
    # 检查.env文件
    print("\n📁 环境变量文件:")
    env_file = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_file):
        print(f"  ✅ .env 文件存在: {env_file}")
        # 检查.env中是否有支付宝配置
        with open(env_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'ALIPAY' in content:
                print("  ✅ .env 中包含支付宝配置")
            else:
                print("  ⚠️  .env 中未找到支付宝配置")
    else:
        print(f"  ❌ .env 文件不存在: {env_file}")
        print("  💡 提示: 可以复制 env.example.txt 创建 .env 文件")
    
    print("\n" + "=" * 50)
    
except Exception as e:
    print(f"❌ 检查失败: {str(e)}")
    import traceback
    traceback.print_exc()
