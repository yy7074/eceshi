"""
项目动态选项API（用户端）
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from decimal import Decimal

from app.api.deps import get_db, get_current_user_optional
from app.models.user import User
from app.models.project import Project
from app.models.project_option import ProjectOption, OptionType, PriceType
from app.schemas.project_option import (
    ProjectOptionTree,
    OptionsCalculateRequest,
    OptionsCalculateResponse,
    OptionPriceDetail,
    OptionSelectionInput
)
from app.core.response import SuccessResponse

router = APIRouter()


def build_option_tree(options: List[ProjectOption], parent_id: Optional[int] = None) -> List[dict]:
    """
    构建选项树结构
    """
    tree = []
    for opt in options:
        if opt.parent_id == parent_id:
            node = {
                "id": opt.id,
                "name": opt.name,
                "option_type": opt.option_type.value if isinstance(opt.option_type, OptionType) else opt.option_type,
                "price": float(opt.price) if opt.price else 0,
                "price_type": opt.price_type.value if isinstance(opt.price_type, PriceType) else opt.price_type,
                "hint_text": opt.hint_text,
                "placeholder": opt.placeholder,
                "is_required": opt.is_required,
                "sort_order": opt.sort_order,
                "children": build_option_tree(options, opt.id)
            }
            tree.append(node)

    # 按排序字段排序
    tree.sort(key=lambda x: x["sort_order"])
    return tree


def get_option_path(db: Session, option: ProjectOption) -> str:
    """
    获取选项的完整路径名称
    如：基础检测 > 样品处理 > 研磨
    """
    path_names = []
    current = option

    while current:
        path_names.insert(0, current.name)
        if current.parent_id:
            current = db.query(ProjectOption).filter(ProjectOption.id == current.parent_id).first()
        else:
            break

    return " > ".join(path_names)


def calculate_option_price(
    option: ProjectOption,
    base_price: Decimal,
    sample_count: int
) -> Decimal:
    """
    计算单个选项的价格
    """
    price = option.price if option.price else Decimal("0")
    price_type = option.price_type.value if isinstance(option.price_type, PriceType) else option.price_type

    if price_type == "fixed":
        return price
    elif price_type == "per_sample":
        return price * sample_count
    elif price_type == "percentage":
        return base_price * (price / 100)

    return Decimal("0")


@router.get("/project/{project_id}/options")
async def get_project_options(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    获取项目的动态选项树
    用于预约页面展示
    """
    # 验证项目存在
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")

    # 查询项目的选项（包括项目直接关联和分类关联的选项）
    options = db.query(ProjectOption).filter(
        and_(
            ProjectOption.is_active == True,
            (
                (ProjectOption.project_id == project_id) |
                (ProjectOption.category_id == project.category_id)
            )
        )
    ).all()

    # 构建树结构
    tree = build_option_tree(options)

    return SuccessResponse(data={
        "project_id": project_id,
        "options": tree
    })


@router.get("/category/{category_id}/options")
async def get_category_options(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    获取分类的动态选项树
    """
    # 查询分类的选项
    options = db.query(ProjectOption).filter(
        and_(
            ProjectOption.is_active == True,
            ProjectOption.category_id == category_id
        )
    ).all()

    # 构建树结构
    tree = build_option_tree(options)

    return SuccessResponse(data={
        "category_id": category_id,
        "options": tree
    })


@router.post("/options/calculate")
async def calculate_options_price(
    data: OptionsCalculateRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    计算选项总价格
    实时计算用户选择的选项费用
    """
    # 获取项目基础价格
    project = db.query(Project).filter(Project.id == data.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")

    base_price = Decimal(str(project.current_price)) * data.sample_count

    # 计算各选项价格
    total_options_fee = Decimal("0")
    details = []

    for selection in data.selections:
        option = db.query(ProjectOption).filter(
            ProjectOption.id == selection.option_id,
            ProjectOption.is_active == True
        ).first()

        if not option:
            continue

        # 计算价格
        calculated_price = calculate_option_price(option, base_price, data.sample_count)
        total_options_fee += calculated_price

        # 获取选项路径
        option_path = get_option_path(db, option)

        details.append(OptionPriceDetail(
            option_id=option.id,
            option_name=option.name,
            option_path=option_path,
            price=option.price if option.price else Decimal("0"),
            price_type=option.price_type.value if isinstance(option.price_type, PriceType) else option.price_type,
            calculated_price=calculated_price
        ))

    return SuccessResponse(data=OptionsCalculateResponse(
        total_options_fee=total_options_fee,
        details=details
    ))


@router.get("/options/{option_id}")
async def get_option_detail(
    option_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    获取单个选项详情
    """
    option = db.query(ProjectOption).filter(
        ProjectOption.id == option_id,
        ProjectOption.is_active == True
    ).first()

    if not option:
        raise HTTPException(status_code=404, detail="选项不存在")

    return SuccessResponse(data={
        "id": option.id,
        "name": option.name,
        "option_type": option.option_type.value if isinstance(option.option_type, OptionType) else option.option_type,
        "price": float(option.price) if option.price else 0,
        "price_type": option.price_type.value if isinstance(option.price_type, PriceType) else option.price_type,
        "hint_text": option.hint_text,
        "placeholder": option.placeholder,
        "is_required": option.is_required,
        "path": get_option_path(db, option)
    })
