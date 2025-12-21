"""报告下载API"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os

from app.core.database import get_db
from app.core.response import success_response, error_response
from app.models.report import Report
from app.models.order import Order
from app.models.user import User
from app.api.v1.deps import get_current_user

router = APIRouter()


@router.get("/list")
async def get_reports(
    status: Optional[str] = Query(None, description="状态"),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取报告列表"""
    query = db.query(Report).filter(Report.user_id == current_user.id)
    
    if status:
        query = query.filter(Report.status == status)
    if keyword:
        query = query.filter(
            (Report.report_no.contains(keyword)) |
            (Report.order_no.contains(keyword)) |
            (Report.project_name.contains(keyword)) |
            (Report.sample_name.contains(keyword))
        )
    
    query = query.order_by(Report.created_at.desc())
    
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return success_response(data={
        "items": [
            {
                "id": r.id,
                "report_no": r.report_no,
                "order_id": r.order_id,
                "order_no": r.order_no,
                "project_name": r.project_name,
                "sample_name": r.sample_name,
                "status": r.status,
                "status_text": get_status_text(r.status),
                "file_url": r.file_url,
                "file_size": format_file_size(r.file_size) if r.file_size else None,
                "download_count": r.download_count,
                "completed_at": r.completed_at.strftime("%Y-%m-%d %H:%M:%S") if r.completed_at else None,
                "created_at": r.created_at.strftime("%Y-%m-%d %H:%M:%S") if r.created_at else None
            }
            for r in items
        ],
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.get("/{report_id}")
async def get_report_detail(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取报告详情"""
    report = db.query(Report).filter(
        Report.id == report_id,
        Report.user_id == current_user.id
    ).first()
    
    if not report:
        return error_response(message="报告不存在")
    
    return success_response(data={
        "id": report.id,
        "report_no": report.report_no,
        "order_id": report.order_id,
        "order_no": report.order_no,
        "project_name": report.project_name,
        "sample_name": report.sample_name,
        "status": report.status,
        "status_text": get_status_text(report.status),
        "file_url": report.file_url,
        "file_size": format_file_size(report.file_size) if report.file_size else None,
        "download_count": report.download_count,
        "completed_at": report.completed_at.strftime("%Y-%m-%d %H:%M:%S") if report.completed_at else None,
        "created_at": report.created_at.strftime("%Y-%m-%d %H:%M:%S") if report.created_at else None
    })


@router.get("/order/{order_id}")
async def get_report_by_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """根据订单获取报告"""
    # 验证订单归属
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    
    if not order:
        return error_response(message="订单不存在")
    
    report = db.query(Report).filter(Report.order_id == order_id).first()
    
    if not report:
        return error_response(message="报告尚未生成")
    
    return success_response(data={
        "id": report.id,
        "report_no": report.report_no,
        "status": report.status,
        "status_text": get_status_text(report.status),
        "file_url": report.file_url,
        "completed_at": report.completed_at.strftime("%Y-%m-%d %H:%M:%S") if report.completed_at else None
    })


@router.post("/{report_id}/download")
async def download_report(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """下载报告"""
    report = db.query(Report).filter(
        Report.id == report_id,
        Report.user_id == current_user.id
    ).first()
    
    if not report:
        return error_response(message="报告不存在")
    
    if report.status != "completed":
        return error_response(message="报告尚未完成")
    
    if not report.file_url:
        return error_response(message="报告文件不存在")
    
    # 增加下载次数
    report.download_count = (report.download_count or 0) + 1
    db.commit()
    
    return success_response(data={
        "download_url": report.file_url,
        "file_name": f"检测报告_{report.report_no}.pdf"
    })


def get_status_text(status: str) -> str:
    """获取状态文本"""
    status_map = {
        "pending": "待生成",
        "processing": "生成中",
        "completed": "已完成"
    }
    return status_map.get(status, status)


def format_file_size(size: int) -> str:
    """格式化文件大小"""
    if size < 1024:
        return f"{size}B"
    elif size < 1024 * 1024:
        return f"{size / 1024:.1f}KB"
    else:
        return f"{size / 1024 / 1024:.1f}MB"

