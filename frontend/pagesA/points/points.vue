<template>
	<view class="points-page">
		<!-- 当前积分卡片 -->
		<view class="points-card">
			<view class="card-left">
				<text class="card-label">当前积分</text>
				<text class="card-points">{{ currentPoints }}</text>
				<text class="card-link" @click="goPointsDetail">积分明细 ›</text>
			</view>
		<view class="card-right">
			<text class="coins-emoji">💰</text>
			<text class="coins-emoji shine">✨</text>
		</view>
			<view class="card-rules" @click="showRules">
				<text>积分规则</text>
			</view>
		</view>
		
		<!-- Tab切换 -->
		<view class="tabs-container">
			<scroll-view scroll-x class="tabs-scroll">
				<view class="tabs">
					<view 
						v-for="(tab, index) in tabs" 
						:key="index"
						:class="['tab-item', currentTab === index ? 'active' : '']"
						@click="switchTab(index)"
					>
						{{ tab }}
					</view>
					<view class="tab-more" @click="showMore">
						<text>更多好礼，点击查看</text>
					</view>
				</view>
			</scroll-view>
			<view class="tab-indicator" :style="{ left: indicatorLeft }"></view>
		</view>
		
		<!-- 商品列表 -->
		<view class="goods-list">
			<view v-if="filteredGoods.length > 0" class="goods-grid">
				<view 
					v-for="(item, index) in filteredGoods" 
					:key="index"
					class="goods-item"
					@click="viewGoodsDetail(item)"
				>
					<image :src="item.image" mode="aspectFill" class="goods-image"></image>
					<view class="goods-info">
						<text class="goods-name">{{ item.name }}</text>
						<view class="goods-footer">
							<text class="goods-points">{{ item.points }}积分</text>
							<button class="exchange-btn" @click.stop="exchangeGoods(item)">立即兑换</button>
						</view>
					</view>
				</view>
			</view>
			
			<!-- 空状态 -->
			<view v-else class="empty-state">
				<text class="empty-icon">🎁</text>
				<text class="empty-text">暂无可兑换商品</text>
			</view>
		</view>
	</view>
</template>

<script>
export default {
	data() {
		return {
			currentPoints: 100,
			currentTab: 0,
			tabs: ['全部', '优惠券', '京东E卡', '实物礼'],
			indicatorLeft: '0rpx',
			goodsList: [
				{
					id: 1,
					name: '500元测试现金抵用券',
					points: 13440,
					category: '优惠券',
					image: '/static/points/coupon-500.svg'
				},
				{
					id: 2,
					name: '100元测试现金抵用券',
					points: 2688,
					category: '优惠券',
					image: '/static/points/coupon-100.svg'
				},
				{
					id: 3,
					name: '小熊电煮锅',
					points: 3032,
					category: '实物礼',
					image: 'https://picsum.photos/300/300?random=3'
				},
				{
					id: 4,
					name: '小米电动牙刷T200',
					points: 3544,
					category: '实物礼',
					image: 'https://picsum.photos/300/300?random=4'
				},
				{
					id: 5,
					name: '骨传导耳机',
					points: 6638,
					category: '实物礼',
					image: 'https://picsum.photos/300/300?random=5'
				},
				{
					id: 6,
					name: '苏泊尔养生壶',
					points: 5794,
					category: '实物礼',
					image: 'https://picsum.photos/300/300?random=6'
				},
				{
					id: 7,
					name: '50元京东E卡',
					points: 5000,
					category: '京东E卡',
					image: '/static/points/jd-50.svg'
				},
				{
					id: 8,
					name: '100元京东E卡',
					points: 10000,
					category: '京东E卡',
					image: '/static/points/jd-100.svg'
				}
			]
		}
	},
	
	computed: {
		filteredGoods() {
			if (this.currentTab === 0) {
				// 全部
				return this.goodsList
			} else {
				// 按分类筛选
				const category = this.tabs[this.currentTab]
				return this.goodsList.filter(item => item.category === category)
			}
		}
	},
	
	onLoad() {
		this.loadPoints()
		this.loadGoods()
	},
	
	methods: {
		// 加载积分
		async loadPoints() {
			try {
				// TODO: 调用API获取用户积分
				// const res = await api.getUserPoints()
				// this.currentPoints = res.data.points
			} catch (error) {
				console.error('加载积分失败', error)
			}
		},
		
		// 加载商品列表
		async loadGoods() {
			try {
				// TODO: 调用API获取兑换商品列表
				// const res = await api.getPointsGoods()
				// this.goodsList = res.data.list
			} catch (error) {
				console.error('加载商品失败', error)
			}
		},
		
		// 切换Tab
		switchTab(index) {
			this.currentTab = index
			// 计算指示器位置
			const tabWidth = 150 // 每个tab的宽度（rpx）
			this.indicatorLeft = (index * tabWidth + 25) + 'rpx'
		},
		
		// 积分明细
		goPointsDetail() {
			uni.showToast({
				title: '积分明细功能开发中',
				icon: 'none'
			})
		},
		
		// 积分规则
		showRules() {
			uni.showModal({
				title: '积分规则',
				content: '1. 注册即送100积分\n2. 每次下单可获得订单金额1%的积分\n3. 每日签到可获得10积分\n4. 邀请好友注册可获得50积分\n5. 积分可用于兑换优惠券、礼品等',
				showCancel: false,
				confirmText: '我知道了'
			})
		},
		
		// 更多好礼
		showMore() {
			uni.showToast({
				title: '敬请期待更多好礼',
				icon: 'none'
			})
		},
		
		// 查看商品详情
		viewGoodsDetail(item) {
			uni.showToast({
				title: '商品详情功能开发中',
				icon: 'none'
			})
		},
		
		// 兑换商品
		exchangeGoods(item) {
			if (this.currentPoints < item.points) {
				uni.showModal({
					title: '积分不足',
					content: `兑换${item.name}需要${item.points}积分，您当前只有${this.currentPoints}积分`,
					showCancel: false
				})
				return
			}
			
			uni.showModal({
				title: '确认兑换',
				content: `确定要用${item.points}积分兑换【${item.name}】吗？`,
				success: (res) => {
					if (res.confirm) {
						this.doExchange(item)
					}
				}
			})
		},
		
		// 执行兑换
		async doExchange(item) {
			try {
				uni.showLoading({ title: '兑换中...' })
				
				// TODO: 调用API兑换商品
				// const res = await api.exchangeGoods(item.id)
				
				await new Promise(resolve => setTimeout(resolve, 1000))
				
				uni.hideLoading()
				
				uni.showToast({
					title: '兑换成功',
					icon: 'success'
				})
				
				// 刷新积分
				this.currentPoints -= item.points
				this.loadPoints()
			} catch (error) {
				uni.hideLoading()
				console.error('兑换失败', error)
				uni.showToast({
					title: error.message || '兑换失败',
					icon: 'none'
				})
			}
		}
	}
}
</script>

<style lang="scss" scoped>
.points-page {
	min-height: 100vh;
	background: linear-gradient(180deg, #4facfe 0%, #00f2fe 30%, #f5f5f5 30%);
}

/* 积分卡片 */
.points-card {
	margin: 20rpx 30rpx;
	background: white;
	border-radius: 20rpx;
	padding: 40rpx 30rpx;
	display: flex;
	position: relative;
	box-shadow: 0 8rpx 30rpx rgba(79, 172, 254, 0.2);
	
	.card-left {
		flex: 1;
		display: flex;
		flex-direction: column;
		
		.card-label {
			font-size: 28rpx;
			color: #666;
			margin-bottom: 15rpx;
		}
		
		.card-points {
			font-size: 80rpx;
			font-weight: bold;
			color: #333;
			line-height: 1.2;
			margin-bottom: 20rpx;
		}
		
		.card-link {
			font-size: 26rpx;
			color: #4facfe;
		}
	}
	
	.card-right {
		width: 180rpx;
		height: 180rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		position: relative;
		
		.coins-emoji {
			font-size: 100rpx;
			
			&.shine {
				position: absolute;
				top: 10rpx;
				right: 10rpx;
				font-size: 50rpx;
			}
		}
	}
	
	.card-rules {
		position: absolute;
		top: 30rpx;
		right: 30rpx;
		padding: 10rpx 20rpx;
		background: linear-gradient(135deg, #ffd89b 0%, #19547b 100%);
		border-radius: 20rpx;
		font-size: 24rpx;
		color: white;
		box-shadow: 0 4rpx 10rpx rgba(255, 216, 155, 0.4);
	}
}

/* Tab切换 */
.tabs-container {
	background: white;
	padding: 0 30rpx;
	position: relative;
	
	.tabs-scroll {
		white-space: nowrap;
		
		.tabs {
			display: inline-flex;
			padding-bottom: 20rpx;
			
			.tab-item {
				display: inline-block;
				padding: 20rpx 25rpx;
				font-size: 28rpx;
				color: #666;
				transition: all 0.3s;
				
				&.active {
					color: #4facfe;
					font-weight: bold;
				}
			}
			
			.tab-more {
				display: inline-block;
				padding: 20rpx 25rpx;
				font-size: 24rpx;
				color: #ff6b6b;
				margin-left: 20rpx;
			}
		}
	}
	
	.tab-indicator {
		position: absolute;
		bottom: 0;
		width: 60rpx;
		height: 4rpx;
		background: #4facfe;
		border-radius: 2rpx;
		transition: left 0.3s;
	}
}

/* 商品列表 */
.goods-list {
	padding: 20rpx 30rpx;
	
	.goods-grid {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: 20rpx;
		
		.goods-item {
			background: white;
			border-radius: 16rpx;
			overflow: hidden;
			box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.05);
			
			.goods-image {
				width: 100%;
				height: 300rpx;
				background: #f5f5f5;
			}
			
			.goods-info {
				padding: 20rpx;
				
				.goods-name {
					font-size: 26rpx;
					color: #333;
					display: block;
					margin-bottom: 20rpx;
					overflow: hidden;
					text-overflow: ellipsis;
					white-space: nowrap;
				}
				
				.goods-footer {
					display: flex;
					justify-content: space-between;
					align-items: center;
					
					.goods-points {
						font-size: 28rpx;
						font-weight: bold;
						color: #4facfe;
					}
					
					.exchange-btn {
						background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
						color: white;
						border: none;
						border-radius: 50rpx;
						padding: 10rpx 25rpx;
						font-size: 24rpx;
						line-height: 1;
					}
				}
			}
		}
	}
}

.empty-state {
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: 150rpx 0;
	
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
