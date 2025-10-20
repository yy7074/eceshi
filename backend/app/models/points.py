"""
积分系统数据模型
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class PointsGoods(Base):
    """积分商品表"""
    __tablename__ = "points_goods"
    
    id = Column(Integer, primary_key=True, index=True, comment="商品ID")
    name = Column(String(100), nullable=False, comment="商品名称")
    points = Column(Integer, nullable=False, comment="所需积分")
    category = Column(String(50), nullable=False, comment="商品分类")
    image = Column(String(500), comment="商品图片")
    description = Column(Text, comment="商品描述")
    stock = Column(Integer, default=0, comment="库存数量")
    is_active = Column(Boolean, default=True, comment="是否上架")
    sort_order = Column(Integer, default=0, comment="排序")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    
    # 关系
    exchange_records = relationship("PointsExchangeRecord", back_populates="goods")


class PointsRecord(Base):
    """积分记录表"""
    __tablename__ = "points_records"
    
    id = Column(Integer, primary_key=True, index=True, comment="记录ID")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True, comment="用户ID")
    points = Column(Integer, nullable=False, comment="积分变动（正数为增加，负数为减少）")
    type = Column(String(50), nullable=False, comment="积分类型：order,exchange,signin,invite等")
    related_id = Column(Integer, comment="关联ID（订单ID、兑换ID等）")
    description = Column(String(200), comment="积分描述")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    
    # 关系
    user = relationship("User", back_populates="points_records")


class PointsExchangeRecord(Base):
    """积分兑换记录表"""
    __tablename__ = "points_exchange_records"
    
    id = Column(Integer, primary_key=True, index=True, comment="兑换ID")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True, comment="用户ID")
    goods_id = Column(Integer, ForeignKey("points_goods.id"), nullable=False, comment="商品ID")
    points = Column(Integer, nullable=False, comment="兑换消耗积分")
    status = Column(String(20), default="pending", comment="兑换状态：pending,confirmed,shipped,completed,cancelled")
    express_company = Column(String(50), comment="快递公司")
    express_no = Column(String(50), comment="快递单号")
    address_snapshot = Column(Text, comment="地址快照（JSON）")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    
    # 关系
    user = relationship("User", back_populates="exchange_records")
    goods = relationship("PointsGoods", back_populates="exchange_records")

