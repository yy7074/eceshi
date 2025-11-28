"""
抽奖系统API
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import Optional
from datetime import datetime, timedelta
import random

from app.core.database import get_db
from app.core.response import Response
from app.api.v1.deps import get_current_user
from app.models.user import User
from app.models.lottery import LotteryPrize, LotteryRecord, LotteryChance, PrizeType, PrizeStatus


router = APIRouter()


@router.get("/chances", summary="获取抽奖次数")
async def get_lottery_chances(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取用户的抽奖次数"""
    # 查询未使用且未过期的抽奖机会
    now = datetime.utcnow()
    chances = db.query(LotteryChance).filter(
        LotteryChance.user_id == current_user.id,
        LotteryChance.is_used == False,
        (LotteryChance.expire_at == None) | (LotteryChance.expire_at > now)
    ).count()
    
    # 获取今日已抽奖次数
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_draws = db.query(LotteryRecord).filter(
        LotteryRecord.user_id == current_user.id,
        LotteryRecord.created_at >= today_start
    ).count()
    
    return Response.success(data={
        "chances": chances,
        "today_draws": today_draws
    })


@router.post("/draw", summary="进行抽奖")
async def do_lottery(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """进行一次抽奖"""
    now = datetime.utcnow()
    
    # 检查是否有抽奖机会
    chance = db.query(LotteryChance).filter(
        LotteryChance.user_id == current_user.id,
        LotteryChance.is_used == False,
        (LotteryChance.expire_at == None) | (LotteryChance.expire_at > now)
    ).first()
    
    if not chance:
        raise HTTPException(status_code=400, detail="暂无抽奖次数")
    
    # 获取所有可用奖品
    prizes = db.query(LotteryPrize).filter(
        LotteryPrize.is_active == True
    ).order_by(LotteryPrize.sort_order).all()
    
    if not prizes:
        raise HTTPException(status_code=400, detail="暂无可抽取的奖品")
    
    # 按概率抽奖
    total_probability = sum(p.probability for p in prizes)
    if total_probability == 0:
        raise HTTPException(status_code=400, detail="奖品概率配置错误")
    
    rand = random.randint(1, 10000)
    cumulative = 0
    selected_prize = None
    
    for prize in prizes:
        cumulative += prize.probability
        if rand <= cumulative:
            selected_prize = prize
            break
    
    # 如果没选中任何奖品，选择最后一个（通常是谢谢参与）
    if not selected_prize:
        selected_prize = prizes[-1]
    
    # 检查奖品是否还有库存
    if selected_prize.total_limit > 0 and selected_prize.issued_count >= selected_prize.total_limit:
        # 库存不足，选择谢谢参与或其他奖品
        empty_prize = db.query(LotteryPrize).filter(
            LotteryPrize.prize_type == PrizeType.EMPTY,
            LotteryPrize.is_active == True
        ).first()
        if empty_prize:
            selected_prize = empty_prize
    
    # 创建中奖记录
    record = LotteryRecord(
        user_id=current_user.id,
        prize_id=selected_prize.id,
        prize_name=selected_prize.name,
        prize_type=selected_prize.prize_type.value if selected_prize.prize_type else None,
        prize_value=selected_prize.value,
        prize_icon=selected_prize.icon,
        status=PrizeStatus.UNCLAIMED if selected_prize.prize_type != PrizeType.EMPTY else PrizeStatus.CLAIMED,
        expire_at=now + timedelta(days=7)  # 7天内领取
    )
    db.add(record)
    
    # 更新奖品发放数量
    selected_prize.issued_count += 1
    
    # 标记抽奖机会已使用
    chance.is_used = True
    chance.used_at = now
    
    db.commit()
    db.refresh(record)
    
    # 更新机会记录
    chance.record_id = record.id
    db.commit()
    
    return Response.success(data={
        "prize": {
            "id": selected_prize.id,
            "name": selected_prize.name,
            "type": selected_prize.prize_type.value if selected_prize.prize_type else None,
            "icon": selected_prize.icon,
            "value": float(selected_prize.value) if selected_prize.value else 0
        },
        "record_id": record.id,
        "need_claim": selected_prize.prize_type != PrizeType.EMPTY
    }, message="抽奖成功！")


@router.get("/prizes", summary="获取奖品列表")
async def get_prizes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取所有奖品列表"""
    prizes = db.query(LotteryPrize).filter(
        LotteryPrize.is_active == True
    ).order_by(LotteryPrize.sort_order).all()
    
    return Response.success(data={
        "items": [
            {
                "id": p.id,
                "name": p.name,
                "type": p.prize_type.value if p.prize_type else None,
                "icon": p.icon,
                "value": float(p.value) if p.value else 0,
                "probability": f"{p.probability / 100:.1f}%"  # 转换为百分比显示
            }
            for p in prizes
        ]
    })


@router.get("/records", summary="获取中奖记录")
async def get_lottery_records(
    status: Optional[str] = Query(None, description="状态筛选"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取我的中奖记录"""
    query = db.query(LotteryRecord).filter(
        LotteryRecord.user_id == current_user.id
    )
    
    if status:
        query = query.filter(LotteryRecord.status == status)
    
    total = query.count()
    records = query.order_by(desc(LotteryRecord.created_at)).offset((page - 1) * page_size).limit(page_size).all()
    
    return Response.success(data={
        "items": [
            {
                "id": r.id,
                "prize_name": r.prize_name,
                "prize_type": r.prize_type,
                "prize_icon": r.prize_icon,
                "prize_value": float(r.prize_value) if r.prize_value else 0,
                "status": r.status.value if r.status else None,
                "status_text": get_status_text(r.status),
                "created_at": r.created_at.isoformat() if r.created_at else None,
                "claimed_at": r.claimed_at.isoformat() if r.claimed_at else None,
                "expire_at": r.expire_at.isoformat() if r.expire_at else None
            }
            for r in records
        ],
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.post("/claim/{record_id}", summary="领取奖品")
async def claim_prize(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """领取中奖奖品"""
    record = db.query(LotteryRecord).filter(
        LotteryRecord.id == record_id,
        LotteryRecord.user_id == current_user.id
    ).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="中奖记录不存在")
    
    if record.status == PrizeStatus.CLAIMED:
        raise HTTPException(status_code=400, detail="奖品已领取")
    
    if record.status == PrizeStatus.EXPIRED:
        raise HTTPException(status_code=400, detail="奖品已过期")
    
    now = datetime.utcnow()
    if record.expire_at and now > record.expire_at:
        record.status = PrizeStatus.EXPIRED
        db.commit()
        raise HTTPException(status_code=400, detail="奖品已过期")
    
    # 根据奖品类型发放奖励
    prize = db.query(LotteryPrize).filter(LotteryPrize.id == record.prize_id).first()
    
    if prize:
        if prize.prize_type == PrizeType.POINTS:
            # 发放积分
            current_user.points_balance = (current_user.points_balance or 0) + (prize.points_amount or 0)
        elif prize.prize_type == PrizeType.CASH:
            # 发放现金红包到余额
            current_user.prepaid_balance = (current_user.prepaid_balance or 0) + prize.value
        elif prize.prize_type == PrizeType.COUPON and prize.coupon_id:
            # 发放优惠券
            from app.models.coupon import Coupon, UserCoupon, UserCouponStatus
            coupon = db.query(Coupon).filter(Coupon.id == prize.coupon_id).first()
            if coupon:
                user_coupon = UserCoupon(
                    user_id=current_user.id,
                    coupon_id=coupon.id,
                    coupon_name=coupon.name,
                    coupon_type=coupon.type.value if coupon.type else None,
                    discount_value=coupon.cash_amount or coupon.reduction_amount,
                    status=UserCouponStatus.UNUSED,
                    expire_at=now + timedelta(days=coupon.valid_days or 30)
                )
                db.add(user_coupon)
                record.coupon_id = user_coupon.id
    
    record.status = PrizeStatus.CLAIMED
    record.claimed_at = now
    db.commit()
    
    return Response.success(message="奖品领取成功")


@router.get("/recent", summary="获取最近中奖记录（公开）")
async def get_recent_records(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """获取最近中奖记录（用于展示）"""
    records = db.query(LotteryRecord).filter(
        LotteryRecord.prize_type != "empty"
    ).order_by(desc(LotteryRecord.created_at)).limit(limit).all()
    
    # 获取用户信息
    user_ids = [r.user_id for r in records]
    users = {u.id: u for u in db.query(User).filter(User.id.in_(user_ids)).all()}
    
    return Response.success(data={
        "items": [
            {
                "user": mask_phone(users.get(r.user_id).phone if users.get(r.user_id) else "***"),
                "prize": r.prize_name,
                "icon": r.prize_icon,
                "time": format_time_ago(r.created_at)
            }
            for r in records
        ]
    })


def get_status_text(status):
    """获取状态文本"""
    if not status:
        return "未知"
    status_map = {
        PrizeStatus.UNCLAIMED: "未领取",
        PrizeStatus.CLAIMED: "已领取",
        PrizeStatus.EXPIRED: "已过期"
    }
    return status_map.get(status, "未知")


def mask_phone(phone):
    """隐藏手机号中间四位"""
    if not phone or len(phone) < 7:
        return "***"
    return phone[:3] + "****" + phone[-4:]


def format_time_ago(dt):
    """格式化时间为多久前"""
    if not dt:
        return ""
    now = datetime.utcnow()
    diff = now - dt
    if diff.days > 0:
        return f"{diff.days}天前"
    elif diff.seconds >= 3600:
        return f"{diff.seconds // 3600}小时前"
    elif diff.seconds >= 60:
        return f"{diff.seconds // 60}分钟前"
    else:
        return "刚刚"

