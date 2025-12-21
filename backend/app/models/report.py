"""报告管理模型"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base


class Report(Base):
    """检测报告"""
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    report_no = Column(String(50), unique=True, nullable=False, comment="报告编号")
    user_id = Column(Integer, nullable=False, index=True, comment="用户ID")
    order_id = Column(Integer, nullable=False, index=True, comment="订单ID")
    order_no = Column(String(50), comment="订单号")
    project_name = Column(String(200), comment="项目名称")
    sample_name = Column(String(200), comment="样品名称")
    status = Column(String(20), default="pending", comment="状态: pending/processing/completed")
    file_url = Column(String(500), comment="报告文件URL")
    file_size = Column(Integer, comment="文件大小(字节)")
    download_count = Column(Integer, default=0, comment="下载次数")
    completed_at = Column(DateTime, comment="完成时间")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

