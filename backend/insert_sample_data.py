"""
插入示例数据
"""
import sys
sys.path.insert(0, '.')

from app.core.config import settings
from app.core.database import SessionLocal
from app.models.project import Laboratory, ProjectCategory, Project
from decimal import Decimal
import time


def insert_sample_data():
    """插入示例数据"""
    db = SessionLocal()
    
    try:
        print("📦 开始插入示例数据...")
        
        # 1. 插入实验室
        print("\n1️⃣ 插入实验室...")
        labs = [
            Laboratory(
                lab_no=f"LAB{int(time.time())}001",
                name="清华大学材料学院分析测试中心",
                short_name="清华材料中心",
                type="高校实验室",
                level="国家级",
                institution="清华大学",
                province="北京市",
                city="北京市",
                address="海淀区清华园1号",
                contact_person="张老师",
                contact_phone="010-12345678",
                rating=Decimal("4.9"),
                order_count=1250,
                is_verified=True,
                status="active",
                introduction="清华大学材料学院分析测试中心拥有先进的材料分析测试设备，为科研和工业提供专业的检测服务。"
            ),
            Laboratory(
                lab_no=f"LAB{int(time.time())}002",
                name="北京大学化学与分子工程学院测试中心",
                short_name="北大化学中心",
                type="高校实验室",
                level="国家级",
                institution="北京大学",
                province="北京市",
                city="北京市",
                address="海淀区颐和园路5号",
                contact_person="李老师",
                contact_phone="010-87654321",
                rating=Decimal("4.8"),
                order_count=980,
                is_verified=True,
                status="active",
                introduction="北京大学化学与分子工程学院测试中心提供全面的化学分析和材料表征服务。"
            ),
            Laboratory(
                lab_no=f"LAB{int(time.time())}003",
                name="上海交通大学分析测试中心",
                short_name="交大测试中心",
                type="高校实验室",
                level="省部级",
                institution="上海交通大学",
                province="上海市",
                city="上海市",
                address="闵行区东川路800号",
                contact_person="王老师",
                contact_phone="021-12345678",
                rating=Decimal("4.7"),
                order_count=756,
                is_verified=True,
                status="active"
            )
        ]
        
        for lab in labs:
            db.add(lab)
        db.commit()
        print(f"  ✅ 已插入 {len(labs)} 个实验室")
        
        # 2. 插入项目分类
        print("\n2️⃣ 插入项目分类...")
        categories = [
            ProjectCategory(name="电镜专场", code="SEM", icon="🔬", is_hot=True, sort_order=1),
            ProjectCategory(name="材料测试", code="MAT", icon="🧪", is_hot=True, sort_order=2),
            ProjectCategory(name="化学分析", code="CHE", icon="⚗️", is_hot=False, sort_order=3),
            ProjectCategory(name="生物检测", code="BIO", icon="🧬", is_hot=False, sort_order=4),
            ProjectCategory(name="物理性能", code="PHY", icon="⚡", is_hot=False, sort_order=5),
        ]
        
        for cat in categories:
            db.add(cat)
        db.commit()
        print(f"  ✅ 已插入 {len(categories)} 个分类")
        
        # 刷新以获取ID
        for cat in categories:
            db.refresh(cat)
        for lab in labs:
            db.refresh(lab)
        
        # 3. 插入项目
        print("\n3️⃣ 插入检测项目...")
        projects = [
            Project(
                project_no=f"PRJ{int(time.time())}001",
                name="场发射扫描电镜（SEM）",
                category_id=categories[0].id,
                lab_id=labs[0].id,
                original_price=Decimal("400.00"),
                current_price=Decimal("312.00"),
                unit="样品",
                service_cycle_min=3,
                service_cycle_max=5,
                equipment_name="场发射扫描电镜",
                equipment_model="FEI Quanta 450",
                introduction="场发射扫描电镜是一种高分辨率的表面形貌观察仪器，可以观察样品的微观结构和形貌。",
                sample_requirements="样品尺寸：≤1cm×1cm×0.5cm；样品需干燥、导电；粉末样品需固定在导电胶上。",
                booking_notice="1. 请提前3天预约\n2. 样品需提前送达\n3. 特殊样品需提前说明",
                cover_image="https://via.placeholder.com/400x300",
                status="active",
                is_hot=True,
                is_recommended=True,
                view_count=3256,
                booking_count=456,
                satisfaction=Decimal("98.5"),
                sort_order=1
            ),
            Project(
                project_no=f"PRJ{int(time.time())}002",
                name="X射线衍射（XRD）",
                category_id=categories[1].id,
                lab_id=labs[0].id,
                original_price=Decimal("300.00"),
                current_price=Decimal("250.00"),
                unit="样品",
                service_cycle_min=2,
                service_cycle_max=4,
                equipment_name="X射线衍射仪",
                equipment_model="Bruker D8 Advance",
                introduction="X射线衍射用于分析晶体结构、物相组成、晶粒尺寸等。",
                sample_requirements="粉末样品：≥100mg；块体样品：平整表面，尺寸≤2cm×2cm。",
                booking_notice="1. 请提前2天预约\n2. 粉末样品需磨细\n3. 块体样品需平整",
                cover_image="https://via.placeholder.com/400x300",
                status="active",
                is_hot=True,
                view_count=2134,
                booking_count=312,
                satisfaction=Decimal("97.2"),
                sort_order=2
            ),
            Project(
                project_no=f"PRJ{int(time.time())}003",
                name="傅里叶红外光谱（FTIR）",
                category_id=categories[2].id,
                lab_id=labs[1].id,
                original_price=Decimal("200.00"),
                current_price=Decimal("180.00"),
                unit="样品",
                service_cycle_min=1,
                service_cycle_max=3,
                equipment_name="傅里叶红外光谱仪",
                equipment_model="Thermo Nicolet iS50",
                introduction="红外光谱用于鉴定有机化合物的官能团、分析物质的分子结构。",
                sample_requirements="固体、液体、粉末均可；样品量：≥10mg。",
                cover_image="https://via.placeholder.com/400x300",
                status="active",
                view_count=1892,
                booking_count=234,
                satisfaction=Decimal("96.8"),
                sort_order=3
            ),
            Project(
                project_no=f"PRJ{int(time.time())}004",
                name="热重分析（TGA）",
                category_id=categories[1].id,
                lab_id=labs[1].id,
                original_price=Decimal("250.00"),
                current_price=Decimal("220.00"),
                unit="样品",
                service_cycle_min=2,
                service_cycle_max=3,
                equipment_name="热重分析仪",
                equipment_model="TA Q500",
                introduction="热重分析用于测定物质在加热过程中的质量变化，研究热稳定性、分解过程等。",
                sample_requirements="样品量：5-10mg；耐高温样品优先。",
                cover_image="https://via.placeholder.com/400x300",
                status="active",
                view_count=1456,
                booking_count=178,
                satisfaction=Decimal("95.6"),
                sort_order=4
            ),
            Project(
                project_no=f"PRJ{int(time.time())}005",
                name="透射电镜（TEM）",
                category_id=categories[0].id,
                lab_id=labs[2].id,
                original_price=Decimal("500.00"),
                current_price=Decimal("450.00"),
                unit="样品",
                service_cycle_min=5,
                service_cycle_max=7,
                equipment_name="透射电子显微镜",
                equipment_model="FEI Tecnai G2 F20",
                introduction="透射电镜可以观察纳米级别的材料内部结构，分辨率可达0.2nm。",
                sample_requirements="样品需制备成超薄切片（≤100nm）或分散在铜网上的纳米颗粒。",
                booking_notice="1. 样品制备周期长，请提前7天预约\n2. 特殊样品需要讨论制样方案",
                cover_image="https://via.placeholder.com/400x300",
                status="active",
                is_hot=True,
                is_recommended=True,
                view_count=2789,
                booking_count=289,
                satisfaction=Decimal("99.1"),
                sort_order=5
            )
        ]
        
        for proj in projects:
            db.add(proj)
        db.commit()
        print(f"  ✅ 已插入 {len(projects)} 个检测项目")
        
        print("\n🎉 示例数据插入完成！")
        print("\n📊 数据统计：")
        print(f"  - 实验室：{len(labs)} 个")
        print(f"  - 分类：{len(categories)} 个")
        print(f"  - 项目：{len(projects)} 个")
        
    except Exception as e:
        print(f"\n❌ 插入数据失败：{e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    insert_sample_data()

