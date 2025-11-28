"""
发票模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Enum, Numeric, Text, BigInteger
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class InvoiceType(enum.Enum):
    """发票类型"""
    NORMAL = "normal"  # 普通发票
    SPECIAL = "special"  # 专用发票


class InvoiceStatus(enum.Enum):
    """发票状态"""
    PENDING = "pending"  # 待审核
    APPROVED = "approved"  # 已通过
    REJECTED = "rejected"  # 已拒绝
    ISSUED = "issued"  # 已开票


class Invoice(Base):
    """发票申请表"""
    __tablename__ = "invoices"
    
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    invoice_no = Column(String(64), unique=True, index=True, comment="发票申请编号")
    user_id = Column(BigInteger, nullable=False, index=True, comment="用户ID")
    
    # 发票类型
    invoice_type = Column(Enum(InvoiceType), default=InvoiceType.NORMAL, comment="发票类型")
    
    # 发票抬头信息
    title_type = Column(String(20), default="personal", comment="抬头类型: personal/company")
    title = Column(String(200), nullable=False, comment="发票抬头")
    tax_number = Column(String(50), comment="税号")
    bank_name = Column(String(100), comment="开户银行")
    bank_account = Column(String(50), comment="银行账号")
    company_address = Column(String(200), comment="公司地址")
    company_phone = Column(String(20), comment="公司电话")
    
    # 发票内容
    content = Column(String(100), default="检测服务费", comment="发票内容")
    amount = Column(Numeric(10, 2), nullable=False, comment="开票金额")
    
    # 关联订单
    order_ids = Column(Text, comment="关联订单ID列表（JSON格式）")
    
    # 接收信息
    receiver_email = Column(String(100), comment="接收邮箱（电子发票）")
    receiver_phone = Column(String(20), comment="接收手机号")
    receiver_address = Column(String(300), comment="邮寄地址（纸质发票）")
    
    # 发票信息
    invoice_code = Column(String(50), comment="发票代码")
    invoice_number = Column(String(50), comment="发票号码")
    invoice_url = Column(String(500), comment="电子发票下载链接")
    
    # 状态
    status = Column(Enum(InvoiceStatus), default=InvoiceStatus.PENDING, comment="发票状态")
    reject_reason = Column(String(200), comment="拒绝原因")
    
    # 时间
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="申请时间")
    reviewed_at = Column(DateTime(timezone=True), comment="审核时间")
    issued_at = Column(DateTime(timezone=True), comment="开票时间")
    
    def __repr__(self):
        return f"<Invoice {self.invoice_no}>"

