"""
信用系统API
信用额度、欠款管理、还款
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func as sql_func
from decimal import Decimal
from datetime import datetime, timedelta
import json
import uuid

from app.core.database import get_db
from app.core.response import Response
from app.models.user import User
from app.models.credit import (
    CreditRecord, CreditDebt, Repayment, CreditLimitApplication,
    CreditTransactionType, CreditTransactionStatus, RepaymentStatus
)
from app.models.order import Order, OrderStatusHistory
from app.schemas.credit import (
    CreditInfoResponse, CreditPayRequest, RepaymentRequest,
    CreditLimitApplicationRequest
)
from app.api.v1.deps import get_current_user


router = APIRouter()


@router.get("/info", summary="获取信用额度信息")
async def get_credit_info(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取当前用户的信用额度信息
    包括：总额度、已用额度、可用额度、总欠款
    """
    # 计算总欠款
    total_debt = db.query(sql_func.sum(CreditDebt.remaining_amount)).filter(
        CreditDebt.user_id == current_user.id,
        CreditDebt.status != RepaymentStatus.PAID
    ).scalar() or Decimal('0')

    available_credit = current_user.credit_limit - current_user.used_credit

    return Response.success(data={
        "credit_limit": float(current_user.credit_limit),
        "used_credit": float(current_user.used_credit),
        "available_credit": float(available_credit),
        "total_debt": float(total_debt),
        "is_certified": current_user.is_certified
    })


@router.get("/debts", summary="获取欠款列表")
async def get_debt_list(
    status: str = None,
    page: int = 1,
    page_size: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取用户欠款列表

    - status: 筛选状态 unpaid/partial/paid
    """
    query = db.query(CreditDebt).filter(CreditDebt.user_id == current_user.id)

    if status:
        try:
            status_enum = RepaymentStatus(status)
            query = query.filter(CreditDebt.status == status_enum)
        except ValueError:
            pass

    # 总欠款
    total_debt = db.query(sql_func.sum(CreditDebt.remaining_amount)).filter(
        CreditDebt.user_id == current_user.id,
        CreditDebt.status != RepaymentStatus.PAID
    ).scalar() or Decimal('0')

    # 总数
    total = query.count()

    # 分页
    offset = (page - 1) * page_size
    debts = query.order_by(CreditDebt.created_at.desc()).offset(offset).limit(page_size).all()

    debt_list = []
    for debt in debts:
        debt_list.append({
            "id": debt.id,
            "order_id": debt.order_id,
            "order_no": debt.order_no,
            "original_amount": float(debt.original_amount),
            "paid_amount": float(debt.paid_amount),
            "remaining_amount": float(debt.remaining_amount),
            "status": debt.status.value if debt.status else "unpaid",
            "due_date": debt.due_date.isoformat() if debt.due_date else None,
            "created_at": debt.created_at.isoformat() if debt.created_at else None
        })

    return Response.success(data={
        "total_debt": float(total_debt),
        "debt_count": total,
        "page": page,
        "page_size": page_size,
        "debts": debt_list
    })


@router.post("/pay", summary="信用支付")
async def credit_pay(
    request: CreditPayRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    使用信用额度支付订单

    1. 检查是否已认证
    2. 检查可用额度是否足够
    3. 创建欠款记录
    4. 更新用户已用额度
    5. 创建交易记录
    """
    # 检查认证
    if not current_user.is_certified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="请先完成实名认证"
        )

    # 检查订单
    order = db.query(Order).filter(Order.id == request.order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订单不存在"
        )

    if order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权操作此订单"
        )

    # 检查可用额度
    available_credit = current_user.credit_limit - current_user.used_credit
    if request.amount > available_credit:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"可用额度不足，当前可用: {available_credit}"
        )

    # 创建欠款记录
    due_date = datetime.now() + timedelta(days=30)  # 30天后到期
    debt = CreditDebt(
        user_id=current_user.id,
        order_id=order.id,
        order_no=order.order_no,
        original_amount=request.amount,
        paid_amount=Decimal('0'),
        remaining_amount=request.amount,
        status=RepaymentStatus.UNPAID,
        due_date=due_date
    )
    db.add(debt)

    # 记录交易前余额
    balance_before = available_credit

    # 更新用户已用额度
    current_user.used_credit = current_user.used_credit + request.amount
    balance_after = current_user.credit_limit - current_user.used_credit

    # 更新订单支付状态
    order.credit_amount = request.amount
    order.paid_fee = (order.paid_fee or Decimal("0")) + request.amount
    order.payment_method = "credit"
    order.payment_status = "paid"
    order.status = "confirmed"
    order.paid_at = datetime.now()
    order.payment_time = datetime.now()

    history = OrderStatusHistory(
        order_id=order.id,
        from_status="pending_payment",
        to_status="confirmed",
        operator_id=current_user.id,
        operator_type="user",
        remark="信用支付成功"
    )
    db.add(history)

    # 创建交易记录
    record = CreditRecord(
        user_id=current_user.id,
        transaction_type=CreditTransactionType.CONSUME,
        amount=request.amount,
        balance_before=balance_before,
        balance_after=balance_after,
        order_id=order.id,
        order_no=order.order_no,
        status=CreditTransactionStatus.SUCCESS,
        remark=f"订单{order.order_no}信用支付"
    )
    db.add(record)

    db.commit()
    db.refresh(debt)

    return Response.success(
        message="信用支付成功",
        data={
            "debt_id": debt.id,
            "remaining_credit": float(balance_after)
        }
    )


@router.post("/repay", summary="还款")
async def repay(
    request: RepaymentRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    还款

    1. 支持指定欠款ID还款
    2. 不指定则按时间顺序还款
    3. 支持余额支付或第三方支付
    """
    # 获取待还欠款
    if request.debt_ids:
        debts = db.query(CreditDebt).filter(
            CreditDebt.user_id == current_user.id,
            CreditDebt.id.in_(request.debt_ids),
            CreditDebt.status != RepaymentStatus.PAID
        ).order_by(CreditDebt.created_at).all()
    else:
        # 按时间顺序获取未还清的欠款
        debts = db.query(CreditDebt).filter(
            CreditDebt.user_id == current_user.id,
            CreditDebt.status != RepaymentStatus.PAID
        ).order_by(CreditDebt.created_at).all()

    if not debts:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="没有待还款的欠款"
        )

    # 计算总欠款
    total_remaining = sum(d.remaining_amount for d in debts)

    # 还款金额不能超过总欠款
    repay_amount = min(request.amount, total_remaining)

    # 生成还款单号
    repayment_no = f"RP{datetime.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:6].upper()}"

    # 如果是余额支付
    if request.payment_method == "balance":
        if current_user.prepaid_balance < repay_amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="余额不足"
            )

        # 扣除余额
        current_user.prepaid_balance = current_user.prepaid_balance - repay_amount

        # 分配还款到各欠款
        remaining_repay = repay_amount
        repaid_debt_ids = []

        for debt in debts:
            if remaining_repay <= 0:
                break

            if remaining_repay >= debt.remaining_amount:
                # 全额还清此欠款
                pay_this = debt.remaining_amount
                debt.paid_amount = debt.original_amount
                debt.remaining_amount = Decimal('0')
                debt.status = RepaymentStatus.PAID
                debt.paid_at = datetime.now()
            else:
                # 部分还款
                pay_this = remaining_repay
                debt.paid_amount = debt.paid_amount + pay_this
                debt.remaining_amount = debt.remaining_amount - pay_this
                debt.status = RepaymentStatus.PARTIAL

            remaining_repay -= pay_this
            repaid_debt_ids.append(debt.id)

        # 释放信用额度
        current_user.used_credit = current_user.used_credit - repay_amount

        # 创建还款记录
        repayment = Repayment(
            user_id=current_user.id,
            repayment_no=repayment_no,
            amount=repay_amount,
            payment_method="balance",
            debt_ids=json.dumps(repaid_debt_ids),
            status=CreditTransactionStatus.SUCCESS,
            paid_at=datetime.now()
        )
        db.add(repayment)

        # 创建交易记录
        record = CreditRecord(
            user_id=current_user.id,
            transaction_type=CreditTransactionType.REPAY,
            amount=repay_amount,
            balance_before=current_user.credit_limit - current_user.used_credit - repay_amount,
            balance_after=current_user.credit_limit - current_user.used_credit,
            status=CreditTransactionStatus.SUCCESS,
            remark=f"还款{repay_amount}元"
        )
        db.add(record)

        db.commit()

        return Response.success(
            message="还款成功",
            data={
                "repayment_no": repayment_no,
                "amount": float(repay_amount),
                "status": "success"
            }
        )

    else:
        # 第三方支付，创建待支付的还款记录
        repayment = Repayment(
            user_id=current_user.id,
            repayment_no=repayment_no,
            amount=repay_amount,
            payment_method=request.payment_method,
            debt_ids=json.dumps([d.id for d in debts]),
            status=CreditTransactionStatus.PENDING
        )
        db.add(repayment)
        db.commit()

        # TODO: 调用第三方支付接口生成支付链接
        payment_url = f"/api/v1/payments/repay?repayment_no={repayment_no}"

        return Response.success(
            message="请完成支付",
            data={
                "repayment_no": repayment_no,
                "amount": float(repay_amount),
                "status": "pending",
                "payment_url": payment_url
            }
        )


@router.get("/records", summary="获取交易记录")
async def get_credit_records(
    transaction_type: str = None,
    page: int = 1,
    page_size: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取信用交易记录

    - transaction_type: 筛选类型 consume/repay/refund/grant/adjust
    """
    query = db.query(CreditRecord).filter(CreditRecord.user_id == current_user.id)

    if transaction_type:
        try:
            type_enum = CreditTransactionType(transaction_type)
            query = query.filter(CreditRecord.transaction_type == type_enum)
        except ValueError:
            pass

    total = query.count()

    offset = (page - 1) * page_size
    records = query.order_by(CreditRecord.created_at.desc()).offset(offset).limit(page_size).all()

    record_list = []
    for record in records:
        record_list.append({
            "id": record.id,
            "transaction_type": record.transaction_type.value if record.transaction_type else None,
            "amount": float(record.amount),
            "balance_before": float(record.balance_before) if record.balance_before else None,
            "balance_after": float(record.balance_after) if record.balance_after else None,
            "order_no": record.order_no,
            "status": record.status.value if record.status else None,
            "remark": record.remark,
            "created_at": record.created_at.isoformat() if record.created_at else None
        })

    return Response.success(data={
        "total": total,
        "page": page,
        "page_size": page_size,
        "records": record_list
    })


@router.get("/repayments", summary="获取还款记录")
async def get_repayment_records(
    page: int = 1,
    page_size: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取还款记录列表"""
    query = db.query(Repayment).filter(Repayment.user_id == current_user.id)

    total = query.count()

    offset = (page - 1) * page_size
    repayments = query.order_by(Repayment.created_at.desc()).offset(offset).limit(page_size).all()

    repayment_list = []
    for r in repayments:
        repayment_list.append({
            "id": r.id,
            "repayment_no": r.repayment_no,
            "amount": float(r.amount),
            "payment_method": r.payment_method,
            "status": r.status.value if r.status else None,
            "created_at": r.created_at.isoformat() if r.created_at else None,
            "paid_at": r.paid_at.isoformat() if r.paid_at else None
        })

    return Response.success(data={
        "total": total,
        "page": page,
        "page_size": page_size,
        "repayments": repayment_list
    })


@router.post("/limit/apply", summary="申请提升额度")
async def apply_credit_limit(
    request: CreditLimitApplicationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    申请提升信用额度

    需要联系技术老师审核
    """
    if not current_user.is_certified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="请先完成实名认证"
        )

    # 检查是否有待审核的申请
    pending = db.query(CreditLimitApplication).filter(
        CreditLimitApplication.user_id == current_user.id,
        CreditLimitApplication.status == "pending"
    ).first()

    if pending:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="您有待审核的额度申请"
        )

    # 创建申请
    application = CreditLimitApplication(
        user_id=current_user.id,
        current_limit=current_user.credit_limit,
        requested_limit=request.requested_limit,
        reason=request.reason,
        status="pending"
    )
    db.add(application)
    db.commit()

    return Response.success(
        message="申请已提交，请联系您的技术老师进行审核",
        data={
            "application_id": application.id,
            "current_limit": float(current_user.credit_limit),
            "requested_limit": float(request.requested_limit)
        }
    )


@router.get("/limit/applications", summary="获取额度申请记录")
async def get_limit_applications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取额度申请记录"""
    applications = db.query(CreditLimitApplication).filter(
        CreditLimitApplication.user_id == current_user.id
    ).order_by(CreditLimitApplication.created_at.desc()).all()

    app_list = []
    for app in applications:
        app_list.append({
            "id": app.id,
            "current_limit": float(app.current_limit) if app.current_limit else 0,
            "requested_limit": float(app.requested_limit) if app.requested_limit else 0,
            "approved_limit": float(app.approved_limit) if app.approved_limit else None,
            "status": app.status,
            "review_remark": app.review_remark,
            "created_at": app.created_at.isoformat() if app.created_at else None,
            "reviewed_at": app.reviewed_at.isoformat() if app.reviewed_at else None
        })

    return Response.success(data=app_list)
