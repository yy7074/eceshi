#!/usr/bin/env python3
"""
微信支付V2签名测试工具
"""
import hashlib
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 获取配置
WECHAT_MCH_ID = os.getenv('WECHAT_MCH_ID')
WECHAT_PAY_KEY = os.getenv('WECHAT_PAY_KEY')
WECHAT_APPID = os.getenv('WECHAT_APPID')

print("=" * 60)
print("微信支付V2配置检查")
print("=" * 60)

# 1. 检查配置
print(f"\n【配置信息】")
print(f"AppID: {WECHAT_APPID}")
print(f"商户号: {WECHAT_MCH_ID}")
print(f"API密钥: {WECHAT_PAY_KEY}")
print(f"API密钥长度: {len(WECHAT_PAY_KEY) if WECHAT_PAY_KEY else 0} 字符")
print(f"API密钥字节: {WECHAT_PAY_KEY.encode('utf-8') if WECHAT_PAY_KEY else None}")

# 2. 检查密钥格式
if WECHAT_PAY_KEY:
    has_space = ' ' in WECHAT_PAY_KEY
    has_newline = '\n' in WECHAT_PAY_KEY
    has_special = any(ord(c) < 32 or ord(c) > 126 for c in WECHAT_PAY_KEY)
    
    print(f"\n【密钥检查】")
    print(f"包含空格: {'是 ❌' if has_space else '否 ✅'}")
    print(f"包含换行: {'是 ❌' if has_newline else '否 ✅'}")
    print(f"包含特殊字符: {'是 ❌' if has_special else '否 ✅'}")
    print(f"标准长度(32位): {'是 ✅' if len(WECHAT_PAY_KEY) == 32 else f'否 ❌ (实际{len(WECHAT_PAY_KEY)}位)'}")

# 3. 测试签名生成
print(f"\n【签名测试】")

# 使用官方示例测试
test_params = {
    'appid': 'wxd678efh567hg6787',
    'mch_id': '1230000109',
    'nonce_str': 'ibuaiVcKdpRxkhJA',
    'body': 'test',
    'out_trade_no': '1217752501201407033233368018',
    'total_fee': '1',
    'spbill_create_ip': '8.8.8.8',
    'notify_url': 'http://www.example.com/notify',
    'trade_type': 'JSAPI'
}

# 排序
sorted_params = sorted(test_params.items(), key=lambda x: x[0])
string_a = '&'.join([f"{k}={v}" for k, v in sorted_params])
string_sign_temp = f"{string_a}&key=192006250b4c09247ec02edce69f6a2d"

print(f"待签名字符串: {string_sign_temp}")

sign = hashlib.md5(string_sign_temp.encode('utf-8')).hexdigest().upper()
print(f"生成的签名: {sign}")
print(f"官方示例签名应为类似格式")

# 4. 使用实际配置测试
if WECHAT_PAY_KEY and len(WECHAT_PAY_KEY) == 32:
    print(f"\n【使用您的配置测试】")
    
    actual_params = {
        'appid': WECHAT_APPID,
        'mch_id': WECHAT_MCH_ID,
        'nonce_str': 'test123456789012345678901234567',
        'body': '测试',
        'out_trade_no': 'TEST20250101000001',
        'total_fee': '1',
        'spbill_create_ip': '127.0.0.1',
        'notify_url': 'https://catdog.dachaonet.com/api/v1/recharge/wechat/notify',
        'trade_type': 'JSAPI',
        'openid': 'test_openid'
    }
    
    sorted_params = sorted(actual_params.items(), key=lambda x: x[0])
    string_a = '&'.join([f"{k}={v}" for k, v in sorted_params])
    string_sign_temp = f"{string_a}&key={WECHAT_PAY_KEY}"
    
    print(f"待签名字符串: {string_sign_temp}")
    
    sign = hashlib.md5(string_sign_temp.encode('utf-8')).hexdigest().upper()
    print(f"生成的签名: {sign}")

print("\n" + "=" * 60)
print("检查完成")
print("=" * 60)

