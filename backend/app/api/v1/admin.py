"""
后台管理API
包括用户管理、项目管理等
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from typing import Optional
from decimal import Decimal

from app.core.database import get_db
from app.core.response import Response
from app.api.v1.deps import get_current_admin_user
from app.models.user import User, UserStatus
from app.models.project import Project, ProjectCategory
from app.schemas.project import ProjectCreate, ProjectUpdate
from pydantic import BaseModel


router = APIRouter()


# ========== 用户管理 ==========

@router.get("/users", summary="获取用户列表（管理员）")
async def get_users(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    search: Optional[str] = Query(None, description="搜索关键字（手机号/昵称）"),
    status: Optional[str] = Query(None, description="用户状态"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """
    管理员获取用户列表
    - 支持分页
    - 支持搜索（手机号、昵称）
    - 支持按状态筛选
    """
    query = db.query(User)
    
    # 搜索
    if search:
        query = query.filter(
            or_(
                User.phone.like(f"%{search}%"),
                User.nickname.like(f"%{search}%")
            )
        )
    
    # 状态筛选
    if status:
        query = query.filter(User.status == status)
    
    # 总数
    total = query.count()
    
    # 分页
    users = query.order_by(User.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    return Response.success(
        data={
            "items": [
                {
                    "id": u.id,
                    "phone": u.phone,
                    "nickname": u.nickname,
                    "avatar": u.avatar,
                    "email": u.email,
                    "is_certified": u.is_certified,
                    "membership_level": u.membership_level.value if u.membership_level else 0,
                    "credit_limit": float(u.credit_limit),
                    "used_credit": float(u.used_credit),
                    "prepaid_balance": float(u.prepaid_balance),
                    "points_balance": u.points_balance,
                    "total_spent": float(u.total_spent),
                    "total_orders": u.total_orders,
                    "status": u.status.value if u.status else "active",
                    "created_at": u.created_at.isoformat() if u.created_at else None,
                    "last_login_at": u.last_login_at.isoformat() if u.last_login_at else None
                }
                for u in users
            ],
            "total": total,
            "page": page,
            "page_size": page_size
        }
    )


@router.get("/users/{user_id}", summary="获取用户详情（管理员）")
async def get_user_detail(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员获取用户详细信息"""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    return Response.success(
        data={
            "id": user.id,
            "phone": user.phone,
            "nickname": user.nickname,
            "avatar": user.avatar,
            "email": user.email,
            "wechat_openid": user.wechat_openid,
            "is_certified": user.is_certified,
            "real_name": user.real_name,
            "id_card": user.id_card,
            "membership_level": user.membership_level.value if user.membership_level else 0,
            "credit_limit": float(user.credit_limit),
            "used_credit": float(user.used_credit),
            "prepaid_balance": float(user.prepaid_balance),
            "points_balance": user.points_balance,
            "total_points_earned": user.total_points_earned,
            "total_points_used": user.total_points_used,
            "total_spent": float(user.total_spent),
            "total_orders": user.total_orders,
            "status": user.status.value if user.status else "active",
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None,
            "last_login_at": user.last_login_at.isoformat() if user.last_login_at else None
        }
    )


@router.put("/users/{user_id}/status", summary="修改用户状态（管理员）")
async def update_user_status(
    user_id: int,
    status: str = Query(..., description="用户状态: active/inactive/banned"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员修改用户状态"""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 验证状态值
    try:
        user_status = UserStatus(status)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的状态值"
        )
    
    user.status = user_status
    db.commit()
    
    return Response.success(message="用户状态修改成功")


# ========== 项目管理 ==========

@router.get("/projects", summary="获取项目列表（管理员）")
async def get_projects_admin(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    search: Optional[str] = Query(None, description="搜索关键字（项目名称/编号）"),
    category_id: Optional[int] = Query(None, description="分类ID"),
    status: Optional[str] = Query(None, description="项目状态"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """
    管理员获取项目列表
    - 支持分页
    - 支持搜索（项目名称、编号）
    - 支持分类筛选
    - 支持状态筛选
    """
    query = db.query(Project)
    
    # 搜索
    if search:
        query = query.filter(
            or_(
                Project.name.like(f"%{search}%"),
                Project.project_no.like(f"%{search}%")
            )
        )
    
    # 分类筛选
    if category_id:
        query = query.filter(Project.category_id == category_id)
    
    # 状态筛选
    if status:
        query = query.filter(Project.status == status)
    
    # 总数
    total = query.count()
    
    # 分页
    projects = query.order_by(Project.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    return Response.success(
        data={
            "items": [
                {
                    "id": p.id,
                    "project_no": p.project_no,
                    "name": p.name,
                    "category_id": p.category_id,
                    "category_name": p.category.name if p.category else None,
                    "description": p.introduction,  # 使用introduction字段
                    "original_price": float(p.original_price),
                    "current_price": float(p.current_price),
                    "cover_image": p.cover_image,
                    "is_hot": p.is_hot,
                    "is_recommended": p.is_recommended,
                    "status": p.status,
                    "view_count": p.view_count,
                    "order_count": p.order_count,
                    "created_at": p.created_at.isoformat() if p.created_at else None
                }
                for p in projects
            ],
            "total": total,
            "page": page,
            "page_size": page_size
        }
    )


@router.post("/projects", summary="创建项目（管理员）")
async def create_project_admin(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员创建项目"""
    # 检查项目编号是否已存在
    existing = db.query(Project).filter(Project.project_no == project.project_no).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="项目编号已存在"
        )
    
    # 创建项目
    new_project = Project(**project.dict())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    
    return Response.success(
        data={"id": new_project.id},
        message="项目创建成功"
    )


@router.put("/projects/{project_id}", summary="更新项目（管理员）")
async def update_project_admin(
    project_id: int,
    project: ProjectUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员更新项目信息"""
    existing_project = db.query(Project).filter(Project.id == project_id).first()
    
    if not existing_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="项目不存在"
        )
    
    # 更新字段
    for key, value in project.dict(exclude_unset=True).items():
        setattr(existing_project, key, value)
    
    db.commit()
    
    return Response.success(message="项目更新成功")


@router.put("/projects/{project_id}/status", summary="修改项目状态（管理员）")
async def update_project_status_admin(
    project_id: int,
    status: str = Query(..., description="项目状态: active/inactive/archived"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员修改项目状态"""
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="项目不存在"
        )
    
    project.status = status
    db.commit()
    
    return Response.success(message="项目状态修改成功")


@router.delete("/projects/{project_id}", summary="删除项目（管理员）")
async def delete_project_admin(
    project_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员删除项目（软删除）"""
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="项目不存在"
        )
    
    # 软删除：设置状态为 archived
    project.status = "archived"
    db.commit()
    
    return Response.success(message="项目删除成功")


# ==================== 订单管理 ====================

@router.get("/orders", summary="获取订单列表（管理员）")
async def get_orders_admin(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    search: Optional[str] = Query(None, description="搜索关键字（订单号/用户手机号）"),
    status: Optional[str] = Query(None, description="订单状态筛选"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员获取订单列表"""
    from app.models.order import Order
    from sqlalchemy import or_
    from sqlalchemy.orm import joinedload
    
    # 构建查询
    query = db.query(Order).options(
        joinedload(Order.user),
        joinedload(Order.project)
    )
    
    # 搜索过滤
    if search:
        query = query.join(Order.user).filter(
            or_(
                Order.order_no.like(f"%{search}%"),
                User.phone.like(f"%{search}%"),
                User.nickname.like(f"%{search}%")
            )
        )
    
    # 状态过滤
    if status:
        query = query.filter(Order.status == status)
    
    # 总数
    total = query.count()
    
    # 分页查询
    orders_db = query.order_by(Order.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    # 格式化返回
    orders = []
    for o in orders_db:
        orders.append({
            "id": o.id,
            "order_no": o.order_no,
            "user_id": o.user_id,
            "user_phone": o.user.phone if o.user else None,
            "user_nickname": o.user.nickname if o.user else None,
            "project_id": o.project_id,
            "project_name": o.project.name if o.project else None,
            "sample_name": o.sample_name,
            "quantity": o.quantity,
            "total_amount": float(o.total_amount) if o.total_amount else 0,
            "status": o.status,
            "created_at": o.created_at.isoformat() if o.created_at else None,
            "paid_at": o.paid_at.isoformat() if o.paid_at else None
        })
    
    return Response.success(data={
        "items": orders,
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.get("/orders/{order_id}", summary="获取订单详情（管理员）")
async def get_order_detail_admin(
    order_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员获取订单详情"""
    from app.models.order import Order
    from sqlalchemy.orm import joinedload
    
    order = db.query(Order).options(
        joinedload(Order.user),
        joinedload(Order.project),
        joinedload(Order.address)
    ).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订单不存在"
        )
    
    return Response.success(data={
        "id": order.id,
        "order_no": order.order_no,
        "user": {
            "id": order.user.id if order.user else None,
            "phone": order.user.phone if order.user else None,
            "nickname": order.user.nickname if order.user else None
        },
        "project": {
            "id": order.project.id if order.project else None,
            "name": order.project.name if order.project else None,
            "cover_image": order.project.cover_image if order.project else None
        },
        "sample_name": order.sample_name,
        "sample_state": order.sample_state,
        "quantity": order.quantity,
        "unit_price": float(order.unit_price) if order.unit_price else 0,
        "total_amount": float(order.total_amount) if order.total_amount else 0,
        "status": order.status,
        "address": {
            "receiver": order.address.receiver if order.address else None,
            "phone": order.address.phone if order.address else None,
            "address": order.address.full_address() if order.address and hasattr(order.address, 'full_address') else None
        } if order.address else None,
        "created_at": order.created_at.isoformat() if order.created_at else None,
        "paid_at": order.paid_at.isoformat() if order.paid_at else None,
        "confirmed_at": order.confirmed_at.isoformat() if order.confirmed_at else None,
        "completed_at": order.completed_at.isoformat() if order.completed_at else None
    })


@router.put("/orders/{order_id}/status", summary="修改订单状态（管理员）")
async def update_order_status_admin(
    order_id: int,
    new_status: str = Query(..., description="新状态: unpaid/paid/confirmed/testing/completed/cancelled"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员修改订单状态"""
    from app.models.order import Order
    from datetime import datetime
    
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订单不存在"
        )
    
    # 更新状态
    old_status = order.status
    order.status = new_status
    
    # 更新时间戳
    if new_status == "paid" and not order.paid_at:
        order.paid_at = datetime.utcnow()
    elif new_status == "confirmed" and not order.confirmed_at:
        order.confirmed_at = datetime.utcnow()
    elif new_status == "completed" and not order.completed_at:
        order.completed_at = datetime.utcnow()
    
    db.commit()
    
    return Response.success(message=f"订单状态已从 {old_status} 更新为 {new_status}")

