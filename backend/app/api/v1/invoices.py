"""
发票管理API
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
import uuid

from app.core.database import get_db
from app.core.response import Response
from app.api.v1.deps import get_current_user
from app.models.user import User
from app.models.invoice import Invoice, InvoiceType, InvoiceStatus


router = APIRouter()


class InvoiceApplyRequest(BaseModel):
    """发票申请请求"""
    title_type: str = "personal"  # personal/company
    title: str  # 发票抬头
    tax_number: Optional[str] = None  # 税号
    bank_name: Optional[str] = None  # 开户银行
    bank_account: Optional[str] = None  # 银行账号
    company_address: Optional[str] = None  # 公司地址
    company_phone: Optional[str] = None  # 公司电话
    content: str = "检测服务费"  # 发票内容
    amount: float  # 开票金额
    order_ids: Optional[List[int]] = None  # 关联订单ID
    receiver_email: Optional[str] = None  # 接收邮箱
    receiver_phone: Optional[str] = None  # 接收手机号
    receiver_address: Optional[str] = None  # 邮寄地址


@router.post("/apply", summary="申请开票")
async def apply_invoice(
    data: InvoiceApplyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """用户申请开票"""
    # 验证抬头类型
    if data.title_type == "company" and not data.tax_number:
        raise HTTPException(status_code=400, detail="企业发票需要填写税号")
    
    # 生成发票申请编号
    invoice_no = f"INV{datetime.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:6].upper()}"
    
    # 创建发票申请
    invoice = Invoice(
        invoice_no=invoice_no,
        user_id=current_user.id,
        invoice_type=InvoiceType.NORMAL,
        title_type=data.title_type,
        title=data.title,
        tax_number=data.tax_number,
        bank_name=data.bank_name,
        bank_account=data.bank_account,
        company_address=data.company_address,
        company_phone=data.company_phone,
        content=data.content,
        amount=data.amount,
        order_ids=str(data.order_ids) if data.order_ids else None,
        receiver_email=data.receiver_email,
        receiver_phone=data.receiver_phone,
        receiver_address=data.receiver_address,
        status=InvoiceStatus.PENDING
    )
    
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    
    return Response.success(
        data={"id": invoice.id, "invoice_no": invoice.invoice_no},
        message="发票申请提交成功"
    )


@router.get("/list", summary="获取发票列表")
async def get_invoices(
    status: Optional[str] = Query(None, description="状态筛选"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取我的发票列表"""
    query = db.query(Invoice).filter(Invoice.user_id == current_user.id)
    
    if status:
        query = query.filter(Invoice.status == status)
    
    total = query.count()
    invoices = query.order_by(desc(Invoice.created_at)).offset((page - 1) * page_size).limit(page_size).all()
    
    return Response.success(data={
        "items": [
            {
                "id": inv.id,
                "invoice_no": inv.invoice_no,
                "title": inv.title,
                "title_type": inv.title_type,
                "amount": float(inv.amount) if inv.amount else 0,
                "content": inv.content,
                "status": inv.status.value if inv.status else None,
                "status_text": get_status_text(inv.status),
                "invoice_url": inv.invoice_url,
                "created_at": inv.created_at.isoformat() if inv.created_at else None,
                "issued_at": inv.issued_at.isoformat() if inv.issued_at else None,
                "reject_reason": inv.reject_reason
            }
            for inv in invoices
        ],
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.get("/{invoice_id}", summary="获取发票详情")
async def get_invoice_detail(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取发票详情"""
    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id,
        Invoice.user_id == current_user.id
    ).first()
    
    if not invoice:
        raise HTTPException(status_code=404, detail="发票不存在")
    
    return Response.success(data={
        "id": invoice.id,
        "invoice_no": invoice.invoice_no,
        "invoice_type": invoice.invoice_type.value if invoice.invoice_type else None,
        "title_type": invoice.title_type,
        "title": invoice.title,
        "tax_number": invoice.tax_number,
        "bank_name": invoice.bank_name,
        "bank_account": invoice.bank_account,
        "company_address": invoice.company_address,
        "company_phone": invoice.company_phone,
        "content": invoice.content,
        "amount": float(invoice.amount) if invoice.amount else 0,
        "receiver_email": invoice.receiver_email,
        "receiver_phone": invoice.receiver_phone,
        "receiver_address": invoice.receiver_address,
        "invoice_code": invoice.invoice_code,
        "invoice_number": invoice.invoice_number,
        "invoice_url": invoice.invoice_url,
        "status": invoice.status.value if invoice.status else None,
        "status_text": get_status_text(invoice.status),
        "reject_reason": invoice.reject_reason,
        "created_at": invoice.created_at.isoformat() if invoice.created_at else None,
        "reviewed_at": invoice.reviewed_at.isoformat() if invoice.reviewed_at else None,
        "issued_at": invoice.issued_at.isoformat() if invoice.issued_at else None
    })


@router.get("/invoiceable/orders", summary="获取可开票订单")
async def get_invoiceable_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取可开票的订单列表"""
    from app.models.order import Order
    
    # 查询已完成且未开票的订单
    orders = db.query(Order).filter(
        Order.user_id == current_user.id,
        Order.status == "completed"
        # 可以添加未开票的条件
    ).order_by(desc(Order.completed_at)).all()
    
    return Response.success(data={
        "items": [
            {
                "id": o.id,
                "order_no": o.order_no,
                "project_name": o.project_name,
                "total_fee": float(o.total_fee) if o.total_fee else 0,
                "completed_at": o.completed_at.isoformat() if o.completed_at else None
            }
            for o in orders
        ]
    })


def get_status_text(status):
    """获取状态文本"""
    if not status:
        return "未知"
    status_map = {
        InvoiceStatus.PENDING: "待审核",
        InvoiceStatus.APPROVED: "已通过",
        InvoiceStatus.REJECTED: "已拒绝",
        InvoiceStatus.ISSUED: "已开票"
    }
    return status_map.get(status, "未知")

