<template>
	<view class="wallet-page">
		<!-- 头部背景 -->
		<view class="header-bg">
			<view class="balance-info">
				<text class="label">钱包余额（元）</text>
				<text class="amount">{{ balance.toFixed(2) }}</text>
			</view>
		</view>
		
		<!-- 快捷操作 -->
		<view class="quick-actions">
			<view class="action-item" @click="handleRecharge">
				<text class="action-icon">💰</text>
				<text class="action-text">充值</text>
			</view>
			<view class="action-item" @click="handleWithdraw">
				<text class="action-icon">💸</text>
				<text class="action-text">提现</text>
			</view>
			<view class="action-item" @click="handleTransfer">
				<text class="action-icon">🔄</text>
				<text class="action-text">转账</text>
			</view>
		</view>
		
		<!-- 账单记录 -->
		<view class="records-section">
			<view class="section-title">
				<text>账单记录</text>
			</view>
			
			<!-- Tab切换 -->
			<view class="tabs">
				<view 
					v-for="(tab, index) in tabs" 
					:key="index"
					:class="['tab-item', currentTab === index ? 'active' : '']"
					@click="switchTab(index)"
				>
					{{ tab }}
				</view>
			</view>
			
			<!-- 记录列表 -->
			<view v-if="records.length > 0" class="records-list">
				<view v-for="(item, index) in records" :key="index" class="record-item">
					<view class="record-info">
						<text class="record-type">{{ item.type }}</text>
						<text class="record-time">{{ item.time }}</text>
					</view>
					<text :class="['record-amount', item.income ? 'income' : 'expense']">
						{{ item.income ? '+' : '-' }}{{ item.amount.toFixed(2) }}
					</text>
				</view>
			</view>
			
			<!-- 空状态 -->
			<view v-else class="empty-state">
				<text class="empty-icon">📝</text>
				<text class="empty-text">暂无账单记录</text>
			</view>
		</view>
	</view>
</template>

<script>
import api from '@/utils/api.js'

export default {
	data() {
		return {
			balance: 0,
			currentTab: 0,
			tabs: ['全部', '收入', '支出'],
			records: [],
			page: 1,
			pageSize: 20,
			hasMore: true
		}
	},
	
	onLoad() {
		this.loadWalletInfo()
		this.loadRecords()
	},
	
	onPullDownRefresh() {
		this.page = 1
		this.records = []
		this.loadWalletInfo()
		this.loadRecords().then(() => {
			uni.stopPullDownRefresh()
		})
	},
	
	onReachBottom() {
		if (this.hasMore) {
			this.page++
			this.loadRecords()
		}
	},
	
	methods: {
		// 加载钱包信息
		async loadWalletInfo() {
			try {
				const res = await api.getBalance()
				this.balance = res.data.prepaid_balance || 0
			} catch (error) {
				console.error('加载钱包信息失败', error)
				this.balance = 0
			}
		},
		
		// 加载账单记录
		async loadRecords() {
			try {
				// 获取充值记录
				const res = await api.getRechargeRecords({
					page: this.page,
					page_size: this.pageSize
				})
				
				if (res.data && res.data.items) {
					const newRecords = res.data.items.map(item => ({
						type: this.getRecordType(item),
						time: this.formatTime(item.created_at),
						amount: parseFloat(item.actual_amount || item.amount),
						income: true, // 充值都是收入
						status: item.status,
						raw: item
					}))
					
					if (this.page === 1) {
						this.records = newRecords
					} else {
						this.records.push(...newRecords)
					}
					
					this.hasMore = this.records.length < res.data.total
				}
				
				// 根据当前tab过滤记录
				this.filterRecords()
				
			} catch (error) {
				console.error('加载账单失败', error)
			}
		},
		
		// 获取记录类型文本
		getRecordType(item) {
			const statusMap = {
				'pending': '充值中',
				'success': '充值成功',
				'failed': '充值失败',
				'refunded': '已退款'
			}
			return statusMap[item.status] || '钱包充值'
		},
		
		// 格式化时间
		formatTime(timeStr) {
			if (!timeStr) return ''
			const date = new Date(timeStr)
			const year = date.getFullYear()
			const month = String(date.getMonth() + 1).padStart(2, '0')
			const day = String(date.getDate()).padStart(2, '0')
			const hour = String(date.getHours()).padStart(2, '0')
			const minute = String(date.getMinutes()).padStart(2, '0')
			return `${year}-${month}-${day} ${hour}:${minute}`
		},
		
		// 过滤记录
		filterRecords() {
			// 0: 全部, 1: 收入, 2: 支出
			// 目前只有充值记录（收入），所以不需要特殊过滤
			// 如果以后有支出记录，这里可以添加过滤逻辑
		},
		
		// 切换Tab
		switchTab(index) {
			this.currentTab = index
			this.page = 1
			this.records = []
			this.loadRecords()
		},
		
		// 充值
		handleRecharge() {
			uni.navigateTo({
				url: '/pagesA/recharge/recharge'
			})
		},
		
		// 提现
		handleWithdraw() {
			uni.showModal({
				title: '提现说明',
				content: '钱包余额暂不支持提现，可用于支付订单费用',
				showCancel: false
			})
		},
		
		// 转账
		handleTransfer() {
			uni.showModal({
				title: '转账说明',
				content: '转账功能即将上线，敬请期待',
				showCancel: false
			})
		}
	}
}
</script>

<style lang="scss" scoped>
.wallet-page {
	min-height: 100vh;
	background: #f5f5f5;
}

.header-bg {
	background: #1890ff;
	padding: 60rpx 30rpx 80rpx;
	
	.balance-info {
		display: flex;
		flex-direction: column;
		align-items: center;
		color: white;
		
		.label {
			font-size: 28rpx;
			margin-bottom: 20rpx;
			opacity: 0.9;
		}
		
		.amount {
			font-size: 60rpx;
			font-weight: bold;
		}
	}
}

.quick-actions {
	display: flex;
	justify-content: space-around;
	background: white;
	margin: -40rpx 30rpx 20rpx;
	border-radius: 16rpx;
	padding: 40rpx 0;
	box-shadow: 0 2rpx 20rpx rgba(0, 0, 0, 0.05);
	
	.action-item {
		display: flex;
		flex-direction: column;
		align-items: center;
		
		.action-icon {
			font-size: 50rpx;
			margin-bottom: 15rpx;
		}
		
		.action-text {
			font-size: 26rpx;
			color: #666;
		}
	}
}

.records-section {
	background: white;
	margin: 0 30rpx;
	border-radius: 16rpx;
	padding: 30rpx;
	
	.section-title {
		font-size: 32rpx;
		font-weight: bold;
		color: #333;
		margin-bottom: 30rpx;
	}
	
	.tabs {
		display: flex;
		border-bottom: 1rpx solid #eee;
		margin-bottom: 30rpx;
		
		.tab-item {
			flex: 1;
			text-align: center;
			padding: 20rpx 0;
			font-size: 28rpx;
			color: #666;
			position: relative;
			
			&.active {
				color: #667eea;
				font-weight: bold;
				
				&::after {
					content: '';
					position: absolute;
					bottom: 0;
					left: 50%;
					transform: translateX(-50%);
					width: 60rpx;
					height: 4rpx;
					background: #667eea;
					border-radius: 2rpx;
				}
			}
		}
	}
	
	.records-list {
		.record-item {
			display: flex;
			justify-content: space-between;
			align-items: center;
			padding: 30rpx 0;
			border-bottom: 1rpx solid #f5f5f5;
			
			&:last-child {
				border-bottom: none;
			}
			
			.record-info {
				display: flex;
				flex-direction: column;
				
				.record-type {
					font-size: 28rpx;
					color: #333;
					margin-bottom: 10rpx;
				}
				
				.record-time {
					font-size: 24rpx;
					color: #999;
				}
			}
			
			.record-amount {
				font-size: 32rpx;
				font-weight: bold;
				
				&.income {
					color: #51cf66;
				}
				
				&.expense {
					color: #ff6b6b;
				}
			}
		}
	}
}

.empty-state {
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: 80rpx 0;
	
	.empty-icon {
		font-size: 100rpx;
		margin-bottom: 20rpx;
		opacity: 0.5;
	}
	
	.empty-text {
		font-size: 28rpx;
		color: #999;
	}
}
</style>

