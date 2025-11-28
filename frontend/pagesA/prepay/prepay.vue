<template>
	<view class="prepay-page">
		<!-- 头部统计 -->
		<view class="header-stats">
			<view class="stat-item">
				<text class="stat-value">{{ totalPrepay.toFixed(2) }}</text>
				<text class="stat-label">累计预付（元）</text>
			</view>
			<view class="stat-item">
				<text class="stat-value">{{ usedPrepay.toFixed(2) }}</text>
				<text class="stat-label">已使用（元）</text>
			</view>
			<view class="stat-item">
				<text class="stat-value">{{ remainPrepay.toFixed(2) }}</text>
				<text class="stat-label">剩余（元）</text>
			</view>
		</view>
		
		<!-- Tab筛选 -->
		<view class="filter-tabs">
			<view :class="['filter-item', recordType === '' ? 'active' : '']" @click="switchType('')">全部</view>
			<view :class="['filter-item', recordType === 'recharge' ? 'active' : '']" @click="switchType('recharge')">充值</view>
			<view :class="['filter-item', recordType === 'consume' ? 'active' : '']" @click="switchType('consume')">消费</view>
		</view>
		
		<!-- 记录列表 -->
		<view class="records-section">
			<view v-if="records.length > 0" class="records-list">
				<view v-for="(item, index) in records" :key="index" class="record-item">
					<view class="record-left">
						<view class="record-icon" :class="item.type">
							{{ item.type === 'in' ? '💰' : '💳' }}
						</view>
						<view class="record-info">
							<text class="record-title">{{ item.title }}</text>
							<text class="record-time">{{ item.time }}</text>
						</view>
					</view>
					<view class="record-right">
						<text :class="['record-amount', item.type === 'in' ? 'income' : 'expense']">
							{{ item.type === 'in' ? '+' : '-' }}{{ item.amount.toFixed(2) }}
						</text>
						<text class="record-status">{{ item.status_text }}</text>
					</view>
				</view>
			</view>
			
			<!-- 空状态 -->
			<view v-else class="empty-state">
				<text class="empty-icon">📊</text>
				<text class="empty-text">暂无预付记录</text>
				<button class="recharge-btn" @click="goRecharge">去充值</button>
			</view>
		</view>
		
		<!-- 加载更多 -->
		<view v-if="records.length > 0 && hasMore" class="load-more" @click="loadMore">
			<text>{{ loading ? '加载中...' : '加载更多' }}</text>
		</view>
	</view>
</template>

<script>
import api from '@/utils/api.js'

export default {
	data() {
		return {
			totalPrepay: 0,
			usedPrepay: 0,
			remainPrepay: 0,
			recordType: '',
			records: [],
			page: 1,
			pageSize: 20,
			hasMore: true,
			loading: false
		}
	},
	
	onLoad() {
		this.loadData()
	},
	
	onPullDownRefresh() {
		this.page = 1
		this.records = []
		this.hasMore = true
		this.loadData().finally(() => {
			uni.stopPullDownRefresh()
		})
	},
	
	onReachBottom() {
		if (this.hasMore && !this.loading) {
			this.loadMore()
		}
	},
	
	methods: {
		// 加载数据
		async loadData() {
			await Promise.all([
				this.loadStats(),
				this.loadRecords()
			])
		},
		
		// 加载统计数据
		async loadStats() {
			try {
				const res = await api.getPrepayStats()
				this.totalPrepay = res.data.total_prepay || 0
				this.usedPrepay = res.data.used_prepay || 0
				this.remainPrepay = res.data.remain_prepay || 0
			} catch (error) {
				console.error('加载预付统计失败', error)
			}
		},
		
		// 加载记录
		async loadRecords() {
			this.loading = true
			try {
				const res = await api.getPrepayRecords({
					record_type: this.recordType || undefined,
					page: this.page,
					page_size: this.pageSize
				})
				
				const items = res.data.items || []
				
				if (this.page === 1) {
					this.records = items
				} else {
					this.records = [...this.records, ...items]
				}
				
				this.hasMore = items.length >= this.pageSize
				
			} catch (error) {
				console.error('加载预付记录失败', error)
			} finally {
				this.loading = false
			}
		},
		
		// 切换类型
		switchType(type) {
			this.recordType = type
			this.page = 1
			this.records = []
			this.hasMore = true
			this.loadRecords()
		},
		
		// 加载更多
		loadMore() {
			this.page++
			this.loadRecords()
		},
		
		// 去充值
		goRecharge() {
			uni.navigateTo({
				url: '/pagesA/recharge/recharge'
			})
		}
	}
}
</script>

<style lang="scss" scoped>
.prepay-page {
	min-height: 100vh;
	background: #f5f5f5;
}

.header-stats {
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	padding: 60rpx 30rpx;
	display: flex;
	justify-content: space-around;
	
	.stat-item {
		display: flex;
		flex-direction: column;
		align-items: center;
		color: white;
		
		.stat-value {
			font-size: 40rpx;
			font-weight: bold;
			margin-bottom: 10rpx;
		}
		
		.stat-label {
			font-size: 24rpx;
			opacity: 0.9;
		}
	}
}

.filter-tabs {
	display: flex;
	background: white;
	padding: 20rpx 30rpx;
	gap: 20rpx;
	
	.filter-item {
		padding: 15rpx 30rpx;
		background: #f5f5f5;
		border-radius: 50rpx;
		font-size: 26rpx;
		color: #666;
		
		&.active {
			background: #667eea;
			color: white;
		}
	}
}

.records-section {
	background: white;
	margin: 20rpx 30rpx;
	border-radius: 16rpx;
	padding: 30rpx;
	
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
			
			.record-left {
				display: flex;
				align-items: center;
				flex: 1;
				
				.record-icon {
					width: 80rpx;
					height: 80rpx;
					border-radius: 50%;
					display: flex;
					align-items: center;
					justify-content: center;
					font-size: 36rpx;
					margin-right: 20rpx;
					
					&.in {
						background: #fff3e0;
					}
					
					&.out {
						background: #e8f5e9;
					}
				}
				
				.record-info {
					display: flex;
					flex-direction: column;
					
					.record-title {
						font-size: 28rpx;
						color: #333;
						margin-bottom: 10rpx;
					}
					
					.record-time {
						font-size: 24rpx;
						color: #999;
					}
				}
			}
			
			.record-right {
				display: flex;
				flex-direction: column;
				align-items: flex-end;
				
				.record-amount {
					font-size: 32rpx;
					font-weight: bold;
					margin-bottom: 10rpx;
					
					&.income {
						color: #ff6b6b;
					}
					
					&.expense {
						color: #51cf66;
					}
				}
				
				.record-status {
					font-size: 24rpx;
					color: #52c41a;
				}
			}
		}
	}
}

.empty-state {
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: 100rpx 0;
	
	.empty-icon {
		font-size: 120rpx;
		margin-bottom: 30rpx;
		opacity: 0.5;
	}
	
	.empty-text {
		font-size: 28rpx;
		color: #999;
		margin-bottom: 40rpx;
	}
	
	.recharge-btn {
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		color: white;
		border: none;
		border-radius: 50rpx;
		padding: 25rpx 60rpx;
		font-size: 28rpx;
	}
}

.load-more {
	text-align: center;
	padding: 30rpx;
	font-size: 26rpx;
	color: #999;
}
</style>
