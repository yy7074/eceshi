"""样品追踪模型"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base


class SampleTracking(Base):
    """样品追踪记录"""
    __tablename__ = "sample_trackings"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False, index=True, comment="订单ID")
    order_no = Column(String(50), comment="订单号")
    sample_name = Column(String(200), comment="样品名称")
    status = Column(String(50), nullable=False, comment="状态")
    status_text = Column(String(100), comment="状态描述")
    location = Column(String(200), comment="当前位置")
    operator = Column(String(100), comment="操作人")
    remark = Column(Text, comment="备注")
    created_at = Column(DateTime, server_default=func.now())


class SampleLogistics(Base):
    """样品物流信息"""
    __tablename__ = "sample_logistics"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False, index=True, comment="订单ID")
    logistics_type = Column(String(20), default="send", comment="类型: send/return")
    company = Column(String(100), comment="快递公司")
    tracking_no = Column(String(100), comment="快递单号")
    sender_name = Column(String(100), comment="寄件人")
    sender_phone = Column(String(20), comment="寄件人电话")
    sender_address = Column(String(500), comment="寄件地址")
    receiver_name = Column(String(100), comment="收件人")
    receiver_phone = Column(String(20), comment="收件人电话")
    receiver_address = Column(String(500), comment="收件地址")
    status = Column(String(20), default="pending", comment="状态")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

