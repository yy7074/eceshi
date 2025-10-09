"""
项目和实验室相关模型
"""
from sqlalchemy import Column, BigInteger, String, Integer, DateTime, Boolean, Text, JSON, Numeric
from sqlalchemy.sql import func
from app.core.database import Base


class Laboratory(Base):
    """实验室表"""
    __tablename__ = "laboratories"
    
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    lab_no = Column(String(32), unique=True, nullable=False, comment="实验室编号")
    
    # 基本信息
    name = Column(String(200), nullable=False, comment="实验室名称")
    short_name = Column(String(100), comment="简称")
    type = Column(String(50), comment="实验室类型")
    level = Column(String(50), comment="实验室级别")
    
    # 所属机构
    institution = Column(String(200), comment="所属机构")
    province = Column(String(50), comment="省份")
    city = Column(String(50), comment="城市")
    address = Column(String(500), comment="详细地址")
    
    # 联系方式
    contact_person = Column(String(50), comment="联系人")
    contact_phone = Column(String(20), comment="联系电话")
    contact_email = Column(String(100), comment="联系邮箱")
    
    # 状态
    status = Column(String(20), default="active", comment="状态")
    is_verified = Column(Boolean, default=False, comment="是否认证")
    
    # 评分
    rating = Column(Numeric(3, 1), default=5.0, comment="评分")
    order_count = Column(Integer, default=0, comment="订单数量")
    
    # 简介
    introduction = Column(Text, comment="实验室简介")
    equipment_list = Column(JSON, comment="设备清单")
    
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, onupdate=func.now(), comment="更新时间")


class ProjectCategory(Base):
    """项目分类表"""
    __tablename__ = "project_categories"
    
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    
    # 分类信息
    name = Column(String(100), nullable=False, comment="分类名称")
    code = Column(String(50), unique=True, comment="分类代码")
    parent_id = Column(BigInteger, comment="父分类ID")
    level = Column(Integer, default=1, comment="层级")
    sort_order = Column(Integer, default=0, comment="排序")
    
    # 展示信息
    icon = Column(String(200), comment="图标")
    cover_image = Column(String(500), comment="封面图")
    description = Column(Text, comment="描述")
    
    # 状态
    is_hot = Column(Boolean, default=False, comment="是否热门")
    is_active = Column(Boolean, default=True, comment="是否启用")
    
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")


class Project(Base):
    """检测项目表"""
    __tablename__ = "projects"
    
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    project_no = Column(String(32), unique=True, nullable=False, comment="项目编号")
    
    # 基本信息
    name = Column(String(200), nullable=False, comment="项目名称")
    category_id = Column(BigInteger, nullable=False, index=True, comment="分类ID")
    lab_id = Column(BigInteger, nullable=False, index=True, comment="实验室ID")
    
    # 价格信息
    original_price = Column(Numeric(10, 2), nullable=False, comment="原价")
    current_price = Column(Numeric(10, 2), nullable=False, comment="现价")
    unit = Column(String(20), default="样品", comment="单位")
    
    # 服务信息
    service_cycle_min = Column(Integer, comment="最短服务周期（工作日）")
    service_cycle_max = Column(Integer, comment="最长服务周期（工作日）")
    
    # 仪器信息
    equipment_name = Column(String(200), comment="仪器名称")
    equipment_model = Column(String(200), comment="仪器型号")
    
    # 详细信息
    introduction = Column(Text, comment="项目介绍")
    sample_requirements = Column(Text, comment="样品要求")
    test_parameters = Column(JSON, comment="检测参数")
    booking_notice = Column(Text, comment="预约须知")
    faq = Column(JSON, comment="常见问题")
    
    # 图片
    cover_image = Column(String(500), comment="封面图")
    detail_images = Column(JSON, comment="详情图")
    
    # 状态
    status = Column(String(20), default="active", comment="状态")
    is_hot = Column(Boolean, default=False, comment="是否热门")
    is_recommended = Column(Boolean, default=False, comment="是否推荐")
    
    # 统计
    view_count = Column(Integer, default=0, comment="浏览量")
    booking_count = Column(Integer, default=0, comment="预约量")
    satisfaction = Column(Numeric(5, 2), default=100.0, comment="满意度")
    
    # 排序
    sort_order = Column(Integer, default=0, comment="排序")
    
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, onupdate=func.now(), comment="更新时间")


class ProjectReview(Base):
    """项目评价表"""
    __tablename__ = "project_reviews"
    
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    
    # 关联信息
    project_id = Column(BigInteger, nullable=False, index=True, comment="项目ID")
    order_id = Column(BigInteger, nullable=False, index=True, comment="订单ID")
    user_id = Column(BigInteger, nullable=False, index=True, comment="用户ID")
    lab_id = Column(BigInteger, nullable=False, comment="实验室ID")
    
    # 评价内容
    rating = Column(Integer, nullable=False, comment="评分1-5")
    content = Column(Text, comment="评价内容")
    tags = Column(JSON, comment="评价标签")
    images = Column(JSON, comment="评价图片")
    
    # 回复
    reply_content = Column(Text, comment="商家回复")
    reply_time = Column(DateTime, comment="回复时间")
    
    # 状态
    is_anonymous = Column(Boolean, default=False, comment="是否匿名")
    status = Column(String(20), default="published", comment="状态")
    
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")

