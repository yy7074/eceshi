"""
项目动态选项相关Schema
"""
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from pydantic import AliasChoices, BaseModel, Field
from enum import Enum


class OptionTypeEnum(str, Enum):
    """选项类型"""
    SINGLE = "single"  # 单选（卡片式）
    MULTI = "multi"  # 多选（卡片式）
    INPUT = "input"  # 输入框
    DROPDOWN = "dropdown"  # 下拉选择器
    CHECKBOX_GROUP = "checkbox_group"  # 复选框组（横向平铺）
    RADIO_GROUP = "radio_group"  # 单选按钮组（横向平铺）


class PriceTypeEnum(str, Enum):
    """价格类型"""
    FIXED = "fixed"
    PER_SAMPLE = "per_sample"
    PERCENTAGE = "percentage"


# ==================== 选项 CRUD ====================

class ProjectOptionBase(BaseModel):
    """选项基础字段"""
    name: str = Field(..., description="选项名称")
    option_type: OptionTypeEnum = Field(OptionTypeEnum.SINGLE, description="选项类型")
    price: Decimal = Field(0, description="价格调整")
    price_type: PriceTypeEnum = Field(PriceTypeEnum.FIXED, description="价格类型")
    hint_text: Optional[str] = Field(None, description="红色提示文字")
    placeholder: Optional[str] = Field(None, description="输入框占位符")
    allow_children: bool = Field(True, description="是否需要/允许展开子选项")
    requires_input: bool = Field(False, description="选中后是否需要输入")
    input_mode: str = Field("single", description="输入模式: single/multiple")
    group_name: Optional[str] = Field(None, description="分组名称（如：样品信息、测试参数）")
    display_inline: bool = Field(False, description="是否行内显示（标签+控件同行）")
    sort_order: int = Field(0, description="排序")
    is_required: bool = Field(False, description="是否必填")
    is_active: bool = Field(True, description="是否启用")


class ProjectOptionCreate(ProjectOptionBase):
    """创建选项"""
    project_id: Optional[int] = Field(None, description="关联项目ID")
    category_id: Optional[int] = Field(None, description="关联分类ID")
    parent_id: Optional[int] = Field(None, description="父选项ID")


class ProjectOptionUpdate(BaseModel):
    """更新选项"""
    project_id: Optional[int] = Field(None, description="关联项目ID")
    category_id: Optional[int] = Field(None, description="关联分类ID")
    parent_id: Optional[int] = Field(None, description="父选项ID")
    name: Optional[str] = Field(None, description="选项名称")
    option_type: Optional[OptionTypeEnum] = Field(None, description="选项类型")
    price: Optional[Decimal] = Field(None, description="价格调整")
    price_type: Optional[PriceTypeEnum] = Field(None, description="价格类型")
    hint_text: Optional[str] = Field(None, description="红色提示文字")
    placeholder: Optional[str] = Field(None, description="输入框占位符")
    allow_children: Optional[bool] = Field(None, description="是否需要/允许展开子选项")
    requires_input: Optional[bool] = Field(None, description="选中后是否需要输入")
    input_mode: Optional[str] = Field(None, description="输入模式: single/multiple")
    group_name: Optional[str] = Field(None, description="分组名称")
    display_inline: Optional[bool] = Field(None, description="是否行内显示")
    sort_order: Optional[int] = Field(None, description="排序")
    is_required: Optional[bool] = Field(None, description="是否必填")
    is_active: Optional[bool] = Field(None, description="是否启用")


class ProjectOptionInDB(ProjectOptionBase):
    """数据库中的选项"""
    id: int
    project_id: Optional[int]
    category_id: Optional[int]
    parent_id: Optional[int]
    level: int
    path: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class ProjectOptionTree(BaseModel):
    """选项树结构（用于前端展示）"""
    id: int
    name: str
    option_type: str
    price: Decimal
    price_type: str
    hint_text: Optional[str]
    placeholder: Optional[str]
    allow_children: bool = True
    requires_input: bool = False
    input_mode: str = "single"
    group_name: Optional[str]
    display_inline: bool = False
    is_required: bool
    sort_order: int
    children: List["ProjectOptionTree"] = []

    class Config:
        from_attributes = True


# 解决前向引用
ProjectOptionTree.model_rebuild()


# ==================== 选项选择 ====================

class OptionSelectionInput(BaseModel):
    """用户选择的单个选项"""
    option_id: int = Field(..., description="选项ID")
    input_value: Optional[str] = Field(None, description="输入值（input类型时使用）")
    input_values: Optional[List[str]] = Field(None, description="多个输入值")
    input_mode: Optional[str] = Field(None, description="输入模式: single/multiple")


class OptionSelectionsInput(BaseModel):
    """用户提交的所有选项选择"""
    selections: List[OptionSelectionInput] = Field(..., description="选项选择列表")


# ==================== 价格计算 ====================

class OptionsCalculateRequest(BaseModel):
    """选项价格计算请求"""
    project_id: int = Field(..., description="项目ID")
    sample_count: int = Field(1, ge=1, description="样品数量")
    selections: List[OptionSelectionInput] = Field(
        default_factory=list,
        validation_alias=AliasChoices("selections", "option_selections"),
        description="选项选择列表"
    )


class OptionPriceDetail(BaseModel):
    """单个选项价格明细"""
    option_id: int
    option_name: str
    option_path: str
    price: Decimal
    price_type: str
    calculated_price: Decimal


class OptionsCalculateResponse(BaseModel):
    """选项价格计算结果"""
    total_options_fee: Decimal = Field(..., description="选项总费用")
    details: List[OptionPriceDetail] = Field([], description="费用明细")


# ==================== 订单选项记录 ====================

class OrderOptionSelectionCreate(BaseModel):
    """创建订单选项记录"""
    order_id: int
    option_id: int
    option_name: str
    option_path: str
    input_value: Optional[str] = None
    calculated_price: Decimal = 0


class OrderOptionSelectionInDB(BaseModel):
    """数据库中的订单选项记录"""
    id: int
    order_id: int
    option_id: int
    option_name: str
    option_path: str
    input_value: Optional[str]
    calculated_price: Decimal
    created_at: datetime

    class Config:
        from_attributes = True
