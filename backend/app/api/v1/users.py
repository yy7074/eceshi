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


@router.get("/list", summary="获取用户列表（管理员）")
async def get_users_list(
    page: int = 1,
    page_size: int = 20,
    search: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取用户列表（仅管理员可用）
    
    - page: 页码，从1开始
    - page_size: 每页数量，默认20
    - search: 搜索关键词（手机号、昵称）
    """
    # 构建查询
    query = db.query(User)
    
    # 搜索过滤
    if search:
        query = query.filter(
            (User.phone.like(f"%{search}%")) | 
            (User.nickname.like(f"%{search}%"))
        )
    
    # 总数
    total = query.count()
    
    # 分页
    offset = (page - 1) * page_size
    users = query.order_by(User.created_at.desc()).offset(offset).limit(page_size).all()
    
    # 转换为字典
    users_data = []
    for user in users:
        users_data.append({
            "id": user.id,
            "phone": user.phone,
            "nickname": user.nickname,
            "avatar": user.avatar,
            "email": user.email,
            "wechat_openid": user.wechat_openid,
            "is_certified": user.is_certified,
            "membership_level": user.membership_level.value,
            "credit_limit": float(user.credit_limit),
            "used_credit": float(user.used_credit),
            "prepaid_balance": float(user.prepaid_balance),
            "points_balance": user.points_balance,
            "total_spent": float(user.total_spent),
            "total_orders": user.total_orders,
            "status": user.status.value,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "last_login_at": user.last_login_at.isoformat() if user.last_login_at else None
        })
    
    return Response.success(data={
        "list": users_data,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size
    })


@router.get("/{user_id}", summary="获取用户详情（管理员）")
async def get_user_detail(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取指定用户的详细信息（仅管理员可用）"""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    return Response.success(data={
        "id": user.id,
        "phone": user.phone,
        "nickname": user.nickname,
        "avatar": user.avatar,
        "email": user.email,
        "wechat_openid": user.wechat_openid,
        "wechat_unionid": user.wechat_unionid,
        "is_certified": user.is_certified,
        "real_name": user.real_name,
        "id_card": user.id_card,
        "membership_level": user.membership_level.value,
        "credit_limit": float(user.credit_limit),
        "used_credit": float(user.used_credit),
        "prepaid_balance": float(user.prepaid_balance),
        "points_balance": user.points_balance,
        "total_points_earned": user.total_points_earned,
        "total_points_used": user.total_points_used,
        "total_spent": float(user.total_spent),
        "total_orders": user.total_orders,
        "status": user.status.value,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "updated_at": user.updated_at.isoformat() if user.updated_at else None,
        "last_login_at": user.last_login_at.isoformat() if user.last_login_at else None
    })


@router.put("/{user_id}/status", summary="更新用户状态（管理员）")
async def update_user_status(
    user_id: int,
    status: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    更新用户状态（仅管理员可用）
    
    - status: active（激活）/ inactive（未激活）/ banned（禁用）
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 更新状态
    from app.models.user import UserStatus
    if status == "active":
        user.status = UserStatus.ACTIVE
    elif status == "inactive":
        user.status = UserStatus.INACTIVE
    elif status == "banned":
        user.status = UserStatus.BANNED
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的状态值"
        )
    
    db.commit()
    
    return Response.success(message="状态更新成功")

