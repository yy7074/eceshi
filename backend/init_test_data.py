#!/usr/bin/env python3
"""
初始化测试数据脚本
运行方式: cd backend && python init_test_data.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta
from decimal import Decimal
from sqlalchemy.orm import Session

from app.core.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.project import Project, ProjectCategory
from app.models.laboratory import Laboratory, LabType, LabStatus
from app.models.coupon import Coupon, UserCoupon
from app.models.banner import Banner
from app.models.announcement import Announcement
from app.models.help import HelpCategory, HelpArticle
from app.models.points import PointsGoods
from app.models.lottery import LotteryPrize
from app.core.security import get_password_hash


def init_test_data():
    """初始化测试数据"""
    db = SessionLocal()
    
    try:
        print("🚀 开始初始化测试数据...")
        
        # 1. 创建项目分类
        print("\n📁 创建项目分类...")
        categories_data = [
            {"name": "材料分析", "code": "material", "icon": "🔬", "description": "材料成分、结构、性能分析", "sort_order": 1},
            {"name": "表面分析", "code": "surface", "icon": "🔍", "description": "表面形貌、成分、结构分析", "sort_order": 2},
            {"name": "热分析", "code": "thermal", "icon": "🌡️", "description": "热性能、热稳定性分析", "sort_order": 3},
            {"name": "光谱分析", "code": "spectrum", "icon": "🌈", "description": "各类光谱测试分析", "sort_order": 4},
            {"name": "力学测试", "code": "mechanical", "icon": "💪", "description": "力学性能测试", "sort_order": 5},
            {"name": "环境检测", "code": "environment", "icon": "🌿", "description": "环境样品检测分析", "sort_order": 6},
            {"name": "生物医学", "code": "biomedical", "icon": "🧬", "description": "生物医学相关检测", "sort_order": 7},
            {"name": "电化学", "code": "electrochemistry", "icon": "⚡", "description": "电化学性能测试", "sort_order": 8},
        ]
        
        for cat_data in categories_data:
            existing = db.query(ProjectCategory).filter(ProjectCategory.code == cat_data["code"]).first()
            if not existing:
                category = ProjectCategory(
                    name=cat_data["name"],
                    code=cat_data["code"],
                    icon=cat_data.get("icon"),
                    description=cat_data.get("description"),
                    sort_order=cat_data.get("sort_order", 0),
                    is_active=True
                )
                db.add(category)
                print(f"  ✅ 创建分类: {cat_data['name']}")
            else:
                print(f"  ⏭️ 分类已存在: {cat_data['name']}")
        
        db.commit()
        
        # 2. 创建实验室
        print("\n🏛️ 创建实验室...")
        labs_data = [
            {
                "name": "平台实验室",
                "lab_no": "LAB001",
                "code": "platform",
                "short_name": "平台实验室",
                "lab_type": "platform",
                "type": "comprehensive",
                "level": "national",
                "status": "active",
                "is_verified": True,
                "institution": "科研检测服务平台",
                "province": "北京市",
                "city": "北京市",
                "address": "北京市海淀区中关村科技园",
                "contact_name": "张工程师",
                "contact_phone": "010-12345678",
                "contact_email": "lab@eceshi.com",
                "description": "平台自营综合检测实验室，提供全方位检测服务",
                "rating": 4.9,
                "order_count": 1000,
            },
            {
                "name": "清华大学材料分析中心",
                "lab_no": "LAB002",
                "code": "tsinghua",
                "short_name": "清华材料中心",
                "lab_type": "university",
                "type": "material",
                "level": "national",
                "status": "active",
                "is_verified": True,
                "institution": "清华大学",
                "province": "北京市",
                "city": "北京市",
                "address": "北京市海淀区清华园1号",
                "contact_name": "李教授",
                "contact_phone": "010-62785678",
                "contact_email": "material@tsinghua.edu.cn",
                "description": "清华大学材料科学与工程学院分析测试中心",
                "rating": 4.8,
                "order_count": 500,
            },
            {
                "name": "中科院化学所分析中心",
                "lab_no": "LAB003",
                "code": "cas_chemistry",
                "short_name": "中科院化学所",
                "lab_type": "research",
                "type": "chemistry",
                "level": "national",
                "status": "active",
                "is_verified": True,
                "institution": "中国科学院化学研究所",
                "province": "北京市",
                "city": "北京市",
                "address": "北京市海淀区中关村北一街2号",
                "contact_name": "王研究员",
                "contact_phone": "010-62554678",
                "contact_email": "analysis@iccas.ac.cn",
                "description": "中国科学院化学研究所公共分析测试平台",
                "rating": 4.9,
                "order_count": 800,
            },
        ]
        
        for lab_data in labs_data:
            existing = db.query(Laboratory).filter(Laboratory.lab_no == lab_data["lab_no"]).first()
            if not existing:
                # 转换枚举类型
                lab_type_str = lab_data.pop("lab_type", "university")
                status_str = lab_data.pop("status", "active")
                
                # 映射 lab_type 字符串到枚举
                lab_type_map = {
                    "platform": LabType.THIRD_PARTY,  # 平台实验室作为第三方
                    "university": LabType.UNIVERSITY,
                    "research": LabType.RESEARCH,
                    "enterprise": LabType.ENTERPRISE,
                    "hospital": LabType.HOSPITAL,
                }
                
                # 映射 status 字符串到枚举
                status_map = {
                    "pending": LabStatus.PENDING,
                    "approved": LabStatus.APPROVED,
                    "active": LabStatus.ACTIVE,
                    "suspended": LabStatus.SUSPENDED,
                    "closed": LabStatus.CLOSED,
                }
                
                lab = Laboratory(
                    **lab_data,
                    lab_type=lab_type_map.get(lab_type_str, LabType.UNIVERSITY),
                    status=status_map.get(status_str, LabStatus.ACTIVE)
                )
                db.add(lab)
                print(f"  ✅ 创建实验室: {lab_data['name']}")
            else:
                print(f"  ⏭️ 实验室已存在: {lab_data['name']}")
        
        db.commit()
        
        # 获取分类和实验室ID
        categories = {cat.code: cat.id for cat in db.query(ProjectCategory).all()}
        labs = {lab.code: lab.id for lab in db.query(Laboratory).all()}
        
        # 3. 创建检测项目
        print("\n🧪 创建检测项目...")
        projects_data = [
            # 材料分析
            {"name": "扫描电镜（SEM）", "category": "material", "lab": "platform", "price": 180, "unit": "样", "cycle_min": 3, "cycle_max": 5, "equipment": "蔡司 Sigma 500", "intro": "高分辨率扫描电子显微镜，可观察样品表面形貌和微观结构", "is_hot": True},
            {"name": "透射电镜（TEM）", "category": "material", "lab": "platform", "price": 350, "unit": "样", "cycle_min": 5, "cycle_max": 7, "equipment": "FEI Tecnai G2", "intro": "高分辨透射电子显微镜，可观察材料内部微观结构", "is_hot": True},
            {"name": "X射线衍射（XRD）", "category": "material", "lab": "platform", "price": 200, "unit": "样", "cycle_min": 2, "cycle_max": 3, "equipment": "Bruker D8 Advance", "intro": "用于材料物相分析、晶体结构测定", "is_hot": True},
            {"name": "能谱分析（EDS）", "category": "material", "lab": "platform", "price": 150, "unit": "点", "cycle_min": 2, "cycle_max": 3, "equipment": "Oxford X-Max", "intro": "元素成分定性和半定量分析"},
            
            # 表面分析
            {"name": "X射线光电子能谱（XPS）", "category": "surface", "lab": "tsinghua", "price": 400, "unit": "样", "cycle_min": 5, "cycle_max": 7, "equipment": "Thermo ESCALAB 250Xi", "intro": "表面元素组成和化学态分析", "is_hot": True},
            {"name": "原子力显微镜（AFM）", "category": "surface", "lab": "platform", "price": 300, "unit": "样", "cycle_min": 3, "cycle_max": 5, "equipment": "Bruker Dimension Icon", "intro": "纳米级表面形貌和力学性能测量"},
            {"name": "接触角测量", "category": "surface", "lab": "platform", "price": 100, "unit": "样", "cycle_min": 1, "cycle_max": 2, "equipment": "Dataphysics OCA25", "intro": "表面润湿性和表面能测量"},
            
            # 热分析
            {"name": "热重分析（TGA）", "category": "thermal", "lab": "platform", "price": 200, "unit": "样", "cycle_min": 2, "cycle_max": 3, "equipment": "TA Q500", "intro": "材料热稳定性和组分分析", "is_hot": True},
            {"name": "差示扫描量热（DSC）", "category": "thermal", "lab": "platform", "price": 200, "unit": "样", "cycle_min": 2, "cycle_max": 3, "equipment": "TA Q2000", "intro": "相变温度、熔点、结晶度测量"},
            {"name": "热机械分析（TMA）", "category": "thermal", "lab": "cas_chemistry", "price": 250, "unit": "样", "cycle_min": 3, "cycle_max": 5, "equipment": "TA Q400", "intro": "热膨胀系数和软化温度测量"},
            
            # 光谱分析
            {"name": "傅里叶红外光谱（FTIR）", "category": "spectrum", "lab": "platform", "price": 150, "unit": "样", "cycle_min": 1, "cycle_max": 2, "equipment": "Thermo Nicolet iS50", "intro": "有机官能团和分子结构分析", "is_hot": True},
            {"name": "拉曼光谱", "category": "spectrum", "lab": "platform", "price": 200, "unit": "样", "cycle_min": 2, "cycle_max": 3, "equipment": "Horiba LabRAM HR", "intro": "分子振动和晶体结构分析"},
            {"name": "紫外可见光谱（UV-Vis）", "category": "spectrum", "lab": "platform", "price": 100, "unit": "样", "cycle_min": 1, "cycle_max": 2, "equipment": "Shimadzu UV-2600", "intro": "光吸收特性和浓度测量"},
            {"name": "荧光光谱（PL）", "category": "spectrum", "lab": "tsinghua", "price": 200, "unit": "样", "cycle_min": 2, "cycle_max": 3, "equipment": "Edinburgh FLS1000", "intro": "荧光特性和量子效率测量"},
            
            # 力学测试
            {"name": "万能材料试验", "category": "mechanical", "lab": "platform", "price": 150, "unit": "样", "cycle_min": 2, "cycle_max": 3, "equipment": "Instron 5967", "intro": "拉伸、压缩、弯曲力学性能测试"},
            {"name": "纳米压痕测试", "category": "mechanical", "lab": "tsinghua", "price": 300, "unit": "点", "cycle_min": 3, "cycle_max": 5, "equipment": "Hysitron TI950", "intro": "纳米硬度和弹性模量测量"},
            {"name": "动态力学分析（DMA）", "category": "mechanical", "lab": "platform", "price": 250, "unit": "样", "cycle_min": 2, "cycle_max": 4, "equipment": "TA Q800", "intro": "动态力学性能和阻尼特性分析"},
            
            # 电化学
            {"name": "循环伏安测试（CV）", "category": "electrochemistry", "lab": "cas_chemistry", "price": 150, "unit": "样", "cycle_min": 2, "cycle_max": 3, "equipment": "CHI 760E", "intro": "电化学氧化还原特性分析"},
            {"name": "电化学阻抗谱（EIS）", "category": "electrochemistry", "lab": "cas_chemistry", "price": 200, "unit": "样", "cycle_min": 2, "cycle_max": 3, "equipment": "Gamry Reference 3000", "intro": "电极界面和电化学动力学分析"},
            {"name": "电池充放电测试", "category": "electrochemistry", "lab": "platform", "price": 300, "unit": "样", "cycle_min": 7, "cycle_max": 14, "equipment": "LAND CT2001A", "intro": "电池容量和循环性能测试"},
        ]
        
        project_no = 1
        for proj_data in projects_data:
            existing = db.query(Project).filter(Project.name == proj_data["name"]).first()
            if not existing:
                project = Project(
                    project_no=f"PRJ{project_no:04d}",
                    name=proj_data["name"],
                    category_id=categories.get(proj_data["category"]),
                    lab_id=labs.get(proj_data["lab"], labs.get("platform")),
                    original_price=Decimal(str(proj_data["price"] * 1.2)),
                    current_price=Decimal(str(proj_data["price"])),
                    unit=proj_data["unit"],
                    service_cycle_min=proj_data["cycle_min"],
                    service_cycle_max=proj_data["cycle_max"],
                    equipment_name=proj_data.get("equipment"),
                    introduction=proj_data.get("intro"),
                    status="active",
                    is_hot=proj_data.get("is_hot", False),
                    is_recommended=proj_data.get("is_hot", False),
                    view_count=100 + project_no * 10,
                    order_count=10 + project_no,
                )
                db.add(project)
                print(f"  ✅ 创建项目: {proj_data['name']}")
                project_no += 1
            else:
                print(f"  ⏭️ 项目已存在: {proj_data['name']}")
        
        db.commit()
        
        # 4. 创建测试用户并充值余额
        print("\n👤 创建测试用户...")
        test_users = [
            {"phone": "13800138000", "nickname": "测试用户A", "balance": 1000},
            {"phone": "13800138001", "nickname": "测试用户B", "balance": 500},
            {"phone": "13900000000", "nickname": "管理员", "balance": 10000, "is_admin": True},
        ]
        
        for user_data in test_users:
            existing = db.query(User).filter(User.phone == user_data["phone"]).first()
            if not existing:
                user = User(
                    phone=user_data["phone"],
                    nickname=user_data["nickname"],
                    password=get_password_hash("123456"),
                    prepaid_balance=Decimal(str(user_data["balance"])),
                    points_balance=100,
                    is_admin=user_data.get("is_admin", False),
                    status="active"
                )
                db.add(user)
                print(f"  ✅ 创建用户: {user_data['phone']} (余额: ¥{user_data['balance']})")
            else:
                # 更新余额
                existing.prepaid_balance = Decimal(str(user_data["balance"]))
                existing.points_balance = 100
                print(f"  ⏭️ 用户已存在，已更新余额: {user_data['phone']} (余额: ¥{user_data['balance']})")
        
        db.commit()
        
        # 5. 创建优惠券
        print("\n🎫 创建优惠券...")
        coupons_data = [
            {"name": "新用户专享券", "type": "fixed", "value": 50, "min_amount": 200, "total": 1000, "days": 30},
            {"name": "满500减100券", "type": "fixed", "value": 100, "min_amount": 500, "total": 500, "days": 60},
            {"name": "9折优惠券", "type": "percent", "value": 10, "min_amount": 100, "total": 500, "days": 30},
            {"name": "限时特惠券", "type": "fixed", "value": 30, "min_amount": 100, "total": 200, "days": 7},
        ]
        
        for coupon_data in coupons_data:
            existing = db.query(Coupon).filter(Coupon.name == coupon_data["name"]).first()
            if not existing:
                coupon = Coupon(
                    name=coupon_data["name"],
                    coupon_type=coupon_data["type"],
                    discount_value=Decimal(str(coupon_data["value"])),
                    min_order_amount=Decimal(str(coupon_data["min_amount"])),
                    total_count=coupon_data["total"],
                    used_count=0,
                    start_time=datetime.now(),
                    end_time=datetime.now() + timedelta(days=coupon_data["days"]),
                    status="active"
                )
                db.add(coupon)
                print(f"  ✅ 创建优惠券: {coupon_data['name']}")
            else:
                print(f"  ⏭️ 优惠券已存在: {coupon_data['name']}")
        
        db.commit()
        
        # 6. 创建Banner
        print("\n🖼️ 创建Banner...")
        banners_data = [
            {"title": "新用户专享优惠", "image": "https://via.placeholder.com/750x300/4A90E2/FFFFFF?text=新用户专享", "link_type": "page", "link_url": "/pages/coupon/coupon", "sort": 1},
            {"title": "热门检测服务", "image": "https://via.placeholder.com/750x300/7B68EE/FFFFFF?text=热门检测", "link_type": "page", "link_url": "/pages/project/list", "sort": 2},
            {"title": "限时优惠活动", "image": "https://via.placeholder.com/750x300/FF6B6B/FFFFFF?text=限时优惠", "link_type": "page", "link_url": "/pagesA/lottery/lottery", "sort": 3},
        ]
        
        for banner_data in banners_data:
            existing = db.query(Banner).filter(Banner.title == banner_data["title"]).first()
            if not existing:
                banner = Banner(
                    title=banner_data["title"],
                    image_url=banner_data["image"],
                    link_type=banner_data["link_type"],
                    link_url=banner_data["link_url"],
                    sort_order=banner_data["sort"],
                    is_active=True
                )
                db.add(banner)
                print(f"  ✅ 创建Banner: {banner_data['title']}")
            else:
                print(f"  ⏭️ Banner已存在: {banner_data['title']}")
        
        db.commit()
        
        # 7. 创建公告
        print("\n📢 创建公告...")
        announcements_data = [
            {"title": "平台服务升级公告", "content": "尊敬的用户，为了给您提供更好的服务体验，我们将于本周末进行系统升级维护。升级期间服务不受影响，感谢您的理解与支持！", "type": "notice"},
            {"title": "新增检测项目上线", "content": "平台新增多项热门检测项目，包括AFM、XPS等高端分析服务，欢迎体验！新用户下单可享专属优惠。", "type": "activity"},
            {"title": "春节放假通知", "content": "2026年春节期间（1月28日-2月4日），平台正常接单，但实验室检测服务将顺延至节后处理，敬请知悉。", "type": "notice"},
        ]
        
        for ann_data in announcements_data:
            existing = db.query(Announcement).filter(Announcement.title == ann_data["title"]).first()
            if not existing:
                announcement = Announcement(
                    title=ann_data["title"],
                    content=ann_data["content"],
                    announcement_type=ann_data["type"],
                    is_active=True,
                    is_top=False
                )
                db.add(announcement)
                print(f"  ✅ 创建公告: {ann_data['title']}")
            else:
                print(f"  ⏭️ 公告已存在: {ann_data['title']}")
        
        db.commit()
        
        # 8. 创建帮助中心内容
        print("\n❓ 创建帮助中心...")
        help_categories = [
            {"name": "下单指南", "code": "order", "sort": 1},
            {"name": "支付问题", "code": "payment", "sort": 2},
            {"name": "样品寄送", "code": "sample", "sort": 3},
            {"name": "报告下载", "code": "report", "sort": 4},
            {"name": "发票问题", "code": "invoice", "sort": 5},
        ]
        
        for cat_data in help_categories:
            existing = db.query(HelpCategory).filter(HelpCategory.code == cat_data["code"]).first()
            if not existing:
                category = HelpCategory(
                    name=cat_data["name"],
                    code=cat_data["code"],
                    sort_order=cat_data["sort"],
                    is_active=True
                )
                db.add(category)
                print(f"  ✅ 创建帮助分类: {cat_data['name']}")
        
        db.commit()
        
        # 获取帮助分类ID
        help_cats = {cat.code: cat.id for cat in db.query(HelpCategory).all()}
        
        help_articles = [
            {"category": "order", "title": "如何下单？", "content": "1. 选择检测项目\n2. 填写样品信息\n3. 选择收货地址\n4. 提交订单并支付\n5. 邮寄样品到实验室"},
            {"category": "order", "title": "可以修改订单吗？", "content": "订单支付前可以取消重新下单。支付后如需修改，请联系客服处理。"},
            {"category": "payment", "title": "支持哪些支付方式？", "content": "目前支持：\n1. 余额支付\n2. 微信支付\n3. 支付宝支付\n4. 信用支付（需申请额度）"},
            {"category": "payment", "title": "如何充值余额？", "content": "进入[我的]-[钱包]-[充值]，选择充值金额后完成支付即可。充值有赠送活动，多充多送！"},
            {"category": "sample", "title": "样品如何寄送？", "content": "下单后，请将样品寄送到订单中显示的实验室地址。建议使用顺丰快递，并在包裹上注明订单号。"},
            {"category": "report", "title": "报告多久出来？", "content": "一般检测周期为3-7个工作日，具体以项目页面显示为准。加急服务可缩短至24-48小时。"},
            {"category": "invoice", "title": "如何申请发票？", "content": "订单完成后，在订单详情页点击[申请发票]，填写发票信息后提交即可。电子发票将发送到您的邮箱。"},
        ]
        
        for article_data in help_articles:
            existing = db.query(HelpArticle).filter(HelpArticle.title == article_data["title"]).first()
            if not existing:
                article = HelpArticle(
                    category_id=help_cats.get(article_data["category"]),
                    title=article_data["title"],
                    content=article_data["content"],
                    view_count=10,
                    is_active=True
                )
                db.add(article)
                print(f"  ✅ 创建帮助文章: {article_data['title']}")
        
        db.commit()
        
        # 9. 创建积分商品
        print("\n🎁 创建积分商品...")
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
        
        for goods_data in points_goods_data:
            existing = db.query(PointsGoods).filter(PointsGoods.name == goods_data["name"]).first()
            if not existing:
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
                print(f"  ✅ 创建积分商品: {goods_data['name']} ({goods_data['points']}积分)")
        
        db.commit()
        
        # 10. 创建抽奖奖品
        print("\n🎰 创建抽奖奖品...")
        lottery_prizes_data = [
            {"name": "谢谢参与", "type": "thanks", "value": 0, "probability": 50, "stock": 999999},
            {"name": "10积分", "type": "points", "value": 10, "probability": 20, "stock": 10000},
            {"name": "50积分", "type": "points", "value": 50, "probability": 15, "stock": 5000},
            {"name": "10元优惠券", "type": "coupon", "value": 10, "probability": 10, "stock": 1000},
            {"name": "50元优惠券", "type": "coupon", "value": 50, "probability": 4, "stock": 200},
            {"name": "100元优惠券", "type": "coupon", "value": 100, "probability": 1, "stock": 50},
        ]
        
        for prize_data in lottery_prizes_data:
            existing = db.query(LotteryPrize).filter(LotteryPrize.name == prize_data["name"]).first()
            if not existing:
                prize = LotteryPrize(
                    name=prize_data["name"],
                    prize_type=prize_data["type"],
                    prize_value=Decimal(str(prize_data["value"])),
                    probability=Decimal(str(prize_data["probability"])),
                    stock=prize_data["stock"],
                    is_active=True
                )
                db.add(prize)
                print(f"  ✅ 创建奖品: {prize_data['name']}")
        
        db.commit()
        
        print("\n" + "="*50)
        print("✅ 测试数据初始化完成！")
        print("="*50)
        print("\n📋 测试账号：")
        print("  手机号: 13800138000  密码: 123456  余额: ¥1000")
        print("  手机号: 13800138001  密码: 123456  余额: ¥500")
        print("  手机号: 13900000000  密码: 123456  余额: ¥10000 (管理员)")
        print("\n💡 提示：使用手机号+验证码登录，验证码可在后台日志查看")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ 初始化失败: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    init_test_data()
