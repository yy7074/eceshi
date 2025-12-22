"""
订单相关API
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from datetime import datetime
import time
import json
from decimal import Decimal

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.order import Order, OrderSample, OrderFee, OrderStatusHistory, UserAddress
from app.models.project import Project
from app.schemas.order import (
    OrderCreate, OrderCalculate, OrderCalculateResponse,
    OrderDetail, OrderListResponse, OrderListItem, OrderCancel, OrderFeeDetail
)
from app.core.response import SuccessResponse, ErrorResponse

router = APIRouter()


def generate_order_no() -> str:
    """生成订单号"""
    return f"ORD{int(time.time())}{int(time.time() * 1000000) % 1000000}"


@router.post("/calculate")
async def calculate_order(
    data: OrderCalculate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    计算订单费用（下单前）
    """
    # 从数据库查询项目信息
    project = db.query(Project).filter(Project.id == data.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    # 基础费用：项目单价 × 样品数量
    project_fee = Decimal(str(project.current_price)) * data.sample_count
    
    # 加急费用
    urgent_fee = Decimal("100.00") if data.is_urgent else Decimal("0")
    
    # 运费计算
    shipping_fee = Decimal("0")
    if data.shipping_method == "express":
        shipping_fee = Decimal("20.00")
    elif data.shipping_method == "platform":
        shipping_fee = Decimal("30.00")
    
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


@router.post("/create")
async def create_order(
    request_data: dict = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建订单（兼容前端调用，支持多种数据格式）
    """
    import json
    print(f"[订单创建] 接收到的原始数据: {json.dumps(request_data, ensure_ascii=False, default=str)}")
    
    # 兼容前端发送的数据格式
    # 如果前端发送的是简化格式（sample_count, sample_name等），转换为标准格式
    if "samples" not in request_data and "sample_name" in request_data:
        # 前端发送的是简化格式，需要转换
        samples = [{
            "sample_name": request_data.get("sample_name", ""),
            "sample_type": request_data.get("sample_type"),
            "sample_desc": request_data.get("sample_composition") or request_data.get("sample_desc"),
            "quantity": request_data.get("sample_count", 1),
            "photos": request_data.get("attachments", []),
            "test_params": {
                "sample_state": request_data.get("sample_state"),
                "danger_type": request_data.get("danger_type"),
                "storage_requirement": request_data.get("storage_requirement")
            },
            "special_requirements": request_data.get("remark")
        }]
        request_data["samples"] = samples
    
    # 字段映射
    if "delivery_method" in request_data and "shipping_method" not in request_data:
        request_data["shipping_method"] = request_data["delivery_method"]
    
    # 如果没有 shipping_method，根据 address_id 设置默认值
    if "shipping_method" not in request_data:
        if request_data.get("address_id"):
            # 如果有地址，默认使用快递
            request_data["shipping_method"] = "express"
        else:
            # 如果没有地址，默认使用自提
            request_data["shipping_method"] = "self"
        print(f"[订单创建] 自动设置 shipping_method: {request_data['shipping_method']}")
    
    # 验证必需字段（shipping_method 已经有默认值，不需要验证）
    required_fields = ["project_id", "samples"]
    missing_fields = []
    for field in required_fields:
        if field not in request_data:
            missing_fields.append(field)
    
    if missing_fields:
        print(f"[订单创建] 缺少必需字段: {missing_fields}, 当前数据键: {list(request_data.keys())}")
        raise HTTPException(status_code=422, detail=f"缺少必需字段: {', '.join(missing_fields)}")
    
    # 验证 samples 格式
    if not isinstance(request_data["samples"], list) or len(request_data["samples"]) == 0:
        raise HTTPException(status_code=422, detail="samples 必须是非空数组")
    
    # 尝试使用 Pydantic 模型验证
    try:
        data = OrderCreate(**request_data)
    except Exception as e:
        print(f"[订单创建] Pydantic 验证失败: {str(e)}")
        raise HTTPException(status_code=422, detail=f"数据格式错误: {str(e)}")
    
    print(f"[订单创建] 验证通过，开始创建订单")
    # 验证地址（如果需要）
    address = None
    if data.shipping_method in ["express", "platform"] and data.address_id:
        address = db.query(UserAddress).filter(
            UserAddress.id == data.address_id,
            UserAddress.user_id == current_user.id
        ).first()
        if not address:
            raise HTTPException(status_code=400, detail="地址不存在")
    
    # 从数据库查询项目信息
    project = db.query(Project).filter(Project.id == data.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    project_id = data.project_id
    project_fee = project.current_price  # 从数据库获取项目价格
    project_name = project.name
    lab_id = project.lab_id if project.lab_id else 1
    lab_name = project.lab_name if hasattr(project, 'lab_name') else "平台实验室"
    
    # 计算费用：项目单价 × 样品数量
    project_fee = Decimal(str(project_fee)) * len(data.samples)
    
    # 加急费用
    urgent_fee = Decimal("100.00") if data.is_urgent else Decimal("0")
    
    # 运费
    shipping_fee = Decimal("0")
    if data.shipping_method == "express":
        shipping_fee = Decimal("20.00")
    elif data.shipping_method == "platform":
        shipping_fee = Decimal("30.00")
    
    # 优惠金额
    discount_amount = Decimal("0")
    
    # 总费用
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
    
    print(f"[订单创建] 订单创建成功: order_id={order.id}, order_no={order.order_no}, total_fee={order.total_fee}")
    
    # 返回完整的订单信息，包括价格和支付所需信息
    return SuccessResponse(data={
        "order_id": order.id,
        "order_no": order.order_no,
        "status": order.status,
        "project_id": order.project_id,
        "project_name": order.project_name,
        "total_fee": float(order.total_fee),
        "project_fee": float(order.project_fee),
        "urgent_fee": float(order.urgent_fee),
        "shipping_fee": float(order.shipping_fee),
        "discount_amount": float(order.discount_amount),
        "paid_fee": float(order.paid_fee),
        "sample_count": order.sample_count,
        "shipping_method": order.shipping_method,
        "receiver_name": order.receiver_name,
        "receiver_phone": order.receiver_phone,
        "receiver_address": order.receiver_address,
        "is_urgent": order.is_urgent,
        "remark": order.remark,
        "created_at": order.created_at.isoformat() if order.created_at else None
    }, message="订单创建成功")


@router.get("/list")
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


@router.get("/{order_id}")
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


@router.post("/{order_id}/cancel")
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


@router.post("/{order_id}/confirm-receipt")
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

