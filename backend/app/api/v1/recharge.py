"""
钱包充值API
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import Response as FastAPIResponse
from sqlalchemy.orm import Session
import xml.etree.ElementTree as ET
from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

from app.core.database import get_db
from app.core.response import Response
from app.api.deps import get_current_user
from app.models.user import User
from app.models.recharge import RechargeRecord, RechargeStatus, RechargeMethod
from app.services.wechatpay_service import wechatpay_service

router = APIRouter()


class RechargeRequest(BaseModel):
    """充值请求"""
    amount: float = Field(..., description="充值金额", ge=0.01, le=50000)
    payment_method: str = Field(..., description="支付方式: wechat")


class RechargeListQuery(BaseModel):
    """充值记录查询"""
    page: int = Field(1, ge=1)
    page_size: int = Field(10, ge=1, le=100)
    status: Optional[str] = None


def generate_recharge_no() -> str:
    """生成充值单号"""
    import time
    import random
    timestamp = int(time.time() * 1000)
    rand = random.randint(1000, 9999)
    return f"RC{timestamp}{rand}"


def calculate_bonus(amount: Decimal) -> Decimal:
    """计算充值赠送金额"""
    # 充值规则：
    # 100元以下：不赠送
    # 100-499元：赠送5%
    # 500-999元：赠送10%
    # 1000-4999元：赠送15%
    # 5000元及以上：赠送20%
    
    if amount < 100:
        return Decimal("0")
    elif amount < 500:
        return amount * Decimal("0.05")
    elif amount < 1000:
        return amount * Decimal("0.10")
    elif amount < 5000:
        return amount * Decimal("0.15")
    else:
        return amount * Decimal("0.20")


@router.post("/create", summary="创建充值订单")
async def create_recharge(
    data: RechargeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    创建充值订单
    
    充值赠送规则：
    - 100元以下：不赠送
    - 100-499元：赠送5%
    - 500-999元：赠送10%
    - 1000-4999元：赠送15%
    - 5000元及以上：赠送20%
    """
    try:
        # 验证支付方式
        if data.payment_method not in ["wechat"]:
            raise HTTPException(status_code=400, detail="不支持的支付方式")
        
        # 计算金额
        amount = Decimal(str(data.amount))
        bonus_amount = calculate_bonus(amount)
        actual_amount = amount + bonus_amount
        
        # 创建充值记录
        recharge = RechargeRecord(
            user_id=current_user.id,
            recharge_no=generate_recharge_no(),
            amount=amount,
            actual_amount=actual_amount,
            bonus_amount=bonus_amount,
            payment_method=RechargeMethod.WECHAT,
            status=RechargeStatus.PENDING
        )
        db.add(recharge)
        db.commit()
        db.refresh(recharge)
        
        # 微信支付
        if data.payment_method == "wechat":
            # 检查用户是否有openid
            if not current_user.wechat_openid:
                raise HTTPException(status_code=400, detail="请先使用微信登录")
            
            # 调用微信支付服务
            try:
                pay_params = await wechatpay_service.create_recharge_payment(
                    db=db,
                    recharge=recharge,
                    user_id=current_user.id,
                    openid=current_user.wechat_openid
                )
                
                return Response.success(data={
                    "recharge_id": recharge.id,
                    "recharge_no": recharge.recharge_no,
                    "amount": float(amount),
                    "bonus_amount": float(bonus_amount),
                    "actual_amount": float(actual_amount),
                    **pay_params,  # 包含微信支付所需参数
                    "status": "pending"
                }, message="请在新页面完成支付")
                
            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=500, detail=f"创建微信支付失败: {str(e)}")
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"创建充值订单失败: {str(e)}")


@router.get("/records", summary="获取充值记录")
async def get_recharge_records(
    page: int = 1,
    page_size: int = 10,
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户充值记录"""
    try:
        query = db.query(RechargeRecord).filter(
            RechargeRecord.user_id == current_user.id
        )
        
        # 状态筛选
        if status:
            query = query.filter(RechargeRecord.status == status)
        
        # 总数
        total = query.count()
        
        # 分页
        records = query.order_by(
            RechargeRecord.created_at.desc()
        ).offset((page - 1) * page_size).limit(page_size).all()
        
        return Response.success(data={
            "total": total,
            "page": page,
            "page_size": page_size,
            "items": [
                {
                    "id": r.id,
                    "recharge_no": r.recharge_no,
                    "amount": float(r.amount),
                    "bonus_amount": float(r.bonus_amount),
                    "actual_amount": float(r.actual_amount),
                    "payment_method": r.payment_method.value,
                    "status": r.status.value,
                    "created_at": r.created_at.isoformat() if r.created_at else None,
                    "paid_at": r.paid_at.isoformat() if r.paid_at else None,
                    "completed_at": r.completed_at.isoformat() if r.completed_at else None
                }
                for r in records
            ]
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取充值记录失败: {str(e)}")


@router.get("/{recharge_id}", summary="获取充值详情")
async def get_recharge_detail(
    recharge_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取充值订单详情"""
    recharge = db.query(RechargeRecord).filter(
        RechargeRecord.id == recharge_id,
        RechargeRecord.user_id == current_user.id
    ).first()
    
    if not recharge:
        raise HTTPException(status_code=404, detail="充值记录不存在")
    
    return Response.success(data={
        "id": recharge.id,
        "recharge_no": recharge.recharge_no,
        "amount": float(recharge.amount),
        "bonus_amount": float(recharge.bonus_amount),
        "actual_amount": float(recharge.actual_amount),
        "payment_method": recharge.payment_method.value,
        "transaction_id": recharge.transaction_id,
        "status": recharge.status.value,
        "remark": recharge.remark,
        "created_at": recharge.created_at.isoformat() if recharge.created_at else None,
        "paid_at": recharge.paid_at.isoformat() if recharge.paid_at else None,
        "completed_at": recharge.completed_at.isoformat() if recharge.completed_at else None
    })


@router.get("/bonus/rules", summary="获取充值赠送规则")
async def get_bonus_rules():
    """获取充值赠送规则"""
    return Response.success(data={
        "rules": [
            {
                "min_amount": 0,
                "max_amount": 99.99,
                "bonus_rate": 0,
                "description": "100元以下不赠送"
            },
            {
                "min_amount": 100,
                "max_amount": 499.99,
                "bonus_rate": 0.05,
                "description": "充100送5，赠送5%"
            },
            {
                "min_amount": 500,
                "max_amount": 999.99,
                "bonus_rate": 0.10,
                "description": "充500送50，赠送10%"
            },
            {
                "min_amount": 1000,
                "max_amount": 4999.99,
                "bonus_rate": 0.15,
                "description": "充1000送150，赠送15%"
            },
            {
                "min_amount": 5000,
                "max_amount": 50000,
                "bonus_rate": 0.20,
                "description": "充5000送1000，赠送20%"
            }
        ],
        "examples": [
            {"amount": 50, "bonus": 0, "total": 50},
            {"amount": 100, "bonus": 5, "total": 105},
            {"amount": 500, "bonus": 50, "total": 550},
            {"amount": 1000, "bonus": 150, "total": 1150},
            {"amount": 5000, "bonus": 1000, "total": 6000}
        ]
    })


@router.post("/wechat/notify", summary="微信支付回调（充值）")
async def wechat_recharge_notify(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    接收微信支付回调通知（充值）
    """
    try:
        # 读取XML数据
        body = await request.body()
        xml_str = body.decode('utf-8')
        
        print(f"[充值回调] 收到微信回调:")
        print(f"[充值回调] 原始XML: {xml_str}")
        
        # 解析XML
        root = ET.fromstring(xml_str)
        notify_data = {}
        for child in root:
            notify_data[child.tag] = child.text
        
        print(f"[充值回调] 解析数据: {notify_data}")
        
        # 处理回调
        result = await wechatpay_service.handle_recharge_notify(db, notify_data)
        
        if result:
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
        print(f'充值微信支付回调异常: {str(e)}')
        return FastAPIResponse(
            content='<xml><return_code><![CDATA[FAIL]]></return_code><return_msg><![CDATA[FAIL]]></return_msg></xml>',
            media_type='application/xml'
        )

