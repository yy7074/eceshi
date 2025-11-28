<template>
	<view class="lottery-page">
		<!-- 头部说明 -->
		<view class="lottery-header">
			<text class="title">🎰 下单抽奖</text>
			<text class="subtitle">每次下单即可参与抽奖</text>
			<view class="chances-info">
				<text class="label">剩余抽奖次数：</text>
				<text class="count">{{ chances }}</text>
			</view>
		</view>
		
		<!-- 抽奖转盘 -->
		<view class="lottery-wheel">
			<view class="wheel-container" :class="{ spinning: isSpinning }">
				<view class="wheel-center">
					<text class="wheel-icon">🎁</text>
				</view>
				<view class="wheel-prizes">
					<view v-for="(prize, index) in prizesList" :key="index" 
						:class="['prize-sector', { active: selectedPrizeIndex === index }]"
						:style="{ transform: `rotate(${index * 60}deg)` }">
						<text class="prize-icon">{{ prize.icon }}</text>
					</view>
				</view>
			</view>
			<button class="start-btn" @click="startLottery" :disabled="chances === 0 || isSpinning">
				{{ isSpinning ? '抽奖中...' : (chances === 0 ? '暂无抽奖次数' : '开始抽奖') }}
			</button>
		</view>
		
		<!-- 奖品列表 -->
		<view class="prizes-section">
			<view class="section-title">🎁 奖品列表</view>
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
				<text class="section-title">🏆 最近中奖</text>
				<text class="view-all" @click="viewAllPrizes">查看全部 ›</text>
			</view>
			<view v-if="recentPrizes.length > 0" class="records-list">
				<view v-for="(item, index) in recentPrizes" :key="index" class="record-item">
					<text class="record-user">{{ item.user }}</text>
					<text class="record-prize">{{ item.icon }} {{ item.prize }}</text>
					<text class="record-time">{{ item.time }}</text>
				</view>
			</view>
			<view v-else class="empty-tip">
				暂无中奖记录
			</view>
		</view>
		
		<!-- 中奖弹窗 -->
		<uni-popup ref="resultPopup" type="center">
			<view class="result-popup">
				<view class="result-icon">{{ prizeResult.icon || '🎉' }}</view>
				<view class="result-title">恭喜您获得</view>
				<view class="result-prize">{{ prizeResult.name }}</view>
				<button v-if="prizeResult.need_claim" class="claim-btn" @click="claimPrize">立即领取</button>
				<button v-else class="close-btn" @click="closeResultPopup">知道了</button>
			</view>
		</uni-popup>
	</view>
</template>

<script>
import api from '@/utils/api.js'

export default {
	data() {
		return {
			chances: 0,
			isSpinning: false,
			selectedPrizeIndex: -1,
			prizesList: [
				{ icon: '🎁', name: '5元优惠券', probability: '30%' },
				{ icon: '💰', name: '10元现金', probability: '20%' },
				{ icon: '🎫', name: '20元优惠券', probability: '15%' },
				{ icon: '💎', name: '50元现金', probability: '10%' },
				{ icon: '🏆', name: '100元优惠券', probability: '5%' },
				{ icon: '⭐', name: '谢谢参与', probability: '20%' }
			],
			recentPrizes: [],
			prizeResult: {}
		}
	},
	
	onLoad() {
		this.loadData()
	},
	
	onPullDownRefresh() {
		this.loadData().finally(() => {
			uni.stopPullDownRefresh()
		})
	},
	
	methods: {
		// 加载数据
		async loadData() {
			await Promise.all([
				this.loadChances(),
				this.loadPrizes(),
				this.loadRecentRecords()
			])
		},
		
		// 获取抽奖次数
		async loadChances() {
			try {
				const res = await api.getLotteryChances()
				this.chances = res.data.chances || 0
			} catch (error) {
				console.error('获取抽奖次数失败', error)
			}
		},
		
		// 获取奖品列表
		async loadPrizes() {
			try {
				const res = await api.getLotteryPrizes()
				if (res.data.items && res.data.items.length > 0) {
					this.prizesList = res.data.items.map(item => ({
						id: item.id,
						icon: item.icon || '🎁',
						name: item.name,
						probability: item.probability
					}))
				}
			} catch (error) {
				console.error('获取奖品列表失败', error)
			}
		},
		
		// 获取最近中奖记录
		async loadRecentRecords() {
			try {
				const res = await api.getRecentLotteryRecords(10)
				this.recentPrizes = res.data.items || []
			} catch (error) {
				console.error('获取中奖记录失败', error)
			}
		},
		
		// 开始抽奖
		async startLottery() {
			if (this.chances === 0) {
				uni.showToast({ title: '暂无抽奖次数', icon: 'none' })
				return
			}
			
			if (this.isSpinning) return
			
			this.isSpinning = true
			this.selectedPrizeIndex = -1
			
			try {
				// 开始转动动画
				let spinCount = 0
				const spinInterval = setInterval(() => {
					this.selectedPrizeIndex = (this.selectedPrizeIndex + 1) % this.prizesList.length
					spinCount++
				}, 100)
				
				// 调用抽奖API
				const res = await api.doLottery()
				
				// 等待动画效果
				await new Promise(resolve => setTimeout(resolve, 2000))
				
				clearInterval(spinInterval)
				
				// 找到中奖奖品的索引
				const prizeIndex = this.prizesList.findIndex(p => p.name === res.data.prize.name)
				if (prizeIndex >= 0) {
					this.selectedPrizeIndex = prizeIndex
				}
				
				// 显示结果
				this.prizeResult = {
					icon: res.data.prize.icon,
					name: res.data.prize.name,
					need_claim: res.data.need_claim,
					record_id: res.data.record_id
				}
				
				await new Promise(resolve => setTimeout(resolve, 500))
				this.$refs.resultPopup.open()
				
				// 刷新次数
				this.chances = Math.max(0, this.chances - 1)
				this.loadRecentRecords()
				
			} catch (error) {
				uni.showToast({ title: error.message || '抽奖失败', icon: 'none' })
			} finally {
				this.isSpinning = false
			}
		},
		
		// 领取奖品
		async claimPrize() {
			try {
				await api.claimPrize(this.prizeResult.record_id)
				uni.showToast({ title: '领取成功！', icon: 'success' })
				this.closeResultPopup()
			} catch (error) {
				uni.showToast({ title: error.message || '领取失败', icon: 'none' })
			}
		},
		
		// 关闭结果弹窗
		closeResultPopup() {
			this.$refs.resultPopup.close()
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
		width: 400rpx;
		height: 400rpx;
		margin: 0 auto 40rpx;
		position: relative;
		border-radius: 50%;
		background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
		
		&.spinning {
			animation: spin 0.5s linear infinite;
		}
		
		.wheel-center {
			position: absolute;
			top: 50%;
			left: 50%;
			transform: translate(-50%, -50%);
			width: 120rpx;
			height: 120rpx;
			background: white;
			border-radius: 50%;
			display: flex;
			align-items: center;
			justify-content: center;
			z-index: 10;
			box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.2);
			
			.wheel-icon {
				font-size: 60rpx;
			}
		}
		
		.wheel-prizes {
			position: absolute;
			top: 0;
			left: 0;
			right: 0;
			bottom: 0;
			
			.prize-sector {
				position: absolute;
				top: 30rpx;
				left: 50%;
				transform-origin: center 170rpx;
				
				.prize-icon {
					font-size: 40rpx;
				}
				
				&.active {
					.prize-icon {
						transform: scale(1.5);
						animation: pulse 0.3s ease-in-out;
					}
				}
			}
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

@keyframes spin {
	from { transform: rotate(0deg); }
	to { transform: rotate(360deg); }
}

@keyframes pulse {
	0%, 100% { transform: scale(1.5); }
	50% { transform: scale(2); }
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

/* 结果弹窗 */
.result-popup {
	background: white;
	border-radius: 20rpx;
	padding: 60rpx 40rpx;
	text-align: center;
	width: 500rpx;
	
	.result-icon {
		font-size: 120rpx;
		margin-bottom: 30rpx;
	}
	
	.result-title {
		font-size: 28rpx;
		color: #666;
		margin-bottom: 20rpx;
	}
	
	.result-prize {
		font-size: 36rpx;
		font-weight: bold;
		color: #f5576c;
		margin-bottom: 40rpx;
	}
	
	.claim-btn {
		background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
		color: white;
		border: none;
		border-radius: 50rpx;
		padding: 25rpx 60rpx;
		font-size: 28rpx;
	}
	
	.close-btn {
		background: #f5f5f5;
		color: #666;
		border: none;
		border-radius: 50rpx;
		padding: 25rpx 60rpx;
		font-size: 28rpx;
	}
}
</style>
