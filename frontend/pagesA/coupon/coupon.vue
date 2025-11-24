<template>
	<view class="coupon-page">
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
		
		<!-- 统计提示 -->
		<view class="stats-tip" v-if="currentTab === 1">
			<text>共有<text class="highlight">{{ availableCount }}</text>张优惠券可用，累计最高可减免<text class="highlight orange">{{ totalSavings }}</text>元</text>
		</view>
		
		<!-- 优惠券列表 -->
		<view v-if="filteredCoupons.length > 0" class="coupons-list">
			<view v-for="(item, index) in filteredCoupons" :key="index" class="coupon-item">
				<!-- 优惠券主体 -->
				<view :class="['coupon-card', getCouponClass(item)]">
					<view class="coupon-left">
						<text class="coupon-symbol">¥</text>
						<text class="coupon-amount">{{ item.amount }}</text>
					</view>
					<view class="coupon-middle">
						<text class="coupon-name">{{ item.name }}</text>
						<text class="coupon-condition">满{{ item.min_amount }}可用</text>
						<text class="coupon-expire">{{ item.expire_date }}到期</text>
					</view>
					<view class="coupon-right">
						<button 
							v-if="item.status === 'available'"
							class="use-btn"
							@click.stop="useCoupon(item)"
						>
							去使用
						</button>
						<text v-else-if="item.status === 'used'" class="status-text">已使用</text>
						<text v-else class="status-text">已过期</text>
					</view>
				</view>
				
				<!-- 使用说明（可展开） -->
				<view class="coupon-desc" v-if="item.showDesc">
					<text class="desc-title">使用说明：</text>
					<text class="desc-text">{{ item.description }}</text>
					<text class="collapse-btn" @click="toggleDesc(index)">收起 ▲</text>
				</view>
				<view v-else class="expand-btn" @click="toggleDesc(index)">
					<text>使用说明：{{ item.description.substring(0, 20) }}...</text>
					<text class="arrow">▼</text>
				</view>
			</view>
		</view>
		
		<!-- 空状态 -->
		<view v-else class="empty-state">
			<text class="empty-icon">🎫</text>
			<text class="empty-text">{{ getEmptyText() }}</text>
			<button v-if="currentTab === 0" class="btn-get" @click="goGetCoupons">去领券</button>
		</view>
	</view>
</template>

<script>
import api from '@/utils/api.js'

export default {
	data() {
		return {
			currentTab: 1, // 默认显示"待使用"
			tabs: ['活动领券', '待使用', '已使用', '已过期'],
			coupons: [
				{
					id: 1,
					name: '首样减免券',
					amount: 200,
					min_amount: 0,
					expire_date: '2025-11-18',
					status: 'available',
					type: 'discount',
					description: '新客户实名认证-首样免单立减200元。适用于所有检测项目，每个账户限用一次。',
					showDesc: false
				}
			]
		}
	},
	
	computed: {
		// 过滤后的优惠券
		filteredCoupons() {
			if (this.currentTab === 0) {
				// 活动领券 - 显示可领取的券
				return []
			} else if (this.currentTab === 1) {
				// 待使用
				return this.coupons.filter(c => c.status === 'available')
			} else if (this.currentTab === 2) {
				// 已使用
				return this.coupons.filter(c => c.status === 'used')
			} else {
				// 已过期
				return this.coupons.filter(c => c.status === 'expired')
			}
		},
		
		// 可用券数量
		availableCount() {
			return this.coupons.filter(c => c.status === 'available').length
		},
		
		// 累计可节省
		totalSavings() {
			return this.coupons
				.filter(c => c.status === 'available')
				.reduce((sum, c) => sum + c.amount, 0)
		}
	},
	
	onLoad() {
		this.loadCoupons()
	},
	
	methods: {
		// 切换Tab
		switchTab(index) {
			this.currentTab = index
		},
		
		// 加载优惠券
		async loadCoupons() {
			try {
				const status = this.currentTab === 0 ? 'available' : 
				               this.currentTab === 1 ? 'available' : 
				               this.currentTab === 2 ? 'used' : 'expired'
				
				const res = await api.getMyCoupons({ status, page: 1, page_size: 50 })
				
				// 如果API返回数据，使用API数据
				if (res.data.items && res.data.items.length > 0) {
					this.coupons = res.data.items
				}
				// 否则保持现有的展示数据用于UI演示
			} catch (error) {
				console.error('加载优惠券失败', error)
			}
		},
		
		// 展开/收起说明
		toggleDesc(index) {
			this.filteredCoupons[index].showDesc = !this.filteredCoupons[index].showDesc
			this.$forceUpdate()
		},
		
		// 使用优惠券
		useCoupon(item) {
			// 跳转到首页选择项目
			uni.showModal({
				title: '使用优惠券',
				content: '请选择要使用此优惠券的项目',
				confirmText: '去选择',
				success: (res) => {
					if (res.confirm) {
						uni.switchTab({
							url: '/pages/index/index'
						})
					}
				}
			})
		},
		
		// 去领券
		goGetCoupons() {
			uni.showToast({
				title: '领券功能开发中',
				icon: 'none'
			})
		},
		
		// 获取优惠券样式类
		getCouponClass(item) {
			if (item.status === 'available') {
				return 'available'
			} else if (item.status === 'used') {
				return 'used'
			} else {
				return 'expired'
			}
		},
		
		// 获取空状态文本
		getEmptyText() {
			const texts = ['暂无活动券', '暂无可用券', '暂无已使用券', '暂无过期券']
			return texts[this.currentTab] || '暂无优惠券'
		}
	}
}
</script>

<style lang="scss" scoped>
.coupon-page {
	min-height: 100vh;
	background: #f5f5f5;
}

/* Tab切换 */
.tabs {
	display: flex;
	background: white;
	position: sticky;
	top: 0;
	z-index: 10;
	
	.tab-item {
		flex: 1;
		text-align: center;
		padding: 30rpx 0;
		font-size: 28rpx;
		color: #666;
		position: relative;
		
		&.active {
			color: #4dabf7;
			font-weight: bold;
			
			&::after {
				content: '';
				position: absolute;
				bottom: 0;
				left: 50%;
				transform: translateX(-50%);
				width: 60rpx;
				height: 4rpx;
				background: #4dabf7;
				border-radius: 2rpx;
			}
		}
	}
}

/* 统计提示 */
.stats-tip {
	background: #fffbf0;
	padding: 20rpx 30rpx;
	font-size: 26rpx;
	color: #666;
	
	.highlight {
		color: #333;
		font-weight: bold;
	}
	
	.orange {
		color: #ff9800;
	}
}

/* 优惠券列表 */
.coupons-list {
	padding: 20rpx 30rpx;
}

.coupon-item {
	margin-bottom: 30rpx;
}

/* 优惠券卡片 */
.coupon-card {
	border-radius: 16rpx;
	padding: 30rpx;
	display: flex;
	align-items: center;
	position: relative;
	overflow: hidden;
	
	&.available {
		background: linear-gradient(135deg, #a78bfa 0%, #8b5cf6 100%);
		box-shadow: 0 8rpx 30rpx rgba(139, 92, 246, 0.3);
	}
	
	&.used,
	&.expired {
		background: #e0e0e0;
	}
}

.coupon-left {
	display: flex;
	align-items: baseline;
	margin-right: 30rpx;
}

.coupon-symbol {
	font-size: 32rpx;
	color: white;
	font-weight: bold;
}

.coupon-amount {
	font-size: 72rpx;
	font-weight: bold;
	color: white;
}

.coupon-middle {
	flex: 1;
	display: flex;
	flex-direction: column;
	gap: 8rpx;
}

.coupon-name {
	font-size: 28rpx;
	font-weight: bold;
	color: white;
}

.coupon-condition {
	font-size: 24rpx;
	color: white;
	opacity: 0.9;
}

.coupon-expire {
	font-size: 22rpx;
	color: white;
	opacity: 0.8;
}

.coupon-right {
	display: flex;
	align-items: center;
}

.use-btn {
	background: white;
	color: #8b5cf6;
	border: none;
	padding: 15rpx 35rpx;
	border-radius: 50rpx;
	font-size: 26rpx;
	font-weight: bold;
}

.status-text {
	font-size: 24rpx;
	color: white;
	opacity: 0.7;
}

/* 使用说明 */
.expand-btn {
	background: white;
	padding: 20rpx 30rpx;
	border-radius: 0 0 16rpx 16rpx;
	display: flex;
	justify-content: space-between;
	align-items: center;
	font-size: 24rpx;
	color: #666;
	margin-top: -16rpx;
	
	.arrow {
		color: #999;
	}
}

.coupon-desc {
	background: white;
	padding: 20rpx 30rpx;
	border-radius: 0 0 16rpx 16rpx;
	margin-top: -16rpx;
}

.desc-title {
	font-size: 24rpx;
	color: #666;
	font-weight: bold;
	display: block;
	margin-bottom: 10rpx;
}

.desc-text {
	font-size: 24rpx;
	color: #666;
	line-height: 1.6;
	display: block;
	margin-bottom: 15rpx;
}

.collapse-btn {
	font-size: 24rpx;
	color: #4dabf7;
	text-align: center;
	display: block;
}

/* 空状态 */
.empty-state {
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: 200rpx 0;
	
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
	
	.btn-get {
		background: #1890ff;
		color: white;
		border: none;
		border-radius: 50rpx;
		padding: 25rpx 60rpx;
		font-size: 28rpx;
	}
}
</style>
