"""
地址管理API
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.order import UserAddress
from app.schemas.order import AddressCreate, AddressUpdate, AddressInDB
from app.core.response import SuccessResponse

router = APIRouter()


@router.get("/list", response_model=SuccessResponse)
async def get_address_list(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取地址列表
    """
    addresses = db.query(UserAddress).filter(
        UserAddress.user_id == current_user.id
    ).order_by(UserAddress.is_default.desc(), UserAddress.created_at.desc()).all()
    
    result = [AddressInDB.from_orm(addr) for addr in addresses]
    return SuccessResponse(data=result)


@router.post("/add", response_model=SuccessResponse)
async def add_address(
    data: AddressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    添加地址
    """
    # 如果设置为默认地址，先取消其他默认地址
    if data.is_default:
        db.query(UserAddress).filter(
            UserAddress.user_id == current_user.id,
            UserAddress.is_default == True
        ).update({"is_default": False})
    
    # 创建地址
    address = UserAddress(
        user_id=current_user.id,
        receiver_name=data.receiver_name,
        phone=data.phone,
        province=data.province,
        city=data.city,
        district=data.district,
        detail_address=data.detail_address,
        is_default=data.is_default
    )
    
    db.add(address)
    db.commit()
    db.refresh(address)
    
    return SuccessResponse(data=AddressInDB.from_orm(address), message="地址添加成功")


@router.put("/{address_id}", response_model=SuccessResponse)
async def update_address(
    address_id: int,
    data: AddressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新地址
    """
    address = db.query(UserAddress).filter(
        UserAddress.id == address_id,
        UserAddress.user_id == current_user.id
    ).first()
    
    if not address:
        raise HTTPException(status_code=404, detail="地址不存在")
    
    # 如果设置为默认地址，先取消其他默认地址
    if data.is_default:
        db.query(UserAddress).filter(
            UserAddress.user_id == current_user.id,
            UserAddress.id != address_id,
            UserAddress.is_default == True
        ).update({"is_default": False})
    
    # 更新字段
    update_data = data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(address, field, value)
    
    db.commit()
    db.refresh(address)
    
    return SuccessResponse(data=AddressInDB.from_orm(address), message="地址更新成功")


@router.delete("/{address_id}", response_model=SuccessResponse)
async def delete_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除地址
    """
    address = db.query(UserAddress).filter(
        UserAddress.id == address_id,
        UserAddress.user_id == current_user.id
    ).first()
    
    if not address:
        raise HTTPException(status_code=404, detail="地址不存在")
    
    db.delete(address)
    db.commit()
    
    return SuccessResponse(message="地址删除成功")


@router.post("/{address_id}/set-default", response_model=SuccessResponse)
async def set_default_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    设置默认地址
    """
    address = db.query(UserAddress).filter(
        UserAddress.id == address_id,
        UserAddress.user_id == current_user.id
    ).first()
    
    if not address:
        raise HTTPException(status_code=404, detail="地址不存在")
    
    # 取消其他默认地址
    db.query(UserAddress).filter(
        UserAddress.user_id == current_user.id,
        UserAddress.id != address_id,
        UserAddress.is_default == True
    ).update({"is_default": False})
    
    # 设置为默认
    address.is_default = True
    db.commit()
    
    return SuccessResponse(message="已设置为默认地址")

