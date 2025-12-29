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
    orders = query.order_by(desc(Order.created_at)).offset((page - 1) * page_size).limit(page_size).all()

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
            for o in orders
        ],
        "total": total,
        "page": page,
        "page_size": page_size
    })


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

        lab_list.append({
            "id": lab.id,
            "name": lab.name,
            "code": lab.code,
            "institution": lab.institution,
            "province": lab.province,
            "city": lab.city,
            "rating": float(lab.rating) if lab.rating else 5.0,
            "completed_orders": lab.completed_orders or 0,
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
                "lab_type": lab.lab_type.value if lab.lab_type else None,
                "status": lab.status.value if lab.status else None,
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
        output = io.StringIO()
        if data:
            writer = csv.DictWriter(output, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        csv_content = output.getvalue()
        return Response.success(data={
            "format": "csv",
            "content": csv_content,
            "filename": f"orders_{start_date or 'all'}_{end_date or 'all'}.csv"
        })

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
        output = io.StringIO()
        if data:
            writer = csv.DictWriter(output, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        csv_content = output.getvalue()
        return Response.success(data={
            "format": "csv",
            "content": csv_content,
            "filename": f"users_{start_date or 'all'}_{end_date or 'all'}.csv"
        })

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
                trend_data[key] = {"date": key, "count": 0, "amount": 0}
            trend_data[key]["count"] += 1
            trend_data[key]["amount"] += float(order.total_fee or 0)

    # 排序并返回
    sorted_data = sorted(trend_data.values(), key=lambda x: x["date"])

    return Response.success(data={
        "time_range": time_range,
        "trend": sorted_data
    })


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

    return Response.success(data={
        "time_range": time_range,
        "ranking": [
            {
                "project_id": r.project_id,
                "project_name": r.project_name,
                "order_count": r.order_count,
                "total_amount": float(r.total_amount or 0)
            }
            for r in ranking
        ]
    })


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

