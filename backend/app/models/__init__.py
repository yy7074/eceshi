"""
数据库模型
"""
from app.models.user import User, UserCertification, UserStatus, MembershipLevel
from app.models.sms_code import SMSCode
from app.models.order import Order, OrderSample, OrderFee, OrderStatusHistory, Payment, UserAddress
from app.models.project import ProjectCategory, Project, ProjectReview
from app.models.coupon import Coupon, UserCoupon, CouponType, CouponStatus, UserCouponStatus
from app.models.recharge import RechargeRecord, RechargeStatus, RechargeMethod
from app.models.points import PointsGoods, PointsRecord, PointsExchangeRecord
from app.models.group import UserGroup, GroupMember, GroupRole, GroupStatus
from app.models.invite import InviteRecord, WithdrawRecord, InviteConfig, InviteStatus, WithdrawStatus
from app.models.invoice import Invoice, InvoiceType, InvoiceStatus
from app.models.lottery import LotteryPrize, LotteryRecord, LotteryChance, PrizeType, PrizeStatus
# 新增模型
from app.models.banner import Banner
from app.models.announcement import Announcement, UserNotification
from app.models.help import HelpCategory, HelpArticle
from app.models.chat import ChatSession, ChatMessage, QuickReply
from app.models.contract import Contract
from app.models.report import Report
from app.models.sample import SampleTracking, SampleLogistics
from app.models.franchise import FranchiseApplication

__all__ = [
    "User",
    "UserCertification", 
    "UserStatus",
    "MembershipLevel",
    "SMSCode",
    "Order",
    "OrderSample",
    "OrderFee",
    "OrderStatusHistory",
    "Payment",
    "UserAddress",
    "ProjectCategory",
    "Project",
    "ProjectReview",
    "Coupon",
    "UserCoupon",
    "CouponType",
    "CouponStatus",
    "UserCouponStatus",
    "RechargeRecord",
    "RechargeStatus",
    "RechargeMethod",
    "PointsGoods",
    "PointsRecord",
    "PointsExchangeRecord",
    "UserGroup",
    "GroupMember",
    "GroupRole",
    "GroupStatus",
    "InviteRecord",
    "WithdrawRecord",
    "InviteConfig",
    "InviteStatus",
    "WithdrawStatus",
    "Invoice",
    "InvoiceType",
    "InvoiceStatus",
    "LotteryPrize",
    "LotteryRecord",
    "LotteryChance",
    "PrizeType",
    "PrizeStatus",
    # 新增
    "Banner",
    "Announcement",
    "UserNotification",
    "HelpCategory",
    "HelpArticle",
    "ChatSession",
    "ChatMessage",
    "QuickReply",
    "Contract",
    "Report",
    "SampleTracking",
    "SampleLogistics",
    "FranchiseApplication"
]

