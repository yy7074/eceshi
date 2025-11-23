"""
优惠券系统API
"""
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.response import Response
from app.api.v1.deps import get_current_user
from app.models.user import User
from app.models.coupon import Coupon, UserCoupon, CouponStatus, UserCouponStatus


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
    # 构建查询
    query = db.query(UserCoupon).filter(UserCoupon.user_id == current_user.id)
    
    # 根据状态筛选
    if status == "available":
        query = query.filter(
            UserCoupon.status == UserCouponStatus.UNUSED,
            UserCoupon.expire_at > datetime.now()
        )
    elif status == "used":
        query = query.filter(UserCoupon.status == UserCouponStatus.USED)
    elif status == "expired":
        query = query.filter(
            (UserCoupon.status == UserCouponStatus.EXPIRED) |
            (UserCoupon.expire_at <= datetime.now())
        )
    
    # 总数
    total = query.count()
    
    # 分页查询
    items = query.order_by(UserCoupon.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    # 统计可用优惠券数量
    available_count = db.query(UserCoupon).filter(
        UserCoupon.user_id == current_user.id,
        UserCoupon.status == UserCouponStatus.UNUSED,
        UserCoupon.expire_at > datetime.now()
    ).count()
    
    # 格式化返回数据
    coupon_list = []
    for item in items:
        coupon_list.append({
            "id": item.id,
            "coupon_id": item.coupon_id,
            "coupon_name": item.coupon_name,
            "coupon_type": item.coupon_type,
            "discount_value": float(item.discount_value) if item.discount_value else 0,
            "status": item.status.value,
            "received_at": item.received_at.isoformat() if item.received_at else None,
            "expire_at": item.expire_at.isoformat() if item.expire_at else None,
            "order_id": item.order_id,
            "used_at": item.used_at.isoformat() if item.used_at else None
        })
    
    return Response.success(data={
        "items": coupon_list,
        "total": total,
        "page": page,
        "page_size": page_size,
        "available_count": available_count
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
    now = datetime.now()
    
    # 查询可领取的优惠券
    query = db.query(Coupon).filter(
        Coupon.status == CouponStatus.ACTIVE,
        (Coupon.start_time == None) | (Coupon.start_time <= now),
        (Coupon.end_time == None) | (Coupon.end_time >= now)
    )
    
    # 总数
    total = query.count()
    
    # 分页查询
    items = query.order_by(Coupon.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    # 格式化返回数据
    coupon_list = []
    for item in items:
        # 检查是否还有库存
        is_available = True
        if item.total_quantity > 0 and item.received_quantity >= item.total_quantity:
            is_available = False
        
        coupon_list.append({
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "type": item.type.value,
            "discount_rate": float(item.discount_rate) if item.discount_rate else None,
            "cash_amount": float(item.cash_amount) if item.cash_amount else None,
            "full_amount": float(item.full_amount) if item.full_amount else None,
            "reduction_amount": float(item.reduction_amount) if item.reduction_amount else None,
            "min_order_amount": float(item.min_order_amount),
            "valid_days": item.valid_days,
            "total_quantity": item.total_quantity,
            "received_quantity": item.received_quantity,
            "is_available": is_available,
            "start_time": item.start_time.isoformat() if item.start_time else None,
            "end_time": item.end_time.isoformat() if item.end_time else None
        })
    
    return Response.success(data={
        "items": coupon_list,
        "total": total,
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
    # 查询优惠券
    coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
    if not coupon:
        raise HTTPException(status_code=404, detail="优惠券不存在")
    
    # 检查优惠券状态
    if coupon.status != CouponStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="优惠券已下架")
    
    # 检查时间范围
    now = datetime.now()
    if coupon.start_time and coupon.start_time > now:
        raise HTTPException(status_code=400, detail="优惠券尚未开始")
    if coupon.end_time and coupon.end_time < now:
        raise HTTPException(status_code=400, detail="优惠券已过期")
    
    # 检查库存
    if coupon.total_quantity > 0 and coupon.received_quantity >= coupon.total_quantity:
        raise HTTPException(status_code=400, detail="优惠券已被领完")
    
    # 检查是否已领取
    existing = db.query(UserCoupon).filter(
        UserCoupon.user_id == current_user.id,
        UserCoupon.coupon_id == coupon_id,
        UserCoupon.status == UserCouponStatus.UNUSED
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="您已领取过该优惠券")
    
    # 创建用户优惠券
    expire_at = datetime.now() + timedelta(days=coupon.valid_days)
    
    # 确定优惠值
    discount_value = None
    if coupon.type.value == "discount":
        discount_value = coupon.discount_rate
    elif coupon.type.value == "cash":
        discount_value = coupon.cash_amount
    elif coupon.type.value == "full_reduction":
        discount_value = coupon.reduction_amount
    
    user_coupon = UserCoupon(
        user_id=current_user.id,
        coupon_id=coupon.id,
        coupon_name=coupon.name,
        coupon_type=coupon.type.value,
        discount_value=discount_value,
        status=UserCouponStatus.UNUSED,
        expire_at=expire_at
    )
    db.add(user_coupon)
    
    # 更新优惠券领取数量
    coupon.received_quantity += 1
    
    db.commit()
    db.refresh(user_coupon)
    
    return Response.success(data={
        "id": user_coupon.id,
        "expire_at": user_coupon.expire_at.isoformat()
    }, message="领取成功")

