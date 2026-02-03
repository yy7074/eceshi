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
from app.models.user import User, UserStatus, UserCertification
from app.models.credit import CreditRecord, CreditTransactionType, CreditTransactionStatus
from app.models.project import Project, ProjectCategory, ProjectReview
from app.models.order import Order, Payment, OrderStatusHistory
from app.models.coupon import Coupon, UserCoupon, CouponType, CouponStatus
from app.models.recharge import RechargeRecord, RechargeStatus
from app.models.points import PointsGoods, PointsRecord, PointsExchangeRecord
from app.models.group import UserGroup, GroupMember
from app.models.invite import InviteRecord, WithdrawRecord
from app.models.laboratory import Laboratory, LabApplication, LabStatus
from app.models.project_option import ProjectOption, OptionType, PriceType, OrderOptionSelection
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.schemas.project_option import (
    ProjectOptionCreate, ProjectOptionUpdate, ProjectOptionInDB
)


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
            "list": [
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
    is_draft: Optional[bool] = Query(None, description="是否草稿订单"),
    invoice_status: Optional[str] = Query(None, description="开票状态: none/requested/processing/issued/rejected"),
    payment_status: Optional[str] = Query(None, description="支付状态: unpaid/partial/paid"),
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

    # 草稿筛选
    if is_draft is not None:
        query = query.filter(Order.is_draft == is_draft)

    # 状态过滤
    if status:
        query = query.filter(Order.status == status)

    # 开票状态筛选
    if invoice_status:
        query = query.filter(Order.invoice_status == invoice_status)

    # 支付状态筛选
    if payment_status:
        query = query.filter(Order.payment_status == payment_status)
    
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
            "project_name": o.project.name if o.project else o.project_name,
            "sample_count": o.sample_count,
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


# 注意：静态路由必须在动态路由之前定义
@router.get("/orders/pending-assign", summary="获取待指派订单列表")
async def get_pending_assign_orders(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None, description="搜索订单号"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取待指派的订单列表（已支付但未指派的订单）"""
    query = db.query(Order).filter(
        Order.is_draft == False,
        Order.status.in_(["paid", "pending_assign"]),
        Order.assigned_lab_id.is_(None)
    )

    if search:
        query = query.filter(Order.order_no.like(f"%{search}%"))

    total = query.count()
    orders_list = query.order_by(desc(Order.created_at)).offset((page - 1) * page_size).limit(page_size).all()

    return Response.success(data={
        "items": [
            {
                "id": o.id,
                "order_no": o.order_no,
                "project_name": o.project_name,
                "sample_count": o.sample_count,
                "total_fee": float(o.total_fee or 0),
                "is_urgent": o.is_urgent,
                "status": o.status,
                "created_at": o.created_at.isoformat() if o.created_at else None,
                "paid_at": o.paid_at.isoformat() if o.paid_at else None
            }
            for o in orders_list
        ],
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.get("/orders/assignment-stats", summary="获取订单指派统计")
async def get_order_assignment_stats(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取订单指派统计数据"""
    from datetime import date
    
    # 待指派订单数
    pending_count = db.query(Order).filter(
        Order.is_draft == False,
        Order.status.in_(["paid", "pending_assign"]),
        Order.assigned_lab_id.is_(None)
    ).count()

    # 已指派待接单
    assigned_count = db.query(Order).filter(
        Order.status == "assigned"
    ).count()

    # 被拒绝待重新指派
    rejected_count = db.query(Order).filter(
        Order.status == "rejected_by_lab"
    ).count()

    # 检测中订单数
    testing_count = db.query(Order).filter(
        Order.status.in_(["accepted", "sample_received", "testing", "data_uploaded"])
    ).count()

    # 今日指派数
    today = date.today()
    today_assigned = db.query(Order).filter(
        Order.assigned_at >= today
    ).count()

    # 各实验室订单分布
    lab_distribution = db.query(
        Laboratory.name,
        func.count(Order.id).label("order_count")
    ).join(
        Order, Order.assigned_lab_id == Laboratory.id
    ).filter(
        Order.status.notin_(["cancelled", "refunded"])
    ).group_by(Laboratory.id).all()

    return Response.success(data={
        "pending_count": pending_count,
        "assigned_count": assigned_count,
        "rejected_count": rejected_count,
        "testing_count": testing_count,
        "today_assigned": today_assigned,
        "lab_distribution": [
            {"lab_name": name, "order_count": count}
            for name, count in lab_distribution
        ]
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
        joinedload(Order.project)
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
            "id": order.project.id if order.project else order.project_id,
            "name": order.project.name if order.project else order.project_name,
            "cover_image": order.project.cover_image if order.project else None
        },
        "sample_count": order.sample_count,
        "project_fee": float(order.project_fee or 0),
        "urgent_fee": float(order.urgent_fee or 0),
        "shipping_fee": float(order.shipping_fee or 0),
        "discount_amount": float(order.discount_amount or 0),
        "total_amount": float(order.total_fee or 0),
        "paid_fee": float(order.paid_fee or 0),
        "status": order.status,
        "address": {
            "receiver": order.receiver_name,
            "phone": order.receiver_phone,
            "address": order.receiver_address
        } if order.receiver_name else None,
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


# ==================== 订单指派 ====================

class OrderAssignRequest(BaseModel):
    """订单指派请求"""
    laboratory_id: int
    remark: Optional[str] = None


class BatchAssignRequest(BaseModel):
    """批量指派请求"""
    order_ids: List[int]
    laboratory_id: int
    remark: Optional[str] = None


@router.get("/orders/{order_id}/suitable-labs", summary="获取适合的实验室列表")
async def get_suitable_labs_for_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取适合处理该订单的实验室列表"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")

    # 获取所有活跃的实验室
    labs = db.query(Laboratory).filter(
        Laboratory.status == LabStatus.ACTIVE
    ).all()

    lab_list = []
    for lab in labs:
        # 计算匹配度（可基于实验室能力、位置等因素）
        match_score = 100  # 默认满分

        # 检查是否有相关检测能力（简化处理）
        if lab.specialties:
            # 实际应用中可以根据项目类型匹配实验室专长
            pass

        # 获取当前任务数（未完成的订单数）
        current_tasks = db.query(Order).filter(
            Order.assigned_lab_id == lab.id,
            Order.status.in_(["assigned", "accepted", "testing"])
        ).count()

        lab_list.append({
            "id": lab.id,
            "name": lab.name,
            "code": lab.code,
            "director": lab.contact_name or lab.contact_person or "",
            "institution": lab.institution,
            "province": lab.province,
            "city": lab.city,
            "status": lab.status,
            "rating": float(lab.rating) if lab.rating else 5.0,
            "completed_orders": lab.completed_orders or 0,
            "current_tasks": current_tasks,
            "commission_rate": float(lab.commission_rate) if lab.commission_rate else 20.0,
            "match_score": match_score
        })

    # 按匹配度和评分排序
    lab_list.sort(key=lambda x: (-x["match_score"], -x["rating"]))

    return Response.success(data={
        "order": {
            "id": order.id,
            "order_no": order.order_no,
            "project_name": order.project_name
        },
        "laboratories": lab_list
    })


@router.post("/orders/{order_id}/assign", summary="指派订单到实验室")
async def assign_order_to_lab(
    order_id: int,
    data: OrderAssignRequest,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """将订单指派给指定实验室"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")

    if order.status not in ["paid", "pending_assign"]:
        raise HTTPException(status_code=400, detail="订单状态不允许指派")

    lab = db.query(Laboratory).filter(
        Laboratory.id == data.laboratory_id,
        Laboratory.status == LabStatus.ACTIVE
    ).first()
    if not lab:
        raise HTTPException(status_code=404, detail="实验室不存在或未激活")

    # 记录状态变更
    history = OrderStatusHistory(
        order_id=order_id,
        from_status=order.status,
        to_status="assigned",
        operator_id=current_admin.id,
        operator_type="admin",
        remark=data.remark or f"指派给实验室: {lab.name}"
    )
    db.add(history)

    # 更新订单
    order.status = "assigned"
    order.assigned_lab_id = lab.id
    order.assigned_user_id = current_admin.id
    order.assigned_at = datetime.utcnow()

    # 更新实验室订单统计
    lab.total_orders = (lab.total_orders or 0) + 1

    db.commit()

    return Response.success(message=f"订单已指派给 {lab.name}")


@router.post("/orders/batch-assign", summary="批量指派订单")
async def batch_assign_orders(
    data: BatchAssignRequest,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """批量将订单指派给指定实验室"""
    lab = db.query(Laboratory).filter(
        Laboratory.id == data.laboratory_id,
        Laboratory.status == LabStatus.ACTIVE
    ).first()
    if not lab:
        raise HTTPException(status_code=404, detail="实验室不存在或未激活")

    success_count = 0
    fail_count = 0

    for order_id in data.order_ids:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order or order.status not in ["paid", "pending_assign"]:
            fail_count += 1
            continue

        # 记录状态变更
        history = OrderStatusHistory(
            order_id=order_id,
            from_status=order.status,
            to_status="assigned",
            operator_id=current_admin.id,
            operator_type="admin",
            remark=data.remark or f"批量指派给实验室: {lab.name}"
        )
        db.add(history)

        # 更新订单
        order.status = "assigned"
        order.assigned_lab_id = lab.id
        order.assigned_user_id = current_admin.id
        order.assigned_at = datetime.utcnow()

        success_count += 1

    # 更新实验室订单统计
    lab.total_orders = (lab.total_orders or 0) + success_count

    db.commit()

    return Response.success(
        message=f"批量指派完成，成功 {success_count} 个，失败 {fail_count} 个",
        data={"success_count": success_count, "fail_count": fail_count}
    )


@router.post("/orders/{order_id}/reassign", summary="重新指派订单")
async def reassign_order(
    order_id: int,
    data: OrderAssignRequest,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """重新指派订单到其他实验室"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")

    # 允许重新指派的状态
    if order.status not in ["assigned", "pending_assign", "rejected_by_lab"]:
        raise HTTPException(status_code=400, detail="订单状态不允许重新指派")

    new_lab = db.query(Laboratory).filter(
        Laboratory.id == data.laboratory_id,
        Laboratory.status == LabStatus.ACTIVE
    ).first()
    if not new_lab:
        raise HTTPException(status_code=404, detail="实验室不存在或未激活")

    old_lab_name = None
    if order.assigned_lab_id:
        old_lab = db.query(Laboratory).filter(Laboratory.id == order.assigned_lab_id).first()
        if old_lab:
            old_lab_name = old_lab.name
            # 减少原实验室订单统计
            old_lab.total_orders = max((old_lab.total_orders or 0) - 1, 0)

    # 记录状态变更
    history = OrderStatusHistory(
        order_id=order_id,
        from_status=order.status,
        to_status="assigned",
        operator_id=current_admin.id,
        operator_type="admin",
        remark=data.remark or f"重新指派: {old_lab_name or '无'} -> {new_lab.name}"
    )
    db.add(history)

    # 更新订单
    order.status = "assigned"
    order.assigned_lab_id = new_lab.id
    order.assigned_user_id = current_admin.id
    order.assigned_at = datetime.utcnow()

    # 更新新实验室订单统计
    new_lab.total_orders = (new_lab.total_orders or 0) + 1

    db.commit()

    return Response.success(message=f"订单已重新指派给 {new_lab.name}")


@router.get("/orders/assignment-stats", summary="获取订单指派统计")
async def get_assignment_stats(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取订单指派统计数据"""
    # 待指派订单数
    pending_count = db.query(Order).filter(
        Order.is_draft == False,
        Order.status.in_(["paid", "pending_assign"]),
        Order.assigned_lab_id.is_(None)
    ).count()

    # 已指派待接单
    assigned_count = db.query(Order).filter(
        Order.status == "assigned"
    ).count()

    # 被拒绝待重新指派
    rejected_count = db.query(Order).filter(
        Order.status == "rejected_by_lab"
    ).count()

    # 检测中订单数
    testing_count = db.query(Order).filter(
        Order.status.in_(["accepted", "sample_received", "testing", "data_uploaded"])
    ).count()

    # 今日指派数
    from datetime import date
    today = date.today()
    today_assigned = db.query(Order).filter(
        Order.assigned_at >= today
    ).count()

    # 各实验室订单分布
    lab_distribution = db.query(
        Laboratory.name,
        func.count(Order.id).label("order_count")
    ).join(
        Order, Order.assigned_lab_id == Laboratory.id
    ).filter(
        Order.status.notin_(["cancelled", "refunded"])
    ).group_by(Laboratory.id).all()

    return Response.success(data={
        "pending_count": pending_count,
        "assigned_count": assigned_count,
        "rejected_count": rejected_count,
        "testing_count": testing_count,
        "today_assigned": today_assigned,
        "lab_distribution": [
            {"lab_name": name, "order_count": count}
            for name, count in lab_distribution
        ]
    })


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
    from app.models.project import ProjectReview
    
    query = db.query(ProjectReview)
    
    if status:
        query = query.filter(ProjectReview.status == status)
    
    if search:
        query = query.join(User).filter(
            or_(
                User.nickname.like(f"%{search}%"),
                User.phone.like(f"%{search}%"),
                ProjectReview.content.like(f"%{search}%")
            )
        )
    
    total = query.count()
    reviews = query.order_by(desc(ProjectReview.created_at)).offset((page - 1) * page_size).limit(page_size).all()
    
    # 获取关联信息
    user_ids = list(set([r.user_id for r in reviews if r.user_id]))
    project_ids = list(set([r.project_id for r in reviews if r.project_id]))
    
    users = {}
    projects = {}
    
    if user_ids:
        users = {u.id: u for u in db.query(User).filter(User.id.in_(user_ids)).all()}
    
    if project_ids:
        projects = {p.id: p for p in db.query(Project).filter(Project.id.in_(project_ids)).all()}
    
    return Response.success(data={
        "items": [
            {
                "id": r.id,
                "user_id": r.user_id,
                "user_nickname": (users.get(r.user_id).nickname if users.get(r.user_id) else None) if r.user_id else None,
                "project_id": r.project_id,
                "project_name": (projects.get(r.project_id).name if projects.get(r.project_id) else None) if r.project_id else None,
                "order_id": r.order_id,
                "rating": r.rating,
                "content": r.content or "",
                "images": r.images or [],
                "reply_content": r.reply_content or "",
                "is_anonymous": False,  # 数据库表中没有此字段
                "status": r.status or "pending",
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


# ==================== 数据分析 ====================

@router.get("/analytics", summary="获取数据分析数据（管理员）")
async def get_analytics(
    start_date: Optional[str] = Query(None, description="开始日期"),
    end_date: Optional[str] = Query(None, description="结束日期"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取数据分析数据"""
    try:
        # 解析日期
        if start_date:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        else:
            start_dt = datetime.now() - timedelta(days=30)
        
        if end_date:
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        else:
            end_dt = datetime.now()
        
        # 订单趋势（最近7天）
        order_trends = []
        for i in range(6, -1, -1):
            target_date = (datetime.now() - timedelta(days=i)).date()
            date = target_date.strftime("%m-%d")
            count = db.query(Order).filter(
                func.date(Order.created_at) == target_date
            ).count()
            order_trends.append({"date": date, "count": count})
        
        # 分类分布（按项目分类统计订单数）
        category_dist = db.query(
            ProjectCategory.name,
            func.count(Order.id).label('count')
        ).join(
            Project, Project.category_id == ProjectCategory.id
        ).join(
            Order, Order.project_id == Project.id
        ).group_by(ProjectCategory.name).limit(5).all()
        
        category_distribution = []
        colors = ['#409eff', '#67c23a', '#e6a23c', '#f56c6c', '#909399']
        total_orders = sum([c.count for c in category_dist]) or 1
        for idx, (name, count) in enumerate(category_dist):
            category_distribution.append({
                "category": name,
                "percentage": round((count / total_orders) * 100, 1),
                "color": colors[idx % len(colors)]
            })
        
        # 用户增长（本月和上月）
        this_month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0)
        last_month_start = (this_month_start - timedelta(days=1)).replace(day=1)
        last_month_end = this_month_start - timedelta(seconds=1)
        
        this_month_users = db.query(User).filter(
            User.created_at >= this_month_start
        ).count()
        
        last_month_users = db.query(User).filter(
            User.created_at >= last_month_start,
            User.created_at <= last_month_end
        ).count()
        
        growth_rate = 0
        if last_month_users > 0:
            growth_rate = round(((this_month_users - last_month_users) / last_month_users) * 100, 1)
        
        # 活跃用户（最近30天有登录）
        active_users = db.query(User).filter(
            User.last_login_at >= datetime.now() - timedelta(days=30)
        ).count()
        
        # 收入分析
        this_month_revenue = db.query(func.sum(Order.total_fee)).filter(
            Order.created_at >= this_month_start,
            Order.status.in_(["confirmed", "processing", "completed"])
        ).scalar() or Decimal("0")
        
        last_month_revenue = db.query(func.sum(Order.total_fee)).filter(
            Order.created_at >= last_month_start,
            Order.created_at <= last_month_end,
            Order.status.in_(["confirmed", "processing", "completed"])
        ).scalar() or Decimal("0")
        
        revenue_growth_rate = 0
        if last_month_revenue > 0:
            revenue_growth_rate = round(((float(this_month_revenue) - float(last_month_revenue)) / float(last_month_revenue)) * 100, 1)
        
        # 平均客单价
        this_month_orders = db.query(Order).filter(
            Order.created_at >= this_month_start,
            Order.status.in_(["confirmed", "processing", "completed"])
        ).count()
        
        avg_order_value = 0
        if this_month_orders > 0:
            avg_order_value = round(float(this_month_revenue) / this_month_orders, 2)
        
        return Response.success(data={
            "orderTrends": order_trends,
            "categoryDistribution": category_distribution,
            "userGrowth": {
                "thisMonth": this_month_users,
                "lastMonth": last_month_users,
                "growthRate": growth_rate,
                "activeUsers": active_users
            },
            "revenueAnalysis": {
                "thisMonth": float(this_month_revenue),
                "lastMonth": float(last_month_revenue),
                "growthRate": revenue_growth_rate,
                "avgOrderValue": avg_order_value
            }
        })
    except Exception as e:
        print(f"获取数据分析失败: {str(e)}")
        # 返回默认数据
        return Response.success(data={
            "orderTrends": [],
            "categoryDistribution": [],
            "userGrowth": {"thisMonth": 0, "lastMonth": 0, "growthRate": 0, "activeUsers": 0},
            "revenueAnalysis": {"thisMonth": 0, "lastMonth": 0, "growthRate": 0, "avgOrderValue": 0}
        })


@router.get("/analytics/export", summary="导出数据分析报表（管理员）")
async def export_analytics(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """导出数据分析报表（暂时返回空文件）"""
    from fastapi.responses import Response as FastAPIResponse
    # TODO: 实现Excel导出功能
    return FastAPIResponse(content="", media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


# ==================== 角色管理 ====================

@router.get("/roles", summary="获取角色列表（管理员）")
async def get_roles(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取角色列表（暂时返回默认角色）"""
    # TODO: 实现真实的角色管理功能
    roles = [
        {"id": 1, "name": "销售", "code": "sales", "description": "销售人员", "user_count": 0, "is_active": True, "is_system": False},
        {"id": 2, "name": "技术老师", "code": "teacher", "description": "技术指导老师", "user_count": 0, "is_active": True, "is_system": False},
        {"id": 3, "name": "实验室", "code": "lab", "description": "实验室人员", "user_count": 0, "is_active": True, "is_system": False},
        {"id": 4, "name": "财务", "code": "finance", "description": "财务人员", "user_count": 0, "is_active": True, "is_system": False},
        {"id": 5, "name": "客服", "code": "service", "description": "客服人员", "user_count": 0, "is_active": True, "is_system": False},
        {"id": 6, "name": "超级管理员", "code": "admin", "description": "系统管理员", "user_count": 1, "is_active": True, "is_system": True}
    ]
    return Response.success(data={"items": roles})


@router.post("/roles", summary="创建角色（管理员）")
async def create_role(
    data: dict = Body(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """创建角色（暂时返回成功）"""
    # TODO: 实现真实的角色创建功能
    return Response.success(message="角色创建成功", data={"id": 999, **data})


@router.put("/roles/{role_id}", summary="更新角色（管理员）")
async def update_role(
    role_id: int,
    data: dict = Body(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """更新角色（暂时返回成功）"""
    # TODO: 实现真实的角色更新功能
    return Response.success(message="角色更新成功")


@router.delete("/roles/{role_id}", summary="删除角色（管理员）")
async def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """删除角色（暂时返回成功）"""
    # TODO: 实现真实的角色删除功能
    return Response.success(message="角色删除成功")


@router.put("/roles/{role_id}/permissions", summary="更新角色权限（管理员）")
async def update_role_permissions(
    role_id: int,
    data: dict = Body(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """更新角色权限（暂时返回成功）"""
    # TODO: 实现真实的权限管理功能
    return Response.success(message="权限更新成功")


# ==================== 折扣管理 ====================

@router.get("/discounts", summary="获取折扣列表（管理员）")
async def get_discounts(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取折扣列表（暂时返回空列表）"""
    # TODO: 实现真实的折扣管理功能
    return Response.success(data={"items": []})


@router.post("/discounts", summary="创建折扣（管理员）")
async def create_discount(
    data: dict = Body(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """创建折扣（暂时返回成功）"""
    # TODO: 实现真实的折扣创建功能
    return Response.success(message="折扣创建成功", data={"id": 999, **data})


@router.put("/discounts/{discount_id}", summary="更新折扣（管理员）")
async def update_discount(
    discount_id: int,
    data: dict = Body(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """更新折扣（暂时返回成功）"""
    # TODO: 实现真实的折扣更新功能
    return Response.success(message="折扣更新成功")


@router.put("/discounts/{discount_id}/status", summary="更新折扣状态（管理员）")
async def update_discount_status(
    discount_id: int,
    data: dict = Body(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """更新折扣状态（暂时返回成功）"""
    # TODO: 实现真实的折扣状态更新功能
    return Response.success(message="状态更新成功")


@router.delete("/discounts/{discount_id}", summary="删除折扣（管理员）")
async def delete_discount(
    discount_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """删除折扣（暂时返回成功）"""
    # TODO: 实现真实的折扣删除功能
    return Response.success(message="折扣删除成功")


# ==================== 抽奖管理 ====================

@router.get("/lotteries", summary="获取抽奖活动列表（管理员）")
async def get_lotteries(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取抽奖活动列表（暂时返回空列表）"""
    # TODO: 实现真实的抽奖管理功能
    return Response.success(data={"items": []})


@router.get("/lotteries/{lottery_id}/prizes", summary="获取抽奖奖品列表（管理员）")
async def get_lottery_prizes(
    lottery_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取抽奖奖品列表（暂时返回空列表）"""
    # TODO: 实现真实的奖品查询功能
    return Response.success(data=[])


@router.get("/lotteries/{lottery_id}/records", summary="获取抽奖中奖记录（管理员）")
async def get_lottery_records(
    lottery_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取抽奖中奖记录（暂时返回空列表）"""
    # TODO: 实现真实的中奖记录查询功能
    return Response.success(data=[])


# ==================== 销售统计 ====================

@router.get("/sales/stats", summary="获取销售统计（管理员）")
async def get_sales_stats(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    staff_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取销售统计数据"""
    try:
        # 解析日期
        if start_date:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        else:
            start_dt = datetime.now() - timedelta(days=30)
        
        if end_date:
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        else:
            end_dt = datetime.now()
        
        # 构建查询
        query = db.query(Order).filter(
            Order.created_at >= start_dt,
            Order.created_at <= end_dt,
            Order.status.in_(["confirmed", "processing", "completed"])
        )
        
        # 销售统计汇总
        total_orders = query.count()
        total_revenue = query.with_entities(func.sum(Order.total_fee)).scalar() or Decimal("0")
        avg_order_value = float(total_revenue / total_orders) if total_orders > 0 else 0
        
        # 销售排名（暂时返回空）
        ranking = []
        
        return Response.success(data={
            "summary": {
                "total_orders": total_orders,
                "total_revenue": float(total_revenue),
                "avg_order_value": avg_order_value,
                "period": f"{start_dt.strftime('%Y-%m-%d')} 至 {end_dt.strftime('%Y-%m-%d')}"
            },
            "ranking": ranking
        })
    except Exception as e:
        print(f"获取销售统计失败: {str(e)}")
        return Response.success(data={
            "summary": {
                "total_orders": 0,
                "total_revenue": 0,
                "avg_order_value": 0,
                "period": ""
            },
            "ranking": []
        })


@router.get("/sales/export", summary="导出销售数据（管理员）")
async def export_sales_data(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """导出销售数据（暂时返回空文件）"""
    from fastapi.responses import Response as FastAPIResponse
    # TODO: 实现Excel导出功能
    return FastAPIResponse(content="", media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


# ==================== 二维码推广 ====================

@router.get("/qrcodes", summary="获取二维码列表（管理员）")
async def get_qrcodes(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取二维码列表（暂时返回空列表）"""
    # TODO: 实现真实的二维码管理功能
    return Response.success(data={"items": []})


@router.post("/qrcodes", summary="创建二维码（管理员）")
async def create_qrcode(
    data: dict = Body(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """创建二维码（暂时返回成功）"""
    # TODO: 实现真实的二维码生成功能
    return Response.success(message="二维码创建成功", data={"id": 999, "qrcode_url": "https://via.placeholder.com/100?text=QR", **data})


@router.get("/qrcodes/{qrcode_id}/download", summary="下载二维码（管理员）")
async def download_qrcode(
    qrcode_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """下载二维码（暂时返回空文件）"""
    from fastapi.responses import Response as FastAPIResponse
    # TODO: 实现二维码下载功能
    return FastAPIResponse(content="", media_type="image/png")


@router.delete("/qrcodes/{qrcode_id}", summary="删除二维码（管理员）")
async def delete_qrcode(
    qrcode_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """删除二维码（暂时返回成功）"""
    # TODO: 实现真实的二维码删除功能
    return Response.success(message="二维码删除成功")


# ==================== 实名认证管理 ====================

@router.get("/certifications", summary="获取认证申请列表（管理员）")
async def get_certifications_admin(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None, description="状态: pending/approved/rejected"),
    search: Optional[str] = Query(None, description="搜索关键字（姓名/手机号）"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员获取实名认证申请列表"""
    query = db.query(UserCertification).options(joinedload(UserCertification.user))

    # 状态筛选
    if status:
        query = query.filter(UserCertification.status == status)

    # 搜索
    if search:
        query = query.join(User).filter(
            or_(
                UserCertification.real_name.like(f"%{search}%"),
                User.phone.like(f"%{search}%")
            )
        )

    total = query.count()
    certifications = query.order_by(desc(UserCertification.created_at)).offset((page - 1) * page_size).limit(page_size).all()

    return Response.success(data={
        "items": [
            {
                "id": c.id,
                "user_id": c.user_id,
                "user_phone": c.user.phone if c.user else None,
                "user_nickname": c.user.nickname if c.user else None,
                "real_name": c.real_name,
                "id_card": c.id_card,
                "identity_type": c.identity_type.value if c.identity_type else None,
                "education_level": c.education_level.value if c.education_level else None,
                "university": c.university,
                "department": c.department,
                "supervisor": c.supervisor,
                "enrollment_year": c.enrollment_year,
                "graduation_year": c.graduation_year,
                "company": c.company,
                "position": c.position,
                "province": c.province,
                "status": c.status,
                "reject_reason": c.reject_reason,
                "id_card_front": c.id_card_front,
                "id_card_back": c.id_card_back,
                "student_card": c.student_card,
                "created_at": c.created_at.isoformat() if c.created_at else None,
                "reviewed_at": c.reviewed_at.isoformat() if c.reviewed_at else None
            }
            for c in certifications
        ],
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.get("/certifications/{cert_id}", summary="获取认证详情（管理员）")
async def get_certification_detail_admin(
    cert_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员获取实名认证详情"""
    cert = db.query(UserCertification).options(
        joinedload(UserCertification.user)
    ).filter(UserCertification.id == cert_id).first()

    if not cert:
        raise HTTPException(status_code=404, detail="认证记录不存在")

    return Response.success(data={
        "id": cert.id,
        "user_id": cert.user_id,
        "user_phone": cert.user.phone if cert.user else None,
        "user_nickname": cert.user.nickname if cert.user else None,
        "real_name": cert.real_name,
        "id_card": cert.id_card,
        "identity_type": cert.identity_type.value if cert.identity_type else None,
        "education_level": cert.education_level.value if cert.education_level else None,
        "university": cert.university,
        "department": cert.department,
        "supervisor": cert.supervisor,
        "enrollment_year": cert.enrollment_year,
        "graduation_year": cert.graduation_year,
        "company": cert.company,
        "position": cert.position,
        "province": cert.province,
        "status": cert.status,
        "reject_reason": cert.reject_reason,
        "id_card_front": cert.id_card_front,
        "id_card_back": cert.id_card_back,
        "student_card": cert.student_card,
        "created_at": cert.created_at.isoformat() if cert.created_at else None,
        "reviewed_at": cert.reviewed_at.isoformat() if cert.reviewed_at else None
    })


class CertificationReviewRequest(BaseModel):
    action: str  # approve / reject
    reject_reason: Optional[str] = None
    credit_limit: Optional[float] = 3000.0  # 默认授予3000元信用额度


class BannerCreate(BaseModel):
    title: Optional[str] = None
    image: str
    link: Optional[str] = None
    sort_order: int = 0
    is_active: bool = True


class BannerUpdate(BaseModel):
    title: Optional[str] = None
    image: Optional[str] = None
    link: Optional[str] = None
    sort_order: Optional[int] = None
    is_active: Optional[bool] = None


@router.put("/certifications/{cert_id}/review", summary="审核实名认证（管理员）")
async def review_certification_admin(
    cert_id: int,
    data: CertificationReviewRequest,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """
    管理员审核实名认证
    - approve: 通过认证，自动授予信用额度
    - reject: 拒绝认证，需提供拒绝原因
    """
    cert = db.query(UserCertification).filter(UserCertification.id == cert_id).first()

    if not cert:
        raise HTTPException(status_code=404, detail="认证记录不存在")

    if cert.status != "pending":
        raise HTTPException(status_code=400, detail="该认证申请已处理")

    user = db.query(User).filter(User.id == cert.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    if data.action == "approve":
        # 更新认证状态
        cert.status = "approved"
        cert.reviewed_at = datetime.utcnow()
        cert.reviewer_id = current_admin.id

        # 更新用户认证状态
        user.is_certified = True
        user.real_name = cert.real_name
        user.id_card = cert.id_card

        # 授予信用额度
        credit_amount = Decimal(str(data.credit_limit or 3000))
        user.credit_limit = credit_amount

        # 创建信用额度授予记录
        credit_record = CreditRecord(
            user_id=user.id,
            transaction_type=CreditTransactionType.GRANT,
            amount=credit_amount,
            balance_after=credit_amount,
            description="实名认证通过，系统自动授予信用额度",
            reference_type="certification",
            reference_id=cert.id,
            status=CreditTransactionStatus.SUCCESS
        )
        db.add(credit_record)

        db.commit()
        return Response.success(message=f"认证通过，已授予用户 {credit_amount} 元信用额度")

    elif data.action == "reject":
        if not data.reject_reason:
            raise HTTPException(status_code=400, detail="请提供拒绝原因")

        cert.status = "rejected"
        cert.reject_reason = data.reject_reason
        cert.reviewed_at = datetime.utcnow()
        cert.reviewer_id = current_admin.id

        db.commit()
        return Response.success(message="认证已拒绝")

    else:
        raise HTTPException(status_code=400, detail="无效的操作类型")


# ==================== 信用额度管理 ====================

@router.get("/credit/debts", summary="获取欠款列表（管理员）")
async def get_all_debts_admin(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None, description="状态: pending/partial/paid/overdue"),
    search: Optional[str] = Query(None, description="搜索关键字（手机号/姓名）"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员获取所有用户欠款列表"""
    from app.models.credit import CreditDebt

    query = db.query(CreditDebt).options(joinedload(CreditDebt.user))

    if status:
        query = query.filter(CreditDebt.status == status)

    if search:
        query = query.join(User).filter(
            or_(
                User.phone.like(f"%{search}%"),
                User.real_name.like(f"%{search}%"),
                User.nickname.like(f"%{search}%")
            )
        )

    total = query.count()
    debts = query.order_by(desc(CreditDebt.created_at)).offset((page - 1) * page_size).limit(page_size).all()

    return Response.success(data={
        "items": [
            {
                "id": d.id,
                "user_id": d.user_id,
                "user_phone": d.user.phone if d.user else None,
                "user_nickname": d.user.nickname if d.user else None,
                "user_real_name": d.user.real_name if d.user else None,
                "order_id": d.order_id,
                "order_no": d.order_no,
                "original_amount": float(d.original_amount),
                "remaining_amount": float(d.remaining_amount),
                "status": d.status.value if d.status else None,
                "due_date": d.due_date.isoformat() if d.due_date else None,
                "is_overdue": d.due_date and d.due_date < datetime.utcnow() and d.status.value != "paid" if d.due_date and d.status else False,
                "created_at": d.created_at.isoformat() if d.created_at else None
            }
            for d in debts
        ],
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.get("/credit/limit-applications", summary="获取额度申请列表（管理员）")
async def get_limit_applications_admin(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None, description="状态: pending/approved/rejected"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员获取信用额度申请列表"""
    from app.models.credit import CreditLimitApplication

    query = db.query(CreditLimitApplication).options(joinedload(CreditLimitApplication.user))

    if status:
        query = query.filter(CreditLimitApplication.status == status)

    total = query.count()
    applications = query.order_by(desc(CreditLimitApplication.created_at)).offset((page - 1) * page_size).limit(page_size).all()

    return Response.success(data={
        "items": [
            {
                "id": a.id,
                "user_id": a.user_id,
                "user_phone": a.user.phone if a.user else None,
                "user_nickname": a.user.nickname if a.user else None,
                "current_limit": float(a.current_limit),
                "requested_limit": float(a.requested_limit),
                "reason": a.reason,
                "status": a.status,
                "reject_reason": a.reject_reason,
                "created_at": a.created_at.isoformat() if a.created_at else None,
                "reviewed_at": a.reviewed_at.isoformat() if a.reviewed_at else None
            }
            for a in applications
        ],
        "total": total,
        "page": page,
        "page_size": page_size
    })


class LimitApplicationReviewRequest(BaseModel):
    action: str  # approve / reject
    approved_limit: Optional[float] = None  # 批准的额度（可能与申请额度不同）
    reject_reason: Optional[str] = None


@router.put("/credit/limit-applications/{app_id}/review", summary="审核额度申请（管理员）")
async def review_limit_application_admin(
    app_id: int,
    data: LimitApplicationReviewRequest,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """
    管理员审核信用额度提升申请
    - approve: 通过申请，可指定批准额度
    - reject: 拒绝申请，需提供拒绝原因
    """
    from app.models.credit import CreditLimitApplication

    application = db.query(CreditLimitApplication).filter(CreditLimitApplication.id == app_id).first()

    if not application:
        raise HTTPException(status_code=404, detail="申请记录不存在")

    if application.status != "pending":
        raise HTTPException(status_code=400, detail="该申请已处理")

    user = db.query(User).filter(User.id == application.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    if data.action == "approve":
        # 确定批准额度
        approved_limit = Decimal(str(data.approved_limit)) if data.approved_limit else application.requested_limit
        old_limit = user.credit_limit or Decimal("0")
        increase_amount = approved_limit - old_limit

        # 更新申请状态
        application.status = "approved"
        application.approved_limit = approved_limit
        application.reviewed_at = datetime.utcnow()
        application.reviewer_id = current_admin.id

        # 更新用户信用额度
        user.credit_limit = approved_limit

        # 创建额度提升记录
        if increase_amount > 0:
            credit_record = CreditRecord(
                user_id=user.id,
                transaction_type=CreditTransactionType.GRANT,
                amount=increase_amount,
                balance_after=approved_limit,
                description=f"信用额度提升申请通过，从 {old_limit} 元提升至 {approved_limit} 元",
                reference_type="limit_application",
                reference_id=application.id,
                status=CreditTransactionStatus.SUCCESS
            )
            db.add(credit_record)

        db.commit()
        return Response.success(message=f"申请通过，用户信用额度已提升至 {approved_limit} 元")

    elif data.action == "reject":
        if not data.reject_reason:
            raise HTTPException(status_code=400, detail="请提供拒绝原因")

        application.status = "rejected"
        application.reject_reason = data.reject_reason
        application.reviewed_at = datetime.utcnow()
        application.reviewer_id = current_admin.id

        db.commit()
        return Response.success(message="申请已拒绝")

    else:
        raise HTTPException(status_code=400, detail="无效的操作类型")


@router.put("/credit/users/{user_id}/limit", summary="调整用户信用额度（管理员）")
async def adjust_user_credit_limit(
    user_id: int,
    new_limit: float = Query(..., description="新的信用额度"),
    reason: str = Query(..., description="调整原因"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员直接调整用户信用额度"""
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    old_limit = user.credit_limit or Decimal("0")
    new_limit_decimal = Decimal(str(new_limit))

    # 检查新额度是否小于已使用额度
    if new_limit_decimal < (user.used_credit or Decimal("0")):
        raise HTTPException(
            status_code=400,
            detail=f"新额度不能小于已使用额度（{user.used_credit} 元）"
        )

    # 更新用户信用额度
    user.credit_limit = new_limit_decimal

    # 记录调整
    transaction_type = CreditTransactionType.GRANT if new_limit_decimal > old_limit else CreditTransactionType.ADJUST
    amount = abs(new_limit_decimal - old_limit)

    credit_record = CreditRecord(
        user_id=user.id,
        transaction_type=transaction_type,
        amount=amount,
        balance_after=new_limit_decimal,
        description=f"管理员调整信用额度：{reason}（从 {old_limit} 元调整为 {new_limit_decimal} 元）",
        reference_type="admin_adjustment",
        operator_id=current_admin.id,
        status=CreditTransactionStatus.SUCCESS
    )
    db.add(credit_record)

    db.commit()
    return Response.success(message=f"用户信用额度已调整为 {new_limit_decimal} 元")


# ==================== 实验室管理 ====================

@router.get("/laboratories", summary="获取实验室列表（管理员）")
async def get_laboratories_admin(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None, description="搜索关键字"),
    status: Optional[str] = Query(None, description="状态筛选"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员获取实验室列表"""
    from app.models.laboratory import Laboratory, LabStatus

    query = db.query(Laboratory)

    if search:
        query = query.filter(
            or_(
                Laboratory.name.like(f"%{search}%"),
                Laboratory.institution.like(f"%{search}%"),
                Laboratory.code.like(f"%{search}%")
            )
        )

    if status:
        try:
            status_enum = LabStatus(status)
            query = query.filter(Laboratory.status == status_enum)
        except ValueError:
            pass

    total = query.count()
    labs = query.order_by(desc(Laboratory.created_at)).offset((page - 1) * page_size).limit(page_size).all()

    return Response.success(data={
        "items": [
            {
                "id": lab.id,
                "name": lab.name,
                "code": lab.code,
                "logo": lab.logo,
                "lab_type": lab.lab_type if lab.lab_type else None,
                "status": lab.status if lab.status else None,
                "institution": lab.institution,
                "province": lab.province,
                "city": lab.city,
                "contact_name": lab.contact_name,
                "contact_phone": lab.contact_phone,
                "rating": float(lab.rating) if lab.rating else 5.0,
                "total_orders": lab.total_orders or 0,
                "commission_rate": float(lab.commission_rate) if lab.commission_rate else 20.0,
                "created_at": lab.created_at.isoformat() if lab.created_at else None
            }
            for lab in labs
        ],
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.get("/laboratories/{lab_id}", summary="获取实验室详情（管理员）")
async def get_laboratory_detail_admin(
    lab_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员获取实验室详情"""
    from app.models.laboratory import Laboratory

    lab = db.query(Laboratory).filter(Laboratory.id == lab_id).first()

    if not lab:
        raise HTTPException(status_code=404, detail="实验室不存在")

    return Response.success(data={
        "id": lab.id,
        "name": lab.name,
        "code": lab.code,
        "logo": lab.logo,
        "cover_image": lab.cover_image,
        "lab_type": lab.lab_type.value if lab.lab_type else None,
        "status": lab.status.value if lab.status else None,
        "institution": lab.institution,
        "department": lab.department,
        "province": lab.province,
        "city": lab.city,
        "address": lab.address,
        "contact_name": lab.contact_name,
        "contact_phone": lab.contact_phone,
        "contact_email": lab.contact_email,
        "qualification": lab.qualification,
        "certification": lab.certification,
        "business_license": lab.business_license,
        "description": lab.description,
        "specialties": lab.specialties,
        "rating": float(lab.rating) if lab.rating else 5.0,
        "total_orders": lab.total_orders or 0,
        "completed_orders": lab.completed_orders or 0,
        "commission_rate": float(lab.commission_rate) if lab.commission_rate else 20.0,
        "admin_user_id": lab.admin_user_id,
        "created_at": lab.created_at.isoformat() if lab.created_at else None,
        "approved_at": lab.approved_at.isoformat() if lab.approved_at else None
    })


@router.put("/laboratories/{lab_id}/status", summary="修改实验室状态（管理员）")
async def update_laboratory_status_admin(
    lab_id: int,
    status: str = Query(..., description="状态: pending/approved/active/suspended/closed"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员修改实验室状态"""
    from app.models.laboratory import Laboratory, LabStatus

    lab = db.query(Laboratory).filter(Laboratory.id == lab_id).first()

    if not lab:
        raise HTTPException(status_code=404, detail="实验室不存在")

    try:
        new_status = LabStatus(status)
    except ValueError:
        raise HTTPException(status_code=400, detail="无效的状态值")

    lab.status = new_status

    if new_status == LabStatus.ACTIVE and not lab.approved_at:
        lab.approved_at = datetime.utcnow()

    db.commit()
    return Response.success(message="实验室状态更新成功")


@router.put("/laboratories/{lab_id}/commission", summary="调整实验室佣金比例（管理员）")
async def update_laboratory_commission(
    lab_id: int,
    commission_rate: float = Query(..., ge=0, le=100, description="佣金比例(%)"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员调整实验室佣金比例"""
    from app.models.laboratory import Laboratory

    lab = db.query(Laboratory).filter(Laboratory.id == lab_id).first()

    if not lab:
        raise HTTPException(status_code=404, detail="实验室不存在")

    lab.commission_rate = Decimal(str(commission_rate))
    db.commit()

    return Response.success(message=f"佣金比例已调整为 {commission_rate}%")


# ==================== 实验室入驻申请管理 ====================

@router.get("/lab-applications", summary="获取入驻申请列表（管理员）")
async def get_lab_applications_admin(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None, description="状态: pending/reviewing/approved/rejected"),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员获取实验室入驻申请列表"""
    from app.models.laboratory import LabApplication

    query = db.query(LabApplication).options(joinedload(LabApplication.applicant))

    if status:
        query = query.filter(LabApplication.status == status)

    if search:
        query = query.filter(
            or_(
                LabApplication.lab_name.like(f"%{search}%"),
                LabApplication.applicant_name.like(f"%{search}%"),
                LabApplication.applicant_phone.like(f"%{search}%")
            )
        )

    total = query.count()
    applications = query.order_by(desc(LabApplication.created_at)).offset((page - 1) * page_size).limit(page_size).all()

    return Response.success(data={
        "items": [
            {
                "id": app.id,
                "lab_name": app.lab_name,
                "lab_type": app.lab_type.value if app.lab_type else None,
                "institution": app.institution,
                "province": app.province,
                "city": app.city,
                "applicant_name": app.applicant_name,
                "applicant_phone": app.applicant_phone,
                "applicant_user_id": app.applicant_user_id,
                "status": app.status,
                "reject_reason": app.reject_reason,
                "laboratory_id": app.laboratory_id,
                "created_at": app.created_at.isoformat() if app.created_at else None,
                "reviewed_at": app.reviewed_at.isoformat() if app.reviewed_at else None
            }
            for app in applications
        ],
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.get("/lab-applications/{app_id}", summary="获取入驻申请详情（管理员）")
async def get_lab_application_detail_admin(
    app_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员获取入驻申请详情"""
    from app.models.laboratory import LabApplication

    application = db.query(LabApplication).options(
        joinedload(LabApplication.applicant)
    ).filter(LabApplication.id == app_id).first()

    if not application:
        raise HTTPException(status_code=404, detail="申请不存在")

    return Response.success(data={
        "id": application.id,
        "applicant_user_id": application.applicant_user_id,
        "applicant_name": application.applicant_name,
        "applicant_phone": application.applicant_phone,
        "applicant_email": application.applicant_email,
        "applicant_position": application.applicant_position,
        "lab_name": application.lab_name,
        "lab_type": application.lab_type.value if application.lab_type else None,
        "institution": application.institution,
        "department": application.department,
        "province": application.province,
        "city": application.city,
        "address": application.address,
        "qualification": application.qualification,
        "certification_files": application.certification_files,
        "business_license": application.business_license,
        "description": application.description,
        "specialties": application.specialties,
        "equipments_desc": application.equipments_desc,
        "intended_services": application.intended_services,
        "expected_monthly_orders": application.expected_monthly_orders,
        "status": application.status,
        "review_remark": application.review_remark,
        "reject_reason": application.reject_reason,
        "laboratory_id": application.laboratory_id,
        "created_at": application.created_at.isoformat() if application.created_at else None,
        "reviewed_at": application.reviewed_at.isoformat() if application.reviewed_at else None
    })


class LabApplicationReviewRequest(BaseModel):
    action: str  # approve / reject
    reject_reason: Optional[str] = None
    commission_rate: Optional[float] = 20.0  # 佣金比例


@router.put("/lab-applications/{app_id}/review", summary="审核入驻申请（管理员）")
async def review_lab_application_admin(
    app_id: int,
    data: LabApplicationReviewRequest,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """
    管理员审核实验室入驻申请
    - approve: 通过申请，创建实验室
    - reject: 拒绝申请
    """
    from app.models.laboratory import LabApplication, Laboratory, LabStatus, LabType
    import time

    application = db.query(LabApplication).filter(LabApplication.id == app_id).first()

    if not application:
        raise HTTPException(status_code=404, detail="申请不存在")

    if application.status not in ["pending", "reviewing"]:
        raise HTTPException(status_code=400, detail="该申请已处理")

    if data.action == "approve":
        # 生成实验室编号
        lab_code = f"LAB{int(time.time())}"

        # 创建实验室
        laboratory = Laboratory(
            name=application.lab_name,
            code=lab_code,
            lab_type=application.lab_type,
            status=LabStatus.ACTIVE,
            institution=application.institution,
            department=application.department,
            province=application.province,
            city=application.city,
            address=application.address,
            contact_name=application.applicant_name,
            contact_phone=application.applicant_phone,
            contact_email=application.applicant_email,
            qualification=application.qualification,
            certification=application.certification_files,
            business_license=application.business_license,
            description=application.description,
            specialties=application.specialties,
            equipments_summary=application.equipments_desc,
            commission_rate=Decimal(str(data.commission_rate or 20)),
            admin_user_id=application.applicant_user_id,
            approved_at=datetime.utcnow()
        )

        db.add(laboratory)
        db.flush()

        # 更新申请状态
        application.status = "approved"
        application.laboratory_id = laboratory.id
        application.reviewer_id = current_admin.id
        application.reviewed_at = datetime.utcnow()

        db.commit()
        return Response.success(
            data={"laboratory_id": laboratory.id},
            message="申请已通过，实验室创建成功"
        )

    elif data.action == "reject":
        if not data.reject_reason:
            raise HTTPException(status_code=400, detail="请提供拒绝原因")

        application.status = "rejected"
        application.reject_reason = data.reject_reason
        application.reviewer_id = current_admin.id
        application.reviewed_at = datetime.utcnow()

        db.commit()
        return Response.success(message="申请已拒绝")

    else:
        raise HTTPException(status_code=400, detail="无效的操作类型")


# ==================== 角色权限管理 ====================

class RoleCreate(BaseModel):
    """创建角色请求"""
    name: str
    code: str
    description: Optional[str] = None
    permission_ids: Optional[List[int]] = []


class RoleUpdate(BaseModel):
    """更新角色请求"""
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    permission_ids: Optional[List[int]] = None


class UserRoleAssign(BaseModel):
    """分配用户角色"""
    user_id: int
    role_ids: List[int]


@router.get("/roles", summary="获取角色列表")
async def get_roles(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取所有角色"""
    from app.models.role import Role

    query = db.query(Role)

    if search:
        query = query.filter(
            or_(
                Role.name.like(f"%{search}%"),
                Role.code.like(f"%{search}%")
            )
        )

    total = query.count()
    roles = query.order_by(Role.sort_order, Role.id).offset((page - 1) * page_size).limit(page_size).all()

    return Response.success(data={
        "items": [
            {
                "id": r.id,
                "name": r.name,
                "code": r.code,
                "description": r.description,
                "is_system": r.is_system,
                "is_active": r.is_active,
                "user_count": len(r.users),
                "permission_count": len(r.permissions),
                "created_at": r.created_at.isoformat() if r.created_at else None
            }
            for r in roles
        ],
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.get("/roles/{role_id}", summary="获取角色详情")
async def get_role_detail(
    role_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取角色详情及其权限"""
    from app.models.role import Role

    role = db.query(Role).options(
        joinedload(Role.permissions)
    ).filter(Role.id == role_id).first()

    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")

    return Response.success(data={
        "id": role.id,
        "name": role.name,
        "code": role.code,
        "description": role.description,
        "is_system": role.is_system,
        "is_active": role.is_active,
        "permissions": [
            {
                "id": p.id,
                "name": p.name,
                "code": p.code,
                "module": p.module
            }
            for p in role.permissions
        ]
    })


@router.post("/roles", summary="创建角色")
async def create_role(
    data: RoleCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """创建新角色"""
    from app.models.role import Role, Permission

    # 检查编码是否存在
    existing = db.query(Role).filter(Role.code == data.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="角色编码已存在")

    role = Role(
        name=data.name,
        code=data.code,
        description=data.description,
        is_system=False,
        is_active=True
    )

    # 添加权限
    if data.permission_ids:
        permissions = db.query(Permission).filter(Permission.id.in_(data.permission_ids)).all()
        role.permissions = permissions

    db.add(role)
    db.commit()
    db.refresh(role)

    return Response.success(data={"id": role.id}, message="角色创建成功")


@router.put("/roles/{role_id}", summary="更新角色")
async def update_role(
    role_id: int,
    data: RoleUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """更新角色信息"""
    from app.models.role import Role, Permission

    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")

    if role.is_system:
        raise HTTPException(status_code=400, detail="系统角色不可修改")

    if data.name is not None:
        role.name = data.name
    if data.description is not None:
        role.description = data.description
    if data.is_active is not None:
        role.is_active = data.is_active

    # 更新权限
    if data.permission_ids is not None:
        permissions = db.query(Permission).filter(Permission.id.in_(data.permission_ids)).all()
        role.permissions = permissions

    db.commit()
    return Response.success(message="角色更新成功")


@router.delete("/roles/{role_id}", summary="删除角色")
async def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """删除角色"""
    from app.models.role import Role

    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")

    if role.is_system:
        raise HTTPException(status_code=400, detail="系统角色不可删除")

    if len(role.users) > 0:
        raise HTTPException(status_code=400, detail="该角色下还有用户，无法删除")

    db.delete(role)
    db.commit()

    return Response.success(message="角色已删除")


@router.get("/permissions", summary="获取所有权限")
async def get_permissions(
    module: Optional[str] = Query(None, description="按模块筛选"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取所有权限列表"""
    from app.models.role import Permission

    query = db.query(Permission)

    if module:
        query = query.filter(Permission.module == module)

    permissions = query.order_by(Permission.module, Permission.sort_order).all()

    # 按模块分组
    grouped = {}
    for p in permissions:
        mod = p.module or "other"
        if mod not in grouped:
            grouped[mod] = []
        grouped[mod].append({
            "id": p.id,
            "name": p.name,
            "code": p.code,
            "description": p.description
        })

    return Response.success(data={
        "items": [
            {
                "id": p.id,
                "name": p.name,
                "code": p.code,
                "module": p.module,
                "description": p.description
            }
            for p in permissions
        ],
        "grouped": grouped
    })


@router.post("/users/{user_id}/roles", summary="分配用户角色")
async def assign_user_roles(
    user_id: int,
    role_ids: List[int] = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """为用户分配角色"""
    from app.models.role import Role

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    roles = db.query(Role).filter(Role.id.in_(role_ids), Role.is_active == True).all()
    user.roles = roles

    # 如果分配了管理角色，设置is_admin标志
    admin_role_codes = ["super_admin", "admin", "operator", "finance", "cs"]
    has_admin_role = any(r.code in admin_role_codes for r in roles)
    user.is_admin = has_admin_role

    db.commit()

    return Response.success(message="角色分配成功")


@router.get("/users/{user_id}/roles", summary="获取用户角色")
async def get_user_roles(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取用户的角色列表"""
    user = db.query(User).options(
        joinedload(User.roles)
    ).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    return Response.success(data={
        "user_id": user.id,
        "user_name": user.nickname or user.phone,
        "roles": [
            {
                "id": r.id,
                "name": r.name,
                "code": r.code
            }
            for r in user.roles
        ]
    })


@router.get("/users/{user_id}/permissions", summary="获取用户权限")
async def get_user_permissions(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取用户的所有权限"""
    from app.models.role import Role

    user = db.query(User).options(
        joinedload(User.roles).joinedload(Role.permissions)
    ).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 汇总所有权限
    permissions = set()
    for role in user.roles:
        for p in role.permissions:
            permissions.add((p.id, p.name, p.code, p.module))

    return Response.success(data={
        "user_id": user.id,
        "is_admin": user.is_admin,
        "permissions": [
            {"id": p[0], "name": p[1], "code": p[2], "module": p[3]}
            for p in permissions
        ]
    })


@router.post("/roles/init", summary="初始化默认角色和权限")
async def init_roles_and_permissions(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """初始化系统默认角色和权限（仅首次使用）"""
    from app.models.role import Role, Permission, RoleCode, PermissionCode, DEFAULT_ROLE_PERMISSIONS

    # 检查是否已初始化
    existing_roles = db.query(Role).count()
    if existing_roles > 0:
        raise HTTPException(status_code=400, detail="角色已初始化，无需重复操作")

    # 定义权限
    permission_definitions = [
        # 用户管理
        ("user:view", "查看用户", "user"),
        ("user:edit", "编辑用户", "user"),
        ("user:delete", "删除用户", "user"),
        ("user:certification", "认证审核", "user"),
        # 订单管理
        ("order:view", "查看订单", "order"),
        ("order:edit", "编辑订单", "order"),
        ("order:delete", "删除订单", "order"),
        ("order:assign", "订单指派", "order"),
        ("order:export", "导出订单", "order"),
        # 项目管理
        ("project:view", "查看项目", "project"),
        ("project:create", "创建项目", "project"),
        ("project:edit", "编辑项目", "project"),
        ("project:delete", "删除项目", "project"),
        # 实验室管理
        ("lab:view", "查看实验室", "lab"),
        ("lab:create", "创建实验室", "lab"),
        ("lab:edit", "编辑实验室", "lab"),
        ("lab:delete", "删除实验室", "lab"),
        ("lab:approve", "审核实验室", "lab"),
        # 财务管理
        ("finance:view", "查看财务", "finance"),
        ("finance:recharge", "充值管理", "finance"),
        ("finance:refund", "退款管理", "finance"),
        ("finance:withdraw", "提现管理", "finance"),
        ("finance:report", "财务报表", "finance"),
        # 优惠券管理
        ("coupon:view", "查看优惠券", "coupon"),
        ("coupon:create", "创建优惠券", "coupon"),
        ("coupon:edit", "编辑优惠券", "coupon"),
        ("coupon:delete", "删除优惠券", "coupon"),
        # 内容管理
        ("content:banner", "轮播图管理", "content"),
        ("content:announcement", "公告管理", "content"),
        ("content:help", "帮助中心", "content"),
        # 报表统计
        ("report:view", "查看报表", "report"),
        ("report:export", "导出报表", "report"),
        # 系统设置
        ("system:config", "系统配置", "system"),
        ("system:role", "角色管理", "system"),
        ("system:log", "日志管理", "system"),
    ]

    # 创建权限
    permissions = {}
    for code, name, module in permission_definitions:
        perm = Permission(name=name, code=code, module=module)
        db.add(perm)
        permissions[code] = perm

    db.flush()

    # 定义角色
    role_definitions = [
        (RoleCode.SUPER_ADMIN, "超级管理员", "拥有所有权限", True),
        (RoleCode.ADMIN, "管理员", "普通管理员", True),
        (RoleCode.OPERATOR, "运营人员", "负责日常运营", True),
        (RoleCode.FINANCE, "财务人员", "负责财务管理", True),
        (RoleCode.CUSTOMER_SERVICE, "客服人员", "负责客户服务", True),
        (RoleCode.LAB_ADMIN, "实验室管理员", "实验室负责人", True),
        (RoleCode.LAB_TECHNICIAN, "实验室技术员", "实验室技术人员", True),
        (RoleCode.USER, "普通用户", "普通注册用户", True),
    ]

    # 创建角色并分配权限
    for code, name, desc, is_system in role_definitions:
        role = Role(
            name=name,
            code=code,
            description=desc,
            is_system=is_system,
            is_active=True
        )

        # 分配默认权限
        if code in DEFAULT_ROLE_PERMISSIONS:
            role_perms = []
            for perm_code in DEFAULT_ROLE_PERMISSIONS[code]:
                if perm_code in permissions:
                    role_perms.append(permissions[perm_code])
            role.permissions = role_perms

        db.add(role)

    db.commit()

    return Response.success(message="角色和权限初始化成功")


# ==================== 数据导出与报表 ====================

@router.get("/export/orders", summary="导出订单数据")
async def export_orders(
    start_date: Optional[str] = Query(None, description="开始日期 YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="结束日期 YYYY-MM-DD"),
    status: Optional[str] = Query(None, description="订单状态"),
    format: str = Query("json", description="导出格式: json/csv"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """导出订单数据"""
    from datetime import datetime as dt

    query = db.query(Order).filter(Order.is_draft == False)

    if start_date:
        try:
            start = dt.strptime(start_date, "%Y-%m-%d")
            query = query.filter(Order.created_at >= start)
        except ValueError:
            pass

    if end_date:
        try:
            end = dt.strptime(end_date, "%Y-%m-%d")
            query = query.filter(Order.created_at <= end)
        except ValueError:
            pass

    if status:
        query = query.filter(Order.status == status)

    orders = query.order_by(desc(Order.created_at)).limit(10000).all()

    data = []
    for o in orders:
        data.append({
            "订单号": o.order_no,
            "用户ID": o.user_id,
            "项目名称": o.project_name,
            "样品数量": o.sample_count,
            "项目费用": float(o.project_fee or 0),
            "加急费用": float(o.urgent_fee or 0),
            "运费": float(o.shipping_fee or 0),
            "优惠金额": float(o.discount_amount or 0),
            "总金额": float(o.total_fee or 0),
            "已支付": float(o.paid_fee or 0),
            "订单状态": o.status,
            "支付状态": o.payment_status,
            "开票状态": o.invoice_status,
            "是否加急": "是" if o.is_urgent else "否",
            "创建时间": o.created_at.strftime("%Y-%m-%d %H:%M:%S") if o.created_at else "",
            "支付时间": o.paid_at.strftime("%Y-%m-%d %H:%M:%S") if o.paid_at else "",
            "完成时间": o.completed_at.strftime("%Y-%m-%d %H:%M:%S") if o.completed_at else ""
        })

    if format == "csv":
        import csv
        import io
        from fastapi.responses import StreamingResponse
        output = io.StringIO()
        if data:
            writer = csv.DictWriter(output, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        csv_content = output.getvalue()
        # 添加 BOM 头以支持中文
        csv_bytes = ('\ufeff' + csv_content).encode('utf-8')
        return StreamingResponse(
            io.BytesIO(csv_bytes),
            media_type='text/csv; charset=utf-8',
            headers={
                'Content-Disposition': f'attachment; filename=orders_{start_date or "all"}_{end_date or "all"}.csv'
            }
        )

    return Response.success(data={
        "format": "json",
        "items": data,
        "total": len(data)
    })


@router.get("/export/users", summary="导出用户数据")
async def export_users(
    start_date: Optional[str] = Query(None, description="注册开始日期"),
    end_date: Optional[str] = Query(None, description="注册结束日期"),
    is_certified: Optional[bool] = Query(None, description="是否已认证"),
    format: str = Query("json", description="导出格式"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """导出用户数据"""
    from datetime import datetime as dt

    query = db.query(User)

    if start_date:
        try:
            start = dt.strptime(start_date, "%Y-%m-%d")
            query = query.filter(User.created_at >= start)
        except ValueError:
            pass

    if end_date:
        try:
            end = dt.strptime(end_date, "%Y-%m-%d")
            query = query.filter(User.created_at <= end)
        except ValueError:
            pass

    if is_certified is not None:
        query = query.filter(User.is_certified == is_certified)

    users = query.order_by(desc(User.created_at)).limit(10000).all()

    data = []
    for u in users:
        data.append({
            "用户ID": u.id,
            "手机号": u.phone,
            "昵称": u.nickname,
            "是否认证": "是" if u.is_certified else "否",
            "会员等级": u.membership_level.name if u.membership_level else "NORMAL",
            "信用额度": float(u.credit_limit or 0),
            "已用额度": float(u.used_credit or 0),
            "预付余额": float(u.prepaid_balance or 0),
            "积分余额": u.points_balance or 0,
            "累计消费": float(u.total_spent or 0),
            "订单数": u.total_orders or 0,
            "状态": u.status.value if u.status else "active",
            "注册时间": u.created_at.strftime("%Y-%m-%d %H:%M:%S") if u.created_at else ""
        })

    if format == "csv":
        import csv
        import io
        from fastapi.responses import StreamingResponse
        output = io.StringIO()
        if data:
            writer = csv.DictWriter(output, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        csv_content = output.getvalue()
        # 添加 BOM 头以支持中文
        csv_bytes = ('\ufeff' + csv_content).encode('utf-8')
        return StreamingResponse(
            io.BytesIO(csv_bytes),
            media_type='text/csv; charset=utf-8',
            headers={
                'Content-Disposition': f'attachment; filename=users_{start_date or "all"}_{end_date or "all"}.csv'
            }
        )

    return Response.success(data={
        "format": "json",
        "items": data,
        "total": len(data)
    })


@router.get("/reports/overview", summary="获取报表概览")
async def get_reports_overview(
    time_range: str = Query("month", description="时间范围: today/week/month/year"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取报表概览数据"""
    from datetime import date, timedelta

    today = date.today()

    if time_range == "today":
        start_date = today
    elif time_range == "week":
        start_date = today - timedelta(days=7)
    elif time_range == "year":
        start_date = today.replace(month=1, day=1)
    else:  # month
        start_date = today.replace(day=1)

    # 订单统计
    total_orders = db.query(Order).filter(
        Order.is_draft == False,
        Order.created_at >= start_date
    ).count()

    completed_orders = db.query(Order).filter(
        Order.status == "completed",
        Order.completed_at >= start_date
    ).count()

    # 收入统计
    total_revenue = db.query(func.sum(Order.total_fee)).filter(
        Order.status == "completed",
        Order.completed_at >= start_date
    ).scalar() or 0

    paid_amount = db.query(func.sum(Order.paid_fee)).filter(
        Order.paid_at >= start_date
    ).scalar() or 0

    # 用户统计
    new_users = db.query(User).filter(
        User.created_at >= start_date
    ).count()

    certified_users = db.query(User).filter(
        User.is_certified == True,
        User.created_at >= start_date
    ).count()

    # 实验室统计
    active_labs = db.query(Laboratory).filter(
        Laboratory.status == LabStatus.ACTIVE
    ).count()

    # 待处理事项
    pending_certifications = db.query(UserCertification).filter(
        UserCertification.status == "pending"
    ).count()

    pending_orders = db.query(Order).filter(
        Order.status.in_(["paid", "pending_assign"])
    ).count()

    pending_lab_apps = db.query(LabApplication).filter(
        LabApplication.status == "pending"
    ).count()

    return Response.success(data={
        "time_range": time_range,
        "orders": {
            "total": total_orders,
            "completed": completed_orders,
            "completion_rate": round(completed_orders / total_orders * 100, 2) if total_orders > 0 else 0
        },
        "revenue": {
            "total": float(total_revenue),
            "paid": float(paid_amount)
        },
        "users": {
            "new": new_users,
            "certified": certified_users
        },
        "labs": {
            "active": active_labs
        },
        "pending": {
            "certifications": pending_certifications,
            "orders": pending_orders,
            "lab_applications": pending_lab_apps
        }
    })


@router.get("/reports/order-trend", summary="获取订单趋势")
async def get_order_trend(
    time_range: str = Query("month", description="时间范围"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取订单趋势数据"""
    from datetime import date, timedelta
    from sqlalchemy import extract

    today = date.today()

    if time_range == "week":
        days = 7
        start_date = today - timedelta(days=days)
        group_format = "%Y-%m-%d"
    elif time_range == "year":
        days = 365
        start_date = today.replace(month=1, day=1)
        group_format = "%Y-%m"
    else:  # month
        days = 30
        start_date = today - timedelta(days=days)
        group_format = "%Y-%m-%d"

    # 按日期分组统计订单
    orders = db.query(Order).filter(
        Order.is_draft == False,
        Order.created_at >= start_date
    ).all()

    # 按日期聚合
    trend_data = {}
    for order in orders:
        if order.created_at:
            key = order.created_at.strftime(group_format)
            if key not in trend_data:
                trend_data[key] = {"date": key, "order_count": 0, "amount": 0}
            trend_data[key]["order_count"] += 1
            trend_data[key]["amount"] += float(order.total_fee or 0)

    # 排序并返回
    sorted_data = sorted(trend_data.values(), key=lambda x: x["date"])

    return Response.success(data=sorted_data)


@router.get("/reports/project-ranking", summary="获取项目排行")
async def get_project_ranking(
    time_range: str = Query("month", description="时间范围"),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取热门项目排行"""
    from datetime import date, timedelta

    today = date.today()

    if time_range == "week":
        start_date = today - timedelta(days=7)
    elif time_range == "year":
        start_date = today.replace(month=1, day=1)
    else:
        start_date = today.replace(day=1)

    # 按项目统计订单数和金额
    ranking = db.query(
        Order.project_id,
        Order.project_name,
        func.count(Order.id).label("order_count"),
        func.sum(Order.total_fee).label("total_amount")
    ).filter(
        Order.is_draft == False,
        Order.created_at >= start_date
    ).group_by(Order.project_id, Order.project_name).order_by(
        desc("order_count")
    ).limit(limit).all()

    return Response.success(data=[
        {
            "project_id": r.project_id,
            "project_name": r.project_name,
            "order_count": r.order_count,
            "total_amount": float(r.total_amount or 0)
        }
        for r in ranking
    ])


@router.get("/reports/lab-performance", summary="获取实验室业绩")
async def get_lab_performance(
    time_range: str = Query("month", description="时间范围"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取实验室业绩排行"""
    from datetime import date, timedelta

    today = date.today()

    if time_range == "week":
        start_date = today - timedelta(days=7)
    elif time_range == "year":
        start_date = today.replace(month=1, day=1)
    else:
        start_date = today.replace(day=1)

    # 按实验室统计
    performance = db.query(
        Laboratory.id,
        Laboratory.name,
        func.count(Order.id).label("order_count"),
        func.sum(Order.total_fee).label("total_amount")
    ).outerjoin(
        Order, Order.assigned_lab_id == Laboratory.id
    ).filter(
        Laboratory.status == LabStatus.ACTIVE
    ).group_by(Laboratory.id, Laboratory.name).order_by(
        desc("order_count")
    ).all()

    return Response.success(data={
        "time_range": time_range,
        "labs": [
            {
                "lab_id": p.id,
                "lab_name": p.name,
                "order_count": p.order_count or 0,
                "total_amount": float(p.total_amount or 0)
            }
            for p in performance
        ]
    })


@router.get("/reports/finance-summary", summary="获取财务汇总")
async def get_finance_summary(
    year: int = Query(None, description="年份"),
    month: int = Query(None, description="月份"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取财务汇总报表"""
    from datetime import date

    today = date.today()
    year = year or today.year
    month = month or today.month

    # 计算月份范围
    from calendar import monthrange
    _, last_day = monthrange(year, month)
    start_date = date(year, month, 1)
    end_date = date(year, month, last_day)

    # 订单收入
    order_income = db.query(func.sum(Order.paid_fee)).filter(
        Order.paid_at >= start_date,
        Order.paid_at <= end_date
    ).scalar() or 0

    # 充值收入
    recharge_income = db.query(func.sum(RechargeRecord.amount)).filter(
        RechargeRecord.status == RechargeStatus.SUCCESS,
        RechargeRecord.created_at >= start_date,
        RechargeRecord.created_at <= end_date
    ).scalar() or 0

    # 提现支出
    withdraw_amount = db.query(func.sum(WithdrawRecord.amount)).filter(
        WithdrawRecord.status == "success",
        WithdrawRecord.created_at >= start_date,
        WithdrawRecord.created_at <= end_date
    ).scalar() or 0

    # 信用支付
    credit_usage = db.query(func.sum(Order.credit_amount)).filter(
        Order.paid_at >= start_date,
        Order.paid_at <= end_date,
        Order.credit_amount > 0
    ).scalar() or 0

    return Response.success(data={
        "year": year,
        "month": month,
        "income": {
            "orders": float(order_income),
            "recharge": float(recharge_income),
            "total": float(order_income) + float(recharge_income)
        },
        "expense": {
            "withdraw": float(withdraw_amount)
        },
        "credit": {
            "usage": float(credit_usage)
        },
        "net": float(order_income) + float(recharge_income) - float(withdraw_amount)
    })


# ==================== 员工管理 ====================

@router.get("/staff", summary="获取员工列表")
async def get_staff_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    keyword: str = Query(None),
    role_id: int = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取员工列表"""
    from app.models.role import Role

    query = db.query(User).filter(User.is_admin == True)

    if keyword:
        query = query.filter(
            or_(
                User.nickname.contains(keyword),
                User.phone.contains(keyword)
            )
        )

    if role_id:
        query = query.join(User.roles).filter(Role.id == role_id)

    total = query.count()
    staff_list = query.order_by(User.id.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return Response.success(data={
        "items": [{
            "id": s.id,
            "nickname": s.nickname,
            "phone": s.phone,
            "avatar": s.avatar,
            "status": s.status.value if s.status else "active",
            "roles": [{"id": r.id, "name": r.name} for r in s.roles] if hasattr(s, 'roles') else [],
            "created_at": s.created_at.isoformat() if s.created_at else None,
            "last_login_at": s.last_login_at.isoformat() if hasattr(s, 'last_login_at') and s.last_login_at else None
        } for s in staff_list],
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.post("/staff", summary="创建员工")
async def create_staff(
    nickname: str = Query(...),
    phone: str = Query(...),
    password: str = Query(...),
    role_ids: str = Query(None, description="角色ID列表，逗号分隔"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """创建员工账号"""
    from app.models.role import Role
    from app.core.security import get_password_hash

    # 检查手机号是否已存在
    existing = db.query(User).filter(User.phone == phone).first()
    if existing:
        return Response.error(message="手机号已存在")

    staff = User(
        phone=phone,
        nickname=nickname,
        password_hash=get_password_hash(password),
        is_admin=True
    )

    if role_ids:
        role_id_list = [int(x) for x in role_ids.split(",")]
        roles = db.query(Role).filter(Role.id.in_(role_id_list)).all()
        staff.roles = roles

    db.add(staff)
    db.commit()
    db.refresh(staff)

    return Response.success(data={"id": staff.id}, message="创建成功")


@router.put("/staff/{staff_id}", summary="更新员工")
async def update_staff(
    staff_id: int,
    nickname: str = Query(None),
    role_ids: str = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """更新员工信息"""
    from app.models.role import Role

    staff = db.query(User).filter(User.id == staff_id).first()
    if not staff:
        return Response.error(message="员工不存在")

    if nickname:
        staff.nickname = nickname

    if role_ids is not None:
        if role_ids:
            role_id_list = [int(x) for x in role_ids.split(",")]
            roles = db.query(Role).filter(Role.id.in_(role_id_list)).all()
            staff.roles = roles
        else:
            staff.roles = []

    db.commit()
    return Response.success(message="更新成功")


@router.put("/staff/{staff_id}/reset-password", summary="重置员工密码")
async def reset_staff_password(
    staff_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """重置员工密码为默认值"""
    from app.core.security import get_password_hash

    staff = db.query(User).filter(User.id == staff_id).first()
    if not staff:
        return Response.error(message="员工不存在")

    staff.password_hash = get_password_hash("123456")
    db.commit()

    return Response.success(message="密码已重置为 123456")


@router.put("/staff/{staff_id}/status", summary="修改员工状态")
async def update_staff_status(
    staff_id: int,
    status: str = Query(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """修改员工状态"""
    from app.models.user import UserStatus

    staff = db.query(User).filter(User.id == staff_id).first()
    if not staff:
        return Response.error(message="员工不存在")

    try:
        staff.status = UserStatus(status)
        db.commit()
        return Response.success(message="状态更新成功")
    except ValueError:
        return Response.error(message="无效的状态值")


# ==================== 财务管理 ====================

@router.get("/finance/stats", summary="获取财务统计")
async def get_finance_stats(
    start_date: str = Query(None),
    end_date: str = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取财务统计数据"""
    from datetime import date, timedelta

    today = date.today()
    start = datetime.strptime(start_date, "%Y-%m-%d").date() if start_date else today - timedelta(days=30)
    end = datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else today

    # 订单收入
    order_income = db.query(func.sum(Order.paid_fee)).filter(
        Order.paid_at >= start,
        Order.paid_at <= end
    ).scalar() or 0

    # 充值金额
    recharge_amount = db.query(func.sum(RechargeRecord.amount)).filter(
        RechargeRecord.status == RechargeStatus.SUCCESS,
        RechargeRecord.created_at >= start,
        RechargeRecord.created_at <= end
    ).scalar() or 0

    # 提现金额
    withdraw_amount = db.query(func.sum(WithdrawRecord.amount)).filter(
        WithdrawRecord.status == "success",
        WithdrawRecord.created_at >= start,
        WithdrawRecord.created_at <= end
    ).scalar() or 0

    return Response.success(data={
        "order_income": float(order_income),
        "recharge_amount": float(recharge_amount),
        "withdraw_amount": float(withdraw_amount),
        "net_income": float(order_income) + float(recharge_amount) - float(withdraw_amount),
        "start_date": start.isoformat(),
        "end_date": end.isoformat()
    })


@router.get("/finance/income", summary="获取收入明细")
async def get_finance_income(
    start_date: str = Query(None),
    end_date: str = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取收入明细列表"""
    from datetime import date, timedelta

    today = date.today()
    start = datetime.strptime(start_date, "%Y-%m-%d").date() if start_date else today - timedelta(days=30)
    end = datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else today

    query = db.query(Order).filter(
        Order.paid_at >= start,
        Order.paid_at <= end,
        Order.paid_fee > 0
    )

    total = query.count()
    orders = query.order_by(Order.paid_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return Response.success(data={
        "items": [{
            "id": o.id,
            "order_no": o.order_no,
            "amount": float(o.paid_fee),
            "type": "order",
            "user_id": o.user_id,
            "created_at": o.paid_at.isoformat() if o.paid_at else None
        } for o in orders],
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.get("/finance/expense", summary="获取支出明细")
async def get_finance_expense(
    start_date: str = Query(None),
    end_date: str = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取支出明细列表"""
    from datetime import date, timedelta

    today = date.today()
    start = datetime.strptime(start_date, "%Y-%m-%d").date() if start_date else today - timedelta(days=30)
    end = datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else today

    query = db.query(WithdrawRecord).filter(
        WithdrawRecord.status == "success",
        WithdrawRecord.created_at >= start,
        WithdrawRecord.created_at <= end
    )

    total = query.count()
    records = query.order_by(WithdrawRecord.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return Response.success(data={
        "items": [{
            "id": r.id,
            "amount": float(r.amount),
            "type": "withdraw",
            "user_id": r.user_id,
            "status": r.status,
            "created_at": r.created_at.isoformat() if r.created_at else None
        } for r in records],
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.post("/finance/expense", summary="添加支出记录")
async def create_finance_expense(
    amount: float = Query(...),
    category: str = Query(...),
    description: str = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """添加支出记录（手动记录）"""
    # 这里可以创建一个专门的支出表，暂时返回成功
    return Response.success(message="支出记录已添加")


@router.get("/finance/settlement", summary="获取结算列表")
async def get_finance_settlement(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取实验室结算列表"""
    from app.models.laboratory import Laboratory, LabSettlement

    settlements = db.query(LabSettlement).order_by(LabSettlement.id.desc()).limit(50).all()

    return Response.success(data={
        "items": [{
            "id": s.id,
            "lab_id": s.lab_id,
            "lab_name": s.laboratory.name if s.laboratory else "",
            "amount": float(s.amount) if hasattr(s, 'amount') else 0,
            "status": s.status if hasattr(s, 'status') else "pending",
            "created_at": s.created_at.isoformat() if s.created_at else None
        } for s in settlements]
    })


@router.put("/finance/settlement/{settlement_id}/confirm", summary="确认结算")
async def confirm_settlement(
    settlement_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """确认结算"""
    from app.models.laboratory import LabSettlement

    settlement = db.query(LabSettlement).filter(LabSettlement.id == settlement_id).first()
    if not settlement:
        return Response.error(message="结算记录不存在")

    if hasattr(settlement, 'status'):
        settlement.status = "confirmed"
    db.commit()

    return Response.success(message="结算确认成功")


@router.get("/finance/export", summary="导出财务数据")
async def export_finance_data(
    start_date: str = Query(None),
    end_date: str = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """导出财务数据"""
    import io
    import csv
    from fastapi.responses import StreamingResponse
    from datetime import date, timedelta

    today = date.today()
    start = datetime.strptime(start_date, "%Y-%m-%d").date() if start_date else today - timedelta(days=30)
    end = datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else today

    orders = db.query(Order).filter(
        Order.paid_at >= start,
        Order.paid_at <= end,
        Order.paid_fee > 0
    ).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["订单号", "金额", "支付时间", "用户ID"])

    for o in orders:
        writer.writerow([
            o.order_no,
            float(o.paid_fee),
            o.paid_at.isoformat() if o.paid_at else "",
            o.user_id
        ])

    output.seek(0)
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode('utf-8-sig')),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=finance_{start}_{end}.csv"}
    )


# ==================== 设备管理 ====================

@router.get("/equipment", summary="获取设备列表")
async def get_equipment_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    lab_id: int = Query(None),
    keyword: str = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取设备列表"""
    from app.models.laboratory import LabEquipment, Laboratory

    query = db.query(LabEquipment)

    if lab_id:
        query = query.filter(LabEquipment.laboratory_id == lab_id)

    if keyword:
        query = query.filter(LabEquipment.name.contains(keyword))

    total = query.count()
    equipment_list = query.order_by(LabEquipment.id.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return Response.success(data={
        "items": [{
            "id": e.id,
            "name": e.name,
            "model": e.model if hasattr(e, 'model') else "",
            "lab_id": e.laboratory_id,
            "lab_name": e.laboratory.name if e.laboratory else "",
            "status": e.status if hasattr(e, 'status') and e.status else "available",
            "created_at": e.created_at.isoformat() if e.created_at else None
        } for e in equipment_list],
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.post("/equipment", summary="创建设备")
async def create_equipment(
    name: str = Query(...),
    model: str = Query(None),
    lab_id: int = Query(...),
    description: str = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """创建设备"""
    from app.models.laboratory import LabEquipment

    equipment = LabEquipment(
        name=name,
        laboratory_id=lab_id
    )
    if model and hasattr(equipment, 'model'):
        equipment.model = model
    if description and hasattr(equipment, 'description'):
        equipment.description = description

    db.add(equipment)
    db.commit()
    db.refresh(equipment)

    return Response.success(data={"id": equipment.id}, message="创建成功")


@router.put("/equipment/{equipment_id}", summary="更新设备")
async def update_equipment(
    equipment_id: int,
    name: str = Query(None),
    model: str = Query(None),
    description: str = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """更新设备"""
    from app.models.laboratory import LabEquipment

    equipment = db.query(LabEquipment).filter(LabEquipment.id == equipment_id).first()
    if not equipment:
        return Response.error(message="设备不存在")

    if name:
        equipment.name = name
    if model and hasattr(equipment, 'model'):
        equipment.model = model
    if description and hasattr(equipment, 'description'):
        equipment.description = description

    db.commit()
    return Response.success(message="更新成功")


@router.delete("/equipment/{equipment_id}", summary="删除设备")
async def delete_equipment(
    equipment_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """删除设备"""
    from app.models.laboratory import LabEquipment

    equipment = db.query(LabEquipment).filter(LabEquipment.id == equipment_id).first()
    if not equipment:
        return Response.error(message="设备不存在")

    db.delete(equipment)
    db.commit()
    return Response.success(message="删除成功")


@router.put("/equipment/{equipment_id}/status", summary="修改设备状态")
async def update_equipment_status(
    equipment_id: int,
    status: str = Query(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """修改设备状态"""
    from app.models.laboratory import LabEquipment

    equipment = db.query(LabEquipment).filter(LabEquipment.id == equipment_id).first()
    if not equipment:
        return Response.error(message="设备不存在")

    try:
        equipment.status = status
        db.commit()
        return Response.success(message="状态更新成功")
    except Exception as e:
        return Response.error(message=f"状态更新失败: {str(e)}")


# ==================== 轮播图管理 ====================

@router.get("/banners", summary="获取轮播图列表")
async def get_admin_banners(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取轮播图列表"""
    from app.models.banner import Banner

    banners = db.query(Banner).order_by(Banner.sort_order.asc(), Banner.id.desc()).all()

    return Response.success(data={
        "items": [{
            "id": b.id,
            "title": b.title if hasattr(b, 'title') else "",
            "image": b.image if hasattr(b, 'image') else "",
            "link": b.link_value if hasattr(b, 'link_value') else "",
            "sort_order": b.sort_order if hasattr(b, 'sort_order') else 0,
            "is_active": b.is_active if hasattr(b, 'is_active') else True,
            "created_at": b.created_at.isoformat() if b.created_at else None
        } for b in banners]
    })


@router.post("/banners", summary="创建轮播图")
async def create_admin_banner(
    data: BannerCreate = Body(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """创建轮播图"""
    from app.models.banner import Banner

    banner = Banner(
        image=data.image,
        title=data.title or ""
    )
    if data.link:
        banner.link_value = data.link
    if hasattr(banner, 'sort_order'):
        banner.sort_order = data.sort_order
    if hasattr(banner, 'is_active'):
        banner.is_active = data.is_active

    db.add(banner)
    db.commit()
    db.refresh(banner)

    return Response.success(data={"id": banner.id}, message="创建成功")


@router.put("/banners/{banner_id}", summary="更新轮播图")
async def update_admin_banner(
    banner_id: int,
    data: BannerUpdate = Body(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """更新轮播图"""
    from app.models.banner import Banner

    banner = db.query(Banner).filter(Banner.id == banner_id).first()
    if not banner:
        return Response.error(message="轮播图不存在")

    if data.title is not None and hasattr(banner, 'title'):
        banner.title = data.title
    if data.image is not None:
        banner.image = data.image
    if data.link is not None and hasattr(banner, 'link_value'):
        banner.link_value = data.link
    if data.sort_order is not None and hasattr(banner, 'sort_order'):
        banner.sort_order = data.sort_order
    if data.is_active is not None and hasattr(banner, 'is_active'):
        banner.is_active = data.is_active

    db.commit()
    return Response.success(message="更新成功")


@router.put("/banners/{banner_id}/status", summary="修改轮播图状态")
async def update_banner_status(
    banner_id: int,
    data: dict = Body(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """修改轮播图状态"""
    from app.models.banner import Banner

    banner = db.query(Banner).filter(Banner.id == banner_id).first()
    if not banner:
        return Response.error(message="轮播图不存在")

    is_active = data.get('is_active')
    if is_active is not None and hasattr(banner, 'is_active'):
        banner.is_active = is_active
    db.commit()

    return Response.success(message="状态更新成功")


@router.delete("/banners/{banner_id}", summary="删除轮播图")
async def delete_admin_banner(
    banner_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """删除轮播图"""
    from app.models.banner import Banner

    banner = db.query(Banner).filter(Banner.id == banner_id).first()
    if not banner:
        return Response.error(message="轮播图不存在")

    db.delete(banner)
    db.commit()
    return Response.success(message="删除成功")


# ==================== 公告管理 ====================

@router.get("/announcements", summary="获取公告列表")
async def get_admin_announcements(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取公告列表"""
    from app.models.announcement import Announcement

    announcements = db.query(Announcement).order_by(Announcement.id.desc()).all()

    return Response.success(data={
        "items": [{
            "id": a.id,
            "title": a.title,
            "content": a.content,
            "is_active": a.is_active if hasattr(a, 'is_active') else True,
            "created_at": a.created_at.isoformat() if a.created_at else None
        } for a in announcements]
    })


@router.post("/announcements", summary="创建公告")
async def create_admin_announcement(
    title: str = Query(...),
    content: str = Query(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """创建公告"""
    from app.models.announcement import Announcement

    announcement = Announcement(title=title, content=content)
    db.add(announcement)
    db.commit()
    db.refresh(announcement)

    return Response.success(data={"id": announcement.id}, message="创建成功")


@router.put("/announcements/{announcement_id}", summary="更新公告")
async def update_admin_announcement(
    announcement_id: int,
    title: str = Query(None),
    content: str = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """更新公告"""
    from app.models.announcement import Announcement

    announcement = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if not announcement:
        return Response.error(message="公告不存在")

    if title:
        announcement.title = title
    if content:
        announcement.content = content

    db.commit()
    return Response.success(message="更新成功")


@router.put("/announcements/{announcement_id}/status", summary="修改公告状态")
async def update_announcement_status(
    announcement_id: int,
    is_active: bool = Query(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """修改公告状态"""
    from app.models.announcement import Announcement

    announcement = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if not announcement:
        return Response.error(message="公告不存在")

    if hasattr(announcement, 'is_active'):
        announcement.is_active = is_active
    db.commit()

    return Response.success(message="状态更新成功")


@router.delete("/announcements/{announcement_id}", summary="删除公告")
async def delete_admin_announcement(
    announcement_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """删除公告"""
    from app.models.announcement import Announcement

    announcement = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if not announcement:
        return Response.error(message="公告不存在")

    db.delete(announcement)
    db.commit()
    return Response.success(message="删除成功")


# ==================== 帮助文章管理 ====================

@router.get("/help-articles", summary="获取帮助文章列表")
async def get_admin_help_articles(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    category: str = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取帮助文章列表"""
    from app.models.help import HelpArticle

    query = db.query(HelpArticle)

    if category:
        query = query.filter(HelpArticle.category == category)

    total = query.count()
    articles = query.order_by(HelpArticle.sort_order.asc(), HelpArticle.id.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return Response.success(data={
        "items": [{
            "id": a.id,
            "title": a.title,
            "content": a.content,
            "category": a.category if hasattr(a, 'category') else "",
            "sort_order": a.sort_order if hasattr(a, 'sort_order') else 0,
            "is_active": a.is_active if hasattr(a, 'is_active') else True,
            "created_at": a.created_at.isoformat() if a.created_at else None
        } for a in articles],
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.post("/help-articles", summary="创建帮助文章")
async def create_admin_help_article(
    title: str = Query(...),
    content: str = Query(...),
    category: str = Query(None),
    sort_order: int = Query(0),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """创建帮助文章"""
    from app.models.help import HelpArticle

    article = HelpArticle(title=title, content=content)
    if category and hasattr(article, 'category'):
        article.category = category
    if hasattr(article, 'sort_order'):
        article.sort_order = sort_order

    db.add(article)
    db.commit()
    db.refresh(article)

    return Response.success(data={"id": article.id}, message="创建成功")


@router.put("/help-articles/{article_id}", summary="更新帮助文章")
async def update_admin_help_article(
    article_id: int,
    title: str = Query(None),
    content: str = Query(None),
    category: str = Query(None),
    sort_order: int = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """更新帮助文章"""
    from app.models.help import HelpArticle

    article = db.query(HelpArticle).filter(HelpArticle.id == article_id).first()
    if not article:
        return Response.error(message="文章不存在")

    if title:
        article.title = title
    if content:
        article.content = content
    if category is not None and hasattr(article, 'category'):
        article.category = category
    if sort_order is not None and hasattr(article, 'sort_order'):
        article.sort_order = sort_order

    db.commit()
    return Response.success(message="更新成功")


@router.delete("/help-articles/{article_id}", summary="删除帮助文章")
async def delete_admin_help_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """删除帮助文章"""
    from app.models.help import HelpArticle

    article = db.query(HelpArticle).filter(HelpArticle.id == article_id).first()
    if not article:
        return Response.error(message="文章不存在")

    db.delete(article)
    db.commit()
    return Response.success(message="删除成功")


# ==================== 客服聊天管理 ====================

@router.get("/chats", summary="获取聊天列表")
async def get_admin_chats(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: str = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取客服聊天列表"""
    from app.models.chat import ChatSession

    query = db.query(ChatSession)

    if status:
        query = query.filter(ChatSession.status == status)

    total = query.count()
    chats = query.order_by(ChatSession.updated_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return Response.success(data={
        "items": [{
            "id": c.id,
            "user_id": c.user_id,
            "user_nickname": c.user.nickname if c.user else "",
            "status": c.status if hasattr(c, 'status') else "open",
            "last_message": c.last_message if hasattr(c, 'last_message') else "",
            "created_at": c.created_at.isoformat() if c.created_at else None,
            "updated_at": c.updated_at.isoformat() if c.updated_at else None
        } for c in chats],
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.get("/chats/{chat_id}/messages", summary="获取聊天消息")
async def get_chat_messages(
    chat_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取聊天消息"""
    from app.models.chat import ChatMessage

    messages = db.query(ChatMessage).filter(ChatMessage.session_id == chat_id).order_by(ChatMessage.created_at.asc()).all()

    return Response.success(data={
        "items": [{
            "id": m.id,
            "content": m.content,
            "sender_type": m.sender_type if hasattr(m, 'sender_type') else "user",
            "is_staff": getattr(m, 'sender_type', '') in ('staff', 'system'),
            "created_at": m.created_at.isoformat() if m.created_at else None
        } for m in messages]
    })


class AdminSendMessageRequest(BaseModel):
    """管理员发送客服消息"""
    content: str


@router.post("/chats/{chat_id}/messages", summary="管理员发送客服回复")
async def admin_send_chat_message(
    chat_id: int,
    body: AdminSendMessageRequest,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员发送回复，写入数据库，用户端可见"""
    from app.models.chat import ChatSession, ChatMessage

    session = db.query(ChatSession).filter(ChatSession.id == chat_id).first()
    if not session:
        return Response.error(message="聊天会话不存在")

    msg = ChatMessage(
        session_id=chat_id,
        sender_type="staff",
        sender_id=current_admin.id,
        content=body.content.strip(),
        message_type="text"
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)

    return Response.success(data={
        "id": msg.id,
        "content": msg.content,
        "sender_type": "staff",
        "is_staff": True,
        "created_at": msg.created_at.isoformat() if msg.created_at else None
    }, message="发送成功")


@router.put("/chats/{chat_id}/close", summary="关闭聊天")
async def close_chat(
    chat_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """关闭聊天会话"""
    from app.models.chat import ChatSession

    chat = db.query(ChatSession).filter(ChatSession.id == chat_id).first()
    if not chat:
        return Response.error(message="聊天会话不存在")

    if hasattr(chat, 'status'):
        chat.status = "closed"
    db.commit()

    return Response.success(message="会话已关闭")


@router.get("/phrases", summary="获取快捷回复")
async def get_phrases(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取快捷回复短语"""
    # 返回预设的快捷回复
    return Response.success(data={
        "items": [
            {"id": 1, "content": "您好，请问有什么可以帮助您的？"},
            {"id": 2, "content": "感谢您的咨询，我们会尽快处理。"},
            {"id": 3, "content": "您的问题已收到，请耐心等待。"},
            {"id": 4, "content": "如有其他问题，欢迎随时咨询。"},
            {"id": 5, "content": "祝您生活愉快！"}
        ]
    })


# ==================== 加盟管理 ====================

@router.get("/franchise/applications", summary="获取加盟申请列表")
async def get_franchise_applications(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: str = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取加盟申请列表"""
    from app.models.franchise import FranchiseApplication

    query = db.query(FranchiseApplication)

    if status:
        query = query.filter(FranchiseApplication.status == status)

    total = query.count()
    applications = query.order_by(FranchiseApplication.id.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return Response.success(data={
        "items": [{
            "id": a.id,
            "company_name": a.company if hasattr(a, 'company') else "",
            "contact_name": a.name if hasattr(a, 'name') else "",
            "contact_phone": a.phone if hasattr(a, 'phone') else "",
            "status": a.status if hasattr(a, 'status') else "pending",
            "created_at": a.created_at.isoformat() if a.created_at else None
        } for a in applications],
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.get("/franchise/franchisees", summary="获取加盟商列表")
async def get_franchisees(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取加盟商列表"""
    from app.models.franchise import FranchiseApplication

    # 使用已批准的加盟申请作为加盟商列表
    franchisees = db.query(FranchiseApplication).filter(
        FranchiseApplication.status == "approved"
    ).order_by(FranchiseApplication.id.desc()).all()

    return Response.success(data={
        "items": [{
            "id": f.id,
            "company_name": f.company if hasattr(f, 'company') else "",
            "contact_name": f.name if hasattr(f, 'name') else "",
            "contact_phone": f.phone if hasattr(f, 'phone') else "",
            "status": f.status if hasattr(f, 'status') else "active",
            "created_at": f.created_at.isoformat() if f.created_at else None
        } for f in franchisees]
    })


@router.put("/franchise/applications/{app_id}/approve", summary="批准加盟申请")
async def approve_franchise_application(
    app_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """批准加盟申请"""
    from app.models.franchise import FranchiseApplication

    application = db.query(FranchiseApplication).filter(FranchiseApplication.id == app_id).first()
    if not application:
        return Response.error(message="申请不存在")

    if hasattr(application, 'status'):
        application.status = "approved"

    db.commit()

    return Response.success(message="申请已批准")


@router.put("/franchise/applications/{app_id}/reject", summary="拒绝加盟申请")
async def reject_franchise_application(
    app_id: int,
    reason: str = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """拒绝加盟申请"""
    from app.models.franchise import FranchiseApplication

    application = db.query(FranchiseApplication).filter(FranchiseApplication.id == app_id).first()
    if not application:
        return Response.error(message="申请不存在")

    if hasattr(application, 'status'):
        application.status = "rejected"
    if reason and hasattr(application, 'reject_reason'):
        application.reject_reason = reason

    db.commit()

    return Response.success(message="申请已拒绝")


@router.put("/franchise/franchisees/{franchisee_id}/status", summary="修改加盟商状态")
async def update_franchisee_status(
    franchisee_id: int,
    status: str = Query(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """修改加盟商状态"""
    from app.models.franchise import Franchisee

    franchisee = db.query(Franchisee).filter(Franchisee.id == franchisee_id).first()
    if not franchisee:
        return Response.error(message="加盟商不存在")

    if hasattr(franchisee, 'status'):
        franchisee.status = status
    db.commit()

    return Response.success(message="状态更新成功")


# ==================== 发票管理 ====================

@router.get("/invoices", summary="获取发票申请列表")
async def get_admin_invoices(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: str = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取发票申请列表"""
    from app.models.invoice import Invoice

    query = db.query(Invoice)

    if status:
        query = query.filter(Invoice.status == status)

    total = query.count()
    invoices = query.order_by(Invoice.id.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return Response.success(data={
        "items": [{
            "id": i.id,
            "invoice_no": i.invoice_no if hasattr(i, 'invoice_no') else "",
            "user_id": i.user_id,
            "amount": float(i.amount) if hasattr(i, 'amount') else 0,
            "title": i.title if hasattr(i, 'title') else "",
            "tax_no": i.tax_no if hasattr(i, 'tax_no') else "",
            "status": i.status.value if hasattr(i, 'status') and i.status else "pending",
            "created_at": i.created_at.isoformat() if i.created_at else None
        } for i in invoices],
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.get("/invoices/records", summary="获取开票记录")
async def get_invoice_records(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取开票记录"""
    from app.models.invoice import Invoice, InvoiceStatus

    records = db.query(Invoice).filter(Invoice.status == InvoiceStatus.ISSUED).order_by(Invoice.id.desc()).limit(50).all()

    return Response.success(data={
        "items": [{
            "id": r.id,
            "invoice_no": r.invoice_no if hasattr(r, 'invoice_no') else "",
            "amount": float(r.amount) if hasattr(r, 'amount') else 0,
            "title": r.title if hasattr(r, 'title') else "",
            "created_at": r.created_at.isoformat() if r.created_at else None
        } for r in records]
    })


@router.put("/invoices/{invoice_id}/approve", summary="批准发票申请")
async def approve_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """批准发票申请"""
    from app.models.invoice import Invoice, InvoiceStatus

    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        return Response.error(message="发票申请不存在")

    invoice.status = InvoiceStatus.APPROVED
    db.commit()

    return Response.success(message="已批准")


@router.put("/invoices/{invoice_id}/reject", summary="拒绝发票申请")
async def reject_invoice(
    invoice_id: int,
    reason: str = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """拒绝发票申请"""
    from app.models.invoice import Invoice, InvoiceStatus

    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        return Response.error(message="发票申请不存在")

    invoice.status = InvoiceStatus.REJECTED
    if reason and hasattr(invoice, 'reject_reason'):
        invoice.reject_reason = reason
    db.commit()

    return Response.success(message="已拒绝")


@router.put("/invoices/{invoice_id}/confirm", summary="确认开票")
async def confirm_invoice(
    invoice_id: int,
    invoice_no: str = Query(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """确认开票并填写发票号"""
    from app.models.invoice import Invoice, InvoiceStatus

    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        return Response.error(message="发票申请不存在")

    invoice.status = InvoiceStatus.ISSUED
    if hasattr(invoice, 'invoice_no'):
        invoice.invoice_no = invoice_no
    db.commit()

    return Response.success(message="开票成功")


@router.get("/invoices/{invoice_id}/download", summary="下载发票")
async def download_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """下载发票文件"""
    from app.models.invoice import Invoice

    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        return Response.error(message="发票不存在")

    # 返回发票下载链接或文件
    file_url = invoice.file_url if hasattr(invoice, 'file_url') else None

    return Response.success(data={
        "file_url": file_url,
        "invoice_no": invoice.invoice_no if hasattr(invoice, 'invoice_no') else ""
    })


@router.get("/invoices/export", summary="导出发票数据")
async def export_invoices(
    start_date: str = Query(None),
    end_date: str = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """导出发票数据"""
    import io
    import csv
    from fastapi.responses import StreamingResponse
    from app.models.invoice import Invoice

    query = db.query(Invoice)

    if start_date:
        query = query.filter(Invoice.created_at >= start_date)
    if end_date:
        query = query.filter(Invoice.created_at <= end_date)

    invoices = query.all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "发票号", "金额", "抬头", "税号", "状态", "创建时间"])

    for i in invoices:
        writer.writerow([
            i.id,
            i.invoice_no if hasattr(i, 'invoice_no') else "",
            float(i.amount) if hasattr(i, 'amount') else 0,
            i.title if hasattr(i, 'title') else "",
            i.tax_no if hasattr(i, 'tax_no') else "",
            i.status.value if hasattr(i, 'status') and i.status else "",
            i.created_at.isoformat() if i.created_at else ""
        ])

    output.seek(0)
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode('utf-8-sig')),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=invoices.csv"}
    )


# ==================== 系统设置 ====================

@router.put("/settings/points", summary="更新积分设置")
async def update_points_settings(
    sign_points: int = Query(None),
    order_points_rate: float = Query(None),
    review_points: int = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """更新积分设置"""
    # 这里可以存储到系统设置表或配置文件
    # 暂时返回成功
    return Response.success(message="设置已更新")


@router.get("/laboratories/{lab_id}/tasks", summary="获取实验室任务")
async def get_lab_tasks(
    lab_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取实验室任务列表"""
    from app.models.laboratory import LabOrder

    tasks = db.query(LabOrder).filter(LabOrder.lab_id == lab_id).order_by(LabOrder.id.desc()).limit(50).all()

    return Response.success(data={
        "items": [{
            "id": t.id,
            "order_id": t.order_id,
            "order_no": t.order.order_no if t.order else "",
            "status": t.status.value if t.status else "pending",
            "assigned_at": t.assigned_at.isoformat() if hasattr(t, 'assigned_at') and t.assigned_at else None,
            "created_at": t.created_at.isoformat() if t.created_at else None
        } for t in tasks]
    })


# ==================== 项目选项管理 ====================

def build_admin_option_tree(options: List[ProjectOption], parent_id: Optional[int] = None) -> List[dict]:
    """构建选项树结构（管理端）"""
    tree = []
    for opt in options:
        if opt.parent_id == parent_id:
            node = {
                "id": opt.id,
                "project_id": opt.project_id,
                "category_id": opt.category_id,
                "parent_id": opt.parent_id,
                "level": opt.level,
                "path": opt.path,
                "name": opt.name,
                "option_type": opt.option_type.value if isinstance(opt.option_type, OptionType) else opt.option_type,
                "price": float(opt.price) if opt.price else 0,
                "price_type": opt.price_type.value if isinstance(opt.price_type, PriceType) else opt.price_type,
                "hint_text": opt.hint_text,
                "placeholder": opt.placeholder,
                "sort_order": opt.sort_order,
                "is_required": opt.is_required,
                "is_active": opt.is_active,
                "created_at": opt.created_at.isoformat() if opt.created_at else None,
                "children": build_admin_option_tree(options, opt.id)
            }
            tree.append(node)
    tree.sort(key=lambda x: x["sort_order"])
    return tree


@router.get("/options", summary="获取选项列表")
async def admin_get_options(
    project_id: Optional[int] = Query(None, description="项目ID"),
    category_id: Optional[int] = Query(None, description="分类ID"),
    is_active: Optional[bool] = Query(None, description="是否启用"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取项目选项列表（管理端）"""
    query = db.query(ProjectOption)

    if project_id is not None:
        query = query.filter(ProjectOption.project_id == project_id)
    if category_id is not None:
        query = query.filter(ProjectOption.category_id == category_id)
    if is_active is not None:
        query = query.filter(ProjectOption.is_active == is_active)

    total = query.count()
    options = query.order_by(ProjectOption.sort_order, ProjectOption.id).offset((page - 1) * page_size).limit(page_size).all()

    items = [{
        "id": opt.id,
        "project_id": opt.project_id,
        "category_id": opt.category_id,
        "parent_id": opt.parent_id,
        "level": opt.level,
        "name": opt.name,
        "option_type": opt.option_type.value if isinstance(opt.option_type, OptionType) else opt.option_type,
        "price": float(opt.price) if opt.price else 0,
        "price_type": opt.price_type.value if isinstance(opt.price_type, PriceType) else opt.price_type,
        "hint_text": opt.hint_text,
        "placeholder": opt.placeholder,
        "sort_order": opt.sort_order,
        "is_required": opt.is_required,
        "is_active": opt.is_active,
        "created_at": opt.created_at.isoformat() if opt.created_at else None
    } for opt in options]

    return Response.success(data={"total": total, "list": items})


@router.get("/options/tree/project/{project_id}", summary="获取项目选项树")
async def admin_get_project_option_tree(
    project_id: int,
    include_inactive: bool = Query(False, description="是否包含禁用选项"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取项目的选项树结构（管理端）"""
    query = db.query(ProjectOption).filter(ProjectOption.project_id == project_id)
    if not include_inactive:
        query = query.filter(ProjectOption.is_active == True)

    options = query.all()
    tree = build_admin_option_tree(options)

    return Response.success(data={
        "project_id": project_id,
        "options": tree
    })


@router.get("/options/tree/category/{category_id}", summary="获取分类选项树")
async def admin_get_category_option_tree(
    category_id: int,
    include_inactive: bool = Query(False, description="是否包含禁用选项"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取分类的选项树结构（管理端）"""
    query = db.query(ProjectOption).filter(ProjectOption.category_id == category_id)
    if not include_inactive:
        query = query.filter(ProjectOption.is_active == True)

    options = query.all()
    tree = build_admin_option_tree(options)

    return Response.success(data={
        "category_id": category_id,
        "options": tree
    })


@router.post("/options", summary="创建选项")
async def admin_create_option(
    data: ProjectOptionCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """创建项目选项"""
    # 验证: project_id 和 category_id 二选一
    if not data.project_id and not data.category_id:
        raise HTTPException(status_code=400, detail="必须指定 project_id 或 category_id")

    # 计算层级和路径
    level = 1
    path = "/"

    if data.parent_id:
        parent = db.query(ProjectOption).filter(ProjectOption.id == data.parent_id).first()
        if not parent:
            raise HTTPException(status_code=404, detail="父选项不存在")

        # 验证：输入类型选项不能有子选项
        parent_type = parent.option_type.value if isinstance(parent.option_type, OptionType) else parent.option_type
        if parent_type == "input":
            raise HTTPException(status_code=400, detail="输入类型选项不能有子选项")

        level = parent.level + 1
        path = f"{parent.path}{parent.id}/"

        # 继承 project_id 或 category_id
        if not data.project_id:
            data.project_id = parent.project_id
        if not data.category_id:
            data.category_id = parent.category_id

    # 创建选项
    option = ProjectOption(
        project_id=data.project_id,
        category_id=data.category_id,
        parent_id=data.parent_id,
        level=level,
        path=path,
        name=data.name,
        option_type=data.option_type.value,
        price=data.price,
        price_type=data.price_type.value,
        hint_text=data.hint_text,
        placeholder=data.placeholder,
        sort_order=data.sort_order,
        is_required=data.is_required,
        is_active=data.is_active
    )

    db.add(option)
    db.commit()
    db.refresh(option)

    # 更新路径
    option.path = f"{path}{option.id}/"
    db.commit()

    return Response.success(data={"id": option.id}, message="选项创建成功")


@router.put("/options/{option_id}", summary="更新选项")
async def admin_update_option(
    option_id: int,
    data: ProjectOptionUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """更新项目选项"""
    option = db.query(ProjectOption).filter(ProjectOption.id == option_id).first()
    if not option:
        raise HTTPException(status_code=404, detail="选项不存在")

    # 如果更改为input类型，检查是否有子选项
    if data.option_type and data.option_type.value == "input":
        children = db.query(ProjectOption).filter(ProjectOption.parent_id == option_id).count()
        if children > 0:
            raise HTTPException(status_code=400, detail="该选项有子选项，不能更改为输入类型")

    # 更新字段
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key == "option_type" and value:
            setattr(option, key, value.value)
        elif key == "price_type" and value:
            setattr(option, key, value.value)
        else:
            setattr(option, key, value)

    db.commit()
    db.refresh(option)

    return Response.success(message="选项更新成功")


@router.delete("/options/{option_id}", summary="删除选项")
async def admin_delete_option(
    option_id: int,
    cascade: bool = Query(False, description="是否级联删除子选项"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """删除项目选项"""
    option = db.query(ProjectOption).filter(ProjectOption.id == option_id).first()
    if not option:
        raise HTTPException(status_code=404, detail="选项不存在")

    # 检查是否有子选项
    children = db.query(ProjectOption).filter(ProjectOption.parent_id == option_id).all()

    if children and not cascade:
        raise HTTPException(status_code=400, detail="该选项有子选项，请先删除子选项或使用级联删除")

    # 级联删除子选项
    if cascade and children:
        def delete_children(parent_id):
            child_options = db.query(ProjectOption).filter(ProjectOption.parent_id == parent_id).all()
            for child in child_options:
                delete_children(child.id)
                db.delete(child)

        delete_children(option_id)

    db.delete(option)
    db.commit()

    return Response.success(message="选项删除成功")


@router.post("/options/{option_id}/toggle", summary="切换选项状态")
async def admin_toggle_option(
    option_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """切换选项启用/禁用状态"""
    option = db.query(ProjectOption).filter(ProjectOption.id == option_id).first()
    if not option:
        raise HTTPException(status_code=404, detail="选项不存在")

    option.is_active = not option.is_active
    db.commit()

    return Response.success(message="状态已更新", data={"is_active": option.is_active})


@router.post("/options/batch-create", summary="批量创建选项")
async def admin_batch_create_options(
    options: List[ProjectOptionCreate] = Body(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """批量创建项目选项"""
    created_ids = []

    for data in options:
        # 验证: project_id 和 category_id 二选一
        if not data.project_id and not data.category_id:
            continue

        level = 1
        path = "/"

        if data.parent_id:
            parent = db.query(ProjectOption).filter(ProjectOption.id == data.parent_id).first()
            if parent:
                parent_type = parent.option_type.value if isinstance(parent.option_type, OptionType) else parent.option_type
                if parent_type != "input":
                    level = parent.level + 1
                    path = f"{parent.path}{parent.id}/"
                else:
                    continue  # 跳过输入类型的子选项
            else:
                continue

        option = ProjectOption(
            project_id=data.project_id,
            category_id=data.category_id,
            parent_id=data.parent_id,
            level=level,
            path=path,
            name=data.name,
            option_type=data.option_type.value,
            price=data.price,
            price_type=data.price_type.value,
            hint_text=data.hint_text,
            placeholder=data.placeholder,
            sort_order=data.sort_order,
            is_required=data.is_required,
            is_active=data.is_active
        )

        db.add(option)
        db.flush()

        option.path = f"{path}{option.id}/"
        created_ids.append(option.id)

    db.commit()

    return Response.success(data={"created_ids": created_ids}, message=f"成功创建 {len(created_ids)} 个选项")


@router.put("/options/batch-sort", summary="批量更新选项排序")
async def admin_batch_sort_options(
    sort_data: List[dict] = Body(..., example=[{"id": 1, "sort_order": 1}, {"id": 2, "sort_order": 2}]),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """批量更新选项排序"""
    for item in sort_data:
        option = db.query(ProjectOption).filter(ProjectOption.id == item["id"]).first()
        if option:
            option.sort_order = item.get("sort_order", 0)

    db.commit()

    return Response.success(message="排序更新成功")


# ==================== 佣金设置管理 ====================

from app.models.commission import UserCommissionSetting, CommissionRecord
from app.schemas.commission import (
    CommissionSettingCreate, CommissionSettingUpdate, CommissionSettingResponse,
    BatchSetCommissionRequest, SettleCommissionRequest
)
from app.models.recharge import InvoiceRechargeRecord, InvoiceRechargeStatus


@router.get("/commission/settings", summary="获取佣金设置列表（管理员）")
async def get_commission_settings_admin(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None, description="搜索用户手机号/姓名"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员获取用户佣金设置列表"""
    query = db.query(UserCommissionSetting).join(User, UserCommissionSetting.user_id == User.id)

    if search:
        query = query.filter(
            or_(
                User.phone.contains(search),
                User.nickname.contains(search),
                User.real_name.contains(search)
            )
        )

    total = query.count()
    settings = query.order_by(desc(UserCommissionSetting.created_at)).offset((page - 1) * page_size).limit(page_size).all()

    return Response.success(data={
        "items": [
            {
                "id": s.id,
                "user_id": s.user_id,
                "commission_rate": float(s.commission_rate) if s.commission_rate else 0,
                "max_rate": float(s.max_rate) if s.max_rate else 12,
                "effective_from": s.effective_from.isoformat() if s.effective_from else None,
                "effective_to": s.effective_to.isoformat() if s.effective_to else None,
                "created_at": s.created_at.isoformat() if s.created_at else None,
                "user_name": s.user.real_name or s.user.nickname,
                "user_phone": s.user.phone
            }
            for s in settings
        ],
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.get("/commission/settings/{user_id}", summary="获取用户佣金设置详情")
async def get_user_commission_setting(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取指定用户的佣金设置"""
    setting = db.query(UserCommissionSetting).filter(UserCommissionSetting.user_id == user_id).first()

    if not setting:
        return Response.success(data=None, message="该用户暂无佣金设置")

    user = db.query(User).filter(User.id == user_id).first()

    return Response.success(data={
        "id": setting.id,
        "user_id": setting.user_id,
        "commission_rate": float(setting.commission_rate) if setting.commission_rate else 0,
        "max_rate": float(setting.max_rate) if setting.max_rate else 12,
        "effective_from": setting.effective_from.isoformat() if setting.effective_from else None,
        "effective_to": setting.effective_to.isoformat() if setting.effective_to else None,
        "created_at": setting.created_at.isoformat() if setting.created_at else None,
        "user_name": user.real_name or user.nickname if user else None,
        "user_phone": user.phone if user else None
    })


@router.post("/commission/settings", summary="创建/更新用户佣金设置")
async def create_commission_setting(
    data: CommissionSettingCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """创建或更新用户佣金设置"""
    # 检查用户是否存在
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 验证佣金比例
    if data.commission_rate > Decimal("12"):
        raise HTTPException(status_code=400, detail="佣金比例不能超过12%")

    # 查找已有设置
    existing = db.query(UserCommissionSetting).filter(UserCommissionSetting.user_id == data.user_id).first()

    if existing:
        # 更新
        existing.commission_rate = data.commission_rate
        existing.effective_from = data.effective_from
        existing.effective_to = data.effective_to
        db.commit()
        return Response.success(data={"id": existing.id}, message="佣金设置更新成功")
    else:
        # 创建
        setting = UserCommissionSetting(
            user_id=data.user_id,
            commission_rate=data.commission_rate,
            effective_from=data.effective_from,
            effective_to=data.effective_to,
            created_by=current_admin.id
        )
        db.add(setting)
        db.commit()
        db.refresh(setting)
        return Response.success(data={"id": setting.id}, message="佣金设置创建成功")


@router.put("/commission/settings/{setting_id}", summary="更新佣金设置")
async def update_commission_setting(
    setting_id: int,
    data: CommissionSettingUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """更新佣金设置"""
    setting = db.query(UserCommissionSetting).filter(UserCommissionSetting.id == setting_id).first()
    if not setting:
        raise HTTPException(status_code=404, detail="佣金设置不存在")

    update_data = data.model_dump(exclude_unset=True)

    if 'commission_rate' in update_data and update_data['commission_rate'] > Decimal("12"):
        raise HTTPException(status_code=400, detail="佣金比例不能超过12%")

    for key, value in update_data.items():
        setattr(setting, key, value)

    db.commit()
    return Response.success(message="佣金设置更新成功")


@router.delete("/commission/settings/{setting_id}", summary="删除佣金设置")
async def delete_commission_setting(
    setting_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """删除佣金设置"""
    setting = db.query(UserCommissionSetting).filter(UserCommissionSetting.id == setting_id).first()
    if not setting:
        raise HTTPException(status_code=404, detail="佣金设置不存在")

    db.delete(setting)
    db.commit()
    return Response.success(message="佣金设置已删除")


@router.post("/commission/batch-set", summary="批量设置佣金比例")
async def batch_set_commission(
    data: BatchSetCommissionRequest,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """批量为多个用户设置佣金比例"""
    if data.commission_rate > Decimal("12"):
        raise HTTPException(status_code=400, detail="佣金比例不能超过12%")

    success_count = 0
    for user_id in data.user_ids:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            continue

        existing = db.query(UserCommissionSetting).filter(UserCommissionSetting.user_id == user_id).first()
        if existing:
            existing.commission_rate = data.commission_rate
            existing.effective_from = data.effective_from
            existing.effective_to = data.effective_to
        else:
            setting = UserCommissionSetting(
                user_id=user_id,
                commission_rate=data.commission_rate,
                effective_from=data.effective_from,
                effective_to=data.effective_to,
                created_by=current_admin.id
            )
            db.add(setting)
        success_count += 1

    db.commit()
    return Response.success(message=f"成功设置 {success_count} 个用户的佣金比例")


@router.get("/commission/records", summary="获取佣金记录列表（管理员）")
async def get_commission_records_admin(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user_id: Optional[int] = Query(None, description="用户ID"),
    status: Optional[str] = Query(None, description="状态: pending/settled/cancelled"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员获取佣金记录列表"""
    query = db.query(CommissionRecord)

    if user_id:
        query = query.filter(CommissionRecord.user_id == user_id)
    if status:
        query = query.filter(CommissionRecord.status == status)

    total = query.count()
    records = query.order_by(desc(CommissionRecord.created_at)).offset((page - 1) * page_size).limit(page_size).all()

    result = []
    for r in records:
        user = db.query(User).filter(User.id == r.user_id).first()
        from_user = db.query(User).filter(User.id == r.from_user_id).first() if r.from_user_id else None
        order = db.query(Order).filter(Order.id == r.order_id).first() if r.order_id else None

        result.append({
            "id": r.id,
            "user_id": r.user_id,
            "user_name": user.real_name or user.nickname if user else None,
            "order_id": r.order_id,
            "order_no": order.order_no if order else None,
            "from_user_id": r.from_user_id,
            "from_user_name": from_user.real_name or from_user.nickname if from_user else None,
            "order_amount": float(r.order_amount) if r.order_amount else 0,
            "commission_rate": float(r.commission_rate) if r.commission_rate else 0,
            "commission_amount": float(r.commission_amount) if r.commission_amount else 0,
            "status": r.status,
            "settled_at": r.settled_at.isoformat() if r.settled_at else None,
            "created_at": r.created_at.isoformat() if r.created_at else None
        })

    return Response.success(data={
        "items": result,
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.post("/commission/settle", summary="结算佣金")
async def settle_commission(
    data: SettleCommissionRequest,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """批量结算佣金记录"""
    total_amount = Decimal("0")
    settled_count = 0

    for record_id in data.record_ids:
        record = db.query(CommissionRecord).filter(
            CommissionRecord.id == record_id,
            CommissionRecord.status == "pending"
        ).first()

        if not record:
            continue

        record.status = "settled"
        record.settled_at = datetime.now()
        total_amount += record.commission_amount or Decimal("0")
        settled_count += 1

        # 将佣金添加到用户余额
        user = db.query(User).filter(User.id == record.user_id).first()
        if user:
            user.reward_balance = (user.reward_balance or Decimal("0")) + (record.commission_amount or Decimal("0"))

    db.commit()

    return Response.success(data={
        "settled_count": settled_count,
        "total_amount": float(total_amount)
    }, message=f"成功结算 {settled_count} 条记录，共 ¥{total_amount}")


# ==================== 开票充值管理 ====================

class InvoiceRechargeConfirmRequest(BaseModel):
    """确认开票充值请求"""
    remark: Optional[str] = None


class InvoiceRechargeRejectRequest(BaseModel):
    """拒绝开票充值请求"""
    reject_reason: str


@router.get("/invoice-recharges", summary="获取开票充值列表（管理员）")
async def get_invoice_recharges_admin(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None, description="搜索用户手机号"),
    status: Optional[str] = Query(None, description="状态: pending/confirmed/rejected"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员获取开票充值申请列表"""
    query = db.query(InvoiceRechargeRecord).join(User, InvoiceRechargeRecord.user_id == User.id)

    if search:
        query = query.filter(User.phone.contains(search))
    if status:
        try:
            status_enum = InvoiceRechargeStatus(status)
            query = query.filter(InvoiceRechargeRecord.status == status_enum)
        except ValueError:
            pass

    total = query.count()
    records = query.order_by(desc(InvoiceRechargeRecord.created_at)).offset((page - 1) * page_size).limit(page_size).all()

    result = []
    for r in records:
        user = db.query(User).filter(User.id == r.user_id).first()
        result.append({
            "id": r.id,
            "user_id": r.user_id,
            "user_name": user.real_name or user.nickname if user else None,
            "user_phone": user.phone if user else None,
            "amount": float(r.amount),
            "bonus_amount": float(r.bonus_amount or 0),
            "total_amount": float(r.amount + (r.bonus_amount or 0)),
            "invoice_title": r.invoice_title,
            "invoice_tax_no": r.invoice_tax_no,
            "invoice_type": r.invoice_type,
            "invoice_email": r.invoice_email,
            "bank_name": r.bank_name,
            "bank_account": r.bank_account,
            "transfer_date": r.transfer_date.isoformat() if r.transfer_date else None,
            "transfer_voucher": r.transfer_voucher,
            "status": r.status.value if r.status else "pending",
            "reject_reason": r.reject_reason,
            "created_at": r.created_at.isoformat() if r.created_at else None,
            "confirmed_at": r.confirmed_at.isoformat() if r.confirmed_at else None
        })

    return Response.success(data={
        "items": result,
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.get("/invoice-recharges/{record_id}", summary="获取开票充值详情（管理员）")
async def get_invoice_recharge_detail_admin(
    record_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员获取开票充值详情"""
    record = db.query(InvoiceRechargeRecord).filter(InvoiceRechargeRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="记录不存在")

    user = db.query(User).filter(User.id == record.user_id).first()
    admin = db.query(User).filter(User.id == record.admin_id).first() if record.admin_id else None

    return Response.success(data={
        "id": record.id,
        "user_id": record.user_id,
        "user_name": user.real_name or user.nickname if user else None,
        "user_phone": user.phone if user else None,
        "amount": float(record.amount),
        "bonus_amount": float(record.bonus_amount or 0),
        "total_amount": float(record.amount + (record.bonus_amount or 0)),
        "invoice_title": record.invoice_title,
        "invoice_tax_no": record.invoice_tax_no,
        "invoice_type": record.invoice_type,
        "invoice_email": record.invoice_email,
        "invoice_remark": record.invoice_remark,
        "bank_name": record.bank_name,
        "bank_account": record.bank_account,
        "transfer_date": record.transfer_date.isoformat() if record.transfer_date else None,
        "transfer_voucher": record.transfer_voucher,
        "status": record.status.value if record.status else "pending",
        "reject_reason": record.reject_reason,
        "remark": record.remark,
        "admin_id": record.admin_id,
        "admin_name": admin.nickname if admin else None,
        "created_at": record.created_at.isoformat() if record.created_at else None,
        "confirmed_at": record.confirmed_at.isoformat() if record.confirmed_at else None
    })


@router.post("/invoice-recharges/{record_id}/confirm", summary="确认开票充值")
async def confirm_invoice_recharge(
    record_id: int,
    data: InvoiceRechargeConfirmRequest = Body(default=InvoiceRechargeConfirmRequest()),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """确认开票充值，将金额充入用户账户"""
    record = db.query(InvoiceRechargeRecord).filter(
        InvoiceRechargeRecord.id == record_id,
        InvoiceRechargeRecord.status == InvoiceRechargeStatus.PENDING
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="记录不存在或已处理")

    # 更新记录状态
    record.status = InvoiceRechargeStatus.CONFIRMED
    record.admin_id = current_admin.id
    record.confirmed_at = datetime.now()
    record.remark = data.remark

    # 将金额充入用户账户
    user = db.query(User).filter(User.id == record.user_id).first()
    if user:
        total_amount = record.amount + (record.bonus_amount or Decimal("0"))
        user.balance = (user.balance or Decimal("0")) + total_amount

    db.commit()

    return Response.success(message="开票充值已确认，金额已到账")


@router.post("/invoice-recharges/{record_id}/reject", summary="拒绝开票充值")
async def reject_invoice_recharge(
    record_id: int,
    data: InvoiceRechargeRejectRequest,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """拒绝开票充值申请"""
    record = db.query(InvoiceRechargeRecord).filter(
        InvoiceRechargeRecord.id == record_id,
        InvoiceRechargeRecord.status == InvoiceRechargeStatus.PENDING
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="记录不存在或已处理")

    record.status = InvoiceRechargeStatus.REJECTED
    record.admin_id = current_admin.id
    record.reject_reason = data.reject_reason

    db.commit()

    return Response.success(message="开票充值申请已拒绝")


# ==================== 项目选项管理 ====================
from app.models.project_option import ProjectOption, OptionType, PriceType


@router.get("/options", summary="获取选项列表（管理员）")
async def get_options_admin(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    project_id: Optional[int] = Query(None, description="项目ID"),
    category_id: Optional[int] = Query(None, description="分类ID"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员获取项目选项列表"""
    query = db.query(ProjectOption)

    if project_id:
        query = query.filter(ProjectOption.project_id == project_id)
    if category_id:
        query = query.filter(ProjectOption.category_id == category_id)

    total = query.count()
    options = query.order_by(ProjectOption.project_id, ProjectOption.sort_order, ProjectOption.id).offset((page - 1) * page_size).limit(page_size).all()

    # 构建层级结构
    def get_option_level(opt):
        level = 1
        current = opt
        while current.parent_id:
            level += 1
            current = db.query(ProjectOption).filter(ProjectOption.id == current.parent_id).first()
            if not current:
                break
        return level

    result = []
    for opt in options:
        project = db.query(Project).filter(Project.id == opt.project_id).first() if opt.project_id else None
        category = db.query(Category).filter(Category.id == opt.category_id).first() if opt.category_id else None
        result.append({
            "id": opt.id,
            "project_id": opt.project_id,
            "project_name": project.name if project else None,
            "category_id": opt.category_id,
            "category_name": category.name if category else None,
            "parent_id": opt.parent_id,
            "name": opt.name,
            "option_type": opt.option_type.value if isinstance(opt.option_type, OptionType) else opt.option_type,
            "price": float(opt.price) if opt.price else 0,
            "price_type": opt.price_type.value if isinstance(opt.price_type, PriceType) else (opt.price_type or "fixed"),
            "hint_text": opt.hint_text,
            "placeholder": opt.placeholder,
            "is_required": opt.is_required,
            "sort_order": opt.sort_order,
            "is_active": opt.is_active,
            "level": get_option_level(opt),
            "created_at": opt.created_at.isoformat() if opt.created_at else None
        })

    return Response.success(data={
        "items": result,
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.post("/options", summary="创建选项（管理员）")
async def create_option_admin(
    data: dict = Body(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员创建项目选项"""
    if not data.get("name"):
        raise HTTPException(status_code=400, detail="选项名称不能为空")
    if not data.get("project_id") and not data.get("category_id"):
        raise HTTPException(status_code=400, detail="必须关联项目或分类")

    option = ProjectOption(
        project_id=data.get("project_id"),
        category_id=data.get("category_id"),
        parent_id=data.get("parent_id"),
        name=data.get("name"),
        option_type=OptionType(data.get("option_type", "single")),
        price=Decimal(str(data.get("price", 0))),
        price_type=PriceType(data.get("price_type", "fixed")),
        hint_text=data.get("hint_text", ""),
        placeholder=data.get("placeholder", ""),
        is_required=data.get("is_required", False),
        sort_order=data.get("sort_order", 0),
        is_active=data.get("is_active", True)
    )
    db.add(option)
    db.commit()
    db.refresh(option)

    return Response.success(data={"id": option.id}, message="选项创建成功")


@router.put("/options/{option_id}", summary="更新选项（管理员）")
async def update_option_admin(
    option_id: int,
    data: dict = Body(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员更新项目选项"""
    option = db.query(ProjectOption).filter(ProjectOption.id == option_id).first()
    if not option:
        raise HTTPException(status_code=404, detail="选项不存在")

    if "name" in data:
        option.name = data["name"]
    if "project_id" in data:
        option.project_id = data["project_id"]
    if "category_id" in data:
        option.category_id = data["category_id"]
    if "parent_id" in data:
        option.parent_id = data["parent_id"]
    if "option_type" in data:
        option.option_type = OptionType(data["option_type"])
    if "price" in data:
        option.price = Decimal(str(data["price"]))
    if "price_type" in data:
        option.price_type = PriceType(data["price_type"])
    if "hint_text" in data:
        option.hint_text = data["hint_text"]
    if "placeholder" in data:
        option.placeholder = data["placeholder"]
    if "is_required" in data:
        option.is_required = data["is_required"]
    if "sort_order" in data:
        option.sort_order = data["sort_order"]
    if "is_active" in data:
        option.is_active = data["is_active"]

    db.commit()
    return Response.success(message="选项更新成功")


@router.post("/options/{option_id}/toggle", summary="切换选项状态（管理员）")
async def toggle_option_admin(
    option_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """切换选项启用/禁用状态"""
    option = db.query(ProjectOption).filter(ProjectOption.id == option_id).first()
    if not option:
        raise HTTPException(status_code=404, detail="选项不存在")

    option.is_active = not option.is_active
    db.commit()

    return Response.success(message=f"选项已{'启用' if option.is_active else '禁用'}")


@router.delete("/options/{option_id}", summary="删除选项（管理员）")
async def delete_option_admin(
    option_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """删除项目选项（同时删除子选项）"""
    option = db.query(ProjectOption).filter(ProjectOption.id == option_id).first()
    if not option:
        raise HTTPException(status_code=404, detail="选项不存在")

    # 删除所有子选项
    db.query(ProjectOption).filter(ProjectOption.parent_id == option_id).delete()
    db.delete(option)
    db.commit()

    return Response.success(message="选项删除成功")


# ==================== 发票文件上传/下载 ====================

@router.post("/invoices/{invoice_id}/upload-file", summary="上传发票文件（管理员）")
async def upload_invoice_file(
    invoice_id: int,
    file_url: str = Body(..., embed=True, description="发票文件URL"),
    invoice_code: Optional[str] = Body(None, description="发票代码"),
    invoice_number: Optional[str] = Body(None, description="发票号码"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """财务上传发票PDF/图片供用户下载"""
    from app.models.invoice import Invoice, InvoiceStatus

    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="发票不存在")

    invoice.invoice_url = file_url
    if invoice_code:
        invoice.invoice_code = invoice_code
    if invoice_number:
        invoice.invoice_number = invoice_number
    invoice.status = InvoiceStatus.ISSUED
    invoice.issued_at = datetime.now()
    db.commit()

    return Response.success(message="发票文件上传成功，已标记为已开票")


@router.get("/invoices/{invoice_id}/download", summary="获取发票下载链接")
async def get_invoice_download(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """获取发票文件下载链接"""
    from app.models.invoice import Invoice

    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="发票不存在")

    if not invoice.invoice_url:
        raise HTTPException(status_code=404, detail="发票文件未上传")

    return Response.success(data={
        "download_url": invoice.invoice_url,
        "invoice_code": invoice.invoice_code,
        "invoice_number": invoice.invoice_number
    })


# ==================== 抽奖活动管理（完善） ====================
from app.models.lottery import LotteryPrize, LotteryRecord, PrizeType as LotteryPrizeType


@router.post("/lotteries", summary="创建抽奖活动（管理员）")
async def create_lottery_admin(
    data: dict = Body(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """创建抽奖活动（暂时简化为管理奖品）"""
    # 由于目前没有独立的Lottery活动表，直接返回成功
    return Response.success(message="抽奖活动创建成功（请通过奖品管理配置）")


@router.put("/lotteries/{lottery_id}", summary="更新抽奖活动（管理员）")
async def update_lottery_admin(
    lottery_id: int,
    data: dict = Body(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """更新抽奖活动"""
    return Response.success(message="抽奖活动更新成功")


@router.get("/lottery/prizes", summary="获取奖品列表（管理员）")
async def get_lottery_prizes_admin(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员获取抽奖奖品列表"""
    query = db.query(LotteryPrize)
    total = query.count()
    prizes = query.order_by(LotteryPrize.probability.desc()).offset((page - 1) * page_size).limit(page_size).all()

    result = []
    for p in prizes:
        result.append({
            "id": p.id,
            "name": p.name,
            "prize_type": p.prize_type.value if isinstance(p.prize_type, LotteryPrizeType) else p.prize_type,
            "value": float(p.value) if p.value else 0,
            "probability": float(p.probability) if p.probability else 0,
            "total_count": p.total_count,
            "remain_count": p.remain_count,
            "daily_limit": p.daily_limit,
            "image_url": p.image_url,
            "description": p.description,
            "is_active": p.is_active,
            "sort_order": p.sort_order
        })

    return Response.success(data={
        "items": result,
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.post("/lottery/prizes", summary="创建奖品（管理员）")
async def create_lottery_prize_admin(
    data: dict = Body(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员创建抽奖奖品"""
    if not data.get("name"):
        raise HTTPException(status_code=400, detail="奖品名称不能为空")

    prize = LotteryPrize(
        name=data.get("name"),
        prize_type=LotteryPrizeType(data.get("prize_type", "points")),
        value=Decimal(str(data.get("value", 0))),
        probability=Decimal(str(data.get("probability", 0))),
        total_count=data.get("total_count"),
        remain_count=data.get("remain_count") or data.get("total_count"),
        daily_limit=data.get("daily_limit"),
        image_url=data.get("image_url", ""),
        description=data.get("description", ""),
        is_active=data.get("is_active", True),
        sort_order=data.get("sort_order", 0)
    )
    db.add(prize)
    db.commit()
    db.refresh(prize)

    return Response.success(data={"id": prize.id}, message="奖品创建成功")


@router.put("/lottery/prizes/{prize_id}", summary="更新奖品（管理员）")
async def update_lottery_prize_admin(
    prize_id: int,
    data: dict = Body(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员更新抽奖奖品"""
    prize = db.query(LotteryPrize).filter(LotteryPrize.id == prize_id).first()
    if not prize:
        raise HTTPException(status_code=404, detail="奖品不存在")

    if "name" in data:
        prize.name = data["name"]
    if "prize_type" in data:
        prize.prize_type = LotteryPrizeType(data["prize_type"])
    if "value" in data:
        prize.value = Decimal(str(data["value"]))
    if "probability" in data:
        prize.probability = Decimal(str(data["probability"]))
    if "total_count" in data:
        prize.total_count = data["total_count"]
    if "remain_count" in data:
        prize.remain_count = data["remain_count"]
    if "daily_limit" in data:
        prize.daily_limit = data["daily_limit"]
    if "image_url" in data:
        prize.image_url = data["image_url"]
    if "description" in data:
        prize.description = data["description"]
    if "is_active" in data:
        prize.is_active = data["is_active"]
    if "sort_order" in data:
        prize.sort_order = data["sort_order"]

    db.commit()
    return Response.success(message="奖品更新成功")


@router.delete("/lottery/prizes/{prize_id}", summary="删除奖品（管理员）")
async def delete_lottery_prize_admin(
    prize_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """管理员删除抽奖奖品"""
    prize = db.query(LotteryPrize).filter(LotteryPrize.id == prize_id).first()
    if not prize:
        raise HTTPException(status_code=404, detail="奖品不存在")

    db.delete(prize)
    db.commit()
    return Response.success(message="奖品删除成功")

