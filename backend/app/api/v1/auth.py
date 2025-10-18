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
from app.schemas.user import UserRegister, UserLogin, SMSCodeRequest, SMSLoginRequest, WechatLoginRequest, TokenResponse
from app.services.sms_service import sms_service
from app.services.wechat_service import wechat_service


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
    # 如果是注册场景，检查手机号是否已注册
    if request.scene == "register":
        existing_user = db.query(User).filter(User.phone == request.phone).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该手机号已注册"
            )
    
    # login场景：不检查用户是否存在，支持自动注册
    # reset_password场景：检查用户是否存在
    if request.scene == "reset_password":
        existing_user = db.query(User).filter(User.phone == request.phone).first()
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该手机号未注册"
            )
    
    # 发送短信验证码
    result = await sms_service.send_verification_code(
        phone=request.phone,
        db=db,
        scene=request.scene
    )
    
    if result["success"]:
        # 开发环境返回验证码
        if settings.DEBUG and "code" in result:
            return Response.success(
                data={"code": result["code"]},
                message=result["message"]
            )
        return Response.success(message=result["message"])
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["message"]
        )


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
    # 验证短信验证码
    is_valid = await sms_service.verify_code(
        phone=request.phone,
        code=request.sms_code,
        db=db,
        scene="register"
    )
    
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="验证码错误或已过期"
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


@router.post("/sms-login", response_model=TokenResponse, summary="短信验证码登录")
async def sms_login(
    request: SMSLoginRequest,
    db: Session = Depends(get_db)
):
    """
    短信验证码登录
    
    1. 验证短信验证码
    2. 查找用户，不存在则自动注册
    3. 返回JWT令牌
    """
    # 验证短信验证码
    is_valid = await sms_service.verify_code(
        phone=request.phone,
        code=request.sms_code,
        db=db,
        scene="login"
    )
    
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="验证码错误或已过期"
        )
    
    # 查找用户
    user = db.query(User).filter(User.phone == request.phone).first()
    
    # 如果用户不存在，自动注册
    if not user:
        # 生成随机密码（用户不会用到，后续可以通过"重置密码"功能设置）
        import time
        random_password = f"sms_{request.phone}_{int(time.time())}"
        
        user = User(
            phone=request.phone,
            password=get_password_hash(random_password),
            nickname=f"用户{request.phone[-4:]}",
            credit_limit=3000.00
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
    
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


@router.post("/wechat-login", response_model=TokenResponse, summary="微信小程序登录")
async def wechat_login(
    request: WechatLoginRequest,
    db: Session = Depends(get_db)
):
    """
    微信小程序登录
    
    1. 使用code换取openid
    2. 查询或创建用户
    3. 返回JWT令牌
    """
    # 1. 调用微信API获取openid
    session_data = await wechat_service.code_to_session(request.code)
    
    if "errcode" in session_data and session_data["errcode"] != 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"微信登录失败: {session_data.get('errmsg', '未知错误')}"
        )
    
    openid = session_data.get("openid")
    unionid = session_data.get("unionid")
    
    if not openid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="获取微信OpenID失败"
        )
    
    # 2. 根据openid查询用户
    user = db.query(User).filter(User.wechat_openid == openid).first()
    
    # 如果用户不存在，自动创建
    if not user:
        import time
        user = User(
            wechat_openid=openid,
            wechat_unionid=unionid,
            nickname=f"微信用户{openid[-6:]}",
            credit_limit=3000.00
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
    
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
    
    # 3. 生成JWT令牌
    access_token = create_access_token(
        data={"user_id": user.id, "openid": openid}
    )
    
    return TokenResponse(
        access_token=access_token,
        user_id=user.id,
        phone=user.phone,
        nickname=user.nickname
    )

