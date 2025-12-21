"""公告模型"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base


class Announcement(Base):
    """公告"""
    __tablename__ = "announcements"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, comment="标题")
    content = Column(Text, nullable=False, comment="内容")
    summary = Column(String(500), comment="摘要")
    category = Column(String(50), default="system", comment="分类: system/activity/notice")
    is_top = Column(Boolean, default=False, comment="是否置顶")
    is_active = Column(Boolean, default=True, comment="是否启用")
    view_count = Column(Integer, default=0, comment="查看次数")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class UserNotification(Base):
    """用户通知/消息"""
    __tablename__ = "user_notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True, comment="用户ID")
    title = Column(String(200), nullable=False, comment="标题")
    content = Column(Text, comment="内容")
    category = Column(String(50), default="system", comment="分类: system/order/activity")
    is_read = Column(Boolean, default=False, comment="是否已读")
    related_type = Column(String(50), comment="关联类型: order/announcement")
    related_id = Column(Integer, comment="关联ID")
    created_at = Column(DateTime, server_default=func.now())

