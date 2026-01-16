"""
API依赖项
全局依赖，如用户认证、权限验证等
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User


# HTTP Bearer认证方案
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    获取当前登录用户
    从JWT令牌中解析用户信息
    """
    token = credentials.credentials
    
    # 解码JWT令牌
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证令牌",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 获取用户ID
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的令牌数据",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 查询用户
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 检查用户状态
    if user.status.value != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账号已被禁用"
        )
    
    return user


async def get_current_certified_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    获取已实名认证的用户
    某些接口需要用户完成实名认证才能访问
    """
    if not current_user.is_certified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要完成实名认证"
        )

    return current_user


# 可选的Bearer认证
security_optional = HTTPBearer(auto_error=False)


async def get_current_user_optional(
    credentials: HTTPAuthorizationCredentials = Depends(security_optional),
    db: Session = Depends(get_db)
) -> User:
    """
    可选的用户认证
    如果提供了有效的令牌则返回用户，否则返回None
    用于同时支持登录和未登录用户的接口
    """
    if not credentials:
        return None

    token = credentials.credentials

    # 解码JWT令牌
    payload = decode_access_token(token)
    if not payload:
        return None

    # 获取用户ID
    user_id = payload.get("user_id")
    if not user_id:
        return None

    # 查询用户
    user = db.query(User).filter(User.id == user_id).first()
    if not user or user.status.value != "active":
        return None

    return user

