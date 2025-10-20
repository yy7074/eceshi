"""
邀请好友API（简化版）
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.response import Response
from app.api.v1.deps import get_current_user
from app.models.user import User


router = APIRouter()


@router.get("/stats", summary="获取邀请统计")
async def get_invite_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取用户的邀请统计数据
    """
    # TODO: 实现邀请统计逻辑
    return Response.success(data={
        "withdrawable": 0,  # 可提现奖励
        "my_invites": 0,  # 我的邀请人数
        "predicted_orders": 0,  # 预计订单数
        "predicted_rewards": 0,  # 预计奖励
        "earned_rewards": 0  # 已获得奖励
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
    # TODO: 实现邀请记录查询逻辑
    return Response.success(data={
        "items": [],
        "total": 0,
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
    # TODO: 实现提现逻辑
    return Response.success(message="提现申请已提交")

