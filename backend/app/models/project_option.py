"""
项目动态选项相关模型
支持无限层级的选项树结构
"""
from sqlalchemy import Column, BigInteger, String, Integer, DateTime, Boolean, Text, Numeric, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class OptionType(str, enum.Enum):
    """选项类型枚举"""
    SINGLE = "single"     # 单选（卡片式，子选项互斥）
    MULTI = "multi"       # 多选（卡片式，子选项可多选）
    INPUT = "input"       # 输入框（终止分支）
    DROPDOWN = "dropdown"  # 下拉选择器（单选下拉）
    CHECKBOX_GROUP = "checkbox_group"  # 复选框组（横向平铺多选）
    RADIO_GROUP = "radio_group"  # 单选按钮组（横向平铺单选，常用于带加价的选项）


class PriceType(str, enum.Enum):
    """价格类型枚举"""
    FIXED = "fixed"              # 固定价格
    PER_SAMPLE = "per_sample"    # 按样品数量计价
    PERCENTAGE = "percentage"    # 基础价格百分比


class ProjectOption(Base):
    """
    项目动态选项表
    支持无限层级的树形结构
    """
    __tablename__ = "project_options"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)

    # 关联（project_id 和 category_id 二选一）
    project_id = Column(BigInteger, index=True, comment="关联项目ID")
    category_id = Column(BigInteger, index=True, comment="关联分类ID（与project_id二选一）")

    # 树形结构
    parent_id = Column(BigInteger, ForeignKey("project_options.id"), index=True, comment="父选项ID（null为根选项）")
    level = Column(Integer, default=1, comment="层级深度")
    path = Column(String(500), comment="物化路径 如 /1/5/12/")

    # 选项信息
    name = Column(String(200), nullable=False, comment="选项名称")
    option_type = Column(
        SQLEnum(OptionType, values_callable=lambda x: [e.value for e in x]),
        default=OptionType.SINGLE,
        comment="选项类型: single/multi/input"
    )

    # 价格配置
    price = Column(Numeric(10, 2), default=0, comment="价格调整")
    price_type = Column(
        SQLEnum(PriceType, values_callable=lambda x: [e.value for e in x]),
        default=PriceType.FIXED,
        comment="价格类型: fixed/per_sample/percentage"
    )

    # 提示信息
    hint_text = Column(String(500), comment="红色提示文字")
    placeholder = Column(String(200), comment="输入框占位符（input类型时使用）")
    allow_children = Column(Boolean, default=True, comment="是否需要/允许展开子选项")
    requires_input = Column(Boolean, default=False, comment="选中后是否需要填写输入内容")
    input_mode = Column(String(20), default="single", comment="输入模式: single/multiple")

    # 分组和显示配置
    group_name = Column(String(100), comment="分组名称（如：样品信息、测试参数、服务选项）")
    display_inline = Column(Boolean, default=False, comment="是否行内显示（标签+控件同行）")

    # 排序和状态
    sort_order = Column(Integer, default=0, comment="排序")
    is_required = Column(Boolean, default=False, comment="是否必填")
    is_active = Column(Boolean, default=True, comment="是否启用")

    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, onupdate=func.now(), comment="更新时间")

    # 自引用关系 - 获取子选项
    children = relationship(
        "ProjectOption",
        backref="parent",
        remote_side="ProjectOption.id",
        cascade="all, delete-orphan",
        single_parent=True
    )


class OrderOptionSelection(Base):
    """
    订单选项选择记录表
    记录用户在下单时选择的选项
    """
    __tablename__ = "order_option_selections"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)

    # 关联
    order_id = Column(BigInteger, ForeignKey("orders.id"), nullable=False, index=True, comment="订单ID")
    option_id = Column(BigInteger, ForeignKey("project_options.id"), nullable=False, index=True, comment="选项ID")

    # 选项信息快照（用于历史记录）
    option_name = Column(String(200), comment="选项名称快照")
    option_path = Column(String(1000), comment="选项路径快照（如：基础检测 > 样品处理 > 研磨）")

    # 输入值（input类型时使用）
    input_value = Column(String(500), comment="输入类型的值")

    # 价格信息
    calculated_price = Column(Numeric(10, 2), default=0, comment="计算后的价格")

    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")

    # 关系
    option = relationship("ProjectOption")
