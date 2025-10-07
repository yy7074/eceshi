"""
订单相关API
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
import time
from decimal import Decimal

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.order import Order, OrderSample, OrderFee, OrderStatusHistory, UserAddress
from app.schemas.order import (
    OrderCreate, OrderCalculate, OrderCalculateResponse,
    OrderDetail, OrderListResponse, OrderListItem, OrderCancel, OrderFeeDetail
)
from app.core.response import SuccessResponse, ErrorResponse

router = APIRouter()


def generate_order_no() -> str:
    """生成订单号"""
    return f"ORD{int(time.time())}{int(time.time() * 1000000) % 1000000}"


@router.post("/calculate", response_model=SuccessResponse)
async def calculate_order(
    data: OrderCalculate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    计算订单费用（下单前）
    """
    # TODO: 从数据库查询项目信息
    # 这里暂时使用模拟数据
    project_fee = Decimal("312.00")  # 基础费用
    urgent_fee = Decimal("100.00") if data.is_urgent else Decimal("0")
    
    # 运费计算
    shipping_fee = Decimal("0")
    if data.shipping_method == "express":
        shipping_fee = Decimal("20.00")
    elif data.shipping_method == "platform":
        shipping_fee = Decimal("30.00")
    
    # 多样品费用
    if data.sample_count > 1:
        project_fee = project_fee * data.sample_count
    
    # 优惠计算
    discount_amount = Decimal("0")
    if data.coupon_id:
        discount_amount = Decimal("50.00")  # 模拟优惠券
    
    # 积分抵扣（100积分=1元，最多抵扣20%）
    if data.use_points > 0:
        points_discount = Decimal(data.use_points) / 100
        max_discount = (project_fee + urgent_fee + shipping_fee) * Decimal("0.2")
        points_discount = min(points_discount, max_discount)
        discount_amount += points_discount
    
    # 总费用
    total_fee = project_fee + urgent_fee + shipping_fee - discount_amount
    
    # 费用明细
    fee_details = [
        OrderFeeDetail(fee_type="project", fee_name="检测费用", amount=project_fee)
    ]
    if urgent_fee > 0:
        fee_details.append(OrderFeeDetail(fee_type="urgent", fee_name="加急费用", amount=urgent_fee))
    if shipping_fee > 0:
        fee_details.append(OrderFeeDetail(fee_type="shipping", fee_name="运费", amount=shipping_fee))
    if discount_amount > 0:
        fee_details.append(OrderFeeDetail(fee_type="discount", fee_name="优惠", amount=-discount_amount))
    
    result = OrderCalculateResponse(
        project_fee=project_fee,
        urgent_fee=urgent_fee,
        shipping_fee=shipping_fee,
        discount_amount=discount_amount,
        total_fee=total_fee,
        fee_details=fee_details
    )
    
    return SuccessResponse(data=result)


@router.post("/create", response_model=SuccessResponse)
async def create_order(
    data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建订单
    """
    # 验证地址（如果需要）
    address = None
    if data.shipping_method in ["express", "platform"] and data.address_id:
        address = db.query(UserAddress).filter(
            UserAddress.id == data.address_id,
            UserAddress.user_id == current_user.id
        ).first()
        if not address:
            raise HTTPException(status_code=400, detail="地址不存在")
    
    # TODO: 查询项目信息
    # 这里使用模拟数据
    project_id = data.project_id
    project_name = "场发射扫描电镜（SEM）"
    lab_id = 1
    lab_name = "某985高校材料实验室"
    
    # 计算费用
    project_fee = Decimal("312.00") * len(data.samples)
    urgent_fee = Decimal("100.00") if data.is_urgent else Decimal("0")
    shipping_fee = Decimal("20.00") if data.shipping_method == "express" else Decimal("0")
    discount_amount = Decimal("0")
    total_fee = project_fee + urgent_fee + shipping_fee - discount_amount
    
    # 创建订单
    order = Order(
        order_no=generate_order_no(),
        user_id=current_user.id,
        project_id=project_id,
        project_name=project_name,
        lab_id=lab_id,
        lab_name=lab_name,
        status="pending_payment",
        project_fee=project_fee,
        urgent_fee=urgent_fee,
        shipping_fee=shipping_fee,
        discount_amount=discount_amount,
        total_fee=total_fee,
        paid_fee=Decimal("0"),
        sample_count=len(data.samples),
        shipping_method=data.shipping_method,
        is_urgent=data.is_urgent,
        remark=data.remark
    )
    
    # 设置收货信息
    if address:
        order.receiver_name = address.receiver_name
        order.receiver_phone = address.phone
        order.receiver_address = f"{address.province}{address.city}{address.district or ''}{address.detail_address}"
    
    db.add(order)
    db.flush()  # 获取order.id
    
    # 创建样品记录
    for sample_data in data.samples:
        sample = OrderSample(
            order_id=order.id,
            sample_name=sample_data.sample_name,
            sample_type=sample_data.sample_type,
            sample_desc=sample_data.sample_desc,
            quantity=sample_data.quantity,
            photos=sample_data.photos,
            test_params=sample_data.test_params,
            special_requirements=sample_data.special_requirements
        )
        db.add(sample)
    
    # 创建费用明细
    fee_items = [
        ("project", "检测费用", project_fee),
    ]
    if urgent_fee > 0:
        fee_items.append(("urgent", "加急费用", urgent_fee))
    if shipping_fee > 0:
        fee_items.append(("shipping", "运费", shipping_fee))
    
    for fee_type, fee_name, amount in fee_items:
        fee = OrderFee(
            order_id=order.id,
            fee_type=fee_type,
            fee_name=fee_name,
            amount=amount
        )
        db.add(fee)
    
    # 记录状态变更
    history = OrderStatusHistory(
        order_id=order.id,
        from_status=None,
        to_status="pending_payment",
        operator_id=current_user.id,
        operator_type="user",
        remark="创建订单"
    )
    db.add(history)
    
    db.commit()
    db.refresh(order)
    
    return SuccessResponse(data={
        "order_id": order.id,
        "order_no": order.order_no,
        "total_fee": float(order.total_fee)
    }, message="订单创建成功")


@router.get("/list", response_model=SuccessResponse)
async def get_order_list(
    status: Optional[str] = Query("all", description="订单状态"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取订单列表
    """
    query = db.query(Order).filter(Order.user_id == current_user.id)
    
    # 状态筛选
    if status and status != "all":
        query = query.filter(Order.status == status)
    
    # 总数
    total = query.count()
    
    # 分页
    orders = query.order_by(Order.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    # 转换为列表项
    items = []
    for order in orders:
        items.append(OrderListItem(
            id=order.id,
            order_no=order.order_no,
            project_name=order.project_name,
            lab_name=order.lab_name,
            status=order.status,
            total_fee=order.total_fee,
            sample_count=order.sample_count,
            created_at=order.created_at,
            project_image=None  # TODO: 从项目表获取
        ))
    
    result = OrderListResponse(total=total, list=items)
    return SuccessResponse(data=result)


@router.get("/{order_id}", response_model=SuccessResponse)
async def get_order_detail(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取订单详情
    """
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    # 获取样品列表
    samples = db.query(OrderSample).filter(OrderSample.order_id == order_id).all()
    
    # 构建详情
    detail = OrderDetail(
        **order.__dict__,
        samples=samples
    )
    
    return SuccessResponse(data=detail)


@router.post("/{order_id}/cancel", response_model=SuccessResponse)
async def cancel_order(
    order_id: int,
    data: OrderCancel,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    取消订单
    """
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    # 只有待支付和待确认的订单可以直接取消
    if order.status not in ["pending_payment", "confirmed"]:
        raise HTTPException(status_code=400, detail="当前状态不允许取消")
    
    # 更新订单状态
    old_status = order.status
    order.status = "cancelled"
    order.cancel_reason = data.reason
    order.cancelled_at = datetime.now()
    
    # 记录状态变更
    history = OrderStatusHistory(
        order_id=order.id,
        from_status=old_status,
        to_status="cancelled",
        operator_id=current_user.id,
        operator_type="user",
        remark=data.reason
    )
    db.add(history)
    
    db.commit()
    
    return SuccessResponse(message="订单已取消")


@router.post("/{order_id}/confirm-receipt", response_model=SuccessResponse)
async def confirm_receipt(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    确认收样（用户确认实验室收到样品）
    """
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    if order.status != "waiting_test":
        raise HTTPException(status_code=400, detail="订单状态不正确")
    
    # 更新状态
    old_status = order.status
    order.status = "in_progress"
    order.started_at = datetime.now()
    
    # 记录状态变更
    history = OrderStatusHistory(
        order_id=order.id,
        from_status=old_status,
        to_status="in_progress",
        operator_id=current_user.id,
        operator_type="user",
        remark="用户确认收样"
    )
    db.add(history)
    
    db.commit()
    
    return SuccessResponse(message="已确认收样")

