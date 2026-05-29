"""在线客服/聊天模型"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class ChatSession(Base):
    """聊天会话"""
    __tablename__ = "chat_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True, comment="用户ID")
    staff_id = Column(Integer, ForeignKey("users.id"), comment="客服ID")
    status = Column(String(20), default="active", comment="状态: active/closed")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    closed_at = Column(DateTime, comment="关闭时间")

    user = relationship("User", foreign_keys=[user_id])
    staff = relationship("User", foreign_keys=[staff_id])
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")


class ChatMessage(Base):
    """聊天消息"""
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False, index=True, comment="会话ID")
    sender_type = Column(String(20), nullable=False, comment="发送者类型: user/staff/system")
    sender_id = Column(Integer, comment="发送者ID")
    content = Column(Text, nullable=False, comment="消息内容")
    message_type = Column(String(20), default="text", comment="消息类型: text/image/file")
    is_read = Column(Boolean, default=False, comment="是否已读")
    created_at = Column(DateTime, server_default=func.now())

    session = relationship("ChatSession", back_populates="messages")


class QuickReply(Base):
    """快捷回复"""
    __tablename__ = "quick_replies"
    
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String(500), nullable=False, comment="问题")
    answer = Column(Text, nullable=False, comment="回答")
    category = Column(String(50), comment="分类")
    sort_order = Column(Integer, default=0, comment="排序")
    is_active = Column(Boolean, default=True, comment="是否启用")
    created_at = Column(DateTime, server_default=func.now())
