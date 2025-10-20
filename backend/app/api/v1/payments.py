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
from app.services.alipay_service import alipay_service
from app.services.wechatpay_service import wechatpay_service

router = APIRouter()


def generate_payment_no() -> str:
    """生成支付单号"""
    return f"PAY{int(time.time())}{int(time.time() * 1000000) % 1000000}"


@router.post("/create")
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
        try:
            # 调用支付宝服务创建支付
            # 根据平台选择H5或App支付
            payment_type = data.payment_channel if hasattr(data, 'payment_channel') else "h5"
            
            if payment_type == "app":
                # App支付
                result = await alipay_service.create_app_payment(
                    db=db,
                    order_id=order.id,
                    user_id=current_user.id,
                    notify_url=data.notify_url if hasattr(data, 'notify_url') else None
                )
                
                return SuccessResponse(data={
                    "payment_id": result["payment_id"],
                    "order_string": result["order_string"],
                    "out_trade_no": result["out_trade_no"],
                    "status": "pending"
                }, message="请在新页面完成支付")
            else:
                # H5/网页支付
                pay_url = await alipay_service.create_h5_payment(
                    db=db,
                    order_id=order.id,
                    user_id=current_user.id,
                    return_url=data.return_url if hasattr(data, 'return_url') else None,
                    notify_url=data.notify_url if hasattr(data, 'notify_url') else None
                )
                
                return SuccessResponse(data={
                    "pay_url": pay_url,
                    "status": "pending"
                }, message="请在新页面完成支付")
                
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"创建支付失败: {str(e)}")
    
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
        
        # 调用微信支付服务获取支付参数
        try:
            # 获取用户openid
            openid = current_user.wechat_openid
            if not openid:
                raise HTTPException(status_code=400, detail="请先使用微信登录")
            
            pay_params = await wechatpay_service.create_jsapi_payment(
                db=db,
                order=order,
                user_id=current_user.id,
                openid=openid
            )
            
            return SuccessResponse(data={
                "payment_id": payment.id,
                "payment_no": payment.payment_no,
                **pay_params,  # 包含appId, timeStamp, nonceStr, package, signType, paySign
                "status": "pending"
            }, message="请在新页面完成支付")
            
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"创建微信支付失败: {str(e)}")
    
    else:
        raise HTTPException(status_code=400, detail="不支持的支付方式")


@router.get("/{payment_id}/status")
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


@router.post("/{payment_id}/alipay/notify")
async def alipay_notify(
    payment_id: int,
    db: Session = Depends(get_db)
):
    """
    支付宝支付回调
    """
    from fastapi import Request
    from fastapi.responses import PlainTextResponse
    
    # 获取回调数据
    # 注意：实际使用时需要从Request中获取表单数据
    # notify_data = await request.form()
    # notify_data = dict(notify_data)
    
    # 这里简化处理，实际应该验证签名
    try:
        # 示例：处理回调
        # result = await alipay_service.handle_notify(
        #     db=db,
        #     payment_id=payment_id,
        #     notify_data=notify_data
        # )
        # 
        # if result:
        #     return PlainTextResponse("success")
        # else:
        #     return PlainTextResponse("fail")
        
        # 临时返回success
        return PlainTextResponse("success")
    except Exception as e:
        return PlainTextResponse("fail")


@router.post("/wechat/notify")
async def wechat_notify(
    db: Session = Depends(get_db)
):
    """
    微信支付回调
    """
    from fastapi import Request
    from fastapi.responses import Response as FastAPIResponse
    
    try:
        # TODO: 从Request中获取XML数据并解析
        # 实际使用时需要：
        # 1. 读取request.body()
        # 2. 解析XML
        # 3. 验证签名
        # 4. 更新订单状态
        
        # 模拟回调数据
        notify_data = {
            'return_code': 'SUCCESS',
            'result_code': 'SUCCESS',
            'out_trade_no': '',
            'transaction_id': '',
        }
        
        # 处理回调
        result = await wechatpay_service.handle_notify(db, notify_data)
        
        if result:
            # 返回XML格式的success
            return FastAPIResponse(
                content='<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>',
                media_type='application/xml'
            )
        else:
            return FastAPIResponse(
                content='<xml><return_code><![CDATA[FAIL]]></return_code><return_msg><![CDATA[FAIL]]></return_msg></xml>',
                media_type='application/xml'
            )
    except Exception as e:
        print(f'微信支付回调异常: {str(e)}')
        return FastAPIResponse(
            content='<xml><return_code><![CDATA[FAIL]]></return_code><return_msg><![CDATA[FAIL]]></return_msg></xml>',
            media_type='application/xml'
        )

