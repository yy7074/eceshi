"""
用户模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Enum, Numeric, Boolean
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class UserStatus(enum.Enum):
    """用户状态"""
    ACTIVE = "active"  # 活跃
    INACTIVE = "inactive"  # 未激活
    BANNED = "banned"  # 禁用


class MembershipLevel(enum.Enum):
    """会员等级"""
    NORMAL = 0  # 普通用户
    SILVER = 1  # 银卡
    GOLD = 2  # 金卡
    PLATINUM = 3  # 白金卡


class User(Base):
    """用户表"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, comment="用户ID")
    phone = Column(String(20), unique=True, index=True, nullable=True, comment="手机号")
    password = Column(String(255), nullable=True, comment="密码哈希")
    nickname = Column(String(50), comment="昵称")
    avatar = Column(String(255), comment="头像URL")
    email = Column(String(100), comment="邮箱")
    
    # 微信信息
    wechat_openid = Column(String(100), unique=True, index=True, comment="微信OpenID")
    wechat_unionid = Column(String(100), comment="微信UnionID")
    
    # 认证信息
    is_certified = Column(Boolean, default=False, comment="是否实名认证")
    real_name = Column(String(50), comment="真实姓名")
    id_card = Column(String(20), comment="身份证号")
    
    # 会员信息
    membership_level = Column(
        Enum(MembershipLevel),
        default=MembershipLevel.NORMAL,
        comment="会员等级"
    )
    
    # 额度信息
    credit_limit = Column(Numeric(10, 2), default=0, comment="信用额度")
    used_credit = Column(Numeric(10, 2), default=0, comment="已用信用额度")
    prepaid_balance = Column(Numeric(10, 2), default=0, comment="预付余额")
    
    # 积分信息
    points_balance = Column(Integer, default=0, comment="积分余额")
    total_points_earned = Column(Integer, default=0, comment="累计获得积分")
    total_points_used = Column(Integer, default=0, comment="累计使用积分")
    
    # 统计信息
    total_spent = Column(Numeric(10, 2), default=0, comment="累计消费金额")
    total_orders = Column(Integer, default=0, comment="累计订单数")
    
    # 状态
    status = Column(
        Enum(UserStatus),
        default=UserStatus.ACTIVE,
        comment="用户状态"
    )
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    last_login_at = Column(DateTime(timezone=True), comment="最后登录时间")
    
    def __repr__(self):
        return f"<User {self.phone}>"


class UserCertification(Base):
    """用户认证信息表"""
    __tablename__ = "user_certification"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True, comment="用户ID")
    
    # 学生/教职工信息
    enrollment_year = Column(String(10), comment="入学年份")
    graduation_year = Column(String(10), comment="毕业年份")
    province = Column(String(50), comment="省份")
    city = Column(String(50), comment="城市")
    university = Column(String(100), comment="高校")
    department = Column(String(100), comment="院系")
    
    # 导师信息
    supervisor_name = Column(String(50), comment="导师姓名")
    supervisor_title = Column(String(50), comment="导师职称")
    
    # 证件照片
    student_card_photo = Column(String(255), comment="学生证照片")
    id_card_front = Column(String(255), comment="身份证正面")
    id_card_back = Column(String(255), comment="身份证反面")
    
    # 审核状态
    status = Column(String(20), default="pending", comment="审核状态: pending/approved/rejected")
    reject_reason = Column(String(255), comment="拒绝原因")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    certified_at = Column(DateTime(timezone=True), comment="认证通过时间")

