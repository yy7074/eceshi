"""
插入后台管理测试数据
包含用户、订单、优惠券、积分、充值等完整测试数据
"""
import sys
sys.path.insert(0, '.')

from app.core.config import settings
from app.core.database import SessionLocal
from app.models.user import User, UserCertification, UserStatus, MembershipLevel, IdentityType
from app.models.laboratory import Laboratory
from app.models.project import ProjectCategory, Project
from app.models.order import Order, OrderSample, Payment, UserAddress
from app.models.coupon import Coupon, UserCoupon
from app.models.points import PointsRecord
from app.models.recharge import RechargeRecord, RechargeStatus
from app.models.invite import InviteRecord
from app.models.group import UserGroup, GroupMember
from app.models.banner import Banner
from app.models.announcement import Announcement
from app.models.help import HelpArticle
from app.models.chat import ChatMessage
from app.models.report import Report
from app.models.sample import SampleTracking
from app.models.contract import Contract
from app.models.franchise import FranchiseApplication
from decimal import Decimal
from datetime import datetime, timedelta
import time
import random


def generate_order_no():
    """生成订单号"""
    return f"ORD{int(time.time())}{random.randint(1000, 9999)}"


def generate_recharge_no():
    """生成充值单号"""
    return f"RCH{int(time.time())}{random.randint(1000, 9999)}"


def insert_test_data():
    """插入完整测试数据"""
    db = SessionLocal()
    
    try:
        print("📦 开始插入后台管理测试数据...")
        
        # ==================== 1. 插入用户测试数据 ====================
        print("\n1️⃣ 插入用户测试数据...")
        users = []
        
        # 创建管理员用户
        admin_user = User(
            phone="admin",
            password="pbkdf2_sha256$260000$random$admin_hash",  # 简化密码
            nickname="系统管理员",
            avatar="https://via.placeholder.com/150",
            email="admin@eceshi.com",
            is_certified=True,
            real_name="管理员",
            id_card="110101199001011234",
            membership_level=MembershipLevel.PLATINUM,
            credit_limit=Decimal("999999.00"),
            used_credit=Decimal("0"),
            prepaid_balance=Decimal("10000.00"),
            points_balance=50000,
            total_points_earned=50000,
            total_points_used=0,
            total_spent=Decimal("0"),
            total_orders=0,
            status=UserStatus.ACTIVE,
            is_admin=True
        )
        db.add(admin_user)
        db.flush()
        users.append(admin_user)
        
        # 创建普通用户
        user_names = [
            ("张三", "13800138001", "student"),
            ("李四", "13800138002", "teacher"),
            ("王五", "13800138003", "enterprise"),
            ("赵六", "13800138004", "research"),
            ("钱七", "13800138005", "student"),
            ("孙八", "13800138006", "student"),
            ("周九", "13800138007", "teacher"),
            ("吴十", "13800138008", "enterprise"),
        ]
        
        for idx, (name, phone, identity) in enumerate(user_names):
            user = User(
                phone=phone,
                password="pbkdf2_sha256$260000$random$password_hash",  # 简化密码
                nickname=name,
                avatar=f"https://via.placeholder.com/150?text={name}",
                email=f"{phone}@eceshi.com",
                is_certified=random.choice([True, False]),
                real_name=name if random.choice([True, False]) else None,
                id_card=f"11010119900101{1000+idx}" if random.choice([True, False]) else None,
                membership_level=random.choice(list(MembershipLevel)),
                credit_limit=Decimal(str(random.randint(1000, 10000))),
                used_credit=Decimal(str(random.randint(0, 3000))),
                prepaid_balance=Decimal(str(random.randint(0, 5000))),
                points_balance=random.randint(0, 5000),
                total_points_earned=random.randint(1000, 10000),
                total_points_used=random.randint(0, 5000),
                total_spent=Decimal(str(random.randint(0, 20000))),
                total_orders=random.randint(0, 20),
                status=random.choice([UserStatus.ACTIVE, UserStatus.ACTIVE, UserStatus.ACTIVE, UserStatus.INACTIVE]),
                is_admin=False
            )
            db.add(user)
            db.flush()
            users.append(user)
        
        db.commit()
        print(f"  ✅ 已插入 {len(users)} 个用户")
        
        # ==================== 2. 插入实验室 ====================
        print("\n2️⃣ 插入实验室...")
        labs = []
        lab_data = [
            ("清华大学材料学院分析测试中心", "清华材料中心", "北京市", "国家级", 4.9, 1250),
            ("北京大学化学与分子工程学院测试中心", "北大化学中心", "北京市", "国家级", 4.8, 980),
            ("上海交通大学分析测试中心", "交大测试中心", "上海市", "省部级", 4.7, 756),
            ("复旦大学材料科学系测试中心", "复旦材料中心", "上海市", "省部级", 4.6, 623),
            ("浙江大学材料科学与工程学院", "浙大材料学院", "浙江省", "国家级", 4.8, 890),
        ]
        
        for idx, (name, short_name, city, level, rating, order_count) in enumerate(lab_data):
            lab = Laboratory(
                lab_no=f"LAB{int(time.time())}{idx:03d}",
                name=name,
                short_name=short_name,
                type="高校实验室",
                level=level,
                institution=name.split("学院")[0] if "学院" in name else name.split("大学")[0],
                province="北京市" if "北京" in name else ("上海市" if "上海" in name else "浙江省"),
                city=city,
                address=f"{city}测试中心地址{idx+1}号",
                contact_person=f"老师{chr(65+idx)}",
                contact_phone=f"010-{random.randint(10000000, 99999999)}",
                rating=Decimal(str(rating)),
                order_count=order_count,
                is_verified=True,
                status="active",
                introduction=f"{name}提供专业的材料分析和检测服务。"
            )
            db.add(lab)
            db.flush()
            labs.append(lab)
        
        db.commit()
        print(f"  ✅ 已插入 {len(labs)} 个实验室")
        
        # ==================== 3. 插入项目分类 ====================
        print("\n3️⃣ 插入项目分类...")
        categories = []
        category_data = [
            ("电镜专场", "SEM", "🔬", True, 1),
            ("材料测试", "MAT", "🧪", True, 2),
            ("化学分析", "CHE", "⚗️", False, 3),
            ("生物检测", "BIO", "🧬", False, 4),
            ("物理性能", "PHY", "⚡", False, 5),
            ("环境检测", "ENV", "🌍", False, 6),
        ]
        
        for name, code, icon, is_hot, sort_order in category_data:
            cat = ProjectCategory(
                name=name,
                code=code,
                icon=icon,
                is_hot=is_hot,
                sort_order=sort_order,
                description=f"{name}相关检测项目"
            )
            db.add(cat)
            db.flush()
            categories.append(cat)
        
        db.commit()
        print(f"  ✅ 已插入 {len(categories)} 个分类")
        
        # ==================== 4. 插入检测项目 ====================
        print("\n4️⃣ 插入检测项目...")
        projects = []
        project_data = [
            ("场发射扫描电镜（SEM）", "FEI Quanta 450", 400.00, 312.00, 3, 5, categories[0].id, labs[0].id, True, True),
            ("X射线衍射（XRD）", "Bruker D8 Advance", 300.00, 250.00, 2, 4, categories[1].id, labs[0].id, True, False),
            ("傅里叶红外光谱（FTIR）", "Thermo Nicolet iS50", 200.00, 180.00, 1, 3, categories[2].id, labs[1].id, False, False),
            ("热重分析（TGA）", "TA Q500", 250.00, 220.00, 2, 3, categories[1].id, labs[1].id, False, False),
            ("透射电镜（TEM）", "FEI Tecnai G2 F20", 500.00, 450.00, 5, 7, categories[0].id, labs[2].id, True, True),
            ("能谱分析（EDS）", "Oxford X-Max", 150.00, 120.00, 1, 2, categories[0].id, labs[0].id, False, False),
            ("拉曼光谱", "Renishaw inVia", 350.00, 300.00, 2, 4, categories[2].id, labs[1].id, False, False),
            ("紫外-可见光谱", "Agilent Cary 5000", 180.00, 150.00, 1, 2, categories[2].id, labs[2].id, False, False),
            ("核磁共振（NMR）", "Bruker AVANCE III", 800.00, 700.00, 3, 5, categories[2].id, labs[3].id, True, False),
            ("原子力显微镜（AFM）", "Bruker Dimension Icon", 600.00, 520.00, 4, 6, categories[0].id, labs[4].id, True, True),
        ]
        
        for idx, (name, model, original_price, current_price, cycle_min, cycle_max, cat_id, lab_id, is_hot, is_recommended) in enumerate(project_data):
            project = Project(
                project_no=f"PRJ{int(time.time())}{idx:03d}",
                name=name,
                category_id=cat_id,
                lab_id=lab_id,
                original_price=Decimal(str(original_price)),
                current_price=Decimal(str(current_price)),
                unit="样品",
                service_cycle_min=cycle_min,
                service_cycle_max=cycle_max,
                equipment_name=name.split("（")[0],
                equipment_model=model,
                introduction=f"{name}是常用的材料分析测试方法，广泛应用于科研和工业领域。",
                sample_requirements="样品需干燥、清洁，具体要求请联系客服。",
                booking_notice="请提前预约，按时送样。",
                cover_image="https://via.placeholder.com/400x300",
                status="active",
                is_hot=is_hot,
                is_recommended=is_recommended,
                view_count=random.randint(500, 5000),
                booking_count=random.randint(50, 500),
                satisfaction=Decimal(str(random.uniform(95.0, 99.9))),
                sort_order=idx + 1
            )
            db.add(project)
            db.flush()
            projects.append(project)
        
        db.commit()
        print(f"  ✅ 已插入 {len(projects)} 个项目")
        
        # ==================== 5. 插入订单测试数据 ====================
        print("\n5️⃣ 插入订单测试数据...")
        orders = []
        order_statuses = ["pending_payment", "paid", "confirmed", "testing", "completed", "cancelled"]
        
        for i in range(20):
            user = random.choice(users[1:])  # 排除管理员
            project = random.choice(projects)
            lab = next((l for l in labs if l.id == project.lab_id), labs[0])
            status = random.choice(order_statuses)
            
            order = Order(
                order_no=generate_order_no(),
                user_id=user.id,
                project_id=project.id,
                project_name=project.name,
                lab_id=lab.id,
                lab_name=lab.name,
                status=status,
                is_draft=False,
                invoice_status=random.choice(["none", "requested", "processing", "issued"]),
                payment_status="paid" if status != "pending_payment" else "unpaid",
                credit_amount=Decimal("0"),
                project_fee=project.current_price,
                urgent_fee=Decimal("0"),
                shipping_fee=Decimal("0"),
                discount_amount=Decimal("0"),
                total_fee=project.current_price,
                paid_fee=project.current_price if status != "pending_payment" else Decimal("0"),
                sample_count=random.randint(1, 5),
                shipping_method=random.choice(["express", "self"]),
                receiver_name=user.nickname,
                receiver_phone=user.phone,
                receiver_address=f"测试地址{i+1}号",
                payment_method=random.choice(["wechat", "alipay", "balance"]),
                payment_time=datetime.now() - timedelta(days=random.randint(1, 30)) if status != "pending_payment" else None,
                created_at=datetime.now() - timedelta(days=random.randint(1, 60)),
                paid_at=datetime.now() - timedelta(days=random.randint(1, 30)) if status != "pending_payment" else None,
                confirmed_at=datetime.now() - timedelta(days=random.randint(1, 25)) if status in ["confirmed", "testing", "completed"] else None,
                started_at=datetime.now() - timedelta(days=random.randint(1, 20)) if status in ["testing", "completed"] else None,
                completed_at=datetime.now() - timedelta(days=random.randint(1, 15)) if status == "completed" else None,
                cancelled_at=datetime.now() - timedelta(days=random.randint(1, 30)) if status == "cancelled" else None,
                remark=f"测试订单备注{i+1}",
                is_urgent=random.choice([True, False]),
                estimated_completion_time=datetime.now() + timedelta(days=random.randint(3, 10))
            )
            db.add(order)
            db.flush()
            orders.append(order)
            
            # 插入订单样品
            for j in range(order.sample_count):
                sample = OrderSample(
                    order_id=order.id,
                    sample_name=f"样品{j+1}",
                    sample_type=random.choice(["粉末", "块体", "薄膜", "液体"]),
                    sample_desc=f"测试样品{j+1}描述",
                    quantity=1,
                    photos=[],
                    test_params={},
                    special_requirements=""
                )
                db.add(sample)
            
            # 插入支付记录
            if status != "pending_payment":
                payment = Payment(
                    payment_no=f"PAY{int(time.time())}{i:03d}",
                    order_id=order.id,
                    order_no=order.order_no,
                    user_id=user.id,
                    payment_method=order.payment_method,
                    payment_channel=order.payment_method,
                    amount=order.total_fee,
                    status="paid",
                    trade_no=f"TXN{int(time.time())}{i:03d}",
                    paid_at=order.paid_at,
                    created_at=order.created_at
                )
                db.add(payment)
        
        db.commit()
        print(f"  ✅ 已插入 {len(orders)} 个订单")
        
        # ==================== 6. 插入用户地址 ====================
        print("\n6️⃣ 插入用户地址...")
        addresses = []
        for user in users[1:]:
            for i in range(random.randint(1, 3)):
                address = UserAddress(
                    user_id=user.id,
                    receiver_name=user.nickname,
                    phone=user.phone,
                    province=random.choice(["北京市", "上海市", "广东省", "浙江省"]),
                    city=random.choice(["北京市", "上海市", "广州市", "杭州市"]),
                    district=random.choice(["朝阳区", "浦东新区", "天河区", "西湖区"]),
                    detail_address=f"测试小区{i+1}号{i+1}栋{i+1}单元{i+1}01",
                    is_default=(i == 0)
                )
                db.add(address)
                addresses.append(address)
        
        db.commit()
        print(f"  ✅ 已插入 {len(addresses)} 个地址")
        
        # ==================== 7. 插入优惠券 ====================
        print("\n7️⃣ 插入优惠券...")
        coupons = []
        coupon_types = ["fixed", "percent"]
        for i in range(10):
            coupon = Coupon(
                coupon_name=f"测试优惠券{i+1}",
                coupon_type=random.choice(coupon_types),
                discount_value=Decimal(str(random.choice([10, 20, 50, 100]))),
                min_amount=Decimal(str(random.choice([100, 200, 500, 1000]))),
                max_discount=Decimal("100") if random.choice([True, False]) else None,
                total_count=random.randint(50, 500),
                used_count=random.randint(0, 50),
                valid_days=random.randint(7, 90),
                status=random.choice(["active", "active", "active", "inactive"]),
                description=f"测试优惠券{i+1}说明"
            )
            db.add(coupon)
            db.flush()
            coupons.append(coupon)
            
            # 为部分用户发放优惠券
            for user in random.sample(users[1:], random.randint(1, 5)):
                user_coupon = UserCoupon(
                    user_id=user.id,
                    coupon_id=coupon.id,
                    status=random.choice(["unused", "used", "expired"]),
                    obtained_at=datetime.now() - timedelta(days=random.randint(1, 30)),
                    used_at=datetime.now() - timedelta(days=random.randint(1, 20)) if random.choice([True, False]) else None,
                    expires_at=datetime.now() + timedelta(days=random.randint(10, 60))
                )
                db.add(user_coupon)
        
        db.commit()
        print(f"  ✅ 已插入 {len(coupons)} 个优惠券")
        
        # ==================== 8. 插入积分记录 ====================
        print("\n8️⃣ 插入积分记录...")
        points_records = []
        point_types = ["order", "review", "invite", "signup", "daily"]
        
        for user in users[1:]:
            for i in range(random.randint(5, 20)):
                record = PointsRecord(
                    user_id=user.id,
                    points=random.choice([10, 20, 50, 100]),
                    type=random.choice(point_types),
                    description=f"积分记录{i+1}",
                    balance=random.randint(0, 5000)
                )
                db.add(record)
                points_records.append(record)
        
        db.commit()
        print(f"  ✅ 已插入 {len(points_records)} 条积分记录")
        
        # ==================== 9. 插入充值记录 ====================
        print("\n9️⃣ 插入充值记录...")
        recharge_records = []
        recharge_methods = ["wechat", "alipay"]
        
        for user in users[1:]:
            for i in range(random.randint(0, 5)):
                amount = random.choice([100, 200, 500, 1000, 2000])
                record = RechargeRecord(
                    recharge_no=generate_recharge_no(),
                    user_id=user.id,
                    amount=Decimal(str(amount)),
                    actual_amount=Decimal(str(amount * 1.1)),  # 10%赠送
                    payment_method=random.choice(recharge_methods),
                    status=random.choice([RechargeStatus.SUCCESS, RechargeStatus.SUCCESS, RechargeStatus.PENDING, RechargeStatus.FAILED]),
                    transaction_id=f"TXN{int(time.time())}{i:03d}" if random.choice([True, False]) else None,
                    paid_at=datetime.now() - timedelta(days=random.randint(1, 30)) if random.choice([True, False]) else None,
                    completed_at=datetime.now() - timedelta(days=random.randint(1, 30)) if random.choice([True, False]) else None,
                    created_at=datetime.now() - timedelta(days=random.randint(1, 60))
                )
                db.add(record)
                recharge_records.append(record)
        
        db.commit()
        print(f"  ✅ 已插入 {len(recharge_records)} 条充值记录")
        
        # ==================== 10. 插入邀请记录 ====================
        print("\n🔟 插入邀请记录...")
        invite_records = []
        
        for i in range(15):
            inviter = random.choice(users[1:])
            invitee = random.choice([u for u in users[1:] if u.id != inviter.id])
            
            record = InviteRecord(
                inviter_id=inviter.id,
                invitee_id=invitee.id,
                invite_code=f"INV{random.randint(100000, 999999)}",
                status=random.choice(["pending", "completed", "rewarded"]),
                reward_points=random.choice([50, 100, 200]),
                reward_amount=Decimal(str(random.choice([10, 20, 50]))),
                completed_at=datetime.now() - timedelta(days=random.randint(1, 30)) if random.choice([True, False]) else None,
                created_at=datetime.now() - timedelta(days=random.randint(1, 60))
            )
            db.add(record)
            invite_records.append(record)
        
        db.commit()
        print(f"  ✅ 已插入 {len(invite_records)} 条邀请记录")
        
        # ==================== 11. 插入团队 ====================
        print("\n1️⃣1️⃣ 插入团队...")
        groups = []
        
        for i in range(5):
            group = UserGroup(
                group_name=f"测试团队{i+1}",
                group_no=f"GRP{int(time.time())}{i:03d}",
                leader_id=random.choice(users[1:]).id,
                member_count=random.randint(2, 10),
                total_orders=random.randint(5, 50),
                total_amount=Decimal(str(random.randint(1000, 20000))),
                status="active",
                description=f"测试团队{i+1}说明"
            )
            db.add(group)
            db.flush()
            groups.append(group)
            
            # 添加团队成员
            for j in range(random.randint(2, 5)):
                member = GroupMember(
                    group_id=group.id,
                    user_id=random.choice([u for u in users[1:] if u.id != group.leader_id]).id,
                    role=random.choice(["member", "member", "admin"]),
                    joined_at=datetime.now() - timedelta(days=random.randint(1, 60))
                )
                db.add(member)
        
        db.commit()
        print(f"  ✅ 已插入 {len(groups)} 个团队")
        
        # ==================== 12. 插入轮播图 ====================
        print("\n1️⃣2️⃣ 插入轮播图...")
        banners = []
        
        for i in range(5):
            banner = Banner(
                title=f"轮播图{i+1}",
                image_url=f"https://via.placeholder.com/800x400?text=Banner{i+1}",
                link_url=f"/project/{random.choice(projects).id}",
                sort_order=i + 1,
                status="active",
                description=f"轮播图{i+1}说明"
            )
            db.add(banner)
            banners.append(banner)
        
        db.commit()
        print(f"  ✅ 已插入 {len(banners)} 个轮播图")
        
        # ==================== 13. 插入公告 ====================
        print("\n1️⃣3️⃣ 插入公告...")
        announcements = []
        
        for i in range(8):
            announcement = Announcement(
                title=f"系统公告{i+1}",
                content=f"这是第{i+1}条系统公告内容，用于测试后台管理功能。",
                type=random.choice(["notice", "maintenance", "update"]),
                status="published",
                sort_order=i + 1,
                published_at=datetime.now() - timedelta(days=random.randint(1, 30))
            )
            db.add(announcement)
            announcements.append(announcement)
        
        db.commit()
        print(f"  ✅ 已插入 {len(announcements)} 条公告")
        
        # ==================== 14. 插入帮助文档 ====================
        print("\n1️⃣4️⃣ 插入帮助文档...")
        helps = []
        help_categories = ["account", "order", "payment", "other"]
        
        for i in range(12):
            help_doc = HelpArticle(
                title=f"帮助文档{i+1}",
                category=random.choice(help_categories),
                content=f"这是第{i+1}条帮助文档内容，用于解答用户常见问题。",
                status="published",
                sort_order=i + 1,
                view_count=random.randint(0, 1000)
            )
            db.add(help_doc)
            helps.append(help_doc)
        
        db.commit()
        print(f"  ✅ 已插入 {len(helps)} 条帮助文档")
        
        # ==================== 15. 插入聊天记录 ====================
        print("\n1️⃣5️⃣ 插入聊天记录...")
        chats = []
        
        for user in random.sample(users[1:], 5):
            for i in range(random.randint(3, 10)):
                chat = ChatMessage(
                    user_id=user.id,
                    message=f"用户咨询消息{i+1}",
                    reply=f"客服回复消息{i+1}",
                    status=random.choice(["pending", "replied", "closed"]),
                    created_at=datetime.now() - timedelta(days=random.randint(1, 30))
                )
                db.add(chat)
                chats.append(chat)
        
        db.commit()
        print(f"  ✅ 已插入 {len(chats)} 条聊天记录")
        
        # ==================== 16. 插入报告 ====================
        print("\n1️⃣6️⃣ 插入检测报告...")
        reports = []
        
        for order in random.sample(orders, 10):
            report = Report(
                order_id=order.id,
                order_no=order.order_no,
                user_id=order.user_id,
                project_id=order.project_id,
                project_name=order.project_name,
                report_no=f"RPT{int(time.time())}{random.randint(1000, 9999)}",
                file_url=f"https://example.com/reports/{order.order_no}.pdf",
                status=random.choice(["generating", "ready", "downloaded"]),
                generated_at=datetime.now() - timedelta(days=random.randint(1, 10)) if random.choice([True, False]) else None,
                created_at=datetime.now() - timedelta(days=random.randint(1, 20))
            )
            db.add(report)
            reports.append(report)
        
        db.commit()
        print(f"  ✅ 已插入 {len(reports)} 份检测报告")
        
        # ==================== 17. 插入样品追踪 ====================
        print("\n1️⃣7️⃣ 插入样品追踪...")
        samples = []
        sample_statuses = ["received", "testing", "completed", "shipped"]
        
        for order in random.sample(orders, 15):
            for i in range(random.randint(1, 3)):
                sample = SampleTracking(
                    order_id=order.id,
                    order_no=order.order_no,
                    sample_name=f"样品{i+1}",
                    status=random.choice(sample_statuses),
                    tracking_no=f"TRK{int(time.time())}{i:03d}" if random.choice([True, False]) else None,
                    received_at=datetime.now() - timedelta(days=random.randint(1, 10)) if random.choice([True, False]) else None,
                    testing_at=datetime.now() - timedelta(days=random.randint(1, 5)) if random.choice([True, False]) else None,
                    completed_at=datetime.now() - timedelta(days=random.randint(1, 3)) if random.choice([True, False]) else None,
                    shipped_at=datetime.now() - timedelta(days=random.randint(1, 2)) if random.choice([True, False]) else None,
                    created_at=datetime.now() - timedelta(days=random.randint(1, 15))
                )
                db.add(sample)
                samples.append(sample)
        
        db.commit()
        print(f"  ✅ 已插入 {len(samples)} 条样品追踪")
        
        # ==================== 18. 插入合同 ====================
        print("\n1️⃣8️⃣ 插入合同...")
        contracts = []
        
        for order in random.sample(orders, 8):
            contract = Contract(
                order_id=order.id,
                order_no=order.order_no,
                user_id=order.user_id,
                contract_no=f"CON{int(time.time())}{random.randint(1000, 9999)}",
                file_url=f"https://example.com/contracts/{order.order_no}.pdf",
                status=random.choice(["draft", "signed", "completed"]),
                signed_at=datetime.now() - timedelta(days=random.randint(1, 10)) if random.choice([True, False]) else None,
                created_at=datetime.now() - timedelta(days=random.randint(1, 20))
            )
            db.add(contract)
            contracts.append(contract)
        
        db.commit()
        print(f"  ✅ 已插入 {len(contracts)} 份合同")
        
        # ==================== 19. 插入加盟申请 ====================
        print("\n1️⃣9️⃣ 插入加盟申请...")
        franchises = []
        
        for i in range(6):
            franchise = FranchiseApplication(
                company_name=f"测试公司{i+1}",
                contact_person=f"联系人{i+1}",
                contact_phone=f"1390013900{i}",
                contact_email=f"contact{i+1}@example.com",
                province=random.choice(["北京市", "上海市", "广东省", "浙江省"]),
                city=random.choice(["北京市", "上海市", "广州市", "杭州市"]),
                address=f"测试地址{i+1}号",
                business_scope=f"测试业务范围{i+1}",
                investment_budget=random.choice([50, 100, 200, 500]),
                status=random.choice(["pending", "reviewing", "approved", "rejected"]),
                remark=f"测试备注{i+1}",
                created_at=datetime.now() - timedelta(days=random.randint(1, 60))
            )
            db.add(franchise)
            franchises.append(franchise)
        
        db.commit()
        print(f"  ✅ 已插入 {len(franchises)} 条加盟申请")
        
        # ==================== 总结 ====================
        print("\n🎉 后台管理测试数据插入完成！")
        print("\n📊 数据统计：")
        print(f"  - 用户：{len(users)} 个")
        print(f"  - 实验室：{len(labs)} 个")
        print(f"  - 分类：{len(categories)} 个")
        print(f"  - 项目：{len(projects)} 个")
        print(f"  - 订单：{len(orders)} 个")
        print(f"  - 地址：{len(addresses)} 个")
        print(f"  - 优惠券：{len(coupons)} 个")
        print(f"  - 积分记录：{len(points_records)} 条")
        print(f"  - 充值记录：{len(recharge_records)} 条")
        print(f"  - 邀请记录：{len(invite_records)} 条")
        print(f"  - 团队：{len(groups)} 个")
        print(f"  - 轮播图：{len(banners)} 个")
        print(f"  - 公告：{len(announcements)} 条")
        print(f"  - 帮助文档：{len(helps)} 条")
        print(f"  - 聊天记录：{len(chats)} 条")
        print(f"  - 检测报告：{len(reports)} 份")
        print(f"  - 样品追踪：{len(samples)} 条")
        print(f"  - 合同：{len(contracts)} 份")
        print(f"  - 加盟申请：{len(franchises)} 条")
        
        print("\n💡 提示：")
        print("  - 管理员账号：admin")
        print("  - 管理员密码：123456")
        print("  - 测试用户密码：password")
        print("  - 访问后台：http://localhost:3001/admin")
        
    except Exception as e:
        print(f"\n❌ 插入数据失败：{e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    insert_test_data()
