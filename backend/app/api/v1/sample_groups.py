"""
样品组管理API
支持样品分组、批量添加、复制、提交等功能
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from decimal import Decimal

from app.core.database import get_db
from app.core.response import success_response, error_response
from app.api.deps import get_current_user
from app.models.user import User
from app.models.sample_group import SampleGroup, SampleItem
from app.models.project import Project
from app.models.project_option import ProjectOption, PriceType
from app.api.v1.orders import calculate_coupon_discount, mark_user_coupon_used
from app.schemas.sample_group import (
    SampleGroupCreate, SampleGroupUpdate, SampleGroupResponse, SampleGroupListResponse,
    SampleItemCreate, SampleItemUpdate, SampleItemResponse,
    BatchAddSamplesRequest, BatchAddSamplesResponse,
    SubmitGroupsRequest, SubmitGroupsResponse,
    CalculateGroupsPriceRequest, CalculateGroupsPriceResponse, GroupPriceDetail,
    CopyGroupResponse
)

router = APIRouter(prefix="/sample-groups", tags=["样品组管理"])


# ==================== 辅助函数 ====================

def get_user_group(db: Session, group_id: int, user_id: int) -> SampleGroup:
    """获取用户的样品组，验证权限"""
    group = db.query(SampleGroup).filter(
        SampleGroup.id == group_id,
        SampleGroup.user_id == user_id
    ).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="样品组不存在或无权访问"
        )
    return group


def calculate_options_fee(db: Session, option_selections: List[dict], sample_count: int, base_price: Decimal) -> Decimal:
    """计算选项费用"""
    if not option_selections:
        return Decimal("0")

    total_fee = Decimal("0")
    for selection in option_selections:
        option_id = selection.get("option_id")
        if not option_id:
            continue

        option = db.query(ProjectOption).filter(ProjectOption.id == option_id).first()
        if not option or not option.is_active:
            continue

        price = Decimal(str(option.price)) if option.price else Decimal("0")

        if option.price_type == PriceType.FIXED:
            total_fee += price
        elif option.price_type == PriceType.PER_SAMPLE:
            total_fee += price * sample_count
        elif option.price_type == PriceType.PERCENTAGE:
            total_fee += base_price * price / Decimal("100")

    return total_fee


# ==================== 样品组 CRUD ====================

@router.get("", summary="获取用户的样品组列表")
async def get_sample_groups(
    project_id: Optional[int] = Query(None, description="按项目筛选"),
    status_filter: Optional[str] = Query(None, alias="status", description="按状态筛选: draft/submitted"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取当前用户的所有样品组"""
    query = db.query(SampleGroup).filter(SampleGroup.user_id == current_user.id)

    if project_id:
        query = query.filter(SampleGroup.project_id == project_id)
    if status_filter:
        query = query.filter(SampleGroup.status == status_filter)

    groups = query.order_by(SampleGroup.created_at.desc()).all()

    result = []
    for group in groups:
        sample_count = db.query(func.sum(SampleItem.quantity)).filter(
            SampleItem.group_id == group.id
        ).scalar() or 0

        result.append({
            "id": group.id,
            "project_id": group.project_id,
            "group_name": group.group_name,
            "group_index": group.group_index,
            "options_fee": group.options_fee,
            "is_collapsed": group.is_collapsed,
            "status": group.status,
            "sample_count": sample_count,
            "created_at": group.created_at
        })

    return success_response(data=result)


@router.post("", summary="创建样品组")
async def create_sample_group(
    data: SampleGroupCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建新的样品组"""
    # 验证项目存在
    project = db.query(Project).filter(Project.id == data.project_id).first()
    if not project:
        return error_response(message="项目不存在")

    # 获取当前最大分组序号
    max_index = db.query(func.max(SampleGroup.group_index)).filter(
        SampleGroup.user_id == current_user.id,
        SampleGroup.project_id == data.project_id,
        SampleGroup.status == "draft"
    ).scalar() or 0

    # 创建样品组
    group = SampleGroup(
        user_id=current_user.id,
        project_id=data.project_id,
        group_name=data.group_name,
        group_index=max_index + 1,
        option_selections=data.option_selections,
        status="draft"
    )
    db.add(group)
    db.flush()

    # 如果有初始样品，添加样品
    if data.items:
        for item_data in data.items:
            item = SampleItem(
                group_id=group.id,
                **item_data.model_dump()
            )
            db.add(item)

    db.commit()
    db.refresh(group)

    return success_response(data=SampleGroupResponse.model_validate(group).model_dump(), message="创建成功")


@router.get("/{group_id}", summary="获取样品组详情")
async def get_sample_group(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取样品组详情，包含所有样品"""
    group = get_user_group(db, group_id, current_user.id)
    return success_response(data=SampleGroupResponse.model_validate(group).model_dump())


@router.put("/{group_id}", summary="更新样品组")
async def update_sample_group(
    group_id: int,
    data: SampleGroupUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新样品组信息"""
    group = get_user_group(db, group_id, current_user.id)

    if group.status != "draft":
        return error_response(message="已提交的样品组无法修改")

    # 更新字段
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(group, key, value)

    # 如果更新了选项，重新计算费用
    if data.option_selections is not None:
        sample_count = db.query(func.sum(SampleItem.quantity)).filter(
            SampleItem.group_id == group.id
        ).scalar() or 0
        project = db.query(Project).filter(Project.id == group.project_id).first()
        base_price = Decimal(str(project.price)) * sample_count if project else Decimal("0")
        group.options_fee = calculate_options_fee(db, data.option_selections, sample_count, base_price)

    db.commit()
    db.refresh(group)

    return success_response(data=SampleGroupResponse.model_validate(group).model_dump(), message="更新成功")


@router.delete("/{group_id}", summary="删除样品组")
async def delete_sample_group(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除样品组及其所有样品"""
    group = get_user_group(db, group_id, current_user.id)

    if group.status != "draft":
        return error_response(message="已提交的样品组无法删除")

    db.delete(group)
    db.commit()

    return success_response(message="删除成功")


@router.post("/{group_id}/copy", summary="复制样品组")
async def copy_sample_group(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """复制样品组及其所有样品"""
    source_group = get_user_group(db, group_id, current_user.id)

    # 获取当前最大分组序号
    max_index = db.query(func.max(SampleGroup.group_index)).filter(
        SampleGroup.user_id == current_user.id,
        SampleGroup.project_id == source_group.project_id,
        SampleGroup.status == "draft"
    ).scalar() or 0

    # 创建新样品组
    new_group = SampleGroup(
        user_id=current_user.id,
        project_id=source_group.project_id,
        group_name=f"{source_group.group_name or '分组'} (复制)" if source_group.group_name else "分组 (复制)",
        group_index=max_index + 1,
        option_selections=source_group.option_selections,
        options_fee=source_group.options_fee,
        status="draft"
    )
    db.add(new_group)
    db.flush()

    # 复制样品
    for item in source_group.items:
        new_item = SampleItem(
            group_id=new_group.id,
            sample_no=f"{item.sample_no}_copy" if item.sample_no else None,
            sample_name=item.sample_name,
            sample_composition=item.sample_composition,
            sample_state=item.sample_state,
            danger_type=item.danger_type,
            storage_requirement=item.storage_requirement,
            quantity=item.quantity,
            remark=item.remark,
            photos=item.photos
        )
        db.add(new_item)

    db.commit()
    db.refresh(new_group)

    return success_response(
        data=CopyGroupResponse(
            new_group=SampleGroupResponse.model_validate(new_group),
            message="复制成功"
        ).model_dump()
    )


# ==================== 样品管理 ====================

@router.get("/{group_id}/items", summary="获取组内样品列表")
async def get_sample_items(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取样品组内所有样品"""
    group = get_user_group(db, group_id, current_user.id)
    items = [SampleItemResponse.model_validate(item).model_dump() for item in group.items]
    return success_response(data=items)


@router.post("/{group_id}/items", summary="添加样品")
async def add_sample_item(
    group_id: int,
    data: SampleItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """向样品组添加单个样品"""
    group = get_user_group(db, group_id, current_user.id)

    if group.status != "draft":
        return error_response(message="已提交的样品组无法添加样品")

    item = SampleItem(
        group_id=group.id,
        **data.model_dump()
    )
    db.add(item)

    # 重新计算选项费用
    db.flush()
    sample_count = db.query(func.sum(SampleItem.quantity)).filter(
        SampleItem.group_id == group.id
    ).scalar() or 0
    project = db.query(Project).filter(Project.id == group.project_id).first()
    base_price = Decimal(str(project.price)) * sample_count if project else Decimal("0")
    group.options_fee = calculate_options_fee(db, group.option_selections, sample_count, base_price)

    db.commit()
    db.refresh(item)

    return success_response(data=SampleItemResponse.model_validate(item).model_dump(), message="添加成功")


@router.post("/{group_id}/items/batch", summary="批量添加样品")
async def batch_add_sample_items(
    group_id: int,
    data: BatchAddSamplesRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """批量添加样品到样品组"""
    group = get_user_group(db, group_id, current_user.id)

    if group.status != "draft":
        return error_response(message="已提交的样品组无法添加样品")

    added_items = []
    for i in range(data.count):
        number = data.start_number + i
        sample_no = f"{data.prefix}{number}" if data.prefix else f"{number}"

        item = SampleItem(
            group_id=group.id,
            sample_no=sample_no,
            quantity=1
        )
        db.add(item)
        added_items.append(item)

    # 重新计算选项费用
    db.flush()
    sample_count = db.query(func.sum(SampleItem.quantity)).filter(
        SampleItem.group_id == group.id
    ).scalar() or 0
    project = db.query(Project).filter(Project.id == group.project_id).first()
    base_price = Decimal(str(project.price)) * sample_count if project else Decimal("0")
    group.options_fee = calculate_options_fee(db, group.option_selections, sample_count, base_price)

    db.commit()

    for item in added_items:
        db.refresh(item)

    return success_response(
        data=BatchAddSamplesResponse(
            added_count=len(added_items),
            items=[SampleItemResponse.model_validate(item) for item in added_items]
        ).model_dump(),
        message=f"成功添加 {len(added_items)} 个样品"
    )


@router.put("/{group_id}/items/{item_id}", summary="更新样品")
async def update_sample_item(
    group_id: int,
    item_id: int,
    data: SampleItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新样品信息"""
    group = get_user_group(db, group_id, current_user.id)

    if group.status != "draft":
        return error_response(message="已提交的样品组无法修改样品")

    item = db.query(SampleItem).filter(
        SampleItem.id == item_id,
        SampleItem.group_id == group.id
    ).first()
    if not item:
        return error_response(message="样品不存在")

    # 更新字段
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)

    # 如果更新了数量，重新计算选项费用
    if data.quantity is not None:
        sample_count = db.query(func.sum(SampleItem.quantity)).filter(
            SampleItem.group_id == group.id
        ).scalar() or 0
        project = db.query(Project).filter(Project.id == group.project_id).first()
        base_price = Decimal(str(project.price)) * sample_count if project else Decimal("0")
        group.options_fee = calculate_options_fee(db, group.option_selections, sample_count, base_price)

    db.commit()
    db.refresh(item)

    return success_response(data=SampleItemResponse.model_validate(item).model_dump(), message="更新成功")


@router.delete("/{group_id}/items/{item_id}", summary="删除样品")
async def delete_sample_item(
    group_id: int,
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """从样品组删除样品"""
    group = get_user_group(db, group_id, current_user.id)

    if group.status != "draft":
        return error_response(message="已提交的样品组无法删除样品")

    item = db.query(SampleItem).filter(
        SampleItem.id == item_id,
        SampleItem.group_id == group.id
    ).first()
    if not item:
        return error_response(message="样品不存在")

    db.delete(item)

    # 重新计算选项费用
    sample_count = db.query(func.sum(SampleItem.quantity)).filter(
        SampleItem.group_id == group.id,
        SampleItem.id != item_id
    ).scalar() or 0
    project = db.query(Project).filter(Project.id == group.project_id).first()
    base_price = Decimal(str(project.price)) * sample_count if project else Decimal("0")
    group.options_fee = calculate_options_fee(db, group.option_selections, sample_count, base_price)

    db.commit()

    return success_response(message="删除成功")


# ==================== 价格计算 ====================

@router.post("/calculate", summary="计算多组价格")
async def calculate_groups_price(
    data: CalculateGroupsPriceRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """计算多个样品组的价格"""
    groups = db.query(SampleGroup).filter(
        SampleGroup.id.in_(data.group_ids),
        SampleGroup.user_id == current_user.id
    ).all()

    if len(groups) != len(data.group_ids):
        return error_response(message="部分样品组不存在或无权访问")

    group_details = []
    total_sample_count = 0
    total_base_price = Decimal("0")
    total_options_fee = Decimal("0")

    for group in groups:
        sample_count = db.query(func.sum(SampleItem.quantity)).filter(
            SampleItem.group_id == group.id
        ).scalar() or 0

        project = db.query(Project).filter(Project.id == group.project_id).first()
        base_price = Decimal(str(project.price)) * sample_count if project else Decimal("0")
        options_fee = calculate_options_fee(db, group.option_selections, sample_count, base_price)

        group_details.append(GroupPriceDetail(
            group_id=group.id,
            group_name=group.group_name,
            sample_count=sample_count,
            base_price=base_price,
            options_fee=options_fee,
            subtotal=base_price + options_fee
        ))

        total_sample_count += sample_count
        total_base_price += base_price
        total_options_fee += options_fee

    return success_response(data=CalculateGroupsPriceResponse(
        groups=group_details,
        total_sample_count=total_sample_count,
        total_base_price=total_base_price,
        total_options_fee=total_options_fee,
        total_amount=total_base_price + total_options_fee
    ).model_dump())


# ==================== 提交 ====================

@router.post("/submit", summary="批量提交样品组生成订单")
async def submit_sample_groups(
    data: SubmitGroupsRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    批量提交样品组生成订单
    - merge_order=True: 合并为一个订单
    - merge_order=False: 每个样品组生成独立订单
    """
    from app.models.order import Order, OrderSample, OrderFee
    from app.models.project_option import OrderOptionSelection
    import uuid

    groups = db.query(SampleGroup).filter(
        SampleGroup.id.in_(data.group_ids),
        SampleGroup.user_id == current_user.id,
        SampleGroup.status == "draft"
    ).all()

    if len(groups) != len(data.group_ids):
        return error_response(message="部分样品组不存在、无权访问或已提交")

    # 验证所有样品组有样品
    for group in groups:
        if not group.items:
            return error_response(message=f"样品组 '{group.group_name or group.group_index}' 没有样品")

    order_ids = []
    total_amount = Decimal("0")

    if data.merge_order:
        # 合并为一个订单
        # 确保所有样品组是同一个项目
        project_ids = set(g.project_id for g in groups)
        if len(project_ids) > 1:
            return error_response(message="合并订单时所有样品组必须属于同一项目")

        project = db.query(Project).filter(Project.id == groups[0].project_id).first()

        # 计算总价
        total_sample_count = 0
        total_options_fee = Decimal("0")
        all_samples = []

        for group in groups:
            sample_count = sum(item.quantity for item in group.items)
            total_sample_count += sample_count

            base_price = Decimal(str(project.price)) * sample_count if project else Decimal("0")
            options_fee = calculate_options_fee(db, group.option_selections, sample_count, base_price)
            total_options_fee += options_fee

            all_samples.extend(group.items)

        base_amount = Decimal(str(project.price)) * total_sample_count if project else Decimal("0")
        subtotal = base_amount + total_options_fee
        discount_amount = Decimal("0")
        used_user_coupon = None
        if data.coupon_id and project:
            discount_amount, _, used_user_coupon = calculate_coupon_discount(db, current_user, project, data.coupon_id, subtotal)
        order_amount = subtotal - discount_amount

        # 创建订单
        order = Order(
            order_no=f"SG{uuid.uuid4().hex[:12].upper()}",
            user_id=current_user.id,
            project_id=project.id if project else None,
            sample_count=total_sample_count,
            unit_price=project.price if project else Decimal("0"),
            base_amount=base_amount,
            discount_amount=discount_amount,
            options_fee=total_options_fee,
            total_amount=order_amount,
            address_id=data.address_id,
            remark=data.remark,
            status="pending"
        )
        db.add(order)
        db.flush()

        # 添加样品
        for item in all_samples:
            order_sample = OrderSample(
                order_id=order.id,
                sample_no=item.sample_no,
                sample_name=item.sample_name,
                sample_composition=item.sample_composition,
                sample_state=item.sample_state,
                danger_type=item.danger_type,
                storage_requirement=item.storage_requirement,
                quantity=item.quantity,
                remark=item.remark
            )
            db.add(order_sample)

        # 添加选项费用
        if total_options_fee > 0:
            db.add(OrderFee(
                order_id=order.id,
                fee_type="options",
                amount=total_options_fee,
                description="选项费用"
            ))

        # 更新样品组状态
        for group in groups:
            group.status = "submitted"
            group.order_id = order.id

        # 合并订单：优惠券归属第一个生成的订单
        mark_user_coupon_used(used_user_coupon, order.id)

        order_ids.append(order.id)
        total_amount = order_amount

    else:
        # 每个样品组独立订单
        for group in groups:
            project = db.query(Project).filter(Project.id == group.project_id).first()
            sample_count = sum(item.quantity for item in group.items)

            base_price = Decimal(str(project.price)) * sample_count if project else Decimal("0")
            options_fee = calculate_options_fee(db, group.option_selections, sample_count, base_price)
            subtotal = base_price + options_fee
            discount_amount = Decimal("0")
            used_user_coupon_loop = None
            if data.coupon_id and project and not order_ids:
                # 多个独立订单时优惠券只能用于首个订单，避免一券多用
                discount_amount, _, used_user_coupon_loop = calculate_coupon_discount(db, current_user, project, data.coupon_id, subtotal)
            order_amount = subtotal - discount_amount

            # 创建订单
            order = Order(
                order_no=f"SG{uuid.uuid4().hex[:12].upper()}",
                user_id=current_user.id,
                project_id=project.id if project else None,
                sample_count=sample_count,
                unit_price=project.price if project else Decimal("0"),
                base_amount=base_price,
                discount_amount=discount_amount,
                options_fee=options_fee,
                total_amount=order_amount,
                address_id=data.address_id,
                remark=data.remark,
                status="pending"
            )
            db.add(order)
            db.flush()

            # 添加样品
            for item in group.items:
                order_sample = OrderSample(
                    order_id=order.id,
                    sample_no=item.sample_no,
                    sample_name=item.sample_name,
                    sample_composition=item.sample_composition,
                    sample_state=item.sample_state,
                    danger_type=item.danger_type,
                    storage_requirement=item.storage_requirement,
                    quantity=item.quantity,
                    remark=item.remark
                )
                db.add(order_sample)

            # 添加选项费用
            if options_fee > 0:
                db.add(OrderFee(
                    order_id=order.id,
                    fee_type="options",
                    amount=options_fee,
                    description="选项费用"
                ))

            # 更新样品组状态
            group.status = "submitted"
            group.order_id = order.id

            # 把使用过的优惠券标记为已使用
            mark_user_coupon_used(used_user_coupon_loop, order.id)

            order_ids.append(order.id)
            total_amount += order_amount

    db.commit()

    return success_response(
        data=SubmitGroupsResponse(
            order_ids=order_ids,
            total_amount=total_amount,
            message=f"成功创建 {len(order_ids)} 个订单"
        ).model_dump()
    )
