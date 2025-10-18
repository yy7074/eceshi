"""
数据库迁移脚本 - 添加微信登录支持
"""
import sys
sys.path.append('/Users/yy/Documents/GitHub/eceshi/backend')

from app.core.database import engine
from sqlalchemy import text


def upgrade():
    """添加微信相关字段"""
    with engine.connect() as conn:
        try:
            # 修改phone字段允许为空
            print("1. 修改phone字段允许为空...")
            conn.execute(text("""
                ALTER TABLE users 
                MODIFY COLUMN phone VARCHAR(20) NULL
            """))
            
            # 修改password字段允许为空
            print("2. 修改password字段允许为空...")
            conn.execute(text("""
                ALTER TABLE users 
                MODIFY COLUMN password VARCHAR(255) NULL
            """))
            
            # 添加微信openid字段
            print("3. 添加微信openid字段...")
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN wechat_openid VARCHAR(100) NULL COMMENT '微信OpenID' 
                AFTER email
            """))
            
            # 添加微信unionid字段
            print("4. 添加微信unionid字段...")
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN wechat_unionid VARCHAR(100) NULL COMMENT '微信UnionID' 
                AFTER wechat_openid
            """))
            
            # 为wechat_openid添加唯一索引
            print("5. 添加wechat_openid唯一索引...")
            conn.execute(text("""
                CREATE UNIQUE INDEX idx_wechat_openid ON users(wechat_openid)
            """))
            
            conn.commit()
            print("✅ 数据库迁移完成！")
            
        except Exception as e:
            print(f"❌ 迁移失败: {str(e)}")
            conn.rollback()
            raise


def downgrade():
    """回滚微信相关字段"""
    with engine.connect() as conn:
        try:
            print("回滚数据库迁移...")
            
            # 删除索引
            conn.execute(text("DROP INDEX idx_wechat_openid ON users"))
            
            # 删除字段
            conn.execute(text("ALTER TABLE users DROP COLUMN wechat_unionid"))
            conn.execute(text("ALTER TABLE users DROP COLUMN wechat_openid"))
            
            # 恢复NOT NULL约束
            conn.execute(text("ALTER TABLE users MODIFY COLUMN password VARCHAR(255) NOT NULL"))
            conn.execute(text("ALTER TABLE users MODIFY COLUMN phone VARCHAR(20) NOT NULL"))
            
            conn.commit()
            print("✅ 回滚完成！")
            
        except Exception as e:
            print(f"❌ 回滚失败: {str(e)}")
            conn.rollback()
            raise


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='数据库迁移脚本')
    parser.add_argument('action', choices=['upgrade', 'downgrade'], help='执行升级或回滚')
    
    args = parser.parse_args()
    
    if args.action == 'upgrade':
        upgrade()
    else:
        downgrade()

