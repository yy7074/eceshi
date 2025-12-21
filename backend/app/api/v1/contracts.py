"""合同管理API"""
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.response import success_response, error_response
from app.models.contract import Contract
from app.models.order import Order
from app.models.user import User
from app.api.v1.deps import get_current_user

router = APIRouter()


@router.get("/list")
async def get_contracts(
    status: Optional[str] = Query(None, description="状态"),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取合同列表"""
    query = db.query(Contract).filter(Contract.user_id == current_user.id)
    
    if status:
        query = query.filter(Contract.status == status)
    if keyword:
        query = query.filter(
            (Contract.contract_no.contains(keyword)) |
            (Contract.order_no.contains(keyword)) |
            (Contract.title.contains(keyword))
        )
    
    query = query.order_by(Contract.created_at.desc())
    
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return success_response(data={
        "items": [
            {
                "id": c.id,
                "contract_no": c.contract_no,
                "order_id": c.order_id,
                "order_no": c.order_no,
                "title": c.title,
                "amount": float(c.amount) if c.amount else None,
                "status": c.status,
                "status_text": get_status_text(c.status),
                "signed_at": c.signed_at.strftime("%Y-%m-%d") if c.signed_at else None,
                "expired_at": c.expired_at.strftime("%Y-%m-%d") if c.expired_at else None,
                "file_url": c.file_url,
                "created_at": c.created_at.strftime("%Y-%m-%d %H:%M:%S") if c.created_at else None
            }
            for c in items
        ],
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.get("/{contract_id}")
async def get_contract_detail(
    contract_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取合同详情"""
    contract = db.query(Contract).filter(
        Contract.id == contract_id,
        Contract.user_id == current_user.id
    ).first()
    
    if not contract:
        return error_response(message="合同不存在")
    
    return success_response(data={
        "id": contract.id,
        "contract_no": contract.contract_no,
        "order_id": contract.order_id,
        "order_no": contract.order_no,
        "title": contract.title,
        "content": contract.content,
        "amount": float(contract.amount) if contract.amount else None,
        "status": contract.status,
        "status_text": get_status_text(contract.status),
        "signed_at": contract.signed_at.strftime("%Y-%m-%d") if contract.signed_at else None,
        "expired_at": contract.expired_at.strftime("%Y-%m-%d") if contract.expired_at else None,
        "file_url": contract.file_url,
        "created_at": contract.created_at.strftime("%Y-%m-%d %H:%M:%S") if contract.created_at else None
    })


@router.get("/order/{order_id}")
async def get_contract_by_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """根据订单获取合同"""
    # 验证订单归属
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    
    if not order:
        return error_response(message="订单不存在")
    
    contract = db.query(Contract).filter(Contract.order_id == order_id).first()
    
    if not contract:
        return error_response(message="合同不存在")
    
    return success_response(data={
        "id": contract.id,
        "contract_no": contract.contract_no,
        "title": contract.title,
        "status": contract.status,
        "status_text": get_status_text(contract.status),
        "file_url": contract.file_url,
        "signed_at": contract.signed_at.strftime("%Y-%m-%d") if contract.signed_at else None
    })


@router.post("/{contract_id}/download")
async def download_contract(
    contract_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """下载合同"""
    contract = db.query(Contract).filter(
        Contract.id == contract_id,
        Contract.user_id == current_user.id
    ).first()
    
    if not contract:
        return error_response(message="合同不存在")
    
    if not contract.file_url:
        return error_response(message="合同文件不存在")
    
    return success_response(data={
        "download_url": contract.file_url,
        "file_name": f"合同_{contract.contract_no}.pdf"
    })


def get_status_text(status: str) -> str:
    """获取状态文本"""
    status_map = {
        "draft": "草稿",
        "active": "生效中",
        "expired": "已过期",
        "terminated": "已终止"
    }
    return status_map.get(status, status)

