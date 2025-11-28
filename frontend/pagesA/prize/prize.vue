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
					<view class="prize-icon">{{ item.prize_icon || '🎁' }}</view>
					<view class="prize-info">
						<text class="prize-name">{{ item.prize_name }}</text>
						<text class="prize-time">{{ formatTime(item.created_at) }}</text>
					</view>
					<view class="prize-action">
						<text v-if="item.status === 'unclaimed'" class="claim-btn" @click="claimPrize(item)">立即领取</text>
						<text v-else-if="item.status === 'claimed'" class="claimed-text">已领取</text>
						<text v-else class="expired-text">已过期</text>
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
		
		<!-- 加载更多 -->
		<view v-if="prizes.length > 0 && hasMore" class="load-more" @click="loadMore">
			<text>{{ loading ? '加载中...' : '加载更多' }}</text>
		</view>
	</view>
</template>

<script>
import api from '@/utils/api.js'

export default {
	data() {
		return {
			totalPrizes: 0,
			totalAmount: 0,
			prizes: [],
			page: 1,
			pageSize: 20,
			hasMore: true,
			loading: false
		}
	},
	
	onLoad() {
		this.loadPrizes()
	},
	
	onPullDownRefresh() {
		this.page = 1
		this.prizes = []
		this.hasMore = true
		this.loadPrizes().finally(() => {
			uni.stopPullDownRefresh()
		})
	},
	
	onReachBottom() {
		if (this.hasMore && !this.loading) {
			this.loadMore()
		}
	},
	
	methods: {
		// 加载中奖记录
		async loadPrizes() {
			this.loading = true
			try {
				const res = await api.getLotteryRecords({
					page: this.page,
					page_size: this.pageSize
				})
				
				const items = res.data.items || []
				
				if (this.page === 1) {
					this.prizes = items
				} else {
					this.prizes = [...this.prizes, ...items]
				}
				
				// 计算统计
				this.totalPrizes = res.data.total || this.prizes.length
				this.totalAmount = this.prizes
					.filter(p => p.prize_type !== 'empty')
					.reduce((sum, p) => sum + (p.prize_value || 0), 0)
				
				this.hasMore = items.length >= this.pageSize
				
			} catch (error) {
				console.error('加载中奖记录失败', error)
			} finally {
				this.loading = false
			}
		},
		
		// 加载更多
		loadMore() {
			this.page++
			this.loadPrizes()
		},
		
		// 格式化时间
		formatTime(timeStr) {
			if (!timeStr) return ''
			return timeStr.replace('T', ' ').substring(0, 16)
		},
		
		// 领取奖品
		async claimPrize(item) {
			uni.showModal({
				title: '领取奖品',
				content: `确认领取【${item.prize_name}】吗？`,
				success: async (res) => {
					if (res.confirm) {
						try {
							await api.claimPrize(item.id)
							uni.showToast({ title: '领取成功', icon: 'success' })
							item.status = 'claimed'
							this.$forceUpdate()
						} catch (error) {
							uni.showToast({ title: error.message || '领取失败', icon: 'none' })
						}
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
					padding: 15rpx 30rpx;
					background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
					color: white;
					border-radius: 50rpx;
					font-size: 24rpx;
				}
				
				.claimed-text {
					font-size: 24rpx;
					color: #52c41a;
				}
				
				.expired-text {
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

.load-more {
	text-align: center;
	padding: 30rpx;
	font-size: 26rpx;
	color: #999;
}
</style>
