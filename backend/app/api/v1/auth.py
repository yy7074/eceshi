"""
认证相关API
用户注册、登录、短信验证码
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.response import Response
from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserRegister, UserLogin, SMSCodeRequest, TokenResponse


router = APIRouter()


@router.post("/send-sms", summary="发送短信验证码")
async def send_sms_code(
    request: SMSCodeRequest,
    db: Session = Depends(get_db)
):
    """
    发送短信验证码
    
    场景:
    - register: 注册
    - login: 登录
    - reset_password: 重置密码
    """
    # TODO: 集成阿里云短信服务
    # 这里先返回模拟验证码（开发环境）
    
    if settings.DEBUG:
        # 开发环境返回固定验证码
        sms_code = "123456"
        # TODO: 存储到Redis，设置5分钟过期
        return Response.success(
            data={"code": sms_code},  # 生产环境不返回验证码
            message="验证码发送成功（开发模式）"
        )
    
    # 生产环境调用短信API
    # sms_service.send_code(request.phone, request.scene)
    
    return Response.success(message="验证码发送成功")


@router.post("/register", response_model=TokenResponse, summary="用户注册")
async def register(
    request: UserRegister,
    db: Session = Depends(get_db)
):
    """
    用户注册
    
    1. 验证短信验证码
    2. 检查手机号是否已注册
    3. 创建用户
    4. 返回JWT令牌
    """
    # TODO: 验证短信验证码（从Redis获取）
    if settings.DEBUG and request.sms_code != "123456":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="验证码错误"
        )
    
    # 检查手机号是否已注册
    existing_user = db.query(User).filter(User.phone == request.phone).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该手机号已注册"
        )
    
    # 创建新用户
    new_user = User(
        phone=request.phone,
        password=get_password_hash(request.password),
        nickname=f"用户{request.phone[-4:]}",  # 默认昵称
        credit_limit=3000.00,  # 初始信用额度3000元
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # 生成JWT令牌
    access_token = create_access_token(
        data={"user_id": new_user.id, "phone": new_user.phone}
    )
    
    return TokenResponse(
        access_token=access_token,
        user_id=new_user.id,
        phone=new_user.phone,
        nickname=new_user.nickname
    )


@router.post("/login", response_model=TokenResponse, summary="用户登录")
async def login(
    request: UserLogin,
    db: Session = Depends(get_db)
):
    """
    用户登录
    
    1. 验证手机号和密码
    2. 返回JWT令牌
    """
    # 查询用户
    user = db.query(User).filter(User.phone == request.phone).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="手机号或密码错误"
        )
    
    # 验证密码
    if not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="手机号或密码错误"
        )
    
    # 检查用户状态
    if user.status.value != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账号已被禁用"
        )
    
    # 更新最后登录时间
    from datetime import datetime
    user.last_login_at = datetime.utcnow()
    db.commit()
    
    # 生成JWT令牌
    access_token = create_access_token(
        data={"user_id": user.id, "phone": user.phone}
    )
    
    return TokenResponse(
        access_token=access_token,
        user_id=user.id,
        phone=user.phone,
        nickname=user.nickname
    )


@router.post("/wechat-login", summary="微信小程序登录")
async def wechat_login(
    code: str,
    db: Session = Depends(get_db)
):
    """
    微信小程序登录
    
    1. 使用code换取openid
    2. 查询或创建用户
    3. 返回JWT令牌
    """
    # TODO: 实现微信登录逻辑
    # 1. 调用微信API获取openid
    # 2. 根据openid查询用户，不存在则创建
    # 3. 返回JWT令牌
    
    return Response.success(message="微信登录功能开发中")

