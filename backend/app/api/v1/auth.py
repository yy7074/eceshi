"""
认证相关API
用户注册、登录、短信验证码
"""
import base64
import json
import secrets
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from pydantic import BaseModel

from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.response import Response
from app.core.config import settings
from app.core.redis_client import get_redis
from app.models.user import User
from app.schemas.user import UserRegister, UserLogin, SMSCodeRequest, SMSLoginRequest, WechatLoginRequest
from app.services.sms_service import sms_service
from app.services.wechat_service import wechat_service
from app.api.v1.invites import bind_invite_relation


router = APIRouter()

QRCODE_SESSION_TTL = 300  # 5 分钟
QRCODE_REDIS_PREFIX = "qrlogin:"


def _qr_key(session_id: str) -> str:
    return f"{QRCODE_REDIS_PREFIX}{session_id}"


class AdminLoginRequest(BaseModel):
    """管理员登录请求"""
    username: str
    password: str


class QrcodeConfirmRequest(BaseModel):
    """小程序扫码后确认登录"""
    session_id: str
    code: str


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


@router.post("/register", summary="用户注册")
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

    bind_invite_relation(
        db,
        invitee=new_user,
        invite_code=request.invite_code,
        inviter_id=request.inviter_id
    )
    db.commit()
    
    # 生成JWT令牌
    access_token = create_access_token(
        data={"user_id": new_user.id, "phone": new_user.phone}
    )
    
    return Response.success(
        data={
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": new_user.id,
            "phone": new_user.phone,
            "nickname": new_user.nickname,
        },
        message="注册成功"
    )


@router.post("/login", summary="用户登录")
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
    bind_invite_relation(
        db,
        invitee=user,
        invite_code=request.invite_code,
        inviter_id=request.inviter_id
    )
    db.commit()
    
    # 生成JWT令牌
    access_token = create_access_token(
        data={"user_id": user.id, "phone": user.phone}
    )
    
    return Response.success(
        data={
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user.id,
            "phone": user.phone,
            "nickname": user.nickname,
        },
        message="登录成功"
    )


@router.post("/sms-login", summary="短信验证码登录")
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
    bind_invite_relation(
        db,
        invitee=user,
        invite_code=request.invite_code,
        inviter_id=request.inviter_id
    )
    db.commit()
    
    # 生成JWT令牌
    access_token = create_access_token(
        data={"user_id": user.id, "phone": user.phone}
    )
    
    print(f"[短信登录] 用户 {user.id} ({user.phone}) 登录成功，生成token")
    
    # 返回响应（使用Response.success包装，确保前端能正确解析）
    return Response.success(data={
        "access_token": access_token,
        "user_id": user.id,
        "phone": user.phone,
        "nickname": user.nickname
    })


@router.post("/wechat-login", summary="微信小程序登录")
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
    
    phone_number = None
    if request.phone_code:
        phone_data = await wechat_service.get_phone_number(request.phone_code)
        if phone_data.get("errcode", 0) != 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"获取微信手机号失败: {phone_data.get('errmsg', '请重新授权')}"
            )
        phone_info = phone_data.get("phone_info") or {}
        phone_number = phone_info.get("purePhoneNumber") or phone_info.get("phoneNumber")

    # 2. 根据 openid/手机号 查询或创建用户
    openid_user = db.query(User).filter(User.wechat_openid == openid).first()
    phone_user = db.query(User).filter(User.phone == phone_number).first() if phone_number else None

    if phone_user and openid_user and phone_user.id != openid_user.id:
        if phone_user.wechat_openid and phone_user.wechat_openid != openid:
            raise HTTPException(status_code=400, detail="该手机号已绑定其他微信账号")
        # 优先复用已有手机号账号；释放旧的微信临时账号 openid 绑定。
        openid_user.wechat_openid = None
        openid_user.wechat_unionid = None
        phone_user.wechat_openid = openid
        phone_user.wechat_unionid = unionid
        user = phone_user
    elif phone_user:
        user = phone_user
        user.wechat_openid = user.wechat_openid or openid
        user.wechat_unionid = user.wechat_unionid or unionid
    elif openid_user:
        user = openid_user
        if phone_number and not user.phone:
            user.phone = phone_number
            user.nickname = user.nickname or f"用户{phone_number[-4:]}"
    else:
        user = User(
            phone=phone_number,
            wechat_openid=openid,
            wechat_unionid=unionid,
            nickname=f"用户{phone_number[-4:]}" if phone_number else f"微信用户{openid[-6:]}",
            credit_limit=3000.00
        )
        db.add(user)
        db.flush()
    
    # 检查用户状态
    if user.status.value != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账号已被禁用"
        )
    
    # 更新最后登录时间
    from datetime import datetime
    user.last_login_at = datetime.utcnow()
    bind_invite_relation(
        db,
        invitee=user,
        invite_code=request.invite_code,
        inviter_id=request.inviter_id
    )
    db.commit()
    db.refresh(user)
    
    # 3. 生成JWT令牌
    access_token = create_access_token(
        data={"user_id": user.id, "phone": user.phone, "openid": openid}
    )
    
    return Response.success(
        data={
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user.id,
            "phone": user.phone,
            "nickname": user.nickname
        },
        message="登录成功"
    )


@router.post("/admin-login", summary="管理员登录")
async def admin_login(
    request: AdminLoginRequest,
    db: Session = Depends(get_db)
):
    """管理员登录（用户名+密码）。"""
    username = (request.username or "").strip()
    password = request.password or ""

    admin_user = db.query(User).filter(User.phone == username).first()

    if (
        not admin_user
        and username == settings.ADMIN_USERNAME
        and settings.ADMIN_BOOTSTRAP_PASSWORD
    ):
        admin_user = User(
            phone=username,
            password=get_password_hash(settings.ADMIN_BOOTSTRAP_PASSWORD),
            nickname="管理员",
            credit_limit=999999.00,
            is_certified=True,
            is_admin=True
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

    if (
        not admin_user
        or not (admin_user.is_admin or admin_user.phone == settings.ADMIN_USERNAME)
        or not admin_user.password
        or not verify_password(password, admin_user.password)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )

    if admin_user.phone == settings.ADMIN_USERNAME and not admin_user.is_admin:
        admin_user.is_admin = True

    if admin_user.status.value != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账号已被禁用"
        )

    from datetime import datetime
    admin_user.last_login_at = datetime.utcnow()
    db.commit()

    access_token = create_access_token(
        data={"user_id": admin_user.id, "phone": admin_user.phone, "is_admin": True}
    )

    return Response.success(
        data={
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": admin_user.id,
            "phone": admin_user.phone,
            "nickname": admin_user.nickname,
            "is_admin": True
        },
        message="登录成功"
    )


@router.post("/qrcode/create", summary="创建扫码登录会话并返回二维码")
async def create_qrcode_login():
    """
    PC 网页端调用。
    - 生成 session_id
    - 用 session_id 作为 scene 调微信拿带参小程序码
    - 返回 session_id + 二维码 base64
    """
    session_id = secrets.token_hex(16)  # 32 个 0-9a-f 字符，100% 符合微信 scene 字符集
    r = get_redis()
    r.setex(
        _qr_key(session_id),
        QRCODE_SESSION_TTL,
        json.dumps({"status": "pending", "token": None, "user": None}),
    )

    try:
        qrcode_bytes = await wechat_service.get_unlimited_qrcode(
            scene=session_id,
            page="pages/login/login",
        )
    except RuntimeError as e:
        r.delete(_qr_key(session_id))
        raise HTTPException(status_code=500, detail=str(e))

    qrcode_b64 = base64.b64encode(qrcode_bytes).decode()
    # 微信返回通常是 JPEG；用 image/jpeg 前缀，浏览器也能识别其它类型
    return Response.success(data={
        "session_id": session_id,
        "qrcode": f"data:image/jpeg;base64,{qrcode_b64}",
        "expires_in": QRCODE_SESSION_TTL,
    })


@router.get("/qrcode/poll", summary="网页轮询扫码登录状态")
async def poll_qrcode_login(session_id: str):
    """
    status 值：
    - pending：等待扫码
    - confirmed：已扫码并确认，data 里带 token
    - expired：session 已失效
    """
    raw = get_redis().get(_qr_key(session_id))
    if not raw:
        return Response.success(data={"status": "expired"})
    session = json.loads(raw)
    return Response.success(data=session)


@router.post("/qrcode/confirm", summary="小程序扫码后确认登录")
async def confirm_qrcode_login(
    request: QrcodeConfirmRequest,
    db: Session = Depends(get_db),
):
    """
    小程序端 onLoad 拿到 scene（session_id）后调用：
    1. 用 code 换 openid
    2. 查/建用户
    3. 生成 JWT
    4. 把 token 写回 Redis，网页轮询后拿到
    """
    r = get_redis()
    raw = r.get(_qr_key(request.session_id))
    if not raw:
        raise HTTPException(status_code=410, detail="会话已过期，请在网页重新生成二维码")
    session = json.loads(raw)
    if session.get("status") == "confirmed":
        raise HTTPException(status_code=400, detail="该二维码已被使用")

    # 1. code 换 openid
    session_data = await wechat_service.code_to_session(request.code)
    if "errcode" in session_data and session_data["errcode"] != 0:
        raise HTTPException(
            status_code=400,
            detail=f"微信登录失败: errcode={session_data.get('errcode')} {session_data.get('errmsg', '')}",
        )
    openid = session_data.get("openid")
    if not openid:
        raise HTTPException(status_code=400, detail="获取微信 OpenID 失败")

    # 2. 查或建用户
    user = db.query(User).filter(User.wechat_openid == openid).first()
    if not user:
        user = User(
            wechat_openid=openid,
            wechat_unionid=session_data.get("unionid"),
            nickname=f"微信用户{openid[-6:]}",
            credit_limit=3000.00,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    if user.status.value != "active":
        raise HTTPException(status_code=403, detail="账号已被禁用")

    from datetime import datetime
    user.last_login_at = datetime.utcnow()
    db.commit()

    # 3. 生成 token
    token = create_access_token(data={"user_id": user.id, "openid": openid})

    # 4. 写回 Redis（保留剩余 TTL）
    ttl = r.ttl(_qr_key(request.session_id))
    if ttl is None or ttl < 0:
        ttl = 60
    r.setex(
        _qr_key(request.session_id),
        ttl,
        json.dumps({
            "status": "confirmed",
            "token": token,
            "user": {
                "user_id": user.id,
                "nickname": user.nickname,
                "phone": user.phone,
            },
        }),
    )
    return Response.success(message="登录成功，请回到网页")
