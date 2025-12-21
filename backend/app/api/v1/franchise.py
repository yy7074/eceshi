"""加盟申请API"""
from typing import List, Optional
from datetime import datetime
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db
from app.core.response import success_response, error_response
from app.models.franchise import FranchiseApplication
from app.models.user import User
from app.api.v1.deps import get_current_user_optional

router = APIRouter()


class FranchiseRequest(BaseModel):
    name: str
    phone: str
    company: Optional[str] = None
    city: Optional[str] = None
    mode: str = "agent"  # agent/partner/lab
    intention: Optional[str] = None


@router.post("/apply")
async def submit_franchise_application(
    request: FranchiseRequest,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """提交加盟申请"""
    # 验证手机号格式
    if not request.phone or len(request.phone) != 11:
        return error_response(message="请输入正确的手机号")
    
    # 检查是否已有待处理的申请
    existing = db.query(FranchiseApplication).filter(
        FranchiseApplication.phone == request.phone,
        FranchiseApplication.status == "pending"
    ).first()
    
    if existing:
        return error_response(message="您已提交过申请，请耐心等待审核")
    
    # 生成申请编号
    application_no = f"FR{datetime.now().strftime('%Y%m%d%H%M%S')}{str(uuid.uuid4())[:4].upper()}"
    
    # 创建申请
    application = FranchiseApplication(
        application_no=application_no,
        name=request.name,
        phone=request.phone,
        company=request.company,
        city=request.city,
        mode=request.mode,
        intention=request.intention,
        status="pending",
        user_id=current_user.id if current_user else None
    )
    
    db.add(application)
    db.commit()
    db.refresh(application)
    
    return success_response(
        message="申请提交成功，我们将在3个工作日内与您联系",
        data={
            "application_no": application_no
        }
    )


@router.get("/my-applications")
async def get_my_applications(
    current_user: User = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """获取我的申请记录"""
    if not current_user:
        return error_response(message="请先登录")
    
    applications = db.query(FranchiseApplication).filter(
        FranchiseApplication.user_id == current_user.id
    ).order_by(FranchiseApplication.created_at.desc()).all()
    
    return success_response(data={
        "items": [
            {
                "id": a.id,
                "application_no": a.application_no,
                "name": a.name,
                "phone": a.phone,
                "company": a.company,
                "city": a.city,
                "mode": a.mode,
                "mode_text": get_mode_text(a.mode),
                "status": a.status,
                "status_text": get_status_text(a.status),
                "created_at": a.created_at.strftime("%Y-%m-%d %H:%M:%S") if a.created_at else None
            }
            for a in applications
        ]
    })


@router.get("/check")
async def check_application_status(
    phone: str = Query(..., description="手机号"),
    db: Session = Depends(get_db)
):
    """查询申请状态"""
    application = db.query(FranchiseApplication).filter(
        FranchiseApplication.phone == phone
    ).order_by(FranchiseApplication.created_at.desc()).first()
    
    if not application:
        return error_response(message="未找到相关申请记录")
    
    return success_response(data={
        "application_no": application.application_no,
        "status": application.status,
        "status_text": get_status_text(application.status),
        "created_at": application.created_at.strftime("%Y-%m-%d %H:%M:%S") if application.created_at else None,
        "contacted_at": application.contacted_at.strftime("%Y-%m-%d %H:%M:%S") if application.contacted_at else None
    })


@router.get("/modes")
async def get_franchise_modes():
    """获取合作模式列表"""
    modes = [
        {
            "code": "agent",
            "name": "区域代理",
            "description": "获得指定区域独家代理权，享受区域内所有订单的返佣",
            "benefits": ["独家区域保护", "最高20%返佣", "专属运营支持"]
        },
        {
            "code": "partner",
            "name": "项目合作",
            "description": "针对特定项目进行深度合作，按项目结算佣金",
            "benefits": ["灵活合作方式", "按项目结算", "低门槛启动"]
        },
        {
            "code": "lab",
            "name": "实验室入驻",
            "description": "实验室直接入驻平台，承接检测订单获取收益",
            "benefits": ["平台流量支持", "订单保障", "技术支持"]
        }
    ]
    
    return success_response(data={"items": modes})


def get_status_text(status: str) -> str:
    """获取状态文本"""
    status_map = {
        "pending": "待审核",
        "contacted": "已联系",
        "approved": "已通过",
        "rejected": "未通过"
    }
    return status_map.get(status, status)


def get_mode_text(mode: str) -> str:
    """获取模式文本"""
    mode_map = {
        "agent": "区域代理",
        "partner": "项目合作",
        "lab": "实验室入驻"
    }
    return mode_map.get(mode, mode)

