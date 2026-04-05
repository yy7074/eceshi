"""
实验室模型
实验室入驻、设备管理、技术人员
"""
from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Boolean, Text, Numeric, Enum, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class LabStatus(str, enum.Enum):
    """实验室状态"""
    PENDING = "pending"  # 待审核
    APPROVED = "approved"  # 已通过
    REJECTED = "rejected"  # 已拒绝
    ACTIVE = "active"  # 运营中
    SUSPENDED = "suspended"  # 已暂停
    CLOSED = "closed"  # 已关闭


class LabType(str, enum.Enum):
    """实验室类型"""
    UNIVERSITY = "university"  # 高校实验室
    RESEARCH = "research"  # 科研机构
    ENTERPRISE = "enterprise"  # 企业实验室
    THIRD_PARTY = "third_party"  # 第三方检测机构
    HOSPITAL = "hospital"  # 医院实验室
    PLATFORM = "platform"  # 平台自营


class Laboratory(Base):
    """实验室表"""
    __tablename__ = "laboratories"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)

    # 基本信息
    name = Column(String(200), nullable=False, comment="实验室名称")
    lab_no = Column(String(32), unique=True, comment="实验室编号(旧)")
    code = Column(String(50), unique=True, index=True, comment="实验室编号")
    short_name = Column(String(100), comment="简称")
    logo = Column(String(255), comment="实验室Logo")
    cover_image = Column(String(255), comment="封面图片")

    # 类型和状态
    lab_type = Column(
        String(50),
        default="university",
        comment="实验室类型"
    )
    type = Column(String(50), comment="类型(旧)")
    level = Column(String(50), comment="级别")
    status = Column(
        String(50),
        default="pending",
        index=True,
        comment="状态"
    )
    is_verified = Column(Boolean, default=False, comment="是否认证")

    # 所属机构信息
    institution = Column(String(200), comment="所属机构")
    department = Column(String(200), comment="所属院系/部门")
    province = Column(String(50), comment="省份")
    city = Column(String(50), comment="城市")
    address = Column(String(500), comment="详细地址")

    # 负责人信息
    contact_name = Column(String(50), comment="联系人姓名")
    contact_person = Column(String(50), comment="联系人(旧)")
    contact_phone = Column(String(20), comment="联系电话")
    contact_email = Column(String(100), comment="联系邮箱")

    # 资质信息
    qualification = Column(Text, comment="资质描述")
    certification = Column(JSON, comment="资质证书列表")
    business_license = Column(String(255), comment="营业执照")

    # 能力描述
    description = Column(Text, comment="实验室介绍")
    specialties = Column(JSON, comment="专业领域")
    equipments_summary = Column(Text, comment="设备概况")

    # 服务信息
    service_areas = Column(JSON, comment="服务区域")
    service_categories = Column(JSON, comment="服务分类ID列表")
    min_order_amount = Column(Numeric(10, 2), default=0, comment="起订金额")

    # 评价信息
    rating = Column(Numeric(3, 1), default=5.0, comment="评分")
    order_count = Column(Integer, default=0, comment="订单数(旧)")
    total_orders = Column(Integer, default=0, comment="总订单数")
    completed_orders = Column(Integer, default=0, comment="完成订单数")

    # 描述信息(旧)
    introduction = Column(Text, comment="介绍(旧)")
    equipment_list = Column(JSON, comment="设备列表(旧)")

    # 分成比例
    commission_rate = Column(Numeric(5, 2), default=20.0, comment="平台佣金比例(%)")

    # 管理员用户ID
    admin_user_id = Column(BigInteger, comment="管理员用户ID")

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    approved_at = Column(DateTime(timezone=True), comment="审核通过时间")

    # 关系
    equipments = relationship("LabEquipment", back_populates="laboratory")
    staff = relationship("LabStaff", back_populates="laboratory")


class LabApplication(Base):
    """实验室入驻申请表"""
    __tablename__ = "lab_applications"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)

    # 申请人信息
    applicant_user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True, comment="申请人用户ID")
    applicant_name = Column(String(50), comment="申请人姓名")
    applicant_phone = Column(String(20), comment="申请人电话")
    applicant_email = Column(String(100), comment="申请人邮箱")
    applicant_position = Column(String(50), comment="申请人职位")

    # 实验室信息
    lab_name = Column(String(200), nullable=False, comment="实验室名称")
    lab_type = Column(
        String(50),
        default="university",
        comment="实验室类型"
    )
    institution = Column(String(200), comment="所属机构")
    department = Column(String(200), comment="所属院系/部门")
    province = Column(String(50), comment="省份")
    city = Column(String(50), comment="城市")
    address = Column(String(500), comment="详细地址")

    # 资质信息
    qualification = Column(Text, comment="资质描述")
    certification_files = Column(JSON, comment="资质证书文件列表")
    business_license = Column(String(255), comment="营业执照")

    # 能力描述
    description = Column(Text, comment="实验室介绍")
    specialties = Column(JSON, comment="专业领域")
    equipments_desc = Column(Text, comment="设备情况描述")

    # 服务意向
    intended_services = Column(JSON, comment="意向服务类型")
    expected_monthly_orders = Column(Integer, comment="预期月订单量")

    # 审核信息
    status = Column(String(20), default="pending", index=True, comment="状态: pending/reviewing/approved/rejected")
    reviewer_id = Column(BigInteger, comment="审核人ID")
    review_remark = Column(Text, comment="审核备注")
    reject_reason = Column(String(500), comment="拒绝原因")
    reviewed_at = Column(DateTime(timezone=True), comment="审核时间")

    # 关联的实验室ID（审核通过后创建）
    laboratory_id = Column(BigInteger, comment="关联实验室ID")

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 关系
    applicant = relationship("User", backref="lab_applications")


class LabEquipment(Base):
    """实验室设备表"""
    __tablename__ = "lab_equipments"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    laboratory_id = Column(BigInteger, ForeignKey("laboratories.id"), nullable=False, index=True, comment="实验室ID")

    # 设备信息
    name = Column(String(200), nullable=False, comment="设备名称")
    model = Column(String(100), comment="型号规格")
    brand = Column(String(100), comment="品牌")
    serial_number = Column(String(100), comment="设备编号")

    # 分类
    category = Column(String(50), comment="设备类别")

    # 描述
    description = Column(Text, comment="设备描述")
    specifications = Column(JSON, comment="技术参数")
    images = Column(JSON, comment="设备图片")

    # 状态
    status = Column(String(20), default="available", comment="状态: available/in_use/maintenance/retired")

    # 使用信息
    unit_price = Column(Numeric(10, 2), comment="单次使用价格")
    hourly_rate = Column(Numeric(10, 2), comment="每小时费率")

    # 时间戳
    purchase_date = Column(DateTime, comment="购入日期")
    last_maintenance = Column(DateTime, comment="最近维护时间")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 关系
    laboratory = relationship("Laboratory", back_populates="equipments")


class LabStaff(Base):
    """实验室技术人员表"""
    __tablename__ = "lab_staff"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    laboratory_id = Column(BigInteger, ForeignKey("laboratories.id"), nullable=False, index=True, comment="实验室ID")
    user_id = Column(Integer, ForeignKey("users.id"), comment="关联用户ID")

    # 基本信息
    name = Column(String(50), nullable=False, comment="姓名")
    phone = Column(String(20), comment="联系电话")
    email = Column(String(100), comment="邮箱")
    avatar = Column(String(255), comment="头像")

    # 职位信息
    position = Column(String(50), comment="职位")
    title = Column(String(50), comment="职称")
    specialties = Column(JSON, comment="专业领域")

    # 角色
    role = Column(String(20), default="technician", comment="角色: admin/technician/assistant")

    # 状态
    is_active = Column(Boolean, default=True, comment="是否在职")

    # 时间戳
    joined_at = Column(DateTime, comment="入职时间")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关系
    laboratory = relationship("Laboratory", back_populates="staff")
    user = relationship("User", backref="lab_staff_records")


class LabSettlement(Base):
    """实验室结算记录"""
    __tablename__ = "lab_settlements"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    lab_id = Column(BigInteger, ForeignKey("laboratories.id"), nullable=False, comment="实验室ID")
    order_id = Column(BigInteger, ForeignKey("orders.id"), comment="关联订单ID")
    order_no = Column(String(32), comment="订单编号")

    # 金额
    amount = Column(Numeric(10, 2), nullable=False, default=0, comment="结算金额")
    commission_rate = Column(Numeric(5, 2), comment="佣金比例")
    commission_amount = Column(Numeric(10, 2), default=0, comment="平台佣金")
    lab_amount = Column(Numeric(10, 2), default=0, comment="实验室实际获得金额")

    # 状态
    status = Column(String(20), default="pending", comment="结算状态: pending/confirmed/paid")
    confirmed_by = Column(Integer, comment="确认人ID")
    confirmed_at = Column(DateTime, comment="确认时间")
    paid_at = Column(DateTime, comment="打款时间")
    remark = Column(Text, comment="备注")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 关系
    laboratory = relationship("Laboratory", backref="settlements")
