"""
团队功能API（简化版）
"""
from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.core.database import get_db
from app.core.response import Response
from app.api.v1.deps import get_current_user
from app.models.user import User


router = APIRouter()


class CreateGroupRequest(BaseModel):
    """创建团队请求"""
    name: str
    avatar: Optional[str] = None
    unit_type: str
    region: str
    address: str
    leader_name: str
    leader_phone: str
    leader_email: Optional[str] = None


@router.post("/create", summary="创建团队")
async def create_group(
    request: CreateGroupRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    创建团队
    """
    # TODO: 实现团队创建逻辑
    return Response.success(data={"group_id": 1}, message="团队创建成功")


@router.get("/my", summary="获取我的团队")
async def get_my_groups(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取用户所在的团队列表
    """
    # TODO: 实现团队查询逻辑
    return Response.success(data={
        "items": [],
        "total": 0
    })


@router.get("/{group_id}", summary="获取团队详情")
async def get_group_detail(
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取团队详情
    """
    # TODO: 实现团队详情查询逻辑
    return Response.success(data={
        "id": group_id,
        "name": "示例团队",
        "avatar": "",
        "member_count": 0,
        "leader_name": "",
        "created_at": None
    })


@router.post("/join", summary="加入团队")
async def join_group(
    group_code: str = Query(..., description="团队邀请码"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    通过邀请码加入团队
    """
    # TODO: 实现加入团队逻辑
    return Response.success(message="已申请加入团队")


@router.post("/join-by-phone", summary="通过手机号加入团队")
async def join_group_by_phone(
    phone: str = Body(..., embed=True, description="团队负责人手机号"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    通过团队负责人手机号加入团队
    """
    # TODO: 实现通过手机号加入团队逻辑
    return Response.success(message="已申请加入团队")

