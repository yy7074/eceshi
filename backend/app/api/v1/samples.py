"""样品追踪API"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db
from app.core.response import success_response, error_response
from app.models.sample import SampleTracking, SampleLogistics
from app.models.order import Order
from app.models.user import User
from app.api.v1.deps import get_current_user

router = APIRouter()


class LogisticsRequest(BaseModel):
    company: str
    tracking_no: str
    sender_name: Optional[str] = None
    sender_phone: Optional[str] = None
    sender_address: Optional[str] = None


@router.get("/order/{order_id}/status")
async def get_sample_status(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取样品状态"""
    # 验证订单归属
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    
    if not order:
        return error_response(message="订单不存在")
    
    # 获取追踪记录
    trackings = db.query(SampleTracking).filter(
        SampleTracking.order_id == order_id
    ).order_by(SampleTracking.created_at.desc()).all()
    
    # 获取物流信息
    logistics = db.query(SampleLogistics).filter(
        SampleLogistics.order_id == order_id
    ).order_by(SampleLogistics.created_at.desc()).first()
    
    # 如果没有追踪记录，返回默认状态
    if not trackings:
        current_status = get_default_status(order.status)
        trackings_data = [current_status]
    else:
        trackings_data = [
            {
                "id": t.id,
                "status": t.status,
                "status_text": t.status_text,
                "location": t.location,
                "operator": t.operator,
                "remark": t.remark,
                "created_at": t.created_at.strftime("%Y-%m-%d %H:%M:%S") if t.created_at else None
            }
            for t in trackings
        ]
    
    logistics_data = None
    if logistics:
        logistics_data = {
            "id": logistics.id,
            "logistics_type": logistics.logistics_type,
            "company": logistics.company,
            "tracking_no": logistics.tracking_no,
            "sender_name": logistics.sender_name,
            "sender_phone": logistics.sender_phone,
            "receiver_name": logistics.receiver_name,
            "receiver_phone": logistics.receiver_phone,
            "status": logistics.status
        }
    
    return success_response(data={
        "order_id": order_id,
        "order_no": order.order_no,
        "order_status": order.status,
        "trackings": trackings_data,
        "logistics": logistics_data
    })


@router.get("/order/{order_id}/timeline")
async def get_sample_timeline(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取样品追踪时间线"""
    # 验证订单归属
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    
    if not order:
        return error_response(message="订单不存在")
    
    # 获取追踪记录
    trackings = db.query(SampleTracking).filter(
        SampleTracking.order_id == order_id
    ).order_by(SampleTracking.created_at.asc()).all()
    
    # 生成时间线
    timeline = []
    
    # 添加订单创建
    timeline.append({
        "status": "created",
        "status_text": "订单创建",
        "time": order.created_at.strftime("%Y-%m-%d %H:%M:%S") if order.created_at else None,
        "is_completed": True
    })
    
    # 定义状态流程
    status_flow = [
        ("paid", "订单支付", order.status in ["paid", "confirmed", "testing", "completed"]),
        ("sample_sent", "样品寄出", any(t.status == "sample_sent" for t in trackings)),
        ("sample_received", "样品签收", any(t.status == "sample_received" for t in trackings)),
        ("testing", "检测中", order.status in ["testing", "completed"]),
        ("completed", "检测完成", order.status == "completed")
    ]
    
    for status, text, is_completed in status_flow:
        tracking = next((t for t in trackings if t.status == status), None)
        timeline.append({
            "status": status,
            "status_text": text,
            "time": tracking.created_at.strftime("%Y-%m-%d %H:%M:%S") if tracking and tracking.created_at else None,
            "is_completed": is_completed,
            "remark": tracking.remark if tracking else None
        })
    
    return success_response(data={
        "order_id": order_id,
        "order_no": order.order_no,
        "timeline": timeline
    })


@router.post("/order/{order_id}/logistics")
async def submit_logistics(
    order_id: int,
    request: LogisticsRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """提交物流信息"""
    # 验证订单归属
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    
    if not order:
        return error_response(message="订单不存在")
    
    # 创建物流记录
    logistics = SampleLogistics(
        order_id=order_id,
        logistics_type="send",
        company=request.company,
        tracking_no=request.tracking_no,
        sender_name=request.sender_name or current_user.nickname,
        sender_phone=request.sender_phone or current_user.phone,
        sender_address=request.sender_address,
        receiver_name="科研检测实验室",
        receiver_phone="400-123-4567",
        receiver_address="北京市海淀区科技园区xxx号",
        status="shipped"
    )
    db.add(logistics)
    
    # 添加追踪记录
    tracking = SampleTracking(
        order_id=order_id,
        order_no=order.order_no,
        status="sample_sent",
        status_text="样品已寄出",
        location=request.sender_address,
        operator=current_user.nickname,
        remark=f"快递公司：{request.company}，快递单号：{request.tracking_no}"
    )
    db.add(tracking)
    
    db.commit()
    
    return success_response(message="物流信息已提交")


def get_default_status(order_status: str) -> dict:
    """根据订单状态返回默认样品状态"""
    status_map = {
        "unpaid": {"status": "pending", "status_text": "待支付", "location": None, "operator": "系统"},
        "paid": {"status": "wait_send", "status_text": "等待寄样", "location": None, "operator": "系统"},
        "confirmed": {"status": "wait_send", "status_text": "等待寄样", "location": None, "operator": "系统"},
        "testing": {"status": "testing", "status_text": "检测中", "location": "实验室", "operator": "实验室"},
        "completed": {"status": "completed", "status_text": "检测完成", "location": "实验室", "operator": "系统"}
    }
    return status_map.get(order_status, {"status": "unknown", "status_text": "未知状态", "location": None, "operator": None})

