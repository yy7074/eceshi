"""
邀请好友功能API
"""
from fastapi import APIRouter, Depends, Query, Body, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime

from app.core.database import get_db
from app.core.response import Response
from app.api.v1.deps import get_current_user
from app.models.user import User
from app.models.invite import InviteRecord, WithdrawRecord, InviteConfig, InviteStatus, WithdrawStatus


router = APIRouter()


class WithdrawRequest(BaseModel):
    """提现请求"""
    amount: float
    account_type: str  # alipay/wechat/bank
    account_name: str
    account_number: str


@router.get("/stats", summary="获取邀请统计")
async def get_invite_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取用户的邀请统计数据
    """
    # 查询邀请记录
    invite_records = db.query(InviteRecord).filter(
        InviteRecord.inviter_id == current_user.id
    ).all()
    
    # 统计数据
    total_invites = len(invite_records)
    completed_invites = len([r for r in invite_records if r.status == InviteStatus.COMPLETED])
    pending_invites = len([r for r in invite_records if r.status == InviteStatus.PENDING])
    
    # 计算奖励金额
    total_reward = sum(float(r.reward_amount) for r in invite_records if r.status == InviteStatus.COMPLETED)
    
    # 查询已提现金额
    withdrawn_records = db.query(WithdrawRecord).filter(
        WithdrawRecord.user_id == current_user.id,
        WithdrawRecord.status.in_([WithdrawStatus.APPROVED, WithdrawStatus.COMPLETED])
    ).all()
    withdrawn = sum(float(r.amount) for r in withdrawn_records)
    
    # 可提现金额
    withdrawable = total_reward - withdrawn
    
    return Response.success(data={
        "withdrawable": withdrawable,
        "my_invites": total_invites,
        "completed_invites": completed_invites,
        "pending_invites": pending_invites,
        "total_reward": total_reward,
        "withdrawn": withdrawn
    })


@router.get("/records", summary="获取邀请记录")
async def get_invite_records(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取用户的邀请记录
    """
    # 查询邀请记录
    query = db.query(InviteRecord).filter(
        InviteRecord.inviter_id == current_user.id
    )
    
    # 总数
    total = query.count()
    
    # 分页查询
    items = query.order_by(InviteRecord.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    # 格式化返回数据
    records = []
    for item in items:
        records.append({
            "id": item.id,
            "invitee_name": item.invitee_name,
            "invitee_phone": item.invitee_phone,
            "reward_amount": float(item.reward_amount) if item.reward_amount else 0,
            "status": item.status.value,
            "first_order_amount": float(item.first_order_amount) if item.first_order_amount else 0,
            "invited_at": item.invited_at.isoformat() if item.invited_at else None,
            "completed_at": item.completed_at.isoformat() if item.completed_at else None
        })
    
    return Response.success(data={
        "items": records,
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.post("/withdraw", summary="申请提现")
async def withdraw_rewards(
    amount: float = Query(..., description="提现金额"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    申请提现邀请奖励
    """
    # 获取邀请配置
    config = db.query(InviteConfig).filter(InviteConfig.is_active == 1).first()
    if not config:
        raise HTTPException(status_code=400, detail="邀请功能暂未开放")
    
    # 检查提现金额
    amount = Decimal(str(data.amount))
    if amount < config.min_withdraw_amount:
        raise HTTPException(status_code=400, detail=f"最低提现金额为{config.min_withdraw_amount}元")
    
    # 计算可提现金额
    invite_records = db.query(InviteRecord).filter(
        InviteRecord.inviter_id == current_user.id,
        InviteRecord.status == InviteStatus.COMPLETED
    ).all()
    total_reward = sum(r.reward_amount for r in invite_records)
    
    withdrawn_records = db.query(WithdrawRecord).filter(
        WithdrawRecord.user_id == current_user.id,
        WithdrawRecord.status.in_([WithdrawStatus.APPROVED, WithdrawStatus.COMPLETED])
    ).all()
    withdrawn = sum(r.amount for r in withdrawn_records)
    
    available = total_reward - withdrawn
    
    if amount > available:
        raise HTTPException(status_code=400, detail=f"可提现金额不足，当前可提现：{available}元")
    
    # 创建提现记录
    withdraw = WithdrawRecord(
        user_id=current_user.id,
        amount=amount,
        withdraw_type="invite_reward",
        account_type=data.account_type,
        account_name=data.account_name,
        account_number=data.account_number,
        status=WithdrawStatus.PENDING
    )
    db.add(withdraw)
    db.commit()
    db.refresh(withdraw)
    
    return Response.success(data={
        "withdraw_id": withdraw.id,
        "amount": float(withdraw.amount),
        "status": withdraw.status.value
    }, message="提现申请已提交，请等待审核")

