"""
API依赖注入
"""
from typing import Generator, Optional, List, Callable
from functools import wraps
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session, joinedload

from app.core.config import settings
from app.core.database import SessionLocal
from app.models.user import User


# HTTP Bearer Token
security = HTTPBearer()


def get_db() -> Generator:
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    获取当前登录用户
    从JWT token中解析用户ID并查询用户信息
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 解析token
        token = credentials.credentials
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # 查询用户
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    
    # 检查用户状态（如果状态不是active，返回403）
    if hasattr(user, 'status') and user.status:
        if hasattr(user.status, 'value') and user.status.value != "active":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="账号已被禁用"
            )
    
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    获取当前活跃用户
    验证用户状态是否为活跃
    """
    if current_user.status.value != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户已被禁用"
        )
    return current_user


def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    可选获取当前用户
    如果没有token或token无效，返回None而不是抛出异常
    用于不强制登录但登录后有更多功能的场景
    """
    if credentials is None:
        return None
    
    try:
        token = credentials.credentials
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: int = payload.get("user_id")
        if user_id is None:
            return None
    except JWTError:
        return None
    
    user = db.query(User).filter(User.id == user_id).first()
    return user


def get_current_admin_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    获取当前管理员用户
    验证JWT token中是否包含管理员标识
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # 解析token
        token = credentials.credentials
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: int = payload.get("user_id")
        is_admin: bool = payload.get("is_admin", False)

        if user_id is None or not is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="需要管理员权限"
            )
    except JWTError:
        raise credentials_exception

    # 查询用户（预加载角色和权限）
    user = db.query(User).options(
        joinedload(User.roles)
    ).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception

    # 验证是否是管理员账号（通过is_admin字段或角色）
    if not user.is_admin and user.phone != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )

    return user


def get_user_with_roles(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """获取当前用户及其角色权限"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token = credentials.credentials
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # 预加载角色和权限
    from app.models.role import Role, Permission
    user = db.query(User).options(
        joinedload(User.roles).joinedload(Role.permissions)
    ).filter(User.id == user_id).first()

    if user is None:
        raise credentials_exception

    return user


class PermissionChecker:
    """权限检查器"""

    def __init__(self, required_permissions: List[str], require_all: bool = False):
        """
        Args:
            required_permissions: 所需权限列表
            require_all: True表示需要全部权限，False表示只需其中一个
        """
        self.required_permissions = required_permissions
        self.require_all = require_all

    def __call__(self, user: User = Depends(get_user_with_roles)) -> User:
        """检查用户是否拥有所需权限"""
        # 超级管理员或admin用户跳过权限检查
        if user.is_admin or user.phone == "admin":
            return user

        # 检查是否有super_admin角色
        if user.has_role("super_admin"):
            return user

        user_permissions = user.get_permissions()

        if self.require_all:
            # 需要全部权限
            if not all(p in user_permissions for p in self.required_permissions):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="权限不足"
                )
        else:
            # 只需其中一个权限
            if not any(p in user_permissions for p in self.required_permissions):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="权限不足"
                )

        return user


class RoleChecker:
    """角色检查器"""

    def __init__(self, required_roles: List[str], require_all: bool = False):
        """
        Args:
            required_roles: 所需角色列表
            require_all: True表示需要全部角色，False表示只需其中一个
        """
        self.required_roles = required_roles
        self.require_all = require_all

    def __call__(self, user: User = Depends(get_user_with_roles)) -> User:
        """检查用户是否拥有所需角色"""
        # 超级管理员或admin用户跳过角色检查
        if user.is_admin or user.phone == "admin":
            return user

        if self.require_all:
            if not all(user.has_role(r) for r in self.required_roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="角色权限不足"
                )
        else:
            if not any(user.has_role(r) for r in self.required_roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="角色权限不足"
                )

        return user


# 常用权限检查器实例
require_user_management = PermissionChecker(["user:view", "user:edit"])
require_order_management = PermissionChecker(["order:view", "order:edit"])
require_order_assign = PermissionChecker(["order:assign"])
require_finance_view = PermissionChecker(["finance:view"])
require_lab_management = PermissionChecker(["lab:view", "lab:edit"])
require_system_admin = RoleChecker(["super_admin", "admin"])

