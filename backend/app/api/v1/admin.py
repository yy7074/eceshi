"""
后台管理API
包括用户管理、项目管理、优惠券管理、充值管理、积分商品管理、评价管理、团体管理、邀请管理等
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, func, desc
from typing import Optional, List
from decimal import Decimal
from datetime import datetime, timedelta
from pydantic import BaseModel

from app.core.database import get_db
from app.core.response import Response
from app.api.v1.deps import get_current_admin_user
from app.models.user import User, UserStatus
from app.models.project import Project, ProjectCategory, ProjectReview
from app.models.order import Order, Payment
from app.models.coupon import Coupon, UserCoupon, CouponType, CouponStatus
from app.models.recharge import RechargeRecord, RechargeStatus
from app.models.points import PointsGoods, PointsRecord, PointsExchangeRecord
from app.models.group import UserGroup, GroupMember
from app.models.invite import InviteRecord, WithdrawRecord
from app.schemas.project import ProjectCreate, ProjectUpdate


router = APIRouter()


# ========== Pydantic 模型 ==========

class CouponCreate(BaseModel):
    name: str
    description: Optional[str] = None
    type: str = "cash"
    discount_rate: Optional[float] = None
    cash_amount: Optional[float] = None
    full_amount: Optional[float] = None
    reduction_amount: Optional[float] = None
    min_order_amount: float = 0
    max_discount_amount: Optional[float] = None
    total_quantity: int = 0
    valid_days: int = 30

class CouponUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    discount_rate: Optional[float] = None
    cash_amount: Optional[float] = None
    full_amount: Optional[float] = None
    reduction_amount: Optional[float] = None
    min_order_amount: Optional[float] = None
    max_discount_amount: Optional[float] = None
    total_quantity: Optional[int] = None
    valid_days: Optional[int] = None
    status: Optional[str] = None

class CategoryCreate(BaseModel):
    name: str
    code: Optional[str] = None
    parent_id: Optional[int] = None
    icon: Optional[str] = None
    cover_image: Optional[str] = None
    description: Optional[str] = None
    sort_order: int = 0
    is_hot: bool = False

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    icon: Optional[str] = None
    cover_image: Optional[str] = None
    description: Optional[str] = None
    sort_order: Optional[int] = None
    is_hot: Optional[bool] = None
    is_active: Optional[bool] = None

class PointsGoodsCreate(BaseModel):
    name: str
    points: int
    category: str
    image: Optional[str] = None
    description: Optional[str] = None
    stock: int = 0
    sort_order: int = 0

class PointsGoodsUpdate(BaseModel):
    name: Optional[str] = None
    points: Optional[int] = None
    category: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    stock: Optional[int] = None
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None


# ========== 数据统计仪表盘 ==========

@router.get("/dashboard/stats", summary="获取仪表盘统计数据")
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取后台首页统计数据"""
    from datetime import datetime, timedelta
    
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    this_month_start = today.replace(day=1)
    last_month_start = (this_month_start - timedelta(days=1)).replace(day=1)
    last_month_end = this_month_start - timedelta(days=1)
    
    # 用户统计
    total_users = db.query(func.count(User.id)).scalar() or 0
    today_new_users = db.query(func.count(User.id)).filter(
        func.date(User.created_at) == today
    ).scalar() or 0
    yesterday_new_users = db.query(func.count(User.id)).filter(
        func.date(User.created_at) == yesterday
    ).scalar() or 0
    this_month_users = db.query(func.count(User.id)).filter(
        func.date(User.created_at) >= this_month_start
    ).scalar() or 0
    
    # 订单统计
    total_orders = db.query(func.count(Order.id)).scalar() or 0
    today_orders = db.query(func.count(Order.id)).filter(
        func.date(Order.created_at) == today
    ).scalar() or 0
    yesterday_orders = db.query(func.count(Order.id)).filter(
        func.date(Order.created_at) == yesterday
    ).scalar() or 0
    this_month_orders = db.query(func.count(Order.id)).filter(
        func.date(Order.created_at) >= this_month_start
    ).scalar() or 0
    
    # 待处理订单
    pending_orders = db.query(func.count(Order.id)).filter(
        Order.status.in_(['unpaid', 'paid', 'confirmed'])
    ).scalar() or 0
    
    # 收入统计
    total_revenue = db.query(func.sum(Order.total_fee)).filter(
        Order.status.in_(['paid', 'confirmed', 'testing', 'completed'])
    ).scalar() or 0
    today_revenue = db.query(func.sum(Order.total_fee)).filter(
        Order.status.in_(['paid', 'confirmed', 'testing', 'completed']),
        func.date(Order.paid_at) == today
    ).scalar() or 0
    this_month_revenue = db.query(func.sum(Order.total_fee)).filter(
        Order.status.in_(['paid', 'confirmed', 'testing', 'completed']),
        func.date(Order.paid_at) >= this_month_start
    ).scalar() or 0
    
    # 项目统计
    total_projects = db.query(func.count(Project.id)).scalar() or 0
    active_projects = db.query(func.count(Project.id)).filter(
        Project.status == 'active'
    ).scalar() or 0
    
    # 充值统计
    total_recharge = db.query(func.sum(RechargeRecord.amount)).filter(
        RechargeRecord.status == RechargeStatus.SUCCESS
    ).scalar() or 0
    pending_recharge = db.query(func.count(RechargeRecord.id)).filter(
        RechargeRecord.status == RechargeStatus.PENDING
    ).scalar() or 0
    
    # 最近7天订单趋势
    order_trend = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        count = db.query(func.count(Order.id)).filter(
            func.date(Order.created_at) == day
        ).scalar() or 0
        order_trend.append({
            "date": day.strftime("%m-%d"),
            "count": count
        })
    
    # 最近7天收入趋势
    revenue_trend = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        amount = db.query(func.sum(Order.total_fee)).filter(
            Order.status.in_(['paid', 'confirmed', 'testing', 'completed']),
            func.date(Order.paid_at) == day
        ).scalar() or 0
        revenue_trend.append({
            "date": day.strftime("%m-%d"),
            "amount": float(amount)
        })
    
    # 订单状态分布
    order_status_dist = []
    for status_val in ['unpaid', 'paid', 'confirmed', 'testing', 'completed', 'cancelled']:
        count = db.query(func.count(Order.id)).filter(Order.status == status_val).scalar() or 0
        order_status_dist.append({"status": status_val, "count": count})
    
    return Response.success(data={
        "users": {
            "total": total_users,
            "today": today_new_users,
            "yesterday": yesterday_new_users,
            "this_month": this_month_users
        },
        "orders": {
            "total": total_orders,
            "today": today_orders,
            "yesterday": yesterday_orders,
            "this_month": this_month_orders,
            "pending": pending_orders
        },
        "revenue": {
            "total": float(total_revenue),
            "today": float(today_revenue),
            "this_month": float(this_month_revenue)
        },
        "projects": {
            "total": total_projects,
            "active": active_projects
        },
        "recharge": {
            "total": float(total_recharge),
            "pending_count": pending_recharge
        },
        "trends": {
            "orders": order_trend,
            "revenue": revenue_trend
        },
        "order_status_distribution": order_status_dist
    })


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
                    "credit_limit": float(u.credit_limit or 0),
                    "used_credit": float(u.used_credit or 0),
                    "prepaid_balance": float(u.prepaid_balance or 0),
                    "points_balance": u.points_balance or 0,
                    "total_spent": float(u.total_spent or 0),
                    "total_orders": u.total_orders or 0,
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
            "total_amount": float(o.total_fee or 0),
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


# ==================== 分类管理 ====================

@router.get("/categories", summary="获取分类列表（管理员）")
async def get_categories_admin(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员获取分类列表"""
    query = db.query(ProjectCategory)
    
    if search:
        query = query.filter(ProjectCategory.name.like(f"%{search}%"))
    
    total = query.count()
    categories = query.order_by(ProjectCategory.sort_order, ProjectCategory.id).offset((page - 1) * page_size).limit(page_size).all()
    
    return Response.success(data={
        "items": [
            {
                "id": c.id,
                "name": c.name,
                "code": c.code,
                "parent_id": c.parent_id,
                "level": c.level,
                "sort_order": c.sort_order,
                "icon": c.icon,
                "cover_image": c.cover_image,
                "description": c.description,
                "is_hot": c.is_hot,
                "is_active": c.is_active,
                "created_at": c.created_at.isoformat() if c.created_at else None
            }
            for c in categories
        ],
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.post("/categories", summary="创建分类（管理员）")
async def create_category_admin(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员创建分类"""
    category = ProjectCategory(
        name=data.name,
        code=data.code,
        parent_id=data.parent_id,
        icon=data.icon,
        cover_image=data.cover_image,
        description=data.description,
        sort_order=data.sort_order,
        is_hot=data.is_hot
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    
    return Response.success(data={"id": category.id}, message="分类创建成功")


@router.put("/categories/{category_id}", summary="更新分类（管理员）")
async def update_category_admin(
    category_id: int,
    data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员更新分类"""
    category = db.query(ProjectCategory).filter(ProjectCategory.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")
    
    for key, value in data.dict(exclude_unset=True).items():
        setattr(category, key, value)
    
    db.commit()
    return Response.success(message="分类更新成功")


@router.delete("/categories/{category_id}", summary="删除分类（管理员）")
async def delete_category_admin(
    category_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员删除分类"""
    category = db.query(ProjectCategory).filter(ProjectCategory.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")
    
    # 检查是否有项目使用此分类
    project_count = db.query(func.count(Project.id)).filter(Project.category_id == category_id).scalar()
    if project_count > 0:
        raise HTTPException(status_code=400, detail=f"该分类下有 {project_count} 个项目，无法删除")
    
    db.delete(category)
    db.commit()
    return Response.success(message="分类删除成功")


# ==================== 优惠券管理 ====================

@router.get("/coupons", summary="获取优惠券列表（管理员）")
async def get_coupons_admin(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员获取优惠券列表"""
    query = db.query(Coupon)
    
    if search:
        query = query.filter(Coupon.name.like(f"%{search}%"))
    
    if status:
        query = query.filter(Coupon.status == status)
    
    total = query.count()
    coupons = query.order_by(desc(Coupon.created_at)).offset((page - 1) * page_size).limit(page_size).all()
    
    return Response.success(data={
        "items": [
            {
                "id": c.id,
                "name": c.name,
                "description": c.description,
                "type": c.type.value if c.type else None,
                "discount_rate": float(c.discount_rate) if c.discount_rate else None,
                "cash_amount": float(c.cash_amount) if c.cash_amount else None,
                "full_amount": float(c.full_amount) if c.full_amount else None,
                "reduction_amount": float(c.reduction_amount) if c.reduction_amount else None,
                "min_order_amount": float(c.min_order_amount) if c.min_order_amount else 0,
                "max_discount_amount": float(c.max_discount_amount) if c.max_discount_amount else None,
                "total_quantity": c.total_quantity,
                "received_quantity": c.received_quantity,
                "valid_days": c.valid_days,
                "status": c.status.value if c.status else None,
                "start_time": c.start_time.isoformat() if c.start_time else None,
                "end_time": c.end_time.isoformat() if c.end_time else None,
                "created_at": c.created_at.isoformat() if c.created_at else None
            }
            for c in coupons
        ],
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.post("/coupons", summary="创建优惠券（管理员）")
async def create_coupon_admin(
    data: CouponCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员创建优惠券"""
    coupon = Coupon(
        name=data.name,
        description=data.description,
        type=CouponType(data.type),
        discount_rate=data.discount_rate,
        cash_amount=data.cash_amount,
        full_amount=data.full_amount,
        reduction_amount=data.reduction_amount,
        min_order_amount=data.min_order_amount,
        max_discount_amount=data.max_discount_amount,
        total_quantity=data.total_quantity,
        valid_days=data.valid_days,
        status=CouponStatus.ACTIVE
    )
    db.add(coupon)
    db.commit()
    db.refresh(coupon)
    
    return Response.success(data={"id": coupon.id}, message="优惠券创建成功")


@router.put("/coupons/{coupon_id}", summary="更新优惠券（管理员）")
async def update_coupon_admin(
    coupon_id: int,
    data: CouponUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员更新优惠券"""
    coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
    if not coupon:
        raise HTTPException(status_code=404, detail="优惠券不存在")
    
    update_data = data.dict(exclude_unset=True)
    if 'status' in update_data:
        update_data['status'] = CouponStatus(update_data['status'])
    
    for key, value in update_data.items():
        setattr(coupon, key, value)
    
    db.commit()
    return Response.success(message="优惠券更新成功")


@router.delete("/coupons/{coupon_id}", summary="删除优惠券（管理员）")
async def delete_coupon_admin(
    coupon_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员删除优惠券"""
    coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
    if not coupon:
        raise HTTPException(status_code=404, detail="优惠券不存在")
    
    # 软删除：设置状态为下架
    coupon.status = CouponStatus.INACTIVE
    db.commit()
    return Response.success(message="优惠券已下架")


# ==================== 充值管理 ====================

@router.get("/recharges", summary="获取充值记录列表（管理员）")
async def get_recharges_admin(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None, description="搜索充值单号/用户手机号"),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员获取充值记录列表"""
    query = db.query(RechargeRecord)
    
    if search:
        # 关联用户表搜索
        query = query.join(User, RechargeRecord.user_id == User.id).filter(
            or_(
                RechargeRecord.recharge_no.like(f"%{search}%"),
                User.phone.like(f"%{search}%")
            )
        )
    
    if status:
        query = query.filter(RechargeRecord.status == status)
    
    total = query.count()
    records = query.order_by(desc(RechargeRecord.created_at)).offset((page - 1) * page_size).limit(page_size).all()
    
    # 获取用户信息
    user_ids = [r.user_id for r in records]
    users = {u.id: u for u in db.query(User).filter(User.id.in_(user_ids)).all()}
    
    return Response.success(data={
        "items": [
            {
                "id": r.id,
                "recharge_no": r.recharge_no,
                "user_id": r.user_id,
                "user_phone": users.get(r.user_id).phone if users.get(r.user_id) else None,
                "user_nickname": users.get(r.user_id).nickname if users.get(r.user_id) else None,
                "amount": float(r.amount) if r.amount else 0,
                "actual_amount": float(r.actual_amount) if r.actual_amount else 0,
                "bonus_amount": float(r.bonus_amount) if r.bonus_amount else 0,
                "payment_method": r.payment_method.value if r.payment_method else None,
                "status": r.status.value if r.status else None,
                "remark": r.remark,
                "created_at": r.created_at.isoformat() if r.created_at else None,
                "paid_at": r.paid_at.isoformat() if r.paid_at else None
            }
            for r in records
        ],
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.put("/recharges/{recharge_id}/status", summary="修改充值状态（管理员）")
async def update_recharge_status_admin(
    recharge_id: int,
    new_status: str = Query(..., description="新状态: pending/success/failed/refunded"),
    remark: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员修改充值状态"""
    record = db.query(RechargeRecord).filter(RechargeRecord.id == recharge_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="充值记录不存在")
    
    old_status = record.status.value if record.status else None
    record.status = RechargeStatus(new_status)
    
    if remark:
        record.remark = remark
    
    # 如果状态改为成功，更新用户余额
    if new_status == "success" and old_status != "success":
        user = db.query(User).filter(User.id == record.user_id).first()
        if user:
            actual_amount = record.actual_amount or record.amount
            user.prepaid_balance = (user.prepaid_balance or 0) + actual_amount
            record.completed_at = datetime.utcnow()
    
    db.commit()
    return Response.success(message=f"充值状态已从 {old_status} 更新为 {new_status}")


# ==================== 积分商品管理 ====================

@router.get("/points-goods", summary="获取积分商品列表（管理员）")
async def get_points_goods_admin(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员获取积分商品列表"""
    query = db.query(PointsGoods)
    
    if search:
        query = query.filter(PointsGoods.name.like(f"%{search}%"))
    
    if category:
        query = query.filter(PointsGoods.category == category)
    
    total = query.count()
    goods = query.order_by(PointsGoods.sort_order, desc(PointsGoods.created_at)).offset((page - 1) * page_size).limit(page_size).all()
    
    return Response.success(data={
        "items": [
            {
                "id": g.id,
                "name": g.name,
                "points": g.points,
                "category": g.category,
                "image": g.image,
                "description": g.description,
                "stock": g.stock,
                "is_active": g.is_active,
                "sort_order": g.sort_order,
                "created_at": g.created_at.isoformat() if g.created_at else None
            }
            for g in goods
        ],
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.post("/points-goods", summary="创建积分商品（管理员）")
async def create_points_goods_admin(
    data: PointsGoodsCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员创建积分商品"""
    goods = PointsGoods(
        name=data.name,
        points=data.points,
        category=data.category,
        image=data.image,
        description=data.description,
        stock=data.stock,
        sort_order=data.sort_order,
        is_active=True
    )
    db.add(goods)
    db.commit()
    db.refresh(goods)
    
    return Response.success(data={"id": goods.id}, message="积分商品创建成功")


@router.put("/points-goods/{goods_id}", summary="更新积分商品（管理员）")
async def update_points_goods_admin(
    goods_id: int,
    data: PointsGoodsUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员更新积分商品"""
    goods = db.query(PointsGoods).filter(PointsGoods.id == goods_id).first()
    if not goods:
        raise HTTPException(status_code=404, detail="积分商品不存在")
    
    for key, value in data.dict(exclude_unset=True).items():
        setattr(goods, key, value)
    
    db.commit()
    return Response.success(message="积分商品更新成功")


@router.delete("/points-goods/{goods_id}", summary="删除积分商品（管理员）")
async def delete_points_goods_admin(
    goods_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员删除积分商品"""
    goods = db.query(PointsGoods).filter(PointsGoods.id == goods_id).first()
    if not goods:
        raise HTTPException(status_code=404, detail="积分商品不存在")
    
    goods.is_active = False
    db.commit()
    return Response.success(message="积分商品已下架")


# ==================== 评价管理 ====================

@router.get("/reviews", summary="获取评价列表（管理员）")
async def get_reviews_admin(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员获取评价列表"""
    query = db.query(ProjectReview)
    
    if status:
        query = query.filter(ProjectReview.status == status)
    
    total = query.count()
    reviews = query.order_by(desc(ProjectReview.created_at)).offset((page - 1) * page_size).limit(page_size).all()
    
    # 获取关联信息
    user_ids = [r.user_id for r in reviews]
    project_ids = [r.project_id for r in reviews]
    users = {u.id: u for u in db.query(User).filter(User.id.in_(user_ids)).all()}
    projects = {p.id: p for p in db.query(Project).filter(Project.id.in_(project_ids)).all()}
    
    return Response.success(data={
        "items": [
            {
                "id": r.id,
                "user_id": r.user_id,
                "user_nickname": users.get(r.user_id).nickname if users.get(r.user_id) else None,
                "project_id": r.project_id,
                "project_name": projects.get(r.project_id).name if projects.get(r.project_id) else None,
                "order_id": r.order_id,
                "rating": r.rating,
                "content": r.content,
                "images": r.images,
                "reply_content": r.reply_content,
                "is_anonymous": r.is_anonymous,
                "status": r.status,
                "created_at": r.created_at.isoformat() if r.created_at else None
            }
            for r in reviews
        ],
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.put("/reviews/{review_id}/reply", summary="回复评价（管理员）")
async def reply_review_admin(
    review_id: int,
    content: str = Query(..., description="回复内容"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员回复评价"""
    review = db.query(ProjectReview).filter(ProjectReview.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="评价不存在")
    
    review.reply_content = content
    review.reply_time = datetime.utcnow()
    db.commit()
    return Response.success(message="回复成功")


@router.put("/reviews/{review_id}/status", summary="修改评价状态（管理员）")
async def update_review_status_admin(
    review_id: int,
    status: str = Query(..., description="状态: published/hidden"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员修改评价状态"""
    review = db.query(ProjectReview).filter(ProjectReview.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="评价不存在")
    
    review.status = status
    db.commit()
    return Response.success(message="状态修改成功")


# ==================== 团体管理 ====================

@router.get("/groups", summary="获取团体列表（管理员）")
async def get_groups_admin(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员获取团体列表"""
    query = db.query(UserGroup)
    
    if search:
        query = query.filter(
            or_(
                UserGroup.name.like(f"%{search}%"),
                UserGroup.invite_code.like(f"%{search}%")
            )
        )
    
    if status:
        query = query.filter(UserGroup.status == status)
    
    total = query.count()
    groups = query.order_by(desc(UserGroup.created_at)).offset((page - 1) * page_size).limit(page_size).all()
    
    return Response.success(data={
        "items": [
            {
                "id": g.id,
                "name": g.name,
                "avatar": g.avatar,
                "description": g.description,
                "owner_id": g.owner_id,
                "owner_name": g.owner_name,
                "owner_phone": g.owner_phone,
                "university": g.university,
                "department": g.department,
                "invite_code": g.invite_code,
                "member_count": g.member_count,
                "total_orders": g.total_orders,
                "total_spent": g.total_spent,
                "status": g.status.value if g.status else None,
                "is_certified": g.is_certified,
                "created_at": g.created_at.isoformat() if g.created_at else None
            }
            for g in groups
        ],
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.put("/groups/{group_id}/status", summary="修改团体状态（管理员）")
async def update_group_status_admin(
    group_id: int,
    status: str = Query(..., description="状态: active/inactive/disbanded"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员修改团体状态"""
    from app.models.group import GroupStatus
    group = db.query(UserGroup).filter(UserGroup.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="团体不存在")
    
    group.status = GroupStatus(status)
    db.commit()
    return Response.success(message="团体状态修改成功")


@router.put("/groups/{group_id}/certify", summary="认证团体（管理员）")
async def certify_group_admin(
    group_id: int,
    is_certified: bool = Query(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员认证团体"""
    group = db.query(UserGroup).filter(UserGroup.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="团体不存在")
    
    group.is_certified = is_certified
    db.commit()
    return Response.success(message="认证状态更新成功")


# ==================== 邀请管理 ====================

@router.get("/invites", summary="获取邀请记录列表（管理员）")
async def get_invites_admin(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员获取邀请记录列表"""
    query = db.query(InviteRecord)
    
    if search:
        query = query.filter(
            or_(
                InviteRecord.inviter_phone.like(f"%{search}%"),
                InviteRecord.invitee_phone.like(f"%{search}%")
            )
        )
    
    if status:
        query = query.filter(InviteRecord.status == status)
    
    total = query.count()
    records = query.order_by(desc(InviteRecord.created_at)).offset((page - 1) * page_size).limit(page_size).all()
    
    return Response.success(data={
        "items": [
            {
                "id": r.id,
                "inviter_id": r.inviter_id,
                "inviter_name": r.inviter_name,
                "inviter_phone": r.inviter_phone,
                "invitee_id": r.invitee_id,
                "invitee_name": r.invitee_name,
                "invitee_phone": r.invitee_phone,
                "reward_amount": float(r.reward_amount) if r.reward_amount else 0,
                "reward_type": r.reward_type,
                "status": r.status.value if r.status else None,
                "first_order_amount": float(r.first_order_amount) if r.first_order_amount else 0,
                "invited_at": r.invited_at.isoformat() if r.invited_at else None,
                "completed_at": r.completed_at.isoformat() if r.completed_at else None
            }
            for r in records
        ],
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.get("/withdraws", summary="获取提现记录列表（管理员）")
async def get_withdraws_admin(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员获取提现记录列表"""
    query = db.query(WithdrawRecord)
    
    if status:
        query = query.filter(WithdrawRecord.status == status)
    
    total = query.count()
    records = query.order_by(desc(WithdrawRecord.created_at)).offset((page - 1) * page_size).limit(page_size).all()
    
    # 获取用户信息
    user_ids = [r.user_id for r in records]
    users = {u.id: u for u in db.query(User).filter(User.id.in_(user_ids)).all()}
    
    return Response.success(data={
        "items": [
            {
                "id": r.id,
                "user_id": r.user_id,
                "user_phone": users.get(r.user_id).phone if users.get(r.user_id) else None,
                "user_nickname": users.get(r.user_id).nickname if users.get(r.user_id) else None,
                "amount": float(r.amount) if r.amount else 0,
                "withdraw_type": r.withdraw_type,
                "account_type": r.account_type,
                "account_name": r.account_name,
                "account_number": r.account_number,
                "status": r.status.value if r.status else None,
                "reject_reason": r.reject_reason,
                "created_at": r.created_at.isoformat() if r.created_at else None,
                "reviewed_at": r.reviewed_at.isoformat() if r.reviewed_at else None
            }
            for r in records
        ],
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.put("/withdraws/{withdraw_id}/review", summary="审核提现（管理员）")
async def review_withdraw_admin(
    withdraw_id: int,
    action: str = Query(..., description="操作: approve/reject"),
    reject_reason: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员审核提现"""
    from app.models.invite import WithdrawStatus
    
    record = db.query(WithdrawRecord).filter(WithdrawRecord.id == withdraw_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="提现记录不存在")
    
    if record.status != WithdrawStatus.PENDING:
        raise HTTPException(status_code=400, detail="该提现申请已处理")
    
    if action == "approve":
        record.status = WithdrawStatus.APPROVED
    elif action == "reject":
        record.status = WithdrawStatus.REJECTED
        record.reject_reason = reject_reason
    else:
        raise HTTPException(status_code=400, detail="无效的操作")
    
    record.reviewer_id = current_admin.id
    record.reviewed_at = datetime.utcnow()
    db.commit()
    
    return Response.success(message="审核完成")

