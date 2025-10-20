"""
微信支付服务
"""
import time
import hashlib
import random
import string
import httpx
import xml.etree.ElementTree as ET
from decimal import Decimal
from datetime import datetime
from typing import Dict, Optional
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.order import Order, Payment
from app.models.recharge import RechargeRecord, RechargeStatus


class WeChatPayService:
    """微信支付服务"""
    
    def __init__(self):
        # 微信小程序支付配置
        self.app_id = getattr(settings, 'WECHAT_APPID', 'wx2ef4744e64c7bc45')
        self.mch_id = getattr(settings, 'WECHAT_MCH_ID', '')  # 商户号
        self.api_key = getattr(settings, 'WECHAT_PAY_KEY', '')  # API密钥
        self.notify_url = getattr(settings, 'WECHAT_PAY_NOTIFY_URL', 'https://catdog.dachaonet.com/api/v1/payments/wechat/notify')
    
    def generate_nonce_str(self, length: int = 32) -> str:
        """生成随机字符串"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    def generate_sign(self, params: Dict, sign_type: str = 'MD5') -> str:
        """
        生成签名
        
        签名算法：
        1. 将参数按key排序
        2. 拼接成key=value&key2=value2的格式
        3. 添加key=API_KEY
        4. MD5加密并转大写
        """
        # 过滤空值和sign字段（只过滤None、空字符串，保留0等值）
        filtered = {k: v for k, v in params.items() 
                   if v is not None and v != '' and k != 'sign'}
        
        # 按key排序
        sorted_params = sorted(filtered.items(), key=lambda x: x[0])
        
        # 拼接字符串
        string_a = '&'.join([f"{k}={v}" for k, v in sorted_params])
        
        # 添加API密钥
        string_sign_temp = f"{string_a}&key={self.api_key}"
        
        # 打印签名调试信息
        print(f"[签名] 待签名字符串: {string_sign_temp}")
        
        # MD5加密
        if sign_type == 'MD5':
            sign = hashlib.md5(string_sign_temp.encode('utf-8')).hexdigest().upper()
        else:
            # HMAC-SHA256或其他签名方式
            sign = hashlib.md5(string_sign_temp.encode('utf-8')).hexdigest().upper()
        
        print(f"[签名] 生成的签名: {sign}")
        
        return sign
    
    def dict_to_xml(self, params: Dict) -> str:
        """
        将字典转换为XML格式
        
        注意：
        - 字符串类型需要CDATA标签
        - 数字类型不需要CDATA标签
        """
        # 数字类型字段列表（不需要CDATA）
        numeric_fields = {'total_fee', 'refund_fee'}
        
        xml = '<xml>'
        for key, value in params.items():
            if key in numeric_fields:
                # 数字类型不用CDATA
                xml += f'<{key}>{value}</{key}>'
            else:
                # 字符串类型用CDATA
                xml += f'<{key}><![CDATA[{value}]]></{key}>'
        xml += '</xml>'
        
        return xml
    
    def xml_to_dict(self, xml_str: str) -> Dict:
        """
        将XML转换为字典
        """
        try:
            root = ET.fromstring(xml_str)
            result = {}
            for child in root:
                result[child.tag] = child.text
            return result
        except Exception as e:
            print(f"XML解析失败: {str(e)}")
            return {}
    
    async def call_wechat_unifiedorder(self, params: Dict) -> Dict:
        """
        调用微信统一下单API
        
        Args:
            params: 统一下单参数
            
        Returns:
            dict: 微信返回的结果
        """
        url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
        
        # 构建XML请求
        xml_data = self.dict_to_xml(params)
        
        print(f"[微信支付] 发送统一下单请求到: {url}")
        print(f"[微信支付] 完整请求XML:")
        print(xml_data)
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    url,
                    content=xml_data.encode('utf-8'),
                    headers={
                        'Content-Type': 'text/xml; charset=utf-8',
                        'User-Agent': 'wxpay sdk python v1.0'
                    }
                )
                
                print(f"[微信支付] 响应状态码: {response.status_code}")
                print(f"[微信支付] 响应原始XML:")
                print(response.text)
                
                if response.status_code != 200:
                    raise Exception(f"微信API返回错误状态码: {response.status_code}")
                
                # 解析XML响应
                result = self.xml_to_dict(response.text)
                
                print(f"[微信支付] 响应解析数据: {result}")
                
                # 验证签名
                if result.get('return_code') == 'SUCCESS':
                    # 验证响应签名
                    response_sign = result.get('sign', '')
                    calculated_sign = self.generate_sign(result)
                    
                    if response_sign != calculated_sign:
                        print(f"[微信支付] 警告：响应签名验证失败")
                        print(f"  响应签名: {response_sign}")
                        print(f"  计算签名: {calculated_sign}")
                
                return result
                
        except httpx.TimeoutException:
            print("[微信支付] 请求超时")
            raise Exception("微信支付请求超时")
        except Exception as e:
            print(f"[微信支付] 调用统一下单API失败: {str(e)}")
            raise
    
    async def create_jsapi_payment(
        self,
        db: Session,
        order: Order,
        user_id: int,
        openid: str
    ) -> Dict:
        """
        创建JSAPI支付（小程序支付）
        
        Args:
            db: 数据库会话
            order: 订单对象
            user_id: 用户ID
            openid: 用户微信openid
        
        Returns:
            dict: 包含支付参数的字典
        """
        # 检查必需配置
        if not self.mch_id or not self.api_key:
            raise ValueError("未配置微信支付商户号或密钥，请在.env文件中配置WECHAT_MCH_ID和WECHAT_PAY_KEY")
        
        # 计算待支付金额（单位：分）
        total_fee = int((order.total_amount - order.paid_amount) * 100)
        
        # 确保金额大于0
        if total_fee <= 0:
            raise ValueError(f"订单支付金额必须大于0，当前金额: {order.total_amount - order.paid_amount}")
        
        print(f"[订单支付] 创建微信支付订单:")
        print(f"  - 订单号: {order.order_no}")
        print(f"  - 支付金额: {order.total_amount - order.paid_amount}元 ({total_fee}分)")
        print(f"  - 用户OpenID: {openid}")
        print(f"  - 商户号: {self.mch_id}")
        
        # 统一下单参数
        params = {
            'appid': self.app_id,
            'mch_id': self.mch_id,
            'nonce_str': self.generate_nonce_str(),
            'body': f'检测服务-{order.project_name}',
            'out_trade_no': order.order_no,
            'total_fee': str(total_fee),
            'spbill_create_ip': '127.0.0.1',
            'notify_url': self.notify_url,
            'trade_type': 'JSAPI',
            'openid': openid
        }
        
        # 生成签名
        params['sign'] = self.generate_sign(params)
        
        print(f"[订单支付] 统一下单参数: {params}")
        
        try:
            # 调用微信统一下单API
            result = await self.call_wechat_unifiedorder(params)
            
            # 检查返回状态
            if result.get('return_code') != 'SUCCESS':
                error_msg = result.get('return_msg', '未知错误')
                print(f"[订单支付] 统一下单失败: {error_msg}")
                raise Exception(f"微信支付统一下单失败: {error_msg}")
            
            if result.get('result_code') != 'SUCCESS':
                error_code = result.get('err_code', '')
                error_desc = result.get('err_code_des', '未知错误')
                print(f"[订单支付] 支付失败: {error_code} - {error_desc}")
                raise Exception(f"微信支付错误: {error_desc}")
            
            # 获取prepay_id
            prepay_id = result.get('prepay_id')
            if not prepay_id:
                raise Exception("未获取到prepay_id")
            
            print(f"[订单支付] 获取prepay_id成功: {prepay_id}")
            
        except Exception as e:
            print(f"[订单支付] 调用微信API异常: {str(e)}")
            raise Exception(f"创建支付订单失败: {str(e)}")
        
        # 生成小程序支付参数
        timestamp = str(int(time.time()))
        nonce_str = self.generate_nonce_str()
        
        pay_params = {
            'appId': self.app_id,
            'timeStamp': timestamp,
            'nonceStr': nonce_str,
            'package': f'prepay_id={prepay_id}',
            'signType': 'MD5'
        }
        
        # 生成支付签名
        pay_params['paySign'] = self.generate_sign(pay_params)
        
        print(f"[订单支付] 返回支付参数: appId={pay_params['appId']}, timeStamp={timestamp}, package={pay_params['package']}")
        
        return pay_params
    
    
    async def handle_notify(
        self,
        db: Session,
        notify_data: Dict
    ) -> bool:
        """
        处理微信支付回调
        
        Args:
            db: 数据库会话
            notify_data: 回调数据
        
        Returns:
            bool: 处理是否成功
        """
        try:
            # 验证签名
            sign = notify_data.get('sign', '')
            calculated_sign = self.generate_sign(notify_data)
            
            if sign != calculated_sign:
                print('微信支付回调签名验证失败')
                return False
            
            # 获取支付结果
            if notify_data.get('return_code') != 'SUCCESS':
                return False
            
            if notify_data.get('result_code') != 'SUCCESS':
                return False
            
            # 获取订单号
            out_trade_no = notify_data.get('out_trade_no')
            transaction_id = notify_data.get('transaction_id')
            
            # 查询订单
            order = db.query(Order).filter(
                Order.order_no == out_trade_no
            ).first()
            
            if not order:
                print(f'订单不存在: {out_trade_no}')
                return False
            
            # 检查订单是否已支付
            if order.status == 'paid':
                return True
            
            # 更新支付记录
            payment = db.query(Payment).filter(
                Payment.order_id == order.id,
                Payment.status == 'pending'
            ).first()
            
            if payment:
                payment.status = 'success'
                payment.transaction_id = transaction_id
                payment.paid_at = datetime.now()
            
            # 更新订单状态
            order.status = 'paid'
            order.paid_amount = order.total_amount
            order.paid_at = datetime.now()
            
            db.commit()
            
            return True
            
        except Exception as e:
            print(f'处理微信支付回调失败: {str(e)}')
            db.rollback()
            return False
    
    async def create_recharge_payment(
        self,
        db: Session,
        recharge: RechargeRecord,
        user_id: int,
        openid: str
    ) -> Dict:
        """
        创建充值支付（小程序支付）
        
        Args:
            db: 数据库会话
            recharge: 充值记录对象
            user_id: 用户ID
            openid: 用户微信openid
        
        Returns:
            dict: 包含支付参数的字典
        """
        # 计算待支付金额（单位：分）
        total_fee = int(recharge.amount * 100)
        
        # 确保金额大于0
        if total_fee <= 0:
            raise ValueError(f"充值金额必须大于0，当前金额: {recharge.amount}")
        
        # 检查必需配置
        if not self.mch_id or not self.api_key:
            raise ValueError("未配置微信支付商户号或密钥，请在.env文件中配置WECHAT_MCH_ID和WECHAT_PAY_KEY")
        
        # 打印调试信息
        print(f"[充值] 创建微信支付订单:")
        print(f"  - 充值单号: {recharge.recharge_no}")
        print(f"  - 充值金额: {recharge.amount}元 ({total_fee}分)")
        print(f"  - 用户OpenID: {openid}")
        print(f"  - 商户号: {self.mch_id}")
        
        # 统一下单参数
        params = {
            'appid': self.app_id,
            'mch_id': self.mch_id,
            'nonce_str': self.generate_nonce_str(),
            'body': '钱包充值',
            'out_trade_no': recharge.recharge_no,
            'total_fee': str(total_fee),
            'spbill_create_ip': '127.0.0.1',
            'notify_url': self.notify_url.replace('/payments/wechat/notify', '/recharge/wechat/notify'),
            'trade_type': 'JSAPI',
            'openid': openid
        }
        
        # 生成签名
        params['sign'] = self.generate_sign(params)
        
        print(f"[充值] 统一下单参数: {params}")
        
        try:
            # 调用微信统一下单API
            result = await self.call_wechat_unifiedorder(params)
            
            # 检查返回状态
            if result.get('return_code') != 'SUCCESS':
                error_msg = result.get('return_msg', '未知错误')
                print(f"[充值] 统一下单失败: {error_msg}")
                raise Exception(f"微信支付统一下单失败: {error_msg}")
            
            if result.get('result_code') != 'SUCCESS':
                error_code = result.get('err_code', '')
                error_desc = result.get('err_code_des', '未知错误')
                print(f"[充值] 支付失败: {error_code} - {error_desc}")
                raise Exception(f"微信支付错误: {error_desc}")
            
            # 获取prepay_id
            prepay_id = result.get('prepay_id')
            if not prepay_id:
                raise Exception("未获取到prepay_id")
            
            print(f"[充值] 获取prepay_id成功: {prepay_id}")
            
        except Exception as e:
            print(f"[充值] 调用微信API异常: {str(e)}")
            raise Exception(f"创建支付订单失败: {str(e)}")
        
        # 生成小程序支付参数
        timestamp = str(int(time.time()))
        nonce_str = self.generate_nonce_str()
        
        pay_params = {
            'appId': self.app_id,
            'timeStamp': timestamp,
            'nonceStr': nonce_str,
            'package': f'prepay_id={prepay_id}',
            'signType': 'MD5'
        }
        
        # 生成支付签名
        pay_params['paySign'] = self.generate_sign(pay_params)
        
        print(f"[充值] 返回支付参数: appId={pay_params['appId']}, timeStamp={timestamp}, package={pay_params['package']}")
        
        return pay_params
    
    async def handle_recharge_notify(
        self,
        db: Session,
        notify_data: Dict
    ) -> bool:
        """
        处理充值支付回调
        
        Args:
            db: 数据库会话
            notify_data: 回调数据
        
        Returns:
            bool: 处理是否成功
        """
        try:
            # 验证签名
            sign = notify_data.get('sign', '')
            calculated_sign = self.generate_sign(notify_data)
            
            if sign != calculated_sign:
                print('充值支付回调签名验证失败')
                return False
            
            # 获取支付结果
            if notify_data.get('return_code') != 'SUCCESS':
                return False
            
            if notify_data.get('result_code') != 'SUCCESS':
                return False
            
            # 获取充值单号
            out_trade_no = notify_data.get('out_trade_no')
            transaction_id = notify_data.get('transaction_id')
            
            # 查询充值记录
            recharge = db.query(RechargeRecord).filter(
                RechargeRecord.recharge_no == out_trade_no
            ).first()
            
            if not recharge:
                print(f'充值记录不存在: {out_trade_no}')
                return False
            
            # 检查是否已处理
            if recharge.status == RechargeStatus.SUCCESS:
                return True
            
            # 更新用户余额
            from app.models.user import User
            user = db.query(User).filter(User.id == recharge.user_id).first()
            
            if not user:
                print(f'用户不存在: {recharge.user_id}')
                return False
            
            # 增加余额（充值金额+赠送金额）
            user.prepaid_balance = (user.prepaid_balance or Decimal("0")) + recharge.actual_amount
            
            # 更新充值记录状态
            recharge.status = RechargeStatus.SUCCESS
            recharge.transaction_id = transaction_id
            recharge.paid_at = datetime.now()
            recharge.completed_at = datetime.now()
            
            db.commit()
            
            print(f'充值成功: 用户{user.id}, 充值{float(recharge.amount)}元, 实际到账{float(recharge.actual_amount)}元')
            
            return True
            
        except Exception as e:
            print(f'处理充值支付回调失败: {str(e)}')
            db.rollback()
            return False


# 创建全局实例
wechatpay_service = WeChatPayService()

