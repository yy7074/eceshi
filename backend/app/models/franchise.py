"""加盟申请模型"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base


class FranchiseApplication(Base):
    """加盟申请"""
    __tablename__ = "franchise_applications"
    
    id = Column(Integer, primary_key=True, index=True)
    application_no = Column(String(50), unique=True, nullable=False, comment="申请编号")
    name = Column(String(100), nullable=False, comment="联系人姓名")
    phone = Column(String(20), nullable=False, comment="联系电话")
    company = Column(String(200), comment="公司/机构名称")
    city = Column(String(100), comment="所在城市")
    mode = Column(String(50), default="agent", comment="合作模式: agent/partner/lab")
    intention = Column(Text, comment="合作意向")
    status = Column(String(20), default="pending", comment="状态: pending/contacted/approved/rejected")
    staff_id = Column(Integer, comment="处理人ID")
    staff_remark = Column(Text, comment="处理备注")
    contacted_at = Column(DateTime, comment="联系时间")
    user_id = Column(Integer, comment="关联用户ID(如已注册)")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

