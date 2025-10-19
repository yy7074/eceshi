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
		
		<!-- 记录列表 -->
		<view class="records-section">
			<view class="section-title">预付记录</view>
			
			<view v-if="records.length > 0" class="records-list">
				<view v-for="(item, index) in records" :key="index" class="record-item">
					<view class="record-left">
						<text class="record-title">{{ item.title }}</text>
						<text class="record-time">{{ item.time }}</text>
					</view>
					<view class="record-right">
						<text :class="['record-amount', item.type === 'in' ? 'income' : 'expense']">
							{{ item.type === 'in' ? '+' : '-' }}{{ item.amount.toFixed(2) }}
						</text>
						<text class="record-status">{{ item.statusText }}</text>
					</view>
				</view>
			</view>
			
			<!-- 空状态 -->
			<view v-else class="empty-state">
				<text class="empty-icon">📊</text>
				<text class="empty-text">暂无预付记录</text>
			</view>
		</view>
	</view>
</template>

<script>
export default {
	data() {
		return {
			totalPrepay: 0,
			usedPrepay: 0,
			remainPrepay: 0,
			records: []
		}
	},
	
	onLoad() {
		this.loadData()
	},
	
	methods: {
		// 加载数据
		async loadData() {
			try {
				// TODO: 调用API获取预付记录
				this.totalPrepay = 0
				this.usedPrepay = 0
				this.remainPrepay = 0
				this.records = []
			} catch (error) {
				console.error('加载预付记录失败', error)
			}
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

.records-section {
	background: white;
	margin: 20rpx 30rpx;
	border-radius: 16rpx;
	padding: 30rpx;
	
	.section-title {
		font-size: 32rpx;
		font-weight: bold;
		color: #333;
		margin-bottom: 30rpx;
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
			
			.record-left {
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
					color: #999;
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
	}
}
</style>

