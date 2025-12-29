"""报告管理模型"""
import uuid
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, BigInteger
from sqlalchemy.sql import func
from app.core.database import Base


def generate_report_no():
    """生成报告编号"""
    from datetime import datetime
    return f"RPT{datetime.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:6].upper()}"


class Report(Base):
    """检测报告"""
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    report_no = Column(String(50), unique=True, nullable=False, default=generate_report_no, comment="报告编号")
    user_id = Column(Integer, nullable=False, index=True, comment="用户ID")
    order_id = Column(Integer, nullable=False, index=True, comment="订单ID")
    order_no = Column(String(50), comment="订单号")
    laboratory_id = Column(BigInteger, index=True, comment="实验室ID")

    # 报告类型和内容
    report_type = Column(String(50), default="test_report", comment="报告类型: test_report/raw_data/analysis")
    project_name = Column(String(200), comment="项目名称")
    sample_name = Column(String(200), comment="样品名称")

    # 文件信息
    file_url = Column(String(500), comment="报告文件URL")
    file_name = Column(String(200), comment="文件名称")
    file_size = Column(Integer, comment="文件大小(字节)")
    file_format = Column(String(20), comment="文件格式")

    # 状态与统计
    status = Column(String(20), default="uploaded", comment="状态: uploaded/verified/published")
    download_count = Column(Integer, default=0, comment="下载次数")

    # 操作人信息
    uploader_id = Column(Integer, comment="上传人ID")
    verifier_id = Column(Integer, comment="审核人ID")

    # 备注
    remark = Column(Text, comment="备注")

    # 时间
    completed_at = Column(DateTime, comment="完成时间")
    verified_at = Column(DateTime, comment="审核时间")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

