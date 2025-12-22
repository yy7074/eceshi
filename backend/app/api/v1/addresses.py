"""
地址管理API
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.order import UserAddress
from app.schemas.order import AddressCreate, AddressUpdate, AddressInDB
from app.core.response import SuccessResponse

router = APIRouter()


@router.get("/list")
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


@router.post("/add")
async def add_address(
    request_data: dict = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    添加地址（兼容前端调用，支持额外字段）
    """
    import json
    print(f"[地址添加] 接收到的原始数据: {json.dumps(request_data, ensure_ascii=False, default=str)}")
    
    # 处理前端可能发送的额外字段映射
    # name -> receiver_name
    if "name" in request_data:
        if "receiver_name" not in request_data:
            request_data["receiver_name"] = request_data["name"]
    
    # detail -> detail_address
    if "detail" in request_data:
        if "detail_address" not in request_data:
            request_data["detail_address"] = request_data["detail"]
    
    # receiver_phone -> phone
    if "receiver_phone" in request_data:
        if "phone" not in request_data:
            request_data["phone"] = request_data["receiver_phone"]
    
    # 验证必需字段
    required_fields = ["receiver_name", "phone", "province", "city", "detail_address"]
    missing_fields = []
    for field in required_fields:
        value = request_data.get(field)
        if not value or (isinstance(value, str) and not value.strip()):
            missing_fields.append(field)
    
    if missing_fields:
        print(f"[地址添加] 缺少必需字段: {missing_fields}, 当前数据键: {list(request_data.keys())}")
        raise HTTPException(status_code=422, detail=f"缺少必需字段: {', '.join(missing_fields)}")
    
    # 如果设置为默认地址，先取消其他默认地址
    is_default = request_data.get("is_default", False)
    if is_default:
        db.query(UserAddress).filter(
            UserAddress.user_id == current_user.id,
            UserAddress.is_default == True
        ).update({"is_default": False})
    
    # 创建地址
    address = UserAddress(
        user_id=current_user.id,
        receiver_name=request_data["receiver_name"],
        phone=request_data["phone"],
        province=request_data["province"],
        city=request_data["city"],
        district=request_data.get("district"),
        detail_address=request_data["detail_address"],
        is_default=is_default
    )
    
    db.add(address)
    db.commit()
    db.refresh(address)
    
    return SuccessResponse(data=AddressInDB.from_orm(address), message="地址添加成功")


@router.post("/create")
async def create_address(
    request_data: dict = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建地址（兼容前端调用，支持额外字段）
    """
    import json
    print(f"[地址创建] 接收到的原始数据: {json.dumps(request_data, ensure_ascii=False, default=str)}")
    
    # 处理前端可能发送的额外字段映射
    # name -> receiver_name
    if "name" in request_data:
        if "receiver_name" not in request_data:
            request_data["receiver_name"] = request_data["name"]
    
    # detail -> detail_address
    if "detail" in request_data:
        if "detail_address" not in request_data:
            request_data["detail_address"] = request_data["detail"]
    
    # receiver_phone -> phone
    if "receiver_phone" in request_data:
        if "phone" not in request_data:
            request_data["phone"] = request_data["receiver_phone"]
    
    print(f"[地址创建] 处理后的数据: {json.dumps(request_data, ensure_ascii=False, default=str)}")
    
    # 验证必需字段
    required_fields = ["receiver_name", "phone", "province", "city", "detail_address"]
    missing_fields = []
    for field in required_fields:
        value = request_data.get(field)
        if not value or (isinstance(value, str) and not value.strip()):
            missing_fields.append(field)
    
    if missing_fields:
        print(f"[地址创建] 缺少必需字段: {missing_fields}, 当前数据键: {list(request_data.keys())}")
        raise HTTPException(status_code=422, detail=f"缺少必需字段: {', '.join(missing_fields)}")
    
    # 如果设置为默认地址，先取消其他默认地址
    is_default = request_data.get("is_default", False)
    if is_default:
        db.query(UserAddress).filter(
            UserAddress.user_id == current_user.id,
            UserAddress.is_default == True
        ).update({"is_default": False})
    
    # 创建地址
    address = UserAddress(
        user_id=current_user.id,
        receiver_name=request_data["receiver_name"],
        phone=request_data["phone"],
        province=request_data["province"],
        city=request_data["city"],
        district=request_data.get("district"),
        detail_address=request_data["detail_address"],
        is_default=is_default
    )
    
    db.add(address)
    db.commit()
    db.refresh(address)
    
    return SuccessResponse(data=AddressInDB.from_orm(address), message="地址创建成功")


@router.put("/{address_id}")
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


@router.delete("/{address_id}")
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


@router.post("/{address_id}/set-default")
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

