"""
支付宝支付服务
"""
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.request.AlipayTradeAppPayRequest import AlipayTradeAppPayRequest
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
from alipay.aop.api.request.AlipayTradeQueryRequest import AlipayTradeQueryRequest
from alipay.aop.api.request.AlipayTradeCloseRequest import AlipayTradeCloseRequest
from alipay.aop.api.request.AlipayTradeRefundRequest import AlipayTradeRefundRequest
from alipay.aop.api.util.SignatureUtils import verify_with_rsa
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from decimal import Decimal
import json
from datetime import datetime
import logging

from app.core.config import settings
from app.models.order import Order, Payment

logger = logging.getLogger(__name__)


class AlipayService:
    """支付宝支付服务"""
    
    def __init__(self):
        """初始化支付宝客户端"""
        self.alipay_client = None
        if settings.ALIPAY_APP_ID and settings.ALIPAY_PRIVATE_KEY:
            self._init_client()
        else:
            logger.warning("支付宝配置不完整，支付功能将不可用")
    
    def _init_client(self):
        """初始化支付宝客户端"""
        try:
            # 创建支付宝客户端配置
            alipay_config = AlipayClientConfig()
            alipay_config.server_url = settings.ALIPAY_GATEWAY
            alipay_config.app_id = settings.ALIPAY_APP_ID
            alipay_config.app_private_key = settings.ALIPAY_PRIVATE_KEY
            alipay_config.alipay_public_key = settings.ALIPAY_PUBLIC_KEY
            alipay_config.sign_type = "RSA2"
            
            self.alipay_client = DefaultAlipayClient(alipay_config)
            logger.info("支付宝客户端初始化成功")
        except Exception as e:
            logger.error(f"支付宝客户端初始化失败: {str(e)}")

    async def create_h5_payment(
        self,
        db: Session,
        order_id: int,
        user_id: int,
        return_url: str = None,
        notify_url: str = None
    ) -> str:
        """
        创建支付宝H5/网页支付
        
        Args:
            db: 数据库会话
            order_id: 订单ID
            user_id: 用户ID
            return_url: 支付成功后返回URL
            notify_url: 支付回调通知URL
        
        Returns:
            str: 支付页面URL
        """
        if not self.alipay_client:
            raise ValueError("支付宝服务未配置")
        
        # 获取订单信息
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise ValueError("订单不存在")
            
        if order.user_id != user_id:
            raise ValueError("无权限支付此订单")
            
        if order.status != "pending_payment":
            raise ValueError("订单状态不允许支付")

        # 生成商户订单号
        out_trade_no = f"ORDER_{order_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # 订单信息
        subject = f"科研检测订单-{order.order_no}"
        body = f"订单号: {order.order_no}"
        total_amount = str(order.total_amount)
        
        # 创建支付记录
        payment = Payment(
            order_id=order_id,
            user_id=user_id,
            payment_method="alipay",
            amount=order.total_amount,
            transaction_id=out_trade_no,
            status="pending"
        )
        
        db.add(payment)
        db.commit()
        db.refresh(payment)
        
        # 构建网页支付请求
        request = AlipayTradePagePayRequest()
        biz_content = {
            "out_trade_no": out_trade_no,
            "total_amount": total_amount,
            "subject": subject,
            "body": body,
            "product_code": "FAST_INSTANT_TRADE_PAY",
            "timeout_express": "30m"
        }
        request.biz_content = biz_content
        
        # 设置回调地址
        if return_url:
            request.return_url = return_url
        if notify_url:
            request.notify_url = notify_url
        else:
            # 默认回调地址
            request.notify_url = f"https://your-domain.com/api/v1/payments/{payment.id}/alipay/notify"
        
        # 执行请求，获取支付表单HTML
        response = self.alipay_client.page_execute(request, "GET")
        
        logger.info(f"创建支付宝支付：订单ID={order_id}, 支付ID={payment.id}")
        
        return response

    async def create_app_payment(
        self,
        db: Session,
        order_id: int,
        user_id: int,
        notify_url: str = None
    ) -> Dict[str, Any]:
        """
        创建支付宝App支付
        
        Args:
            db: 数据库会话
            order_id: 订单ID
            user_id: 用户ID
            notify_url: 支付回调通知URL
        
        Returns:
            dict: 支付参数（包含order_string）
        """
        if not self.alipay_client:
            raise ValueError("支付宝服务未配置")
        
        # 获取订单信息
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise ValueError("订单不存在")
            
        if order.user_id != user_id:
            raise ValueError("无权限支付此订单")
            
        if order.status != "pending_payment":
            raise ValueError("订单状态不允许支付")

        # 生成商户订单号
        out_trade_no = f"ORDER_{order_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # 订单信息
        subject = f"科研检测订单-{order.order_no}"
        body = f"订单号: {order.order_no}"
        total_amount = str(order.total_amount)
        
        # 创建支付记录
        payment = Payment(
            order_id=order_id,
            user_id=user_id,
            payment_method="alipay",
            amount=order.total_amount,
            transaction_id=out_trade_no,
            status="pending"
        )
        
        db.add(payment)
        db.commit()
        db.refresh(payment)
        
        # 构建App支付请求
        request = AlipayTradeAppPayRequest()
        biz_content = {
            "out_trade_no": out_trade_no,
            "total_amount": total_amount,
            "subject": subject,
            "body": body,
            "product_code": "QUICK_MSECURITY_PAY",
            "timeout_express": "30m"
        }
        request.biz_content = biz_content
        
        # 设置回调地址
        if notify_url:
            request.notify_url = notify_url
        else:
            request.notify_url = f"https://your-domain.com/api/v1/payments/{payment.id}/alipay/notify"
        
        # 执行请求
        order_string = self.alipay_client.sdk_execute(request)
        
        logger.info(f"创建支付宝App支付：订单ID={order_id}, 支付ID={payment.id}")
        
        return {
            "payment_id": payment.id,
            "order_string": order_string,
            "out_trade_no": out_trade_no,
            "total_amount": total_amount,
            "subject": subject
        }

    async def verify_notify(self, notify_data: Dict[str, Any]) -> bool:
        """
        验证支付宝回调通知签名
        
        Args:
            notify_data: 回调数据
        
        Returns:
            bool: 签名是否有效
        """
        try:
            # 获取签名
            sign = notify_data.get("sign", "")
            if not sign:
                logger.warning("支付宝回调缺少签名")
                return False
            
            # 移除sign和sign_type参数
            verify_data = {k: v for k, v in notify_data.items() 
                          if k not in ["sign", "sign_type"]}
            
            # 验证签名
            is_valid = verify_with_rsa(
                settings.ALIPAY_PUBLIC_KEY, 
                verify_data, 
                sign
            )
            
            if not is_valid:
                logger.warning("支付宝回调签名验证失败")
            
            return is_valid
            
        except Exception as e:
            logger.error(f"验证支付宝通知失败: {str(e)}")
            return False

    async def handle_notify(
        self,
        db: Session,
        payment_id: int,
        notify_data: Dict[str, Any]
    ) -> bool:
        """
        处理支付宝回调通知
        
        Args:
            db: 数据库会话
            payment_id: 支付ID
            notify_data: 回调数据
        
        Returns:
            bool: 处理是否成功
        """
        try:
            # 验证签名
            if not await self.verify_notify(notify_data):
                logger.error("支付宝通知签名验证失败")
                return False
                
            payment = db.query(Payment).filter(Payment.id == payment_id).first()
            if not payment:
                logger.error(f"支付记录不存在: {payment_id}")
                return False
                
            trade_status = notify_data.get("trade_status")
            out_trade_no = notify_data.get("out_trade_no")
            
            # 验证商户订单号
            if payment.transaction_id != out_trade_no:
                logger.error(f"商户订单号不匹配: {payment.transaction_id} != {out_trade_no}")
                return False
            
            # 处理支付状态
            if trade_status in ["TRADE_SUCCESS", "TRADE_FINISHED"]:
                # 支付成功
                payment.status = "paid"
                payment.paid_at = datetime.utcnow()
                
                # 更新订单状态
                order = db.query(Order).filter(Order.id == payment.order_id).first()
                if order:
                    order.status = "paid"
                    order.paid_at = datetime.utcnow()
                
                db.commit()
                logger.info(f"支付成功：支付ID={payment_id}, 订单ID={payment.order_id}")
                return True
                
            elif trade_status == "TRADE_CLOSED":
                # 交易关闭
                payment.status = "failed"
                db.commit()
                logger.info(f"交易关闭：支付ID={payment_id}")
                return True
                
            return False
            
        except Exception as e:
            logger.error(f"处理支付宝通知失败: {str(e)}")
            db.rollback()
            return False

    async def query_payment(self, out_trade_no: str) -> Dict[str, Any]:
        """
        查询支付状态
        
        Args:
            out_trade_no: 商户订单号
        
        Returns:
            dict: 查询结果
        """
        if not self.alipay_client:
            raise ValueError("支付宝服务未配置")
            
        try:
            request = AlipayTradeQueryRequest()
            biz_content = {"out_trade_no": out_trade_no}
            request.biz_content = biz_content
            
            response = self.alipay_client.execute(request)
            return json.loads(response) if response else {}
            
        except Exception as e:
            logger.error(f"查询支付状态失败: {str(e)}")
            return {}

    async def close_payment(self, out_trade_no: str) -> bool:
        """
        关闭支付订单
        
        Args:
            out_trade_no: 商户订单号
        
        Returns:
            bool: 是否成功
        """
        if not self.alipay_client:
            raise ValueError("支付宝服务未配置")
            
        try:
            request = AlipayTradeCloseRequest()
            biz_content = {"out_trade_no": out_trade_no}
            request.biz_content = biz_content
            
            response = self.alipay_client.execute(request)
            result = json.loads(response) if response else {}
            return result.get("code") == "10000"
            
        except Exception as e:
            logger.error(f"关闭支付订单失败: {str(e)}")
            return False

    async def refund(
        self,
        db: Session,
        payment_id: int,
        refund_amount: Decimal = None,
        refund_reason: str = "用户申请退款"
    ) -> Dict[str, Any]:
        """
        申请退款
        
        Args:
            db: 数据库会话
            payment_id: 支付ID
            refund_amount: 退款金额（为空则全额退款）
            refund_reason: 退款原因
        
        Returns:
            dict: 退款结果
        """
        if not self.alipay_client:
            raise ValueError("支付宝服务未配置")
            
        try:
            payment = db.query(Payment).filter(Payment.id == payment_id).first()
            if not payment:
                raise ValueError("支付记录不存在")
                
            if payment.status != "paid":
                raise ValueError("订单未支付，无法退款")
                
            # 退款金额默认为支付金额
            if refund_amount is None:
                refund_amount = payment.amount
                
            # 生成退款单号
            out_refund_no = f"REFUND_{payment_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # 调用支付宝退款接口
            request = AlipayTradeRefundRequest()
            biz_content = {
                "out_trade_no": payment.transaction_id,
                "refund_amount": str(refund_amount),
                "out_request_no": out_refund_no,
                "refund_reason": refund_reason
            }
            request.biz_content = biz_content
            
            response = self.alipay_client.execute(request)
            result = json.loads(response) if response else {}
            
            if result.get("code") == "10000":
                # 退款成功，创建退款记录
                refund_payment = Payment(
                    order_id=payment.order_id,
                    user_id=payment.user_id,
                    payment_method="alipay",
                    amount=-refund_amount,  # 负数表示退款
                    transaction_id=out_refund_no,
                    status="refunded"
                )
                
                db.add(refund_payment)
                db.commit()
                
                logger.info(f"退款成功：支付ID={payment_id}, 退款金额={refund_amount}")
                
                return {
                    "success": True,
                    "refund_id": refund_payment.id,
                    "out_refund_no": out_refund_no,
                    "refund_amount": refund_amount
                }
            else:
                logger.error(f"退款失败：{result.get('msg', '未知错误')}")
                return {
                    "success": False,
                    "error": result.get("msg", "退款失败")
                }
                
        except Exception as e:
            logger.error(f"退款失败: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }


# 创建全局实例
alipay_service = AlipayService()

