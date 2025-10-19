<template>
	<view class="lottery-page">
		<!-- 头部说明 -->
		<view class="lottery-header">
			<text class="title">下单抽奖</text>
			<text class="subtitle">每次下单即可参与抽奖</text>
			<view class="chances-info">
				<text class="label">剩余抽奖次数：</text>
				<text class="count">{{ chances }}</text>
			</view>
		</view>
		
		<!-- 抽奖转盘 -->
		<view class="lottery-wheel">
			<view class="wheel-container">
				<text class="wheel-icon">🎰</text>
				<text class="wheel-text">转盘抽奖</text>
				<text class="wheel-tip">（功能开发中）</text>
			</view>
			<button class="start-btn" @click="startLottery" :disabled="chances === 0">
				{{ chances === 0 ? '暂无抽奖次数' : '开始抽奖' }}
			</button>
		</view>
		
		<!-- 奖品列表 -->
		<view class="prizes-section">
			<view class="section-title">奖品列表</view>
			<view class="prizes-grid">
				<view v-for="(item, index) in prizesList" :key="index" class="prize-item">
					<text class="prize-icon">{{ item.icon }}</text>
					<text class="prize-name">{{ item.name }}</text>
					<text class="prize-prob">{{ item.probability }}</text>
				</view>
			</view>
		</view>
		
		<!-- 中奖记录 -->
		<view class="records-section">
			<view class="section-header">
				<text class="section-title">最近中奖</text>
				<text class="view-all" @click="viewAllPrizes">查看全部 ›</text>
			</view>
			<view v-if="recentPrizes.length > 0" class="records-list">
				<view v-for="(item, index) in recentPrizes" :key="index" class="record-item">
					<text class="record-user">{{ item.user }}</text>
					<text class="record-prize">{{ item.prize }}</text>
					<text class="record-time">{{ item.time }}</text>
				</view>
			</view>
			<view v-else class="empty-tip">
				暂无中奖记录
			</view>
		</view>
	</view>
</template>

<script>
export default {
	data() {
		return {
			chances: 0,
			prizesList: [
				{ icon: '🎁', name: '5元优惠券', probability: '30%' },
				{ icon: '💰', name: '10元现金红包', probability: '20%' },
				{ icon: '🎫', name: '20元优惠券', probability: '15%' },
				{ icon: '💎', name: '50元现金红包', probability: '10%' },
				{ icon: '🏆', name: '100元优惠券', probability: '5%' },
				{ icon: '⭐', name: '免费检测券', probability: '20%' }
			],
			recentPrizes: []
		}
	},
	
	onLoad() {
		this.loadData()
	},
	
	methods: {
		// 加载数据
		async loadData() {
			try {
				// TODO: 调用API获取抽奖次数和记录
				this.chances = 0
				this.recentPrizes = []
			} catch (error) {
				console.error('加载抽奖数据失败', error)
			}
		},
		
		// 开始抽奖
		startLottery() {
			if (this.chances === 0) {
				uni.showToast({
					title: '暂无抽奖次数',
					icon: 'none'
				})
				return
			}
			
			uni.showToast({
				title: '抽奖功能开发中',
				icon: 'none'
			})
		},
		
		// 查看全部中奖记录
		viewAllPrizes() {
			uni.navigateTo({
				url: '/pagesA/prize/prize'
			})
		}
	}
}
</script>

<style lang="scss" scoped>
.lottery-page {
	min-height: 100vh;
	background: linear-gradient(180deg, #fff5f5 0%, #f5f5f5 100%);
	padding-bottom: 40rpx;
}

.lottery-header {
	padding: 60rpx 30rpx 40rpx;
	text-align: center;
	
	.title {
		font-size: 48rpx;
		font-weight: bold;
		color: #333;
		display: block;
		margin-bottom: 20rpx;
	}
	
	.subtitle {
		font-size: 26rpx;
		color: #999;
		display: block;
		margin-bottom: 40rpx;
	}
	
	.chances-info {
		background: white;
		display: inline-flex;
		align-items: center;
		padding: 20rpx 40rpx;
		border-radius: 50rpx;
		box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.1);
		
		.label {
			font-size: 26rpx;
			color: #666;
		}
		
		.count {
			font-size: 36rpx;
			font-weight: bold;
			color: #f5576c;
		}
	}
}

.lottery-wheel {
	margin: 0 30rpx 40rpx;
	background: white;
	border-radius: 16rpx;
	padding: 60rpx 30rpx;
	text-align: center;
	
	.wheel-container {
		margin-bottom: 40rpx;
		
		.wheel-icon {
			font-size: 120rpx;
			display: block;
			margin-bottom: 20rpx;
		}
		
		.wheel-text {
			font-size: 32rpx;
			font-weight: bold;
			color: #333;
			display: block;
			margin-bottom: 10rpx;
		}
		
		.wheel-tip {
			font-size: 24rpx;
			color: #999;
			display: block;
		}
	}
	
	.start-btn {
		background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
		color: white;
		border: none;
		border-radius: 50rpx;
		padding: 30rpx 80rpx;
		font-size: 32rpx;
		font-weight: bold;
		
		&[disabled] {
			opacity: 0.5;
		}
	}
}

.prizes-section {
	background: white;
	margin: 0 30rpx 40rpx;
	border-radius: 16rpx;
	padding: 30rpx;
	
	.section-title {
		font-size: 32rpx;
		font-weight: bold;
		color: #333;
		margin-bottom: 30rpx;
	}
	
	.prizes-grid {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 20rpx;
		
		.prize-item {
			display: flex;
			flex-direction: column;
			align-items: center;
			padding: 30rpx 20rpx;
			background: #f5f5f5;
			border-radius: 12rpx;
			
			.prize-icon {
				font-size: 50rpx;
				margin-bottom: 15rpx;
			}
			
			.prize-name {
				font-size: 24rpx;
				color: #333;
				margin-bottom: 10rpx;
				text-align: center;
			}
			
			.prize-prob {
				font-size: 22rpx;
				color: #f5576c;
			}
		}
	}
}

.records-section {
	background: white;
	margin: 0 30rpx;
	border-radius: 16rpx;
	padding: 30rpx;
	
	.section-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 30rpx;
		
		.section-title {
			font-size: 32rpx;
			font-weight: bold;
			color: #333;
		}
		
		.view-all {
			font-size: 26rpx;
			color: #667eea;
		}
	}
	
	.records-list {
		.record-item {
			display: flex;
			justify-content: space-between;
			align-items: center;
			padding: 20rpx 0;
			border-bottom: 1rpx solid #f5f5f5;
			font-size: 24rpx;
			
			&:last-child {
				border-bottom: none;
			}
			
			.record-user {
				flex: 1;
				color: #333;
			}
			
			.record-prize {
				flex: 1;
				text-align: center;
				color: #f5576c;
			}
			
			.record-time {
				flex: 1;
				text-align: right;
				color: #999;
			}
		}
	}
	
	.empty-tip {
		text-align: center;
		padding: 60rpx 0;
		font-size: 26rpx;
		color: #999;
	}
}
</style>

