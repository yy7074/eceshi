#!/usr/bin/env python3
"""
手动完成充值订单
用于微信回调未到达时手动更新余额
"""
import sys
from sqlalchemy.orm import Session
from decimal import Decimal
from datetime import datetime

# 添加项目路径
sys.path.insert(0, '/Users/yy/Documents/GitHub/eceshi/backend')

from app.core.database import SessionLocal
from app.models.recharge import RechargeRecord, RechargeStatus
from app.models.user import User

def complete_recharge(recharge_no: str):
    """完成指定的充值订单"""
    db: Session = SessionLocal()
    
    try:
        # 查询充值记录
        recharge = db.query(RechargeRecord).filter(
            RechargeRecord.recharge_no == recharge_no
        ).first()
        
        if not recharge:
            print(f"❌ 充值记录不存在: {recharge_no}")
            return False
        
        # 检查状态
        if recharge.status == RechargeStatus.SUCCESS:
            print(f"✅ 该充值订单已经完成")
            print(f"   充值金额: {recharge.amount}元")
            print(f"   实际到账: {recharge.actual_amount}元")
            return True
        
        # 查询用户
        user = db.query(User).filter(User.id == recharge.user_id).first()
        
        if not user:
            print(f"❌ 用户不存在: {recharge.user_id}")
            return False
        
        print(f"\n📋 充值信息:")
        print(f"   用户ID: {user.id}")
        print(f"   用户昵称: {user.nickname}")
        print(f"   充值单号: {recharge.recharge_no}")
        print(f"   充值金额: {recharge.amount}元")
        print(f"   赠送金额: {recharge.bonus_amount}元")
        print(f"   实际到账: {recharge.actual_amount}元")
        print(f"   当前余额: {user.prepaid_balance or 0}元")
        
        # 计算新余额
        old_balance = user.prepaid_balance or Decimal("0")
        new_balance = old_balance + recharge.actual_amount
        
        print(f"\n💰 余额变化:")
        print(f"   原余额: {old_balance}元")
        print(f"   新余额: {new_balance}元")
        
        # 确认
        confirm = input("\n确认完成充值？(y/n): ")
        if confirm.lower() != 'y':
            print("❌ 已取消")
            return False
        
        # 更新用户余额
        user.prepaid_balance = new_balance
        
        # 更新充值记录
        recharge.status = RechargeStatus.SUCCESS
        recharge.transaction_id = "MANUAL_" + datetime.now().strftime("%Y%m%d%H%M%S")
        recharge.paid_at = datetime.now()
        recharge.completed_at = datetime.now()
        recharge.remark = "手动完成"
        
        db.commit()
        
        print(f"\n✅ 充值完成！")
        print(f"   用户余额已更新: {old_balance}元 → {new_balance}元")
        
        return True
        
    except Exception as e:
        print(f"❌ 处理失败: {str(e)}")
        db.rollback()
        return False
    finally:
        db.close()

def list_pending_recharges():
    """列出所有待处理的充值订单"""
    db: Session = SessionLocal()
    
    try:
        recharges = db.query(RechargeRecord).filter(
            RechargeRecord.status == RechargeStatus.PENDING
        ).order_by(RechargeRecord.created_at.desc()).limit(20).all()
        
        if not recharges:
            print("✅ 没有待处理的充值订单")
            return
        
        print(f"\n📋 待处理充值订单 (最近20条):\n")
        print(f"{'序号':<4} {'充值单号':<25} {'用户ID':<8} {'金额':<10} {'实际到账':<10} {'创建时间'}")
        print("-" * 85)
        
        for idx, r in enumerate(recharges, 1):
            created_time = r.created_at.strftime("%m-%d %H:%M")
            print(f"{idx:<4} {r.recharge_no:<25} {r.user_id:<8} {float(r.amount):<10.2f} {float(r.actual_amount):<10.2f} {created_time}")
        
        print("")
        
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 60)
    print("手动完成充值订单工具")
    print("=" * 60)
    
    # 列出待处理订单
    list_pending_recharges()
    
    # 提示输入
    if len(sys.argv) > 1:
        recharge_no = sys.argv[1]
    else:
        recharge_no = input("\n请输入充值单号 (RC开头): ").strip()
    
    if not recharge_no:
        print("❌ 未输入充值单号")
        sys.exit(1)
    
    # 完成充值
    complete_recharge(recharge_no)

