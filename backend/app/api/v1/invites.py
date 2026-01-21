"""
邀请好友功能API
"""
from fastapi import APIRouter, Depends, Query, Body, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc
from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal
from datetime import datetime
import qrcode
from io import BytesIO
import base64
import uuid
import os

from app.core.database import get_db
from app.core.response import Response
from app.core.config import settings
from app.api.v1.deps import get_current_user
from app.models.user import User
from app.models.invite import InviteRecord, WithdrawRecord, InviteConfig, InviteStatus, WithdrawStatus, InviteQRCodeRecord


router = APIRouter()


# ==================== 二维码相关模型 ====================

class QRCodeCreate(BaseModel):
    """创建二维码请求"""
    name: str  # 二维码名称
    scene: str = "personal"  # 场景: personal/company/activity


class InviteQRCode(BaseModel):
    """邀请二维码"""
    id: int
    name: str
    scene: str
    qrcode_url: str
    invite_code: str
    scan_count: int = 0
    register_count: int = 0
    created_at: datetime


class WithdrawRequest(BaseModel):
    """提现请求"""
    amount: float
    account_type: str  # alipay/wechat/bank
    account_name: str
    account_number: str


@router.get("/stats", summary="获取邀请统计")
async def get_invite_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取用户的邀请统计数据
    """
    # 查询邀请记录
    invite_records = db.query(InviteRecord).filter(
        InviteRecord.inviter_id == current_user.id
    ).all()
    
    # 统计数据
    total_invites = len(invite_records)
    completed_invites = len([r for r in invite_records if r.status == InviteStatus.COMPLETED])
    pending_invites = len([r for r in invite_records if r.status == InviteStatus.PENDING])
    
    # 计算奖励金额
    total_reward = sum(float(r.reward_amount) for r in invite_records if r.status == InviteStatus.COMPLETED)
    
    # 查询已提现金额
    withdrawn_records = db.query(WithdrawRecord).filter(
        WithdrawRecord.user_id == current_user.id,
        WithdrawRecord.status.in_([WithdrawStatus.APPROVED, WithdrawStatus.COMPLETED])
    ).all()
    withdrawn = sum(float(r.amount) for r in withdrawn_records)
    
    # 可提现金额
    withdrawable = total_reward - withdrawn
    
    return Response.success(data={
        "withdrawable": withdrawable,
        "my_invites": total_invites,
        "completed_invites": completed_invites,
        "pending_invites": pending_invites,
        "total_reward": total_reward,
        "withdrawn": withdrawn
    })


@router.get("/records", summary="获取邀请记录")
async def get_invite_records(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取用户的邀请记录
    """
    # 查询邀请记录
    query = db.query(InviteRecord).filter(
        InviteRecord.inviter_id == current_user.id
    )
    
    # 总数
    total = query.count()
    
    # 分页查询
    items = query.order_by(InviteRecord.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    
    # 格式化返回数据
    records = []
    for item in items:
        records.append({
            "id": item.id,
            "invitee_name": item.invitee_name,
            "invitee_phone": item.invitee_phone,
            "reward_amount": float(item.reward_amount) if item.reward_amount else 0,
            "status": item.status.value,
            "first_order_amount": float(item.first_order_amount) if item.first_order_amount else 0,
            "invited_at": item.invited_at.isoformat() if item.invited_at else None,
            "completed_at": item.completed_at.isoformat() if item.completed_at else None
        })
    
    return Response.success(data={
        "items": records,
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.post("/withdraw", summary="申请提现")
async def withdraw_rewards(
    amount: float = Query(..., description="提现金额"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    申请提现邀请奖励
    """
    # 获取邀请配置
    config = db.query(InviteConfig).filter(InviteConfig.is_active == 1).first()
    if not config:
        raise HTTPException(status_code=400, detail="邀请功能暂未开放")
    
    # 检查提现金额
    amount = Decimal(str(data.amount))
    if amount < config.min_withdraw_amount:
        raise HTTPException(status_code=400, detail=f"最低提现金额为{config.min_withdraw_amount}元")
    
    # 计算可提现金额
    invite_records = db.query(InviteRecord).filter(
        InviteRecord.inviter_id == current_user.id,
        InviteRecord.status == InviteStatus.COMPLETED
    ).all()
    total_reward = sum(r.reward_amount for r in invite_records)
    
    withdrawn_records = db.query(WithdrawRecord).filter(
        WithdrawRecord.user_id == current_user.id,
        WithdrawRecord.status.in_([WithdrawStatus.APPROVED, WithdrawStatus.COMPLETED])
    ).all()
    withdrawn = sum(r.amount for r in withdrawn_records)
    
    available = total_reward - withdrawn
    
    if amount > available:
        raise HTTPException(status_code=400, detail=f"可提现金额不足，当前可提现：{available}元")
    
    # 创建提现记录
    withdraw = WithdrawRecord(
        user_id=current_user.id,
        amount=amount,
        withdraw_type="invite_reward",
        account_type=data.account_type,
        account_name=data.account_name,
        account_number=data.account_number,
        status=WithdrawStatus.PENDING
    )
    db.add(withdraw)
    db.commit()
    db.refresh(withdraw)
    
    return Response.success(data={
        "withdraw_id": withdraw.id,
        "amount": float(withdraw.amount),
        "status": withdraw.status.value
    }, message="提现申请已提交，请等待审核")


# ==================== 推广二维码功能 ====================

def generate_invite_code():
    """生成唯一邀请码"""
    return uuid.uuid4().hex[:12].upper()


def generate_qrcode_image(url: str) -> bytes:
    """生成二维码图片"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer.getvalue()


@router.get("/qrcode/list", summary="获取我的推广二维码列表")
async def get_my_qrcodes(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取当前用户的推广二维码列表"""
    query = db.query(InviteQRCodeRecord).filter(
        InviteQRCodeRecord.user_id == current_user.id,
        InviteQRCodeRecord.is_active == 1
    )

    total = query.count()
    items = query.order_by(desc(InviteQRCodeRecord.created_at)).offset((page - 1) * page_size).limit(page_size).all()

    return Response.success(data={
        "items": [
            {
                "id": item.id,
                "name": item.name,
                "scene": item.scene,
                "invite_code": item.invite_code,
                "qrcode_url": item.qrcode_url,
                "scan_count": item.scan_count or 0,
                "register_count": item.register_count or 0,
                "created_at": item.created_at.isoformat() if item.created_at else None
            }
            for item in items
        ],
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.post("/qrcode/create", summary="生成推广二维码")
async def create_invite_qrcode(
    data: QRCodeCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    生成推广二维码
    - 生成唯一邀请码
    - 生成二维码图片并上传至OSS
    - 返回二维码信息
    """
    # 生成邀请码
    invite_code = generate_invite_code()

    # 确保邀请码唯一
    while db.query(InviteQRCodeRecord).filter(InviteQRCodeRecord.invite_code == invite_code).first():
        invite_code = generate_invite_code()

    # 生成落地页URL（H5页面，扫码后跳转小程序）
    base_url = getattr(settings, 'H5_BASE_URL', 'https://eceshi.com/h5')
    landing_url = f"{base_url}/invite?code={invite_code}"

    # 生成二维码图片
    qrcode_bytes = generate_qrcode_image(landing_url)

    # 保存二维码图片到本地静态目录
    static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'static', 'qrcodes')
    os.makedirs(static_dir, exist_ok=True)

    filename = f"invite_{current_user.id}_{invite_code}.png"
    filepath = os.path.join(static_dir, filename)

    with open(filepath, 'wb') as f:
        f.write(qrcode_bytes)

    # 生成可访问的URL
    qrcode_url = f"/static/qrcodes/{filename}"

    # 创建记录
    qr_record = InviteQRCodeRecord(
        user_id=current_user.id,
        name=data.name,
        scene=data.scene,
        invite_code=invite_code,
        qrcode_url=qrcode_url,
        is_active=1
    )
    db.add(qr_record)
    db.commit()
    db.refresh(qr_record)

    return Response.success(data={
        "id": qr_record.id,
        "name": qr_record.name,
        "scene": qr_record.scene,
        "invite_code": invite_code,
        "qrcode_url": qrcode_url,
        "landing_url": landing_url
    }, message="二维码生成成功")


@router.get("/qrcode/{qrcode_id}/image", summary="获取二维码图片")
async def get_qrcode_image(
    qrcode_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取二维码图片（用于下载）"""
    qr_record = db.query(InviteQRCodeRecord).filter(
        InviteQRCodeRecord.id == qrcode_id,
        InviteQRCodeRecord.user_id == current_user.id
    ).first()

    if not qr_record:
        raise HTTPException(status_code=404, detail="二维码不存在")

    # 生成落地页URL
    base_url = getattr(settings, 'H5_BASE_URL', 'https://eceshi.com/h5')
    landing_url = f"{base_url}/invite?code={qr_record.invite_code}"

    # 重新生成二维码图片
    qrcode_bytes = generate_qrcode_image(landing_url)

    return StreamingResponse(
        BytesIO(qrcode_bytes),
        media_type="image/png",
        headers={"Content-Disposition": f"attachment; filename=invite_{qr_record.invite_code}.png"}
    )


@router.delete("/qrcode/{qrcode_id}", summary="删除推广二维码")
async def delete_invite_qrcode(
    qrcode_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除推广二维码（软删除）"""
    qr_record = db.query(InviteQRCodeRecord).filter(
        InviteQRCodeRecord.id == qrcode_id,
        InviteQRCodeRecord.user_id == current_user.id
    ).first()

    if not qr_record:
        raise HTTPException(status_code=404, detail="二维码不存在")

    qr_record.is_active = 0
    db.commit()

    return Response.success(message="删除成功")


@router.get("/qrcode/scan/{invite_code}", summary="扫码记录（公开接口）")
async def scan_qrcode(
    invite_code: str,
    db: Session = Depends(get_db)
):
    """
    记录扫码事件（公开接口，无需登录）
    返回邀请人信息和落地页跳转参数
    """
    qr_record = db.query(InviteQRCodeRecord).filter(
        InviteQRCodeRecord.invite_code == invite_code,
        InviteQRCodeRecord.is_active == 1
    ).first()

    if not qr_record:
        raise HTTPException(status_code=404, detail="邀请码无效")

    # 增加扫描计数
    qr_record.scan_count = (qr_record.scan_count or 0) + 1
    db.commit()

    # 获取邀请人信息
    inviter = db.query(User).filter(User.id == qr_record.user_id).first()

    return Response.success(data={
        "invite_code": invite_code,
        "inviter_name": inviter.nickname if inviter else None,
        "scene": qr_record.scene,
        "appid": getattr(settings, 'WECHAT_APPID', ''),
        "path": f"/pages/index/index?inviter={invite_code}"
    })

