<template>
	<view class="prize-page">
		<!-- 头部统计 -->
		<view class="header-banner">
			<text class="total-text">我的中奖次数</text>
			<text class="total-count">{{ totalPrizes }}</text>
			<text class="total-tip">累计中奖金额：¥{{ totalAmount.toFixed(2) }}</text>
		</view>
		
		<!-- 中奖记录 -->
		<view class="prizes-section">
			<view class="section-title">中奖记录</view>
			
			<view v-if="prizes.length > 0" class="prizes-list">
				<view v-for="(item, index) in prizes" :key="index" class="prize-item">
					<view class="prize-icon">{{ item.icon }}</view>
					<view class="prize-info">
						<text class="prize-name">{{ item.name }}</text>
						<text class="prize-time">{{ item.time }}</text>
					</view>
					<view class="prize-action">
						<text v-if="item.status === 'unclaimed'" class="claim-btn" @click="claimPrize(item)">立即领取</text>
						<text v-else class="claimed-text">已领取</text>
					</view>
				</view>
			</view>
			
			<!-- 空状态 -->
			<view v-else class="empty-state">
				<text class="empty-icon">🎁</text>
				<text class="empty-text">暂无中奖记录</text>
				<button class="lottery-btn" @click="goLottery">去抽奖</button>
			</view>
		</view>
	</view>
</template>

<script>
export default {
	data() {
		return {
			totalPrizes: 0,
			totalAmount: 0,
			prizes: []
		}
	},
	
	onLoad() {
		this.loadPrizes()
	},
	
	methods: {
		// 加载中奖记录
		async loadPrizes() {
			try {
				// TODO: 调用API获取中奖记录
				this.totalPrizes = 0
				this.totalAmount = 0
				this.prizes = []
			} catch (error) {
				console.error('加载中奖记录失败', error)
			}
		},
		
		// 领取奖品
		claimPrize(item) {
			uni.showModal({
				title: '领取奖品',
				content: '确认领取该奖品吗？',
				success: (res) => {
					if (res.confirm) {
						uni.showToast({
							title: '领取功能开发中',
							icon: 'none'
						})
					}
				}
			})
		},
		
		// 去抽奖
		goLottery() {
			uni.navigateTo({
				url: '/pagesA/lottery/lottery'
			})
		}
	}
}
</script>

<style lang="scss" scoped>
.prize-page {
	min-height: 100vh;
	background: #f5f5f5;
}

.header-banner {
	background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
	padding: 60rpx 30rpx;
	display: flex;
	flex-direction: column;
	align-items: center;
	color: white;
	
	.total-text {
		font-size: 28rpx;
		opacity: 0.9;
		margin-bottom: 20rpx;
	}
	
	.total-count {
		font-size: 80rpx;
		font-weight: bold;
		margin-bottom: 20rpx;
	}
	
	.total-tip {
		font-size: 26rpx;
		opacity: 0.9;
	}
}

.prizes-section {
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
	
	.prizes-list {
		.prize-item {
			display: flex;
			align-items: center;
			padding: 30rpx 0;
			border-bottom: 1rpx solid #f5f5f5;
			
			&:last-child {
				border-bottom: none;
			}
			
			.prize-icon {
				font-size: 60rpx;
				margin-right: 20rpx;
			}
			
			.prize-info {
				flex: 1;
				display: flex;
				flex-direction: column;
				
				.prize-name {
					font-size: 28rpx;
					color: #333;
					margin-bottom: 10rpx;
				}
				
				.prize-time {
					font-size: 24rpx;
					color: #999;
				}
			}
			
			.prize-action {
				.claim-btn {
					padding: 10rpx 30rpx;
					background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
					color: white;
					border-radius: 50rpx;
					font-size: 24rpx;
				}
				
				.claimed-text {
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
		margin-bottom: 40rpx;
	}
	
	.lottery-btn {
		background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
		color: white;
		border: none;
		border-radius: 50rpx;
		padding: 25rpx 60rpx;
		font-size: 28rpx;
	}
}
</style>

