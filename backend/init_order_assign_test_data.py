#!/usr/bin/env python3
"""
订单分配测试数据脚本
运行方式: cd backend && python init_order_assign_test_data.py

此脚本创建用于测试后台订单分配功能的测试数据：
1. 激活状态的实验室（用于接收分配）
2. 管理员用户（用于执行分配操作）
3. 待分配的订单（paid/pending_assign 状态）
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta
from decimal import Decimal
import time
import random

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models.user import User, UserStatus, MembershipLevel
from app.models.project import Project, ProjectCategory
from app.models.laboratory import Laboratory, LabStatus
from app.models.order import Order, OrderSample, OrderStatusHistory
from app.core.security import get_password_hash


def generate_order_no():
    """生成订单号"""
    return f"ORD{int(time.time())}{random.randint(1000, 9999)}"


def init_order_assign_test_data():
    """初始化订单分配测试数据"""
    db = SessionLocal()
    
    try:
        print("=" * 60)
        print("🚀 开始初始化订单分配测试数据...")
        print("=" * 60)
        
        # ==================== 1. 确保有管理员用户 ====================
        print("\n👤 检查/创建管理员用户...")
        
        admin_user = db.query(User).filter(User.is_admin == True).first()
        if not admin_user:
            admin_user = User(
                phone="13900000000",
                nickname="系统管理员",
                password=get_password_hash("123456"),
                prepaid_balance=Decimal("10000"),
                points_balance=10000,
                is_admin=True,
                status=UserStatus.ACTIVE
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            print(f"  ✅ 创建管理员: 13900000000 / 123456")
        else:
            print(f"  ⏭️ 管理员已存在: {admin_user.phone}")
        
        # ==================== 2. 确保有激活状态的实验室 ====================
        print("\n🏛️ 检查/创建激活状态的实验室...")
        
        active_labs = db.query(Laboratory).filter(
            Laboratory.status == LabStatus.ACTIVE
        ).all()
        
        if len(active_labs) < 3:
            labs_data = [
                {
                    "name": "北京检测中心",
                    "lab_no": f"LAB{int(time.time())}001",
                    "code": "bj_center",
                    "short_name": "北京中心",
                    "lab_type": "third_party",
                    "status": LabStatus.ACTIVE,
                    "is_verified": True,
                    "institution": "北京科技检测有限公司",
                    "province": "北京市",
                    "city": "北京市",
                    "address": "北京市海淀区科学园路1号",
                    "contact_name": "张工程师",
                    "contact_phone": "010-12345678",
                    "contact_email": "beijing@lab.com",
                    "description": "专业提供各类材料检测服务",
                    "rating": Decimal("4.9"),
                    "total_orders": 0,
                },
                {
                    "name": "上海材料分析中心",
                    "lab_no": f"LAB{int(time.time())}002",
                    "code": "sh_material",
                    "short_name": "上海材料",
                    "lab_type": "university",
                    "status": LabStatus.ACTIVE,
                    "is_verified": True,
                    "institution": "上海交通大学",
                    "province": "上海市",
                    "city": "上海市",
                    "address": "上海市闵行区东川路800号",
                    "contact_name": "李教授",
                    "contact_phone": "021-54321678",
                    "contact_email": "shanghai@lab.com",
                    "description": "高校材料分析测试平台",
                    "rating": Decimal("4.8"),
                    "total_orders": 0,
                },
                {
                    "name": "广州第三方检测中心",
                    "lab_no": f"LAB{int(time.time())}003",
                    "code": "gz_third",
                    "short_name": "广州检测",
                    "lab_type": "enterprise",
                    "status": LabStatus.ACTIVE,
                    "is_verified": True,
                    "institution": "广州检测科技有限公司",
                    "province": "广东省",
                    "city": "广州市",
                    "address": "广州市天河区科韵路88号",
                    "contact_name": "王经理",
                    "contact_phone": "020-87654321",
                    "contact_email": "guangzhou@lab.com",
                    "description": "专业第三方检测机构",
                    "rating": Decimal("4.7"),
                    "total_orders": 0,
                },
            ]
            
            for lab_data in labs_data:
                # 检查是否已存在相同编号的实验室
                existing = db.query(Laboratory).filter(
                    Laboratory.code == lab_data["code"]
                ).first()
                
                if not existing:
                    lab = Laboratory(**lab_data)
                    db.add(lab)
                    print(f"  ✅ 创建实验室: {lab_data['name']} (状态: active)")
                else:
                    # 确保状态是激活的
                    existing.status = LabStatus.ACTIVE
                    print(f"  ⏭️ 实验室已存在，已更新为激活状态: {lab_data['name']}")
            
            db.commit()
        else:
            print(f"  ⏭️ 已有 {len(active_labs)} 个激活状态的实验室")
        
        # 重新获取激活的实验室
        active_labs = db.query(Laboratory).filter(
            Laboratory.status == LabStatus.ACTIVE
        ).all()
        
        # ==================== 3. 确保有项目分类 ====================
        print("\n📁 检查/创建项目分类...")
        
        category = db.query(ProjectCategory).first()
        if not category:
            category = ProjectCategory(
                name="材料检测",
                code="material_test",
                icon="🔬",
                description="各类材料分析检测",
                sort_order=1,
                is_active=True
            )
            db.add(category)
            db.commit()
            db.refresh(category)
            print(f"  ✅ 创建分类: 材料检测")
        else:
            print(f"  ⏭️ 分类已存在: {category.name}")
        
        # ==================== 4. 确保有检测项目 ====================
        print("\n🧪 检查/创建检测项目...")
        
        projects = db.query(Project).filter(Project.status == "active").all()
        if len(projects) < 3:
            projects_data = [
                {"name": "扫描电镜(SEM)", "price": 200, "cycle_min": 3, "cycle_max": 5},
                {"name": "X射线衍射(XRD)", "price": 300, "cycle_min": 2, "cycle_max": 4},
                {"name": "热重分析(TGA)", "price": 250, "cycle_min": 2, "cycle_max": 3},
            ]
            
            for idx, proj_data in enumerate(projects_data):
                existing = db.query(Project).filter(Project.name == proj_data["name"]).first()
                if not existing:
                    project = Project(
                        project_no=f"PRJ{int(time.time())}{idx:03d}",
                        name=proj_data["name"],
                        category_id=category.id,
                        lab_id=active_labs[0].id if active_labs else 1,
                        original_price=Decimal(str(proj_data["price"] * 1.2)),
                        current_price=Decimal(str(proj_data["price"])),
                        unit="样",
                        service_cycle_min=proj_data["cycle_min"],
                        service_cycle_max=proj_data["cycle_max"],
                        introduction=f"{proj_data['name']}检测服务",
                        status="active",
                        is_hot=True,
                    )
                    db.add(project)
                    print(f"  ✅ 创建项目: {proj_data['name']}")
            
            db.commit()
        
        # 重新获取项目
        projects = db.query(Project).filter(Project.status == "active").all()
        
        # ==================== 5. 确保有测试用户 ====================
        print("\n👥 检查/创建测试用户...")
        
        test_users = []
        for i in range(1, 4):
            phone = f"1380013800{i}"
            user = db.query(User).filter(User.phone == phone).first()
            if not user:
                user = User(
                    phone=phone,
                    nickname=f"测试用户{i}",
                    password=get_password_hash("123456"),
                    prepaid_balance=Decimal("1000"),
                    points_balance=100,
                    is_admin=False,
                    status=UserStatus.ACTIVE
                )
                db.add(user)
                db.commit()
                db.refresh(user)
                print(f"  ✅ 创建用户: {phone}")
            else:
                print(f"  ⏭️ 用户已存在: {phone}")
            test_users.append(user)
        
        # ==================== 6. 创建待分配的订单 ====================
        print("\n📦 创建待分配订单...")
        
        # 统计现有待分配订单
        pending_orders = db.query(Order).filter(
            Order.is_draft == False,
            Order.status.in_(["paid", "pending_assign"]),
            Order.assigned_lab_id.is_(None)
        ).count()
        
        print(f"  📊 现有待分配订单: {pending_orders} 个")
        
        # 创建新的待分配订单
        new_orders_count = 0
        statuses = ["paid", "pending_assign"]
        
        for i in range(10):  # 创建10个待分配订单
            user = random.choice(test_users)
            project = random.choice(projects) if projects else None
            lab = active_labs[0] if active_labs else None
            
            if not project or not lab:
                print("  ⚠️ 缺少项目或实验室数据，跳过创建订单")
                continue
            
            order = Order(
                order_no=generate_order_no(),
                user_id=user.id,
                project_id=project.id,
                project_name=project.name,
                lab_id=lab.id,
                lab_name=lab.name,
                status=random.choice(statuses),
                is_draft=False,
                invoice_status="none",
                payment_status="paid",
                credit_amount=Decimal("0"),
                assigned_lab_id=None,  # 未分配
                assigned_user_id=None,
                assigned_at=None,
                project_fee=project.current_price,
                urgent_fee=Decimal("0"),
                shipping_fee=Decimal("0"),
                discount_amount=Decimal("0"),
                total_fee=project.current_price,
                paid_fee=project.current_price,
                sample_count=random.randint(1, 3),
                shipping_method="express",
                receiver_name=user.nickname,
                receiver_phone=user.phone,
                receiver_address=f"测试地址{i+1}号",
                payment_method=random.choice(["wechat", "alipay", "balance"]),
                payment_time=datetime.now() - timedelta(hours=random.randint(1, 48)),
                created_at=datetime.now() - timedelta(hours=random.randint(2, 72)),
                paid_at=datetime.now() - timedelta(hours=random.randint(1, 48)),
                remark=f"测试订单-待分配#{i+1}",
                is_urgent=random.choice([True, False]),
                estimated_completion_time=datetime.now() + timedelta(days=random.randint(3, 7))
            )
            db.add(order)
            db.flush()
            
            # 创建订单样品
            for j in range(order.sample_count):
                sample = OrderSample(
                    order_id=order.id,
                    sample_name=f"样品-{order.order_no}-{j+1}",
                    sample_type=random.choice(["粉末", "块体", "薄膜", "溶液"]),
                    sample_desc=f"测试样品{j+1}",
                    quantity=1,
                    photos=[],
                    test_params={},
                    special_requirements=""
                )
                db.add(sample)
            
            new_orders_count += 1
        
        db.commit()
        print(f"  ✅ 新创建 {new_orders_count} 个待分配订单")
        
        # ==================== 7. 创建一些已分配和其他状态的订单 ====================
        print("\n📦 创建其他状态的订单（用于对比测试）...")
        
        other_statuses = [
            ("assigned", "已分配待接单"),
            ("accepted", "实验室已接单"),
            ("testing", "检测中"),
            ("completed", "已完成"),
        ]
        
        other_orders_count = 0
        for status, desc in other_statuses:
            for i in range(2):  # 每种状态2个
                user = random.choice(test_users)
                project = random.choice(projects) if projects else None
                lab = random.choice(active_labs) if active_labs else None
                
                if not project or not lab:
                    continue
                
                order = Order(
                    order_no=generate_order_no(),
                    user_id=user.id,
                    project_id=project.id,
                    project_name=project.name,
                    lab_id=lab.id,
                    lab_name=lab.name,
                    status=status,
                    is_draft=False,
                    invoice_status="none",
                    payment_status="paid",
                    credit_amount=Decimal("0"),
                    assigned_lab_id=lab.id if status != "paid" else None,
                    assigned_user_id=admin_user.id if status != "paid" else None,
                    assigned_at=datetime.now() - timedelta(hours=random.randint(1, 24)) if status != "paid" else None,
                    project_fee=project.current_price,
                    urgent_fee=Decimal("0"),
                    shipping_fee=Decimal("0"),
                    discount_amount=Decimal("0"),
                    total_fee=project.current_price,
                    paid_fee=project.current_price,
                    sample_count=1,
                    shipping_method="express",
                    receiver_name=user.nickname,
                    receiver_phone=user.phone,
                    receiver_address=f"测试地址{i+1}号",
                    payment_method="balance",
                    payment_time=datetime.now() - timedelta(days=random.randint(1, 7)),
                    created_at=datetime.now() - timedelta(days=random.randint(1, 14)),
                    paid_at=datetime.now() - timedelta(days=random.randint(1, 7)),
                    confirmed_at=datetime.now() - timedelta(days=random.randint(1, 5)) if status in ["testing", "completed"] else None,
                    started_at=datetime.now() - timedelta(days=random.randint(1, 3)) if status in ["testing", "completed"] else None,
                    completed_at=datetime.now() - timedelta(days=1) if status == "completed" else None,
                    remark=f"测试订单-{desc}#{i+1}",
                    is_urgent=False,
                )
                db.add(order)
                other_orders_count += 1
        
        db.commit()
        print(f"  ✅ 创建 {other_orders_count} 个其他状态订单")
        
        # ==================== 统计汇总 ====================
        print("\n" + "=" * 60)
        print("📊 数据统计汇总")
        print("=" * 60)
        
        # 订单统计
        total_orders = db.query(Order).filter(Order.is_draft == False).count()
        pending_assign = db.query(Order).filter(
            Order.is_draft == False,
            Order.status.in_(["paid", "pending_assign"]),
            Order.assigned_lab_id.is_(None)
        ).count()
        assigned = db.query(Order).filter(Order.status == "assigned").count()
        testing = db.query(Order).filter(Order.status.in_(["accepted", "sample_received", "testing"])).count()
        completed = db.query(Order).filter(Order.status == "completed").count()
        
        print(f"\n订单统计：")
        print(f"  - 总订单数: {total_orders}")
        print(f"  - 待分配订单: {pending_assign}")
        print(f"  - 已分配待接单: {assigned}")
        print(f"  - 检测中: {testing}")
        print(f"  - 已完成: {completed}")
        
        # 实验室统计
        lab_count = db.query(Laboratory).filter(Laboratory.status == LabStatus.ACTIVE).count()
        print(f"\n实验室统计：")
        print(f"  - 激活实验室数: {lab_count}")
        
        for lab in active_labs[:5]:
            print(f"    • {lab.name} (ID: {lab.id})")
        
        print("\n" + "=" * 60)
        print("✅ 订单分配测试数据初始化完成！")
        print("=" * 60)
        
        print("\n📋 测试说明：")
        print("  1. 访问后台管理: http://localhost:3001/admin")
        print("  2. 使用管理员账号登录")
        print("  3. 进入「订单分配」页面")
        print("  4. 可以看到待分配的订单列表")
        print("  5. 选择订单并分配给实验室")
        
        print("\n🔐 管理员账号：")
        print(f"  手机号: {admin_user.phone}")
        print("  密码: 123456")
        
        print("\n🔗 API 接口：")
        print("  - 待分配订单列表: GET /api/v1/admin/orders?status=pending_assign")
        print("  - 分配订单: POST /api/v1/admin/orders/{order_id}/assign")
        print("  - 批量分配: POST /api/v1/admin/orders/batch-assign")
        print("  - 分配统计: GET /api/v1/admin/orders/assignment-stats")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ 初始化失败: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    init_order_assign_test_data()
