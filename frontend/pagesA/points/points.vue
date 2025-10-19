<template>
	<view class="points-page">
		<!-- 积分卡片 -->
		<view class="points-card">
			<view class="points-header">
				<text class="title">我的积分</text>
			</view>
			<view class="points-value">
				<text class="number">{{ points }}</text>
				<text class="unit">分</text>
			</view>
			<view class="points-actions">
				<button class="btn-exchange" @click="goExchange">积分兑换</button>
				<button class="btn-rules" @click="showRules">积分规则</button>
			</view>
		</view>
		
		<!-- 积分记录 -->
		<view class="records-section">
			<view class="section-title">积分记录</view>
			<view v-if="records.length > 0" class="records-list">
				<view class="record-item" v-for="item in records" :key="item.id">
					<view class="record-info">
						<text class="record-title">{{ item.title }}</text>
						<text class="record-time">{{ item.time }}</text>
					</view>
					<text class="record-points" :class="item.type === 'add' ? 'add' : 'sub'">
						{{ item.type === 'add' ? '+' : '-' }}{{ item.points }}
					</text>
				</view>
			</view>
			<view v-else class="empty-state">
				<text class="empty-icon">📊</text>
				<text class="empty-text">暂无积分记录</text>
			</view>
		</view>
	</view>
</template>

<script>
export default {
	data() {
		return {
			points: 0,
			records: []
		}
	},
	onLoad() {
		this.loadPoints()
	},
	methods: {
		async loadPoints() {
			// TODO: 从API加载积分数据
			this.points = 0
			this.records = []
		},
		goExchange() {
			uni.showToast({
				title: '积分兑换功能开发中',
				icon: 'none'
			})
		},
		showRules() {
			uni.showModal({
				title: '积分规则',
				content: '1. 完成订单获得积分\n2. 邀请好友获得积分\n3. 每日签到获得积分\n4. 积分可用于兑换优惠券',
				showCancel: false
			})
		}
	}
}
</script>

<style lang="scss" scoped>
.points-page {
	min-height: 100vh;
	background: #f5f5f5;
	padding-bottom: 40rpx;
}

.points-card {
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	margin: 20rpx;
	padding: 60rpx 40rpx;
	border-radius: 16rpx;
	
	.points-header {
		margin-bottom: 30rpx;
		
		.title {
			font-size: 28rpx;
			color: rgba(255, 255, 255, 0.9);
		}
	}
	
	.points-value {
		display: flex;
		align-items: baseline;
		margin-bottom: 40rpx;
		
		.number {
			font-size: 80rpx;
			font-weight: bold;
			color: white;
			margin-right: 10rpx;
		}
		
		.unit {
			font-size: 32rpx;
			color: rgba(255, 255, 255, 0.9);
		}
	}
	
	.points-actions {
		display: flex;
		gap: 20rpx;
		
		.btn-exchange,
		.btn-rules {
			flex: 1;
			height: 70rpx;
			line-height: 70rpx;
			text-align: center;
			border-radius: 35rpx;
			font-size: 28rpx;
			border: none;
			
			&::after {
				border: none;
			}
		}
		
		.btn-exchange {
			background: white;
			color: #667eea;
		}
		
		.btn-rules {
			background: rgba(255, 255, 255, 0.2);
			color: white;
		}
	}
}

.records-section {
	background: white;
	margin: 20rpx;
	padding: 30rpx;
	border-radius: 16rpx;
	
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
			padding: 25rpx 0;
			border-bottom: 1rpx solid #f0f0f0;
			
			&:last-child {
				border-bottom: none;
			}
			
			.record-info {
				flex: 1;
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
			
			.record-points {
				font-size: 32rpx;
				font-weight: bold;
				
				&.add {
					color: #4caf50;
				}
				
				&.sub {
					color: #ff6b6b;
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
			font-size: 80rpx;
			margin-bottom: 20rpx;
		}
		
		.empty-text {
			font-size: 26rpx;
			color: #999;
		}
	}
}
</style>

