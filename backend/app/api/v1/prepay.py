"""
预付记录API
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import Optional
from decimal import Decimal

from app.core.database import get_db
from app.core.response import Response
from app.api.v1.deps import get_current_user
from app.models.user import User
from app.models.recharge import RechargeRecord, RechargeStatus
from app.models.order import Order


router = APIRouter()


@router.get("/stats", summary="获取预付统计")
async def get_prepay_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取用户的预付统计信息"""
    # 累计充值（成功的）
    total_recharge = db.query(func.sum(RechargeRecord.actual_amount)).filter(
        RechargeRecord.user_id == current_user.id,
        RechargeRecord.status == RechargeStatus.SUCCESS
    ).scalar() or Decimal(0)
    
    # 累计使用（已支付订单中使用余额支付的部分）
    # 这里简化处理，假设使用预付余额的金额从用户表获取
    total_used = total_recharge - (current_user.prepaid_balance or Decimal(0))
    if total_used < 0:
        total_used = Decimal(0)
    
    # 当前余额
    current_balance = current_user.prepaid_balance or Decimal(0)
    
    return Response.success(data={
        "total_prepay": float(total_recharge),
        "used_prepay": float(total_used),
        "remain_prepay": float(current_balance)
    })


@router.get("/records", summary="获取预付记录")
async def get_prepay_records(
    record_type: Optional[str] = Query(None, description="记录类型: recharge/consume"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取预付记录（充值和消费）"""
    records = []
    
    # 获取充值记录
    if not record_type or record_type == "recharge":
        recharges = db.query(RechargeRecord).filter(
            RechargeRecord.user_id == current_user.id,
            RechargeRecord.status == RechargeStatus.SUCCESS
        ).order_by(desc(RechargeRecord.completed_at)).all()
        
        for r in recharges:
            records.append({
                "id": r.id,
                "type": "in",
                "title": f"充值 - {r.payment_method.value if r.payment_method else ''}",
                "amount": float(r.actual_amount) if r.actual_amount else 0,
                "time": r.completed_at.strftime("%Y-%m-%d %H:%M") if r.completed_at else "",
                "status": "success",
                "status_text": "充值成功",
                "order_no": r.recharge_no
            })
    
    # 获取消费记录（使用余额支付的订单）
    if not record_type or record_type == "consume":
        orders = db.query(Order).filter(
            Order.user_id == current_user.id,
            Order.payment_method == "balance",
            Order.status.in_(['paid', 'confirmed', 'testing', 'completed'])
        ).order_by(desc(Order.paid_at)).all()
        
        for o in orders:
            records.append({
                "id": o.id,
                "type": "out",
                "title": f"订单支付 - {o.project_name}",
                "amount": float(o.paid_fee) if o.paid_fee else 0,
                "time": o.paid_at.strftime("%Y-%m-%d %H:%M") if o.paid_at else "",
                "status": "success",
                "status_text": "支付成功",
                "order_no": o.order_no
            })
    
    # 按时间排序
    records.sort(key=lambda x: x["time"], reverse=True)
    
    # 分页
    total = len(records)
    start = (page - 1) * page_size
    end = start + page_size
    paged_records = records[start:end]
    
    return Response.success(data={
        "items": paged_records,
        "total": total,
        "page": page,
        "page_size": page_size
    })

