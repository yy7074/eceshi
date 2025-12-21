"""合同管理模型"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Numeric
from sqlalchemy.sql import func
from app.core.database import Base


class Contract(Base):
    """合同"""
    __tablename__ = "contracts"
    
    id = Column(Integer, primary_key=True, index=True)
    contract_no = Column(String(50), unique=True, nullable=False, comment="合同编号")
    user_id = Column(Integer, nullable=False, index=True, comment="用户ID")
    order_id = Column(Integer, index=True, comment="关联订单ID")
    order_no = Column(String(50), comment="关联订单号")
    title = Column(String(200), nullable=False, comment="合同标题")
    content = Column(Text, comment="合同内容")
    amount = Column(Numeric(10, 2), comment="合同金额")
    status = Column(String(20), default="active", comment="状态: draft/active/expired/terminated")
    signed_at = Column(DateTime, comment="签订日期")
    expired_at = Column(DateTime, comment="到期日期")
    file_url = Column(String(500), comment="合同文件URL")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

