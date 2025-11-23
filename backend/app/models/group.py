"""
团队模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Enum, Text, Boolean
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class GroupRole(enum.Enum):
    """团队角色"""
    OWNER = "owner"  # 负责人
    ADMIN = "admin"  # 管理员
    MEMBER = "member"  # 成员


class GroupStatus(enum.Enum):
    """团队状态"""
    ACTIVE = "active"  # 活跃
    INACTIVE = "inactive"  # 未激活
    DISBANDED = "disbanded"  # 已解散


class UserGroup(Base):
    """用户团队表"""
    __tablename__ = "user_groups"
    
    id = Column(Integer, primary_key=True, index=True, comment="团队ID")
    name = Column(String(100), nullable=False, comment="团队名称")
    avatar = Column(String(255), comment="团队头像")
    description = Column(Text, comment="团队描述")
    
    # 负责人信息
    owner_id = Column(Integer, nullable=False, index=True, comment="负责人用户ID")
    owner_name = Column(String(50), comment="负责人姓名")
    owner_phone = Column(String(20), comment="负责人手机号")
    
    # 团队信息
    university = Column(String(100), comment="所属高校")
    department = Column(String(100), comment="所属院系")
    invite_code = Column(String(20), unique=True, index=True, comment="邀请码")
    
    # 统计信息
    member_count = Column(Integer, default=1, comment="成员数量")
    total_orders = Column(Integer, default=0, comment="累计订单数")
    total_spent = Column(Integer, default=0, comment="累计消费金额")
    
    # 状态
    status = Column(Enum(GroupStatus), default=GroupStatus.ACTIVE, comment="团队状态")
    is_certified = Column(Boolean, default=False, comment="是否认证")
    
    # 时间
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    def __repr__(self):
        return f"<UserGroup {self.name}>"


class GroupMember(Base):
    """团队成员表"""
    __tablename__ = "group_members"
    
    id = Column(Integer, primary_key=True, index=True, comment="成员ID")
    group_id = Column(Integer, nullable=False, index=True, comment="团队ID")
    user_id = Column(Integer, nullable=False, index=True, comment="用户ID")
    
    # 成员信息
    nickname = Column(String(50), comment="昵称")
    avatar = Column(String(255), comment="头像")
    phone = Column(String(20), comment="手机号")
    
    # 角色
    role = Column(Enum(GroupRole), default=GroupRole.MEMBER, comment="团队角色")
    
    # 统计
    order_count = Column(Integer, default=0, comment="订单数量")
    total_spent = Column(Integer, default=0, comment="消费金额")
    
    # 时间
    joined_at = Column(DateTime(timezone=True), server_default=func.now(), comment="加入时间")
    
    def __repr__(self):
        return f"<GroupMember group_id={self.group_id} user_id={self.user_id}>"
