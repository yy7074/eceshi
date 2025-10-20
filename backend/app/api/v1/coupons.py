"""
优惠券系统API（简化版）
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.response import Response
from app.api.v1.deps import get_current_user
from app.models.user import User


router = APIRouter()


@router.get("/my", summary="获取我的优惠券")
async def get_my_coupons(
    status: str = Query("available", description="券状态：available,used,expired"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取用户的优惠券列表
    """
    # TODO: 实现优惠券查询逻辑
    # 目前返回空列表，确保API可调用
    return Response.success(data={
        "items": [],
        "total": 0,
        "page": page,
        "page_size": page_size,
        "available_count": 0,
        "total_savings": 0
    })


@router.get("/available", summary="获取可领取优惠券")
async def get_available_coupons(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    获取可领取的优惠券列表
    """
    # TODO: 实现可领取优惠券查询逻辑
    return Response.success(data={
        "items": [],
        "total": 0,
        "page": page,
        "page_size": page_size
    })


@router.post("/receive", summary="领取优惠券")
async def receive_coupon(
    coupon_id: int = Query(..., description="优惠券ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    领取优惠券
    """
    # TODO: 实现优惠券领取逻辑
    return Response.success(message="领取成功")

