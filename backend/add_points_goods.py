#!/usr/bin/env python3
"""
添加积分商品测试数据脚本
运行方式: cd backend && python add_points_goods.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.points import PointsGoods


def add_test_points_goods():
    """添加测试积分商品"""
    db = SessionLocal()
    
    try:
        # 测试积分商品数据
        points_goods_data = [
            # 优惠券类
            {"name": "满100减10优惠券", "points": 100, "category": "优惠券", "stock": 1000, "description": "满100元可用，立减10元", "sort_order": 1},
            {"name": "满500减50优惠券", "points": 500, "category": "优惠券", "stock": 500, "description": "满500元可用，立减50元", "sort_order": 2},
            {"name": "500元测试现金抵用券", "points": 13440, "category": "优惠券", "stock": 50, "description": "测试专用，价值500元现金抵用券", "sort_order": 3},
            {"name": "100元测试现金抵用券", "points": 2688, "category": "优惠券", "stock": 100, "description": "测试专用，价值100元现金抵用券", "sort_order": 4},
            # 京东E卡类
            {"name": "京东E卡50元", "points": 2000, "category": "京东E卡", "stock": 100, "description": "京东购物卡，面值50元", "sort_order": 5},
            {"name": "京东E卡100元", "points": 3500, "category": "京东E卡", "stock": 50, "description": "京东购物卡，面值100元", "sort_order": 6},
            # 实物礼品类
            {"name": "小熊电煮锅", "points": 3032, "category": "实物礼", "stock": 30, "description": "小熊多功能电煮锅，1.5L容量，适合宿舍使用", "sort_order": 7},
            {"name": "小米电动牙刷T200", "points": 3544, "category": "实物礼", "stock": 25, "description": "小米米家电动牙刷，声波震动，2分钟智能定时", "sort_order": 8},
            {"name": "骨传导耳机", "points": 6638, "category": "实物礼", "stock": 20, "description": "骨传导运动耳机，不入耳设计，适合运动使用", "sort_order": 9},
            {"name": "苏泊尔养生壶", "points": 5794, "category": "实物礼", "stock": 15, "description": "苏泊尔多功能养生壶，1.5L容量，24小时预约", "sort_order": 10},
            # 测试商品
            {"name": "测试商品A", "points": 500, "category": "测试商品", "stock": 999, "description": "测试用商品A，积分500", "sort_order": 11},
            {"name": "测试商品B", "points": 1000, "category": "测试商品", "stock": 999, "description": "测试用商品B，积分1000", "sort_order": 12},
            {"name": "测试商品C", "points": 2000, "category": "测试商品", "stock": 999, "description": "测试用商品C，积分2000", "sort_order": 13},
        ]
        
        print("🎁 开始添加积分商品...")
        added_count = 0
        skipped_count = 0
        
        for goods_data in points_goods_data:
            # 检查是否已存在同名商品
            existing = db.query(PointsGoods).filter(PointsGoods.name == goods_data["name"]).first()
            if existing:
                print(f"  ⏭️  跳过已存在: {goods_data['name']}")
                skipped_count += 1
                continue
            
            # 创建新商品
            goods = PointsGoods(
                name=goods_data["name"],
                points=goods_data["points"],
                category=goods_data["category"],
                stock=goods_data["stock"],
                description=goods_data.get("description", ""),
                sort_order=goods_data.get("sort_order", 0),
                is_active=True
            )
            db.add(goods)
            print(f"  ✅ 添加积分商品: {goods_data['name']} ({goods_data['points']}积分, {goods_data['category']})")
            added_count += 1
        
        db.commit()
        print(f"\n✨ 完成! 新增 {added_count} 个商品, 跳过 {skipped_count} 个已存在商品")
        
    except Exception as e:
        db.rollback()
        print(f"❌ 错误: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    add_test_points_goods()
