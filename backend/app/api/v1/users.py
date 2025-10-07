"""
用户相关API
用户信息、实名认证、会员管理等
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.response import Response
from app.models.user import User, UserCertification
from app.schemas.user import UserInfo, UserUpdate, CertificationRequest, CertificationResponse
from app.api.deps import get_current_user


router = APIRouter()


@router.get("/me", response_model=UserInfo, summary="获取当前用户信息")
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """获取当前登录用户的详细信息"""
    return current_user


@router.put("/me", response_model=UserInfo, summary="更新用户信息")
async def update_user_info(
    request: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新当前用户信息"""
    # 更新用户信息
    if request.nickname is not None:
        current_user.nickname = request.nickname
    if request.avatar is not None:
        current_user.avatar = request.avatar
    if request.email is not None:
        current_user.email = request.email
    
    db.commit()
    db.refresh(current_user)
    
    return current_user


@router.post("/certification", response_model=CertificationResponse, summary="提交实名认证")
async def submit_certification(
    request: CertificationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    提交实名认证申请
    
    1. 检查是否已认证
    2. 创建认证记录
    3. 更新用户表的实名信息
    """
    # 检查是否已认证
    if current_user.is_certified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="您已完成实名认证"
        )
    
    # 检查是否有待审核的认证
    existing_cert = db.query(UserCertification).filter(
        UserCertification.user_id == current_user.id,
        UserCertification.status == "pending"
    ).first()
    
    if existing_cert:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="您有待审核的认证申请"
        )
    
    # 创建认证记录
    certification = UserCertification(
        user_id=current_user.id,
        enrollment_year=request.enrollment_year,
        graduation_year=request.graduation_year,
        province=request.province,
        city=request.city,
        university=request.university,
        department=request.department,
        supervisor_name=request.supervisor_name,
        supervisor_title=request.supervisor_title,
        student_card_photo=request.student_card_photo,
        id_card_front=request.id_card_front,
        id_card_back=request.id_card_back,
        status="pending"
    )
    
    # 更新用户表的真实姓名和身份证
    current_user.real_name = request.real_name
    current_user.id_card = request.id_card
    
    db.add(certification)
    db.commit()
    db.refresh(certification)
    
    return certification


@router.get("/certification", response_model=CertificationResponse, summary="获取认证信息")
async def get_certification(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取当前用户的认证信息"""
    certification = db.query(UserCertification).filter(
        UserCertification.user_id == current_user.id
    ).order_by(UserCertification.created_at.desc()).first()
    
    if not certification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="未找到认证记录"
        )
    
    return certification


@router.get("/balance", summary="获取账户余额")
async def get_balance(
    current_user: User = Depends(get_current_user)
):
    """
    获取账户余额信息
    包括预付余额、信用额度、积分等
    """
    return Response.success(data={
        "prepaid_balance": float(current_user.prepaid_balance),  # 预付余额
        "credit_limit": float(current_user.credit_limit),  # 信用额度
        "used_credit": float(current_user.used_credit),  # 已用信用额度
        "available_credit": float(current_user.credit_limit - current_user.used_credit),  # 可用信用额度
        "points_balance": current_user.points_balance,  # 积分余额
        "membership_level": current_user.membership_level.value  # 会员等级
    })

