"""
样品组管理相关模型
支持同一测试项目按测试目的分组管理样品
"""
from sqlalchemy import Column, BigInteger, String, Integer, DateTime, Boolean, Text, Numeric, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class SampleGroup(Base):
    """
    样品组表
    用于按测试目的对样品进行分组管理
    """
    __tablename__ = "sample_groups"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)

    # 关联 (注意: users.id 是 Integer, orders.id 和 projects.id 是 BigInteger)
    order_id = Column(BigInteger, ForeignKey("orders.id"), index=True, comment="关联订单（提交后）")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True, comment="用户ID")
    project_id = Column(BigInteger, ForeignKey("projects.id"), nullable=False, index=True, comment="项目ID")

    # 分组信息
    group_name = Column(String(100), comment="分组名称/测试目的")
    group_index = Column(Integer, default=1, comment="分组序号")

    # 选项快照
    option_selections = Column(JSON, comment="该组选择的选项")
    options_fee = Column(Numeric(10, 2), default=0, comment="选项费用")

    # 状态
    is_collapsed = Column(Boolean, default=False, comment="是否收起")
    status = Column(String(20), default="draft", comment="状态: draft/submitted")

    # 时间戳
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, onupdate=func.now(), comment="更新时间")

    # 关系
    items = relationship("SampleItem", back_populates="group", cascade="all, delete-orphan")
    user = relationship("User", backref="sample_groups")
    project = relationship("Project", backref="sample_groups")
    order = relationship("Order", backref="sample_groups")


class SampleItem(Base):
    """
    样品明细表
    记录样品组内的具体样品信息
    """
    __tablename__ = "sample_items"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)

    # 关联
    group_id = Column(BigInteger, ForeignKey("sample_groups.id"), nullable=False, index=True, comment="关联样品组")

    # 样品信息
    sample_no = Column(String(100), comment="样品编号（英文+数字+下划线）")
    sample_name = Column(String(200), comment="样品名称")
    sample_composition = Column(Text, comment="样品成分")
    sample_state = Column(String(50), comment="样品状态")
    danger_type = Column(String(50), comment="危险性")
    storage_requirement = Column(String(100), comment="存放要求")
    quantity = Column(Integer, default=1, comment="数量")

    # 附加信息
    remark = Column(Text, comment="备注")
    photos = Column(JSON, comment="样品照片")

    # 时间戳
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")

    # 关系
    group = relationship("SampleGroup", back_populates="items")
