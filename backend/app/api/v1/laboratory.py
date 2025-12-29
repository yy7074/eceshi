"""
实验室相关API
实验室入驻申请、实验室列表、设备管理
"""
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, func, desc
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel

from app.core.database import get_db
from app.core.response import Response
from app.api.v1.deps import get_current_user, get_current_admin_user
from app.models.user import User
from app.models.laboratory import (
    Laboratory, LabApplication, LabEquipment, LabStaff,
    LabStatus, LabType
)
from app.models.order import Order, OrderSample, OrderStatusHistory
from app.models.report import Report

router = APIRouter()


# ========== Pydantic 模型 ==========

class LabApplicationCreate(BaseModel):
    """实验室入驻申请"""
    lab_name: str
    lab_type: str = "university"
    institution: str
    department: Optional[str] = None
    province: str
    city: str
    address: str
    applicant_name: str
    applicant_phone: str
    applicant_email: Optional[str] = None
    applicant_position: Optional[str] = None
    qualification: Optional[str] = None
    certification_files: Optional[List[str]] = None
    business_license: Optional[str] = None
    description: Optional[str] = None
    specialties: Optional[List[str]] = None
    equipments_desc: Optional[str] = None
    intended_services: Optional[List[str]] = None
    expected_monthly_orders: Optional[int] = None


class LabEquipmentCreate(BaseModel):
    """添加设备"""
    name: str
    model: Optional[str] = None
    brand: Optional[str] = None
    serial_number: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    specifications: Optional[dict] = None
    images: Optional[List[str]] = None
    unit_price: Optional[float] = None
    hourly_rate: Optional[float] = None


class LabStaffCreate(BaseModel):
    """添加技术人员"""
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    position: Optional[str] = None
    title: Optional[str] = None
    specialties: Optional[List[str]] = None
    role: str = "technician"


# ========== 用户端接口 ==========

@router.get("/list", summary="获取实验室列表")
async def get_laboratory_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    lab_type: Optional[str] = Query(None, description="实验室类型"),
    province: Optional[str] = Query(None, description="省份"),
    search: Optional[str] = Query(None, description="搜索关键字"),
    db: Session = Depends(get_db)
):
    """获取已上线的实验室列表（公开接口）"""
    query = db.query(Laboratory).filter(
        Laboratory.status == LabStatus.ACTIVE
    )

    if lab_type:
        query = query.filter(Laboratory.lab_type == lab_type)

    if province:
        query = query.filter(Laboratory.province == province)

    if search:
        query = query.filter(
            or_(
                Laboratory.name.like(f"%{search}%"),
                Laboratory.institution.like(f"%{search}%")
            )
        )

    total = query.count()
    labs = query.order_by(desc(Laboratory.rating), desc(Laboratory.completed_orders)).offset((page - 1) * page_size).limit(page_size).all()

    return Response.success(data={
        "items": [
            {
                "id": lab.id,
                "name": lab.name,
                "code": lab.code,
                "logo": lab.logo,
                "cover_image": lab.cover_image,
                "lab_type": lab.lab_type.value if lab.lab_type else None,
                "institution": lab.institution,
                "province": lab.province,
                "city": lab.city,
                "rating": float(lab.rating) if lab.rating else 5.0,
                "completed_orders": lab.completed_orders or 0,
                "specialties": lab.specialties
            }
            for lab in labs
        ],
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.get("/{lab_id}", summary="获取实验室详情")
async def get_laboratory_detail(
    lab_id: int,
    db: Session = Depends(get_db)
):
    """获取实验室详情"""
    lab = db.query(Laboratory).filter(Laboratory.id == lab_id).first()

    if not lab:
        raise HTTPException(status_code=404, detail="实验室不存在")

    # 获取设备列表
    equipments = db.query(LabEquipment).filter(
        LabEquipment.laboratory_id == lab_id,
        LabEquipment.status == "available"
    ).limit(10).all()

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
        "description": lab.description,
        "specialties": lab.specialties,
        "equipments_summary": lab.equipments_summary,
        "rating": float(lab.rating) if lab.rating else 5.0,
        "total_orders": lab.total_orders or 0,
        "completed_orders": lab.completed_orders or 0,
        "equipments": [
            {
                "id": eq.id,
                "name": eq.name,
                "model": eq.model,
                "brand": eq.brand,
                "category": eq.category,
                "images": eq.images
            }
            for eq in equipments
        ]
    })


@router.post("/apply", summary="提交入驻申请")
async def submit_lab_application(
    data: LabApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """提交实验室入驻申请"""
    # 检查是否已有待审核的申请
    existing = db.query(LabApplication).filter(
        LabApplication.applicant_user_id == current_user.id,
        LabApplication.status.in_(["pending", "reviewing"])
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="您已有待审核的申请，请等待审核结果")

    # 解析实验室类型
    try:
        lab_type_enum = LabType(data.lab_type)
    except ValueError:
        lab_type_enum = LabType.UNIVERSITY

    # 创建申请
    application = LabApplication(
        applicant_user_id=current_user.id,
        applicant_name=data.applicant_name,
        applicant_phone=data.applicant_phone,
        applicant_email=data.applicant_email,
        applicant_position=data.applicant_position,
        lab_name=data.lab_name,
        lab_type=lab_type_enum,
        institution=data.institution,
        department=data.department,
        province=data.province,
        city=data.city,
        address=data.address,
        qualification=data.qualification,
        certification_files=data.certification_files,
        business_license=data.business_license,
        description=data.description,
        specialties=data.specialties,
        equipments_desc=data.equipments_desc,
        intended_services=data.intended_services,
        expected_monthly_orders=data.expected_monthly_orders,
        status="pending"
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return Response.success(data={"id": application.id}, message="入驻申请提交成功，请等待审核")


@router.get("/apply/status", summary="获取我的入驻申请状态")
async def get_my_application_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取当前用户的入驻申请状态"""
    application = db.query(LabApplication).filter(
        LabApplication.applicant_user_id == current_user.id
    ).order_by(desc(LabApplication.created_at)).first()

    if not application:
        return Response.success(data={"has_application": False})

    return Response.success(data={
        "has_application": True,
        "id": application.id,
        "lab_name": application.lab_name,
        "status": application.status,
        "reject_reason": application.reject_reason,
        "laboratory_id": application.laboratory_id,
        "created_at": application.created_at.isoformat() if application.created_at else None,
        "reviewed_at": application.reviewed_at.isoformat() if application.reviewed_at else None
    })


# ========== 实验室管理端接口 ==========

@router.get("/my/info", summary="获取我的实验室信息")
async def get_my_laboratory(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取当前用户管理的实验室信息"""
    lab = db.query(Laboratory).filter(
        Laboratory.admin_user_id == current_user.id
    ).first()

    if not lab:
        raise HTTPException(status_code=404, detail="您暂无管理的实验室")

    return Response.success(data={
        "id": lab.id,
        "name": lab.name,
        "code": lab.code,
        "logo": lab.logo,
        "status": lab.status.value if lab.status else None,
        "institution": lab.institution,
        "department": lab.department,
        "rating": float(lab.rating) if lab.rating else 5.0,
        "total_orders": lab.total_orders or 0,
        "completed_orders": lab.completed_orders or 0,
        "commission_rate": float(lab.commission_rate) if lab.commission_rate else 20.0
    })


@router.get("/my/equipments", summary="获取我的实验室设备列表")
async def get_my_equipments(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取当前用户管理的实验室的设备列表"""
    lab = db.query(Laboratory).filter(
        Laboratory.admin_user_id == current_user.id
    ).first()

    if not lab:
        raise HTTPException(status_code=404, detail="您暂无管理的实验室")

    query = db.query(LabEquipment).filter(LabEquipment.laboratory_id == lab.id)

    if status:
        query = query.filter(LabEquipment.status == status)

    total = query.count()
    equipments = query.order_by(desc(LabEquipment.created_at)).offset((page - 1) * page_size).limit(page_size).all()

    return Response.success(data={
        "items": [
            {
                "id": eq.id,
                "name": eq.name,
                "model": eq.model,
                "brand": eq.brand,
                "serial_number": eq.serial_number,
                "category": eq.category,
                "status": eq.status,
                "unit_price": float(eq.unit_price) if eq.unit_price else None,
                "hourly_rate": float(eq.hourly_rate) if eq.hourly_rate else None,
                "images": eq.images,
                "created_at": eq.created_at.isoformat() if eq.created_at else None
            }
            for eq in equipments
        ],
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.post("/my/equipments", summary="添加设备")
async def add_equipment(
    data: LabEquipmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """为我的实验室添加设备"""
    lab = db.query(Laboratory).filter(
        Laboratory.admin_user_id == current_user.id
    ).first()

    if not lab:
        raise HTTPException(status_code=404, detail="您暂无管理的实验室")

    equipment = LabEquipment(
        laboratory_id=lab.id,
        name=data.name,
        model=data.model,
        brand=data.brand,
        serial_number=data.serial_number,
        category=data.category,
        description=data.description,
        specifications=data.specifications,
        images=data.images,
        unit_price=Decimal(str(data.unit_price)) if data.unit_price else None,
        hourly_rate=Decimal(str(data.hourly_rate)) if data.hourly_rate else None,
        status="available"
    )

    db.add(equipment)
    db.commit()
    db.refresh(equipment)

    return Response.success(data={"id": equipment.id}, message="设备添加成功")


@router.put("/my/equipments/{equipment_id}", summary="更新设备信息")
async def update_equipment(
    equipment_id: int,
    data: dict = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新设备信息"""
    lab = db.query(Laboratory).filter(
        Laboratory.admin_user_id == current_user.id
    ).first()

    if not lab:
        raise HTTPException(status_code=404, detail="您暂无管理的实验室")

    equipment = db.query(LabEquipment).filter(
        LabEquipment.id == equipment_id,
        LabEquipment.laboratory_id == lab.id
    ).first()

    if not equipment:
        raise HTTPException(status_code=404, detail="设备不存在")

    # 更新字段
    updatable_fields = ["name", "model", "brand", "serial_number", "category",
                        "description", "specifications", "images", "status",
                        "unit_price", "hourly_rate"]
    for field in updatable_fields:
        if field in data:
            if field in ["unit_price", "hourly_rate"] and data[field] is not None:
                setattr(equipment, field, Decimal(str(data[field])))
            else:
                setattr(equipment, field, data[field])

    db.commit()
    return Response.success(message="设备信息更新成功")


@router.delete("/my/equipments/{equipment_id}", summary="删除设备")
async def delete_equipment(
    equipment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除设备"""
    lab = db.query(Laboratory).filter(
        Laboratory.admin_user_id == current_user.id
    ).first()

    if not lab:
        raise HTTPException(status_code=404, detail="您暂无管理的实验室")

    equipment = db.query(LabEquipment).filter(
        LabEquipment.id == equipment_id,
        LabEquipment.laboratory_id == lab.id
    ).first()

    if not equipment:
        raise HTTPException(status_code=404, detail="设备不存在")

    db.delete(equipment)
    db.commit()

    return Response.success(message="设备已删除")


@router.get("/my/staff", summary="获取我的实验室技术人员列表")
async def get_my_staff(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取当前用户管理的实验室的技术人员列表"""
    lab = db.query(Laboratory).filter(
        Laboratory.admin_user_id == current_user.id
    ).first()

    if not lab:
        raise HTTPException(status_code=404, detail="您暂无管理的实验室")

    staff_list = db.query(LabStaff).filter(
        LabStaff.laboratory_id == lab.id,
        LabStaff.is_active == True
    ).all()

    return Response.success(data={
        "items": [
            {
                "id": s.id,
                "name": s.name,
                "phone": s.phone,
                "email": s.email,
                "avatar": s.avatar,
                "position": s.position,
                "title": s.title,
                "role": s.role,
                "specialties": s.specialties,
                "joined_at": s.joined_at.isoformat() if s.joined_at else None
            }
            for s in staff_list
        ]
    })


@router.post("/my/staff", summary="添加技术人员")
async def add_staff(
    data: LabStaffCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """为我的实验室添加技术人员"""
    lab = db.query(Laboratory).filter(
        Laboratory.admin_user_id == current_user.id
    ).first()

    if not lab:
        raise HTTPException(status_code=404, detail="您暂无管理的实验室")

    staff = LabStaff(
        laboratory_id=lab.id,
        name=data.name,
        phone=data.phone,
        email=data.email,
        position=data.position,
        title=data.title,
        specialties=data.specialties,
        role=data.role,
        is_active=True,
        joined_at=datetime.utcnow()
    )

    db.add(staff)
    db.commit()
    db.refresh(staff)

    return Response.success(data={"id": staff.id}, message="技术人员添加成功")


# ========== 实验室订单管理接口 ==========

class OrderActionRequest(BaseModel):
    """订单操作请求"""
    remark: Optional[str] = None


class UploadReportRequest(BaseModel):
    """上传报告请求"""
    report_type: str = "test_report"  # test_report/raw_data/analysis
    file_url: str
    file_name: str
    remark: Optional[str] = None


@router.get("/my/orders", summary="获取实验室订单列表")
async def get_lab_orders(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    status: Optional[str] = Query(None, description="订单状态"),
    search: Optional[str] = Query(None, description="搜索订单号/用户"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取当前实验室的订单列表"""
    lab = db.query(Laboratory).filter(
        Laboratory.admin_user_id == current_user.id
    ).first()

    if not lab:
        raise HTTPException(status_code=404, detail="您暂无管理的实验室")

    # 查询指派给该实验室的订单
    query = db.query(Order).filter(
        or_(
            Order.assigned_lab_id == lab.id,
            Order.lab_id == lab.id
        )
    )

    if status:
        query = query.filter(Order.status == status)

    if search:
        query = query.filter(
            or_(
                Order.order_no.like(f"%{search}%"),
                Order.receiver_name.like(f"%{search}%")
            )
        )

    total = query.count()
    orders = query.order_by(desc(Order.created_at)).offset((page - 1) * page_size).limit(page_size).all()

    return Response.success(data={
        "items": [
            {
                "id": order.id,
                "order_no": order.order_no,
                "project_name": order.project_name,
                "status": order.status,
                "sample_count": order.sample_count,
                "total_fee": float(order.total_fee) if order.total_fee else 0,
                "is_urgent": order.is_urgent,
                "receiver_name": order.receiver_name,
                "created_at": order.created_at.isoformat() if order.created_at else None,
                "assigned_at": order.assigned_at.isoformat() if order.assigned_at else None,
                "started_at": order.started_at.isoformat() if order.started_at else None,
                "estimated_completion_time": order.estimated_completion_time.isoformat() if order.estimated_completion_time else None
            }
            for order in orders
        ],
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.get("/my/orders/{order_id}", summary="获取订单详情")
async def get_lab_order_detail(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取订单详情"""
    lab = db.query(Laboratory).filter(
        Laboratory.admin_user_id == current_user.id
    ).first()

    if not lab:
        raise HTTPException(status_code=404, detail="您暂无管理的实验室")

    order = db.query(Order).filter(
        Order.id == order_id,
        or_(
            Order.assigned_lab_id == lab.id,
            Order.lab_id == lab.id
        )
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")

    # 获取样品列表
    samples = db.query(OrderSample).filter(OrderSample.order_id == order_id).all()

    # 获取报告列表
    reports = db.query(Report).filter(Report.order_id == order_id).all()

    # 获取状态历史
    history = db.query(OrderStatusHistory).filter(
        OrderStatusHistory.order_id == order_id
    ).order_by(desc(OrderStatusHistory.created_at)).limit(20).all()

    return Response.success(data={
        "id": order.id,
        "order_no": order.order_no,
        "project_id": order.project_id,
        "project_name": order.project_name,
        "status": order.status,
        "sample_count": order.sample_count,
        "total_fee": float(order.total_fee) if order.total_fee else 0,
        "project_fee": float(order.project_fee) if order.project_fee else 0,
        "urgent_fee": float(order.urgent_fee) if order.urgent_fee else 0,
        "is_urgent": order.is_urgent,
        "receiver_name": order.receiver_name,
        "receiver_phone": order.receiver_phone,
        "receiver_address": order.receiver_address,
        "remark": order.remark,
        "created_at": order.created_at.isoformat() if order.created_at else None,
        "paid_at": order.paid_at.isoformat() if order.paid_at else None,
        "assigned_at": order.assigned_at.isoformat() if order.assigned_at else None,
        "started_at": order.started_at.isoformat() if order.started_at else None,
        "completed_at": order.completed_at.isoformat() if order.completed_at else None,
        "estimated_completion_time": order.estimated_completion_time.isoformat() if order.estimated_completion_time else None,
        "samples": [
            {
                "id": s.id,
                "sample_name": s.sample_name,
                "sample_type": s.sample_type,
                "sample_desc": s.sample_desc,
                "quantity": s.quantity,
                "photos": s.photos,
                "test_params": s.test_params,
                "special_requirements": s.special_requirements
            }
            for s in samples
        ],
        "reports": [
            {
                "id": r.id,
                "report_type": r.report_type,
                "file_url": r.file_url,
                "file_name": r.file_name,
                "created_at": r.created_at.isoformat() if r.created_at else None
            }
            for r in reports
        ],
        "history": [
            {
                "from_status": h.from_status,
                "to_status": h.to_status,
                "remark": h.remark,
                "created_at": h.created_at.isoformat() if h.created_at else None
            }
            for h in history
        ]
    })


@router.post("/my/orders/{order_id}/accept", summary="接受订单")
async def accept_order(
    order_id: int,
    data: OrderActionRequest = Body(default=OrderActionRequest()),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """实验室接受订单"""
    lab = db.query(Laboratory).filter(
        Laboratory.admin_user_id == current_user.id
    ).first()

    if not lab:
        raise HTTPException(status_code=404, detail="您暂无管理的实验室")

    order = db.query(Order).filter(
        Order.id == order_id,
        or_(
            Order.assigned_lab_id == lab.id,
            Order.lab_id == lab.id
        )
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")

    if order.status not in ["pending_assign", "assigned"]:
        raise HTTPException(status_code=400, detail="订单状态不允许此操作")

    # 记录状态变更
    history = OrderStatusHistory(
        order_id=order_id,
        from_status=order.status,
        to_status="accepted",
        operator_id=current_user.id,
        operator_type="lab",
        remark=data.remark or "实验室已接单"
    )
    db.add(history)

    # 更新订单状态
    order.status = "accepted"
    order.assigned_lab_id = lab.id

    db.commit()

    return Response.success(message="已接受订单")


@router.post("/my/orders/{order_id}/reject", summary="拒绝订单")
async def reject_order(
    order_id: int,
    data: OrderActionRequest = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """实验室拒绝订单"""
    lab = db.query(Laboratory).filter(
        Laboratory.admin_user_id == current_user.id
    ).first()

    if not lab:
        raise HTTPException(status_code=404, detail="您暂无管理的实验室")

    order = db.query(Order).filter(
        Order.id == order_id,
        or_(
            Order.assigned_lab_id == lab.id,
            Order.lab_id == lab.id
        )
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")

    if order.status not in ["pending_assign", "assigned"]:
        raise HTTPException(status_code=400, detail="订单状态不允许此操作")

    # 记录状态变更
    history = OrderStatusHistory(
        order_id=order_id,
        from_status=order.status,
        to_status="rejected_by_lab",
        operator_id=current_user.id,
        operator_type="lab",
        remark=data.remark or "实验室拒绝接单"
    )
    db.add(history)

    # 更新订单状态，等待重新指派
    order.status = "pending_assign"
    order.assigned_lab_id = None

    db.commit()

    return Response.success(message="已拒绝订单")


@router.post("/my/orders/{order_id}/start", summary="开始检测")
async def start_testing(
    order_id: int,
    data: OrderActionRequest = Body(default=OrderActionRequest()),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """开始检测实验"""
    lab = db.query(Laboratory).filter(
        Laboratory.admin_user_id == current_user.id
    ).first()

    if not lab:
        raise HTTPException(status_code=404, detail="您暂无管理的实验室")

    order = db.query(Order).filter(
        Order.id == order_id,
        Order.assigned_lab_id == lab.id
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")

    if order.status not in ["accepted", "sample_received"]:
        raise HTTPException(status_code=400, detail="订单状态不允许此操作")

    # 记录状态变更
    history = OrderStatusHistory(
        order_id=order_id,
        from_status=order.status,
        to_status="testing",
        operator_id=current_user.id,
        operator_type="lab",
        remark=data.remark or "开始检测"
    )
    db.add(history)

    # 更新订单状态
    order.status = "testing"
    order.started_at = datetime.utcnow()

    db.commit()

    return Response.success(message="已开始检测")


@router.post("/my/orders/{order_id}/upload-report", summary="上传检测报告")
async def upload_report(
    order_id: int,
    data: UploadReportRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """上传检测报告或原始数据"""
    lab = db.query(Laboratory).filter(
        Laboratory.admin_user_id == current_user.id
    ).first()

    if not lab:
        raise HTTPException(status_code=404, detail="您暂无管理的实验室")

    order = db.query(Order).filter(
        Order.id == order_id,
        Order.assigned_lab_id == lab.id
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")

    if order.status not in ["testing", "data_uploaded"]:
        raise HTTPException(status_code=400, detail="订单状态不允许此操作")

    # 创建报告记录
    report = Report(
        order_id=order_id,
        order_no=order.order_no,
        user_id=order.user_id,
        laboratory_id=lab.id,
        report_type=data.report_type,
        file_url=data.file_url,
        file_name=data.file_name,
        status="uploaded",
        uploader_id=current_user.id,
        remark=data.remark
    )
    db.add(report)

    # 记录状态变更
    history = OrderStatusHistory(
        order_id=order_id,
        from_status=order.status,
        to_status="data_uploaded",
        operator_id=current_user.id,
        operator_type="lab",
        remark=f"上传{data.report_type}: {data.file_name}"
    )
    db.add(history)

    # 更新订单状态
    if order.status == "testing":
        order.status = "data_uploaded"

    db.commit()
    db.refresh(report)

    return Response.success(data={"report_id": report.id}, message="报告上传成功")


@router.post("/my/orders/{order_id}/complete", summary="完成检测")
async def complete_testing(
    order_id: int,
    data: OrderActionRequest = Body(default=OrderActionRequest()),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """标记检测完成"""
    lab = db.query(Laboratory).filter(
        Laboratory.admin_user_id == current_user.id
    ).first()

    if not lab:
        raise HTTPException(status_code=404, detail="您暂无管理的实验室")

    order = db.query(Order).filter(
        Order.id == order_id,
        Order.assigned_lab_id == lab.id
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")

    if order.status not in ["testing", "data_uploaded"]:
        raise HTTPException(status_code=400, detail="订单状态不允许此操作")

    # 检查是否已上传报告
    report_count = db.query(Report).filter(
        Report.order_id == order_id,
        Report.report_type == "test_report"
    ).count()

    if report_count == 0:
        raise HTTPException(status_code=400, detail="请先上传检测报告")

    # 记录状态变更
    history = OrderStatusHistory(
        order_id=order_id,
        from_status=order.status,
        to_status="completed",
        operator_id=current_user.id,
        operator_type="lab",
        remark=data.remark or "检测完成"
    )
    db.add(history)

    # 更新订单状态
    order.status = "completed"
    order.completed_at = datetime.utcnow()

    # 更新实验室统计
    lab.completed_orders = (lab.completed_orders or 0) + 1

    db.commit()

    return Response.success(message="检测已完成")


@router.get("/my/statistics", summary="获取实验室统计数据")
async def get_lab_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取实验室订单统计"""
    lab = db.query(Laboratory).filter(
        Laboratory.admin_user_id == current_user.id
    ).first()

    if not lab:
        raise HTTPException(status_code=404, detail="您暂无管理的实验室")

    # 统计各状态订单数量
    pending_count = db.query(Order).filter(
        Order.assigned_lab_id == lab.id,
        Order.status.in_(["assigned", "pending_assign"])
    ).count()

    accepted_count = db.query(Order).filter(
        Order.assigned_lab_id == lab.id,
        Order.status == "accepted"
    ).count()

    testing_count = db.query(Order).filter(
        Order.assigned_lab_id == lab.id,
        Order.status.in_(["testing", "data_uploaded"])
    ).count()

    completed_count = db.query(Order).filter(
        Order.assigned_lab_id == lab.id,
        Order.status == "completed"
    ).count()

    # 本月收入统计
    from datetime import date
    today = date.today()
    month_start = today.replace(day=1)

    monthly_income = db.query(func.sum(Order.total_fee)).filter(
        Order.assigned_lab_id == lab.id,
        Order.status == "completed",
        Order.completed_at >= month_start
    ).scalar() or 0

    return Response.success(data={
        "pending_count": pending_count,
        "accepted_count": accepted_count,
        "testing_count": testing_count,
        "completed_count": completed_count,
        "total_orders": lab.total_orders or 0,
        "total_completed": lab.completed_orders or 0,
        "rating": float(lab.rating) if lab.rating else 5.0,
        "monthly_income": float(monthly_income),
        "commission_rate": float(lab.commission_rate) if lab.commission_rate else 20.0,
        "balance": float(lab.balance) if lab.balance else 0
    })
