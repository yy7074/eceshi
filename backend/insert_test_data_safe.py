"""
安全插入后台管理测试数据（跳过已存在的数据）
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
from app.models.role import Role, Permission, RoleCode, PermissionCode, DEFAULT_ROLE_PERMISSIONS
from app.core.security import get_password_hash
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
    """安全插入完整测试数据"""
    db = SessionLocal()
    
    try:
        print("📦 开始插入后台管理测试数据（安全模式）...")
        
        # ==================== 0. 初始化角色和权限 ====================
        print("\n0️⃣ 初始化角色和权限...")
        
        # 检查是否已有角色
        existing_roles = db.query(Role).count()
        if existing_roles == 0:
            # 获取权限码列表
            perm_codes = [
                PermissionCode.USER_VIEW, PermissionCode.USER_EDIT, PermissionCode.USER_DELETE, PermissionCode.USER_CERTIFICATION,
                PermissionCode.ORDER_VIEW, PermissionCode.ORDER_EDIT, PermissionCode.ORDER_DELETE, PermissionCode.ORDER_ASSIGN, PermissionCode.ORDER_EXPORT,
                PermissionCode.PROJECT_VIEW, PermissionCode.PROJECT_CREATE, PermissionCode.PROJECT_EDIT, PermissionCode.PROJECT_DELETE,
                PermissionCode.LAB_VIEW, PermissionCode.LAB_CREATE, PermissionCode.LAB_EDIT, PermissionCode.LAB_DELETE, PermissionCode.LAB_APPROVE,
                PermissionCode.FINANCE_VIEW, PermissionCode.FINANCE_RECHARGE, PermissionCode.FINANCE_REFUND, PermissionCode.FINANCE_WITHDRAW, PermissionCode.FINANCE_REPORT,
                PermissionCode.COUPON_VIEW, PermissionCode.COUPON_CREATE, PermissionCode.COUPON_EDIT, PermissionCode.COUPON_DELETE,
                PermissionCode.CONTENT_BANNER, PermissionCode.CONTENT_ANNOUNCEMENT, PermissionCode.CONTENT_HELP,
                PermissionCode.REPORT_VIEW, PermissionCode.REPORT_EXPORT,
                PermissionCode.SYSTEM_CONFIG, PermissionCode.SYSTEM_ROLE, PermissionCode.SYSTEM_LOG,
            ]
            
            # 插入权限
            permissions = {}
            for code in perm_codes:
                perm = Permission(
                    code=code,
                    name=code,
                    description=f"{code}权限"
                )
                db.add(perm)
                db.flush()
                permissions[code] = perm
            
            # 角色列表
            role_data = [
                (RoleCode.SUPER_ADMIN, "超级管理员"),
                (RoleCode.ADMIN, "管理员"),
                (RoleCode.OPERATOR, "运营人员"),
                (RoleCode.FINANCE, "财务人员"),
                (RoleCode.CUSTOMER_SERVICE, "客服人员"),
                (RoleCode.LAB_ADMIN, "实验室管理员"),
                (RoleCode.LAB_TECHNICIAN, "实验室技术员"),
                (RoleCode.USER, "普通用户"),
            ]
            
            # 插入角色
            roles = {}
            for code, name in role_data:
                role = Role(
                    code=code,
                    name=name,
                    description=f"{name}角色",
                    is_system=True
                )
                db.add(role)
                db.flush()
                roles[code] = role
                
                # 分配权限
                if code in DEFAULT_ROLE_PERMISSIONS:
                    for perm_code in DEFAULT_ROLE_PERMISSIONS[code]:
                        if perm_code in permissions:
                            role.permissions.append(permissions[perm_code])
            
            db.commit()
            print(f"  ✅ 已初始化角色和权限")
        else:
            print(f"  ⏭️ 角色已存在，跳过")
        
        # ==================== 1. 插入用户测试数据 ====================
        print("\n1️⃣ 插入用户测试数据...")
        users = []
        
        # 检查管理员用户是否存在
        admin_user = db.query(User).filter(User.phone == "admin").first()
        if not admin_user:
            admin_user = User(
                phone="admin",
                password=get_password_hash("123456"),
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
            print("  ✅ 创建管理员用户")
        else:
            print("  ⏭️ 管理员用户已存在")
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
        
        new_users = 0
        for idx, (name, phone, identity) in enumerate(user_names):
            existing = db.query(User).filter(User.phone == phone).first()
            if existing:
                users.append(existing)
                continue
                
            user = User(
                phone=phone,
                password=get_password_hash("123456"),
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
            new_users += 1
        
        db.commit()
        print(f"  ✅ 新增 {new_users} 个用户，共 {len(users)} 个")
        
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
        
        existing_labs = db.query(Laboratory).count()
        if existing_labs == 0:
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
        else:
            labs = db.query(Laboratory).all()
            print(f"  ⏭️ 实验室已存在，共 {len(labs)} 个")
        
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
        
        existing_cats = db.query(ProjectCategory).count()
        if existing_cats == 0:
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
        else:
            categories = db.query(ProjectCategory).all()
            print(f"  ⏭️ 分类已存在，共 {len(categories)} 个")
        
        # ==================== 4. 插入检测项目 ====================
        print("\n4️⃣ 插入检测项目...")
        projects = []
        
        existing_projects = db.query(Project).count()
        if existing_projects == 0 and len(categories) > 0 and len(labs) > 0:
            project_data = [
                ("场发射扫描电镜（SEM）", "FEI Quanta 450", 400.00, 312.00, 3, 5, 0, 0, True, True),
                ("X射线衍射（XRD）", "Bruker D8 Advance", 300.00, 250.00, 2, 4, 1, 0, True, False),
                ("傅里叶红外光谱（FTIR）", "Thermo Nicolet iS50", 200.00, 180.00, 1, 3, 2, 1, False, False),
                ("热重分析（TGA）", "TA Q500", 250.00, 220.00, 2, 3, 1, 1, False, False),
                ("透射电镜（TEM）", "FEI Tecnai G2 F20", 500.00, 450.00, 5, 7, 0, 2, True, True),
                ("能谱分析（EDS）", "Oxford X-Max", 150.00, 120.00, 1, 2, 0, 0, False, False),
                ("拉曼光谱", "Renishaw inVia", 350.00, 300.00, 2, 4, 2, 1, False, False),
                ("紫外-可见光谱", "Agilent Cary 5000", 180.00, 150.00, 1, 2, 2, 2, False, False),
                ("核磁共振（NMR）", "Bruker AVANCE III", 800.00, 700.00, 3, 5, 2, 3, True, False),
                ("原子力显微镜（AFM）", "Bruker Dimension Icon", 600.00, 520.00, 4, 6, 0, 4, True, True),
            ]
            
            for idx, (name, model, original_price, current_price, cycle_min, cycle_max, cat_idx, lab_idx, is_hot, is_recommended) in enumerate(project_data):
                cat_id = categories[cat_idx % len(categories)].id
                lab_id = labs[lab_idx % len(labs)].id
                
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
        else:
            projects = db.query(Project).all()
            print(f"  ⏭️ 项目已存在，共 {len(projects)} 个")
        
        # ==================== 5. 插入订单测试数据 ====================
        print("\n5️⃣ 插入订单测试数据...")
        orders = []
        
        existing_orders = db.query(Order).count()
        if existing_orders < 10 and len(projects) > 0 and len(labs) > 0:
            order_statuses = ["pending_payment", "paid", "confirmed", "testing", "completed", "cancelled"]
            
            for i in range(20):
                user = random.choice(users[1:]) if len(users) > 1 else users[0]
                project = random.choice(projects)
                lab = next((l for l in labs if l.id == project.lab_id), labs[0] if labs else None)
                status = random.choice(order_statuses)
                
                if not lab:
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
        else:
            orders = db.query(Order).all()
            print(f"  ⏭️ 订单已存在，共 {len(orders)} 个")
        
        # ==================== 6. 插入用户地址 ====================
        print("\n6️⃣ 插入用户地址...")
        
        existing_addresses = db.query(UserAddress).count()
        if existing_addresses == 0:
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
        else:
            print(f"  ⏭️ 地址已存在")
        
        # ==================== 7. 插入优惠券 ====================
        print("\n7️⃣ 插入优惠券...")
        
        existing_coupons = db.query(Coupon).count()
        if existing_coupons == 0:
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
                for user in random.sample(users[1:], min(random.randint(1, 5), len(users)-1)):
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
        else:
            print(f"  ⏭️ 优惠券已存在")
        
        # ==================== 8. 插入积分记录 ====================
        print("\n8️⃣ 插入积分记录...")
        
        existing_points = db.query(PointsRecord).count()
        if existing_points == 0:
            points_records = []
            point_types = ["order", "review", "invite", "signup", "daily"]
            
            for user in users[1:]:
                for i in range(random.randint(5, 20)):
                    record = PointsRecord(
                        user_id=user.id,
                        points=random.choice([10, 20, 50, 100]),
                        type=random.choice(point_types),
                        description=f"积分记录{i+1}"
                    )
                    db.add(record)
                    points_records.append(record)
            db.commit()
            print(f"  ✅ 已插入 {len(points_records)} 条积分记录")
        else:
            print(f"  ⏭️ 积分记录已存在")
        
        # ==================== 9. 插入充值记录 ====================
        print("\n9️⃣ 插入充值记录...")
        
        existing_recharge = db.query(RechargeRecord).count()
        if existing_recharge == 0:
            recharge_records = []
            recharge_methods = ["wechat", "alipay"]
            
            for user in users[1:]:
                for i in range(random.randint(0, 5)):
                    amount = random.choice([100, 200, 500, 1000, 2000])
                    record = RechargeRecord(
                        recharge_no=generate_recharge_no(),
                        user_id=user.id,
                        amount=Decimal(str(amount)),
                        actual_amount=Decimal(str(amount * 1.1)),
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
        else:
            print(f"  ⏭️ 充值记录已存在")
        
        # ==================== 10. 插入邀请记录 ====================
        print("\n🔟 插入邀请记录...")
        
        existing_invites = db.query(InviteRecord).count()
        if existing_invites == 0:
            invite_records = []
            
            for i in range(15):
                inviter = random.choice(users[1:])
                invitee = random.choice([u for u in users[1:] if u.id != inviter.id])
                
                record = InviteRecord(
                    inviter_id=inviter.id,
                    invitee_id=invitee.id,
                    inviter_name=inviter.nickname,
                    inviter_phone=inviter.phone,
                    invitee_name=invitee.nickname,
                    invitee_phone=invitee.phone,
                    reward_amount=Decimal(str(random.choice([10, 20, 50]))),
                    completed_at=datetime.now() - timedelta(days=random.randint(1, 30)) if random.choice([True, False]) else None
                )
                db.add(record)
                invite_records.append(record)
            db.commit()
            print(f"  ✅ 已插入 {len(invite_records)} 条邀请记录")
        else:
            print(f"  ⏭️ 邀请记录已存在")
        
        # ==================== 11. 插入团队 ====================
        print("\n1️⃣1️⃣ 插入团队...")
        
        existing_groups = db.query(UserGroup).count()
        if existing_groups == 0:
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
        else:
            print(f"  ⏭️ 团队已存在")
        
        # ==================== 12. 插入轮播图 ====================
        print("\n1️⃣2️⃣ 插入轮播图...")
        
        existing_banners = db.query(Banner).count()
        if existing_banners == 0:
            banners = []
            
            for i in range(5):
                banner = Banner(
                    title=f"轮播图{i+1}",
                    image_url=f"https://via.placeholder.com/800x400?text=Banner{i+1}",
                    link_url=f"/project/{projects[i % len(projects)].id}" if projects else "/",
                    sort_order=i + 1,
                    status="active",
                    description=f"轮播图{i+1}说明"
                )
                db.add(banner)
                banners.append(banner)
            db.commit()
            print(f"  ✅ 已插入 {len(banners)} 个轮播图")
        else:
            print(f"  ⏭️ 轮播图已存在")
        
        # ==================== 13. 插入公告 ====================
        print("\n1️⃣3️⃣ 插入公告...")
        
        existing_announcements = db.query(Announcement).count()
        if existing_announcements == 0:
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
        else:
            print(f"  ⏭️ 公告已存在")
        
        # ==================== 14. 插入帮助文档 ====================
        print("\n1️⃣4️⃣ 插入帮助文档...")
        
        existing_helps = db.query(HelpArticle).count()
        if existing_helps == 0:
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
        else:
            print(f"  ⏭️ 帮助文档已存在")
        
        # ==================== 15. 插入加盟申请 ====================
        print("\n1️⃣5️⃣ 插入加盟申请...")
        
        existing_franchises = db.query(FranchiseApplication).count()
        if existing_franchises == 0:
            franchises = []
            
            for i in range(6):
                franchise = FranchiseApplication(
                    application_no=f"FA{int(time.time())}{i:03d}",
                    name=f"联系人{i+1}",
                    phone=f"1390013900{i}",
                    company=f"测试公司{i+1}",
                    city=random.choice(["北京市", "上海市", "广州市", "杭州市"]),
                    mode=random.choice(["agent", "partner", "lab"]),
                    intention=f"测试合作意向{i+1}",
                    status=random.choice(["pending", "contacted", "approved", "rejected"])
                )
                db.add(franchise)
                franchises.append(franchise)
            db.commit()
            print(f"  ✅ 已插入 {len(franchises)} 条加盟申请")
        else:
            print(f"  ⏭️ 加盟申请已存在")
        
        # ==================== 总结 ====================
        print("\n🎉 后台管理测试数据插入完成！")
        print("\n📊 当前数据统计：")
        print(f"  - 用户：{db.query(User).count()} 个")
        print(f"  - 实验室：{db.query(Laboratory).count()} 个")
        print(f"  - 分类：{db.query(ProjectCategory).count()} 个")
        print(f"  - 项目：{db.query(Project).count()} 个")
        print(f"  - 订单：{db.query(Order).count()} 个")
        print(f"  - 地址：{db.query(UserAddress).count()} 个")
        print(f"  - 优惠券：{db.query(Coupon).count()} 个")
        print(f"  - 积分记录：{db.query(PointsRecord).count()} 条")
        print(f"  - 充值记录：{db.query(RechargeRecord).count()} 条")
        print(f"  - 邀请记录：{db.query(InviteRecord).count()} 条")
        print(f"  - 团队：{db.query(UserGroup).count()} 个")
        print(f"  - 轮播图：{db.query(Banner).count()} 个")
        print(f"  - 公告：{db.query(Announcement).count()} 条")
        print(f"  - 帮助文档：{db.query(HelpArticle).count()} 条")
        print(f"  - 加盟申请：{db.query(FranchiseApplication).count()} 条")
        
        print("\n💡 提示：")
        print("  - 管理员账号：admin")
        print("  - 管理员密码：123456（需通过API登录）")
        print("  - 测试用户手机号：13800138001 - 13800138008")
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
