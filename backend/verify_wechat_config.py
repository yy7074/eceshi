#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
微信支付配置验证工具
用于检查商户号、AppID、API密钥是否配置正确
"""
import sys
import hashlib
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

def generate_test_sign(api_key):
    """生成测试签名"""
    # 构造一个简单的测试参数
    params = {
        'appid': 'wx2ef4744e64c7bc45',
        'mch_id': '10026954',
        'nonce_str': 'test123456',
        'body': '测试',
        'out_trade_no': 'TEST001',
        'total_fee': '1',
    }
    
    # 按key排序
    sorted_params = sorted(params.items(), key=lambda x: x[0])
    
    # 拼接字符串
    string_a = '&'.join([f"{k}={v}" for k, v in sorted_params])
    
    # 添加API密钥
    string_sign_temp = f"{string_a}&key={api_key}"
    
    # MD5加密
    sign = hashlib.md5(string_sign_temp.encode('utf-8')).hexdigest().upper()
    
    return string_sign_temp, sign

def main():
    print("=" * 80)
    print("微信支付配置验证工具")
    print("=" * 80)
    print()
    
    # 读取配置
    appid = os.getenv('WECHAT_APPID')
    secret = os.getenv('WECHAT_SECRET')
    mch_id = os.getenv('WECHAT_MCH_ID')
    api_key = os.getenv('WECHAT_PAY_KEY')
    notify_url = os.getenv('WECHAT_PAY_NOTIFY_URL')
    
    print("📋 当前配置信息:")
    print(f"  AppID:        {appid}")
    print(f"  AppSecret:    {secret[:8]}...{secret[-8:] if secret and len(secret) > 16 else '***'}")
    print(f"  商户号:       {mch_id}")
    print(f"  API密钥:      {api_key[:8]}...{api_key[-8:] if api_key and len(api_key) > 16 else '***'}")
    print(f"  回调URL:      {notify_url}")
    print()
    
    # 检查配置完整性
    print("🔍 配置完整性检查:")
    issues = []
    
    if not appid or appid == 'your_wechat_appid':
        issues.append("❌ AppID 未配置或使用了占位符")
    else:
        print(f"  ✅ AppID: {appid}")
    
    if not mch_id or mch_id == 'your_mch_id':
        issues.append("❌ 商户号 未配置或使用了占位符")
    else:
        print(f"  ✅ 商户号: {mch_id}")
        # 商户号应该是纯数字
        if not mch_id.isdigit():
            issues.append("⚠️  商户号格式异常（应该是纯数字）")
    
    if not api_key or api_key == 'your_api_key':
        issues.append("❌ API密钥 未配置或使用了占位符")
    else:
        print(f"  ✅ API密钥: {api_key[:8]}...{api_key[-8:]}")
        # API密钥应该是32位
        if len(api_key) != 32:
            issues.append(f"⚠️  API密钥长度异常（当前{len(api_key)}位，应该是32位）")
    
    if not notify_url or 'example.com' in notify_url:
        issues.append("❌ 回调URL 未配置或使用了示例域名")
    else:
        print(f"  ✅ 回调URL: {notify_url}")
    
    print()
    
    # 显示问题
    if issues:
        print("⚠️  发现以下问题:")
        for issue in issues:
            print(f"  {issue}")
        print()
    
    # 生成测试签名
    if api_key and len(api_key) == 32:
        print("🔐 签名测试:")
        string_to_sign, test_sign = generate_test_sign(api_key)
        print(f"  待签名字符串: {string_to_sign}")
        print(f"  生成的签名:   {test_sign}")
        print()
    
    # 配置验证提示
    print("=" * 80)
    print("📝 请在微信商户平台验证以下内容:")
    print("=" * 80)
    print()
    print("1️⃣  登录微信商户平台: https://pay.weixin.qq.com")
    print(f"   使用商户号: {mch_id}")
    print()
    print("2️⃣  验证AppID绑定:")
    print("   【产品中心】→【AppID账号管理】")
    print(f"   确认 {appid} 已绑定到商户号 {mch_id}")
    print()
    print("3️⃣  验证API密钥:")
    print("   【账户中心】→【API安全】→【API密钥】")
    print("   查看/设置 APIv2密钥（32位字符）")
    print(f"   当前配置的密钥: {api_key}")
    print("   ⚠️  如果不确定，建议重新设置API密钥并更新到.env文件")
    print()
    print("4️⃣  验证商户状态:")
    print("   【账户中心】→【账户信息】")
    print("   确认账户状态为【正常】")
    print("   确认已开通【JSAPI支付】功能")
    print()
    print("5️⃣  验证IP白名单（如果有）:")
    print("   【账户中心】→【API安全】→【IP白名单】")
    print("   如果设置了白名单，需要添加服务器IP")
    print()
    
    # API密钥格式说明
    print("=" * 80)
    print("💡 API密钥格式说明:")
    print("=" * 80)
    print()
    print("  正确的APIv2密钥应该是：")
    print("  - 长度：32位")
    print("  - 字符：大小写字母 + 数字")
    print("  - 示例：1A2B3C4D5E6F7G8H9I0J1K2L3M4N5O6P")
    print()
    print(f"  您当前的密钥：{api_key}")
    print(f"  长度：{len(api_key) if api_key else 0} 位")
    print()
    
    if api_key and len(api_key) != 32:
        print("  ⚠️  密钥长度不正确！请检查是否完整复制。")
        print()
    
    print("=" * 80)
    print("🔧 如果确认配置无误但仍然报签名错误，可能原因：")
    print("=" * 80)
    print()
    print("  1. API密钥复制时多了空格或换行符")
    print("  2. 商户号和AppID未绑定")
    print("  3. 商户号被冻结或限制")
    print("  4. 使用了沙箱环境的配置但调用的是正式环境")
    print()
    
    print("=" * 80)
    print("✅ 建议操作:")
    print("=" * 80)
    print()
    print("  1. 登录商户平台，重新设置API密钥")
    print("  2. 复制新密钥时确保没有空格")
    print("  3. 更新 backend/.env 文件中的 WECHAT_PAY_KEY")
    print("  4. 重启后端服务")
    print()

if __name__ == '__main__':
    main()

