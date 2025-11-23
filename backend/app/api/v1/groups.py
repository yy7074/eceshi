"""
团队功能API
"""
from fastapi import APIRouter, Depends, Query, Body, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import random
import string

from app.core.database import get_db
from app.core.response import Response
from app.api.v1.deps import get_current_user
from app.models.user import User
from app.models.group import UserGroup, GroupMember, GroupRole, GroupStatus


router = APIRouter()


def generate_invite_code() -> str:
    """生成邀请码"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


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
    # 检查用户是否已经是某个团队的负责人
    existing_group = db.query(UserGroup).filter(
        UserGroup.owner_id == current_user.id,
        UserGroup.status == GroupStatus.ACTIVE
    ).first()
    
    if existing_group:
        raise HTTPException(status_code=400, detail="您已经创建过团队，一个用户只能创建一个团队")
    
    # 生成唯一的邀请码
    invite_code = generate_invite_code()
    while db.query(UserGroup).filter(UserGroup.invite_code == invite_code).first():
        invite_code = generate_invite_code()
    
    # 创建团队
    group = UserGroup(
        name=request.name,
        avatar=request.avatar,
        description=f"{request.unit_type} - {request.region}",
        owner_id=current_user.id,
        owner_name=request.leader_name,
        owner_phone=request.leader_phone,
        university=request.region,
        department=request.address,
        invite_code=invite_code,
        member_count=1,
        status=GroupStatus.ACTIVE
    )
    db.add(group)
    db.flush()
    
    # 添加创建者为团队成员
    member = GroupMember(
        group_id=group.id,
        user_id=current_user.id,
        nickname=current_user.nickname or request.leader_name,
        avatar=current_user.avatar,
        phone=current_user.phone,
        role=GroupRole.OWNER
    )
    db.add(member)
    
    db.commit()
    db.refresh(group)
    
    return Response.success(data={
        "group_id": group.id,
        "invite_code": group.invite_code,
        "name": group.name
    }, message="团队创建成功")


@router.get("/my", summary="获取我的团队")
async def get_my_groups(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取用户所在的团队列表
    """
    # 查询用户所在的团队
    member_records = db.query(GroupMember).filter(
        GroupMember.user_id == current_user.id
    ).all()
    
    group_ids = [m.group_id for m in member_records]
    
    if not group_ids:
        return Response.success(data={"items": [], "total": 0})
    
    # 查询团队详情
    groups = db.query(UserGroup).filter(
        UserGroup.id.in_(group_ids),
        UserGroup.status == GroupStatus.ACTIVE
    ).all()
    
    # 格式化返回数据
    items = []
    for group in groups:
        # 获取用户在该团队的角色
        member = next((m for m in member_records if m.group_id == group.id), None)
        items.append({
            "id": group.id,
            "name": group.name,
            "avatar": group.avatar,
            "description": group.description,
            "owner_name": group.owner_name,
            "member_count": group.member_count,
            "my_role": member.role.value if member else "member",
            "invite_code": group.invite_code if member and member.role == GroupRole.OWNER else None,
            "created_at": group.created_at.isoformat() if group.created_at else None
        })
    
    return Response.success(data={"items": items, "total": len(items)})


@router.get("/{group_id}", summary="获取团队详情")
async def get_group_detail(
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取团队详情
    """
    # 查询团队
    group = db.query(UserGroup).filter(
        UserGroup.id == group_id,
        UserGroup.status == GroupStatus.ACTIVE
    ).first()
    
    if not group:
        raise HTTPException(status_code=404, detail="团队不存在")
    
    # 查询成员列表
    members = db.query(GroupMember).filter(
        GroupMember.group_id == group_id
    ).order_by(GroupMember.role.asc(), GroupMember.joined_at.asc()).all()
    
    # 检查当前用户是否是成员
    is_member = any(m.user_id == current_user.id for m in members)
    
    # 格式化成员列表
    member_list = []
    for member in members:
        member_list.append({
            "user_id": member.user_id,
            "nickname": member.nickname,
            "avatar": member.avatar,
            "role": member.role.value,
            "order_count": member.order_count,
            "total_spent": float(member.total_spent) if member.total_spent else 0,
            "joined_at": member.joined_at.isoformat() if member.joined_at else None
        })
    
    return Response.success(data={
        "id": group.id,
        "name": group.name,
        "avatar": group.avatar,
        "description": group.description,
        "owner_id": group.owner_id,
        "owner_name": group.owner_name,
        "owner_phone": group.owner_phone,
        "university": group.university,
        "department": group.department,
        "invite_code": group.invite_code if is_member else None,
        "member_count": group.member_count,
        "total_orders": group.total_orders,
        "total_spent": float(group.total_spent) if group.total_spent else 0,
        "is_member": is_member,
        "members": member_list,
        "created_at": group.created_at.isoformat() if group.created_at else None
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
    # 查询团队
    group = db.query(UserGroup).filter(
        UserGroup.invite_code == group_code,
        UserGroup.status == GroupStatus.ACTIVE
    ).first()
    
    if not group:
        raise HTTPException(status_code=404, detail="邀请码无效或团队不存在")
    
    # 检查是否已经是成员
    existing_member = db.query(GroupMember).filter(
        GroupMember.group_id == group.id,
        GroupMember.user_id == current_user.id
    ).first()
    
    if existing_member:
        raise HTTPException(status_code=400, detail="您已经是该团队成员")
    
    # 添加成员
    member = GroupMember(
        group_id=group.id,
        user_id=current_user.id,
        nickname=current_user.nickname,
        avatar=current_user.avatar,
        phone=current_user.phone,
        role=GroupRole.MEMBER
    )
    db.add(member)
    
    # 更新团队成员数
    group.member_count += 1
    
    db.commit()
    
    return Response.success(data={
        "group_id": group.id,
        "group_name": group.name
    }, message="加入团队成功")


@router.post("/join-by-phone", summary="通过手机号加入团队")
async def join_group_by_phone(
    phone: str = Body(..., embed=True, description="团队负责人手机号"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    通过团队负责人手机号加入团队
    """
    # 查询团队负责人
    group = db.query(UserGroup).filter(
        UserGroup.owner_phone == phone,
        UserGroup.status == GroupStatus.ACTIVE
    ).first()
    
    if not group:
        raise HTTPException(status_code=404, detail="未找到该手机号对应的团队")
    
    # 检查是否已经是成员
    existing_member = db.query(GroupMember).filter(
        GroupMember.group_id == group.id,
        GroupMember.user_id == current_user.id
    ).first()
    
    if existing_member:
        raise HTTPException(status_code=400, detail="您已经是该团队成员")
    
    # 添加成员
    member = GroupMember(
        group_id=group.id,
        user_id=current_user.id,
        nickname=current_user.nickname,
        avatar=current_user.avatar,
        phone=current_user.phone,
        role=GroupRole.MEMBER
    )
    db.add(member)
    
    # 更新团队成员数
    group.member_count += 1
    
    db.commit()
    
    return Response.success(data={
        "group_id": group.id,
        "group_name": group.name,
        "invite_code": group.invite_code
    }, message="加入团队成功")

