"""
数据库初始化脚本
创建数据库和表
"""
import sys
from sqlalchemy import create_engine, text
from app.core.config import settings
from app.core.database import Base
from app.models.user import User, UserCertification

def create_database():
    """创建数据库（如果不存在）"""
    # 连接MySQL但不指定数据库
    db_url = settings.DATABASE_URL.rsplit('/', 1)[0]  # 移除数据库名
    engine = create_engine(db_url)
    
    with engine.connect() as conn:
        # 创建数据库
        conn.execute(text("CREATE DATABASE IF NOT EXISTS eceshi CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
        print("✅ 数据库 'eceshi' 创建成功（或已存在）")
    
    engine.dispose()

def create_tables():
    """创建所有表"""
    engine = create_engine(settings.DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    print("✅ 数据库表创建成功")
    
    # 显示创建的表
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"\n📋 已创建的表：")
    for table in tables:
        print(f"  - {table}")
    
    engine.dispose()

def main():
    """主函数"""
    print("🚀 开始初始化数据库...\n")
    
    try:
        # 1. 创建数据库
        print("📦 步骤1: 创建数据库")
        create_database()
        
        # 2. 创建表
        print("\n📦 步骤2: 创建数据库表")
        create_tables()
        
        print("\n✅ 数据库初始化完成！")
        print("\n💡 提示：")
        print("  - 现在可以启动后端服务：uvicorn app.main:app --reload")
        print("  - 访问API文档：http://localhost:8000/api/docs")
        
    except Exception as e:
        print(f"\n❌ 数据库初始化失败：{str(e)}")
        print("\n💡 请检查：")
        print("  1. MySQL服务是否已启动")
        print("  2. .env 文件中的数据库配置是否正确")
        print("  3. MySQL用户是否有创建数据库的权限")
        sys.exit(1)

if __name__ == "__main__":
    main()

