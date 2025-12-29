"""
角色权限模型
实现基于角色的访问控制(RBAC)
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Table
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


# 角色-权限关联表
role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True)
)

# 用户-角色关联表
user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
    Column('created_at', DateTime, server_default=func.now())
)


class Role(Base):
    """角色表"""
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, comment="角色名称")
    code = Column(String(50), unique=True, nullable=False, comment="角色编码")
    description = Column(String(255), comment="角色描述")
    is_system = Column(Boolean, default=False, comment="是否系统内置角色")
    is_active = Column(Boolean, default=True, comment="是否启用")
    sort_order = Column(Integer, default=0, comment="排序")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # 关系
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")
    users = relationship("User", secondary=user_roles, back_populates="roles")


class Permission(Base):
    """权限表"""
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="权限名称")
    code = Column(String(100), unique=True, nullable=False, comment="权限编码")
    module = Column(String(50), comment="所属模块")
    description = Column(String(255), comment="权限描述")
    is_active = Column(Boolean, default=True, comment="是否启用")
    sort_order = Column(Integer, default=0, comment="排序")

    created_at = Column(DateTime, server_default=func.now())

    # 关系
    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")


# 预定义角色编码
class RoleCode:
    """角色编码常量"""
    SUPER_ADMIN = "super_admin"      # 超级管理员
    ADMIN = "admin"                   # 管理员
    OPERATOR = "operator"             # 运营人员
    FINANCE = "finance"               # 财务人员
    CUSTOMER_SERVICE = "cs"           # 客服人员
    LAB_ADMIN = "lab_admin"           # 实验室管理员
    LAB_TECHNICIAN = "lab_technician" # 实验室技术员
    USER = "user"                     # 普通用户


# 预定义权限编码
class PermissionCode:
    """权限编码常量"""
    # 用户管理
    USER_VIEW = "user:view"
    USER_EDIT = "user:edit"
    USER_DELETE = "user:delete"
    USER_CERTIFICATION = "user:certification"

    # 订单管理
    ORDER_VIEW = "order:view"
    ORDER_EDIT = "order:edit"
    ORDER_DELETE = "order:delete"
    ORDER_ASSIGN = "order:assign"
    ORDER_EXPORT = "order:export"

    # 项目管理
    PROJECT_VIEW = "project:view"
    PROJECT_CREATE = "project:create"
    PROJECT_EDIT = "project:edit"
    PROJECT_DELETE = "project:delete"

    # 实验室管理
    LAB_VIEW = "lab:view"
    LAB_CREATE = "lab:create"
    LAB_EDIT = "lab:edit"
    LAB_DELETE = "lab:delete"
    LAB_APPROVE = "lab:approve"

    # 财务管理
    FINANCE_VIEW = "finance:view"
    FINANCE_RECHARGE = "finance:recharge"
    FINANCE_REFUND = "finance:refund"
    FINANCE_WITHDRAW = "finance:withdraw"
    FINANCE_REPORT = "finance:report"

    # 优惠券管理
    COUPON_VIEW = "coupon:view"
    COUPON_CREATE = "coupon:create"
    COUPON_EDIT = "coupon:edit"
    COUPON_DELETE = "coupon:delete"

    # 内容管理
    CONTENT_BANNER = "content:banner"
    CONTENT_ANNOUNCEMENT = "content:announcement"
    CONTENT_HELP = "content:help"

    # 报表统计
    REPORT_VIEW = "report:view"
    REPORT_EXPORT = "report:export"

    # 系统设置
    SYSTEM_CONFIG = "system:config"
    SYSTEM_ROLE = "system:role"
    SYSTEM_LOG = "system:log"


# 角色默认权限配置
DEFAULT_ROLE_PERMISSIONS = {
    RoleCode.SUPER_ADMIN: [
        # 超级管理员拥有所有权限
        PermissionCode.USER_VIEW, PermissionCode.USER_EDIT, PermissionCode.USER_DELETE, PermissionCode.USER_CERTIFICATION,
        PermissionCode.ORDER_VIEW, PermissionCode.ORDER_EDIT, PermissionCode.ORDER_DELETE, PermissionCode.ORDER_ASSIGN, PermissionCode.ORDER_EXPORT,
        PermissionCode.PROJECT_VIEW, PermissionCode.PROJECT_CREATE, PermissionCode.PROJECT_EDIT, PermissionCode.PROJECT_DELETE,
        PermissionCode.LAB_VIEW, PermissionCode.LAB_CREATE, PermissionCode.LAB_EDIT, PermissionCode.LAB_DELETE, PermissionCode.LAB_APPROVE,
        PermissionCode.FINANCE_VIEW, PermissionCode.FINANCE_RECHARGE, PermissionCode.FINANCE_REFUND, PermissionCode.FINANCE_WITHDRAW, PermissionCode.FINANCE_REPORT,
        PermissionCode.COUPON_VIEW, PermissionCode.COUPON_CREATE, PermissionCode.COUPON_EDIT, PermissionCode.COUPON_DELETE,
        PermissionCode.CONTENT_BANNER, PermissionCode.CONTENT_ANNOUNCEMENT, PermissionCode.CONTENT_HELP,
        PermissionCode.REPORT_VIEW, PermissionCode.REPORT_EXPORT,
        PermissionCode.SYSTEM_CONFIG, PermissionCode.SYSTEM_ROLE, PermissionCode.SYSTEM_LOG,
    ],
    RoleCode.ADMIN: [
        PermissionCode.USER_VIEW, PermissionCode.USER_EDIT, PermissionCode.USER_CERTIFICATION,
        PermissionCode.ORDER_VIEW, PermissionCode.ORDER_EDIT, PermissionCode.ORDER_ASSIGN, PermissionCode.ORDER_EXPORT,
        PermissionCode.PROJECT_VIEW, PermissionCode.PROJECT_CREATE, PermissionCode.PROJECT_EDIT,
        PermissionCode.LAB_VIEW, PermissionCode.LAB_EDIT, PermissionCode.LAB_APPROVE,
        PermissionCode.FINANCE_VIEW, PermissionCode.FINANCE_RECHARGE, PermissionCode.FINANCE_REFUND,
        PermissionCode.COUPON_VIEW, PermissionCode.COUPON_CREATE, PermissionCode.COUPON_EDIT,
        PermissionCode.CONTENT_BANNER, PermissionCode.CONTENT_ANNOUNCEMENT, PermissionCode.CONTENT_HELP,
        PermissionCode.REPORT_VIEW, PermissionCode.REPORT_EXPORT,
    ],
    RoleCode.OPERATOR: [
        PermissionCode.USER_VIEW,
        PermissionCode.ORDER_VIEW, PermissionCode.ORDER_EDIT, PermissionCode.ORDER_ASSIGN,
        PermissionCode.PROJECT_VIEW,
        PermissionCode.LAB_VIEW,
        PermissionCode.CONTENT_BANNER, PermissionCode.CONTENT_ANNOUNCEMENT, PermissionCode.CONTENT_HELP,
    ],
    RoleCode.FINANCE: [
        PermissionCode.USER_VIEW,
        PermissionCode.ORDER_VIEW, PermissionCode.ORDER_EXPORT,
        PermissionCode.FINANCE_VIEW, PermissionCode.FINANCE_RECHARGE, PermissionCode.FINANCE_REFUND, PermissionCode.FINANCE_WITHDRAW, PermissionCode.FINANCE_REPORT,
        PermissionCode.REPORT_VIEW, PermissionCode.REPORT_EXPORT,
    ],
    RoleCode.CUSTOMER_SERVICE: [
        PermissionCode.USER_VIEW,
        PermissionCode.ORDER_VIEW,
        PermissionCode.PROJECT_VIEW,
    ],
    RoleCode.LAB_ADMIN: [
        PermissionCode.LAB_VIEW, PermissionCode.LAB_EDIT,
        PermissionCode.ORDER_VIEW,
    ],
    RoleCode.LAB_TECHNICIAN: [
        PermissionCode.ORDER_VIEW,
    ],
    RoleCode.USER: [
        # 普通用户无后台权限
    ],
}
