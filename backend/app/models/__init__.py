"""
数据库模型
"""
from app.models.user import User, UserCertification, UserStatus, MembershipLevel, IdentityType, EducationLevel
from app.models.sms_code import SMSCode
from app.models.order import Order, OrderSample, OrderFee, OrderStatusHistory, Payment, UserAddress
# 实验室模型必须在project之前导入
from app.models.laboratory import (
    Laboratory, LabApplication, LabEquipment, LabStaff,
    LabStatus, LabType
)
from app.models.project import ProjectCategory, Project, ProjectReview
from app.models.coupon import Coupon, UserCoupon, CouponType, CouponStatus, UserCouponStatus
from app.models.recharge import RechargeRecord, RechargeStatus, RechargeMethod, InvoiceRechargeRecord, InvoiceRechargeStatus
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
from app.models.credit import (
    CreditRecord, CreditDebt, Repayment, CreditLimitApplication,
    CreditTransactionType, CreditTransactionStatus, RepaymentStatus
)
from app.models.role import (
    Role, Permission, role_permissions, user_roles,
    RoleCode, PermissionCode, DEFAULT_ROLE_PERMISSIONS
)
from app.models.project_option import (
    ProjectOption, OrderOptionSelection, OptionType, PriceType
)
from app.models.sample_group import SampleGroup, SampleItem
from app.models.commission import UserCommissionSetting, CommissionRecord

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
    "InvoiceRechargeRecord",
    "InvoiceRechargeStatus",
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
    "FranchiseApplication",
    # 信用系统
    "CreditRecord",
    "CreditDebt",
    "Repayment",
    "CreditLimitApplication",
    "CreditTransactionType",
    "CreditTransactionStatus",
    "RepaymentStatus",
    # 实验室系统
    "Laboratory",
    "LabApplication",
    "LabEquipment",
    "LabStaff",
    "LabStatus",
    "LabType",
    # 角色权限系统
    "Role",
    "Permission",
    "role_permissions",
    "user_roles",
    "RoleCode",
    "PermissionCode",
    "DEFAULT_ROLE_PERMISSIONS",
    # 项目动态选项系统
    "ProjectOption",
    "OrderOptionSelection",
    "OptionType",
    "PriceType",
    # 样品组管理
    "SampleGroup",
    "SampleItem",
    # 佣金系统
    "UserCommissionSetting",
    "CommissionRecord"
]

