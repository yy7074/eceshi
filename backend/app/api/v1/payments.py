"""
支付相关API
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import time
from decimal import Decimal

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.order import Order, Payment, OrderStatusHistory
from app.schemas.order import PaymentCreate, PaymentInDB
from app.core.response import SuccessResponse
from app.core.security import verify_password

router = APIRouter()


def generate_payment_no() -> str:
    """生成支付单号"""
    return f"PAY{int(time.time())}{int(time.time() * 1000000) % 1000000}"


@router.post("/create", response_model=SuccessResponse)
async def create_payment(
    data: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建支付
    """
    # 查询订单
    order = db.query(Order).filter(
        Order.id == data.order_id,
        Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    if order.status != "pending_payment":
        raise HTTPException(status_code=400, detail="订单状态不正确")
    
    # 检查是否已支付
    if order.paid_fee >= order.total_fee:
        raise HTTPException(status_code=400, detail="订单已支付")
    
    # 计算待支付金额
    amount_to_pay = order.total_fee - order.paid_fee
    
    # 余额支付
    if data.payment_method == "balance":
        # 验证支付密码（这里简化处理，实际应该有独立的支付密码）
        if not data.payment_password:
            raise HTTPException(status_code=400, detail="请输入支付密码")
        
        # 这里简化验证，实际应该验证专门的支付密码
        if not verify_password(data.payment_password, current_user.hashed_password):
            raise HTTPException(status_code=400, detail="支付密码错误")
        
        # 检查余额
        # TODO: 实际应该从用户账户表获取
        user_balance = Decimal("1000.00")  # 模拟余额
        
        if user_balance < amount_to_pay:
            raise HTTPException(status_code=400, detail="余额不足")
        
        # 创建支付记录
        payment = Payment(
            payment_no=generate_payment_no(),
            order_id=order.id,
            order_no=order.order_no,
            user_id=current_user.id,
            payment_method="balance",
            payment_channel="balance",
            amount=amount_to_pay,
            status="success",
            paid_at=datetime.now()
        )
        db.add(payment)
        
        # 更新订单状态
        order.paid_fee = order.total_fee
        order.status = "confirmed"
        order.payment_method = "balance"
        order.paid_at = datetime.now()
        
        # 记录状态变更
        history = OrderStatusHistory(
            order_id=order.id,
            from_status="pending_payment",
            to_status="confirmed",
            operator_id=current_user.id,
            operator_type="user",
            remark="余额支付成功"
        )
        db.add(history)
        
        # TODO: 扣除用户余额
        
        db.commit()
        db.refresh(payment)
        
        return SuccessResponse(data={
            "payment_id": payment.id,
            "payment_no": payment.payment_no,
            "status": "success",
            "message": "支付成功"
        }, message="支付成功")
    
    # 支付宝支付
    elif data.payment_method == "alipay":
        # 创建支付记录
        payment = Payment(
            payment_no=generate_payment_no(),
            order_id=order.id,
            order_no=order.order_no,
            user_id=current_user.id,
            payment_method="alipay",
            payment_channel="alipay_web",
            amount=amount_to_pay,
            status="pending"
        )
        db.add(payment)
        db.commit()
        db.refresh(payment)
        
        # TODO: 调用支付宝SDK获取支付参数
        pay_params = {
            "url": "https://openapi.alipay.com/gateway.do",
            "params": "mock_params"
        }
        
        return SuccessResponse(data={
            "payment_id": payment.id,
            "payment_no": payment.payment_no,
            "pay_params": pay_params,
            "status": "pending"
        }, message="请在新页面完成支付")
    
    # 微信支付
    elif data.payment_method == "wechat":
        # 创建支付记录
        payment = Payment(
            payment_no=generate_payment_no(),
            order_id=order.id,
            order_no=order.order_no,
            user_id=current_user.id,
            payment_method="wechat",
            payment_channel="wechat_jsapi",
            amount=amount_to_pay,
            status="pending"
        )
        db.add(payment)
        db.commit()
        db.refresh(payment)
        
        # TODO: 调用微信支付SDK获取支付参数
        pay_params = {
            "appId": "wx1234567890",
            "timeStamp": str(int(time.time())),
            "nonceStr": "mock_nonce",
            "package": "prepay_id=mock_prepay_id",
            "signType": "RSA",
            "paySign": "mock_sign"
        }
        
        return SuccessResponse(data={
            "payment_id": payment.id,
            "payment_no": payment.payment_no,
            "pay_params": pay_params,
            "status": "pending"
        }, message="请在新页面完成支付")
    
    else:
        raise HTTPException(status_code=400, detail="不支持的支付方式")


@router.get("/{payment_id}/status", response_model=SuccessResponse)
async def get_payment_status(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    查询支付状态
    """
    payment = db.query(Payment).filter(
        Payment.id == payment_id,
        Payment.user_id == current_user.id
    ).first()
    
    if not payment:
        raise HTTPException(status_code=404, detail="支付记录不存在")
    
    return SuccessResponse(data={
        "payment_id": payment.id,
        "payment_no": payment.payment_no,
        "status": payment.status,
        "amount": float(payment.amount),
        "paid_at": payment.paid_at.isoformat() if payment.paid_at else None
    })


@router.post("/alipay/notify", response_model=SuccessResponse)
async def alipay_notify(
    db: Session = Depends(get_db)
):
    """
    支付宝支付回调
    """
    # TODO: 验证签名、处理回调
    return SuccessResponse(message="success")


@router.post("/wechat/notify", response_model=SuccessResponse)
async def wechat_notify(
    db: Session = Depends(get_db)
):
    """
    微信支付回调
    """
    # TODO: 验证签名、处理回调
    return SuccessResponse(message="success")

