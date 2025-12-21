<template>
	<view class="stats-page">
		<!-- 时间筛选 -->
		<view class="time-filter">
			<view class="filter-item" :class="{ active: timeRange === 'week' }" @click="timeRange = 'week'">本周</view>
			<view class="filter-item" :class="{ active: timeRange === 'month' }" @click="timeRange = 'month'">本月</view>
			<view class="filter-item" :class="{ active: timeRange === 'year' }" @click="timeRange = 'year'">本年</view>
			<view class="filter-item" :class="{ active: timeRange === 'all' }" @click="timeRange = 'all'">全部</view>
		</view>
		
		<!-- 核心数据卡片 -->
		<view class="stats-cards">
			<view class="stats-card primary">
				<text class="card-icon">📦</text>
				<view class="card-content">
					<text class="card-value">{{ stats.totalOrders }}</text>
					<text class="card-label">总订单数</text>
				</view>
			</view>
			<view class="stats-card success">
				<text class="card-icon">💰</text>
				<view class="card-content">
					<text class="card-value">¥{{ stats.totalAmount }}</text>
					<text class="card-label">总消费金额</text>
				</view>
			</view>
			<view class="stats-card warning">
				<text class="card-icon">⭐</text>
				<view class="card-content">
					<text class="card-value">{{ stats.totalPoints }}</text>
					<text class="card-label">累计积分</text>
				</view>
			</view>
			<view class="stats-card info">
				<text class="card-icon">🎫</text>
				<view class="card-content">
					<text class="card-value">{{ stats.totalCoupons }}</text>
					<text class="card-label">优惠券数</text>
				</view>
			</view>
		</view>
		
		<!-- 订单统计 -->
		<view class="section">
			<view class="section-header">
				<text class="section-title">订单统计</text>
			</view>
			<view class="order-stats">
				<view class="order-stat-item">
					<text class="stat-value">{{ orderStats.unpaid }}</text>
					<text class="stat-label">待支付</text>
				</view>
				<view class="order-stat-item">
					<text class="stat-value">{{ orderStats.testing }}</text>
					<text class="stat-label">检测中</text>
				</view>
				<view class="order-stat-item">
					<text class="stat-value">{{ orderStats.completed }}</text>
					<text class="stat-label">已完成</text>
				</view>
				<view class="order-stat-item">
					<text class="stat-value">{{ orderStats.cancelled }}</text>
					<text class="stat-label">已取消</text>
				</view>
			</view>
		</view>
		
		<!-- 检测项目分布 -->
		<view class="section">
			<view class="section-header">
				<text class="section-title">检测项目分布</text>
			</view>
			<view class="project-stats">
				<view class="project-item" v-for="(item, index) in projectStats" :key="index">
					<view class="project-info">
						<text class="project-name">{{ item.name }}</text>
						<text class="project-count">{{ item.count }}次</text>
					</view>
					<view class="progress-bar">
						<view class="progress-fill" :style="{ width: item.percent + '%', background: item.color }"></view>
					</view>
				</view>
			</view>
		</view>
		
		<!-- 消费趋势 -->
		<view class="section">
			<view class="section-header">
				<text class="section-title">消费趋势</text>
			</view>
			<view class="trend-chart">
				<view class="chart-bars">
					<view class="bar-item" v-for="(item, index) in trendData" :key="index">
						<view class="bar" :style="{ height: item.height + '%' }"></view>
						<text class="bar-label">{{ item.label }}</text>
					</view>
				</view>
			</view>
		</view>
		
		<!-- 常用检测 -->
		<view class="section">
			<view class="section-header">
				<text class="section-title">常用检测</text>
				<text class="section-more" @click="goProjects">查看全部</text>
			</view>
			<view class="frequent-list">
				<view class="frequent-item" v-for="item in frequentProjects" :key="item.id" @click="goProjectDetail(item)">
					<view class="item-icon">🔬</view>
					<view class="item-info">
						<text class="item-name">{{ item.name }}</text>
						<text class="item-count">已测{{ item.count }}次</text>
					</view>
					<text class="item-arrow">›</text>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
import api from '@/utils/api.js'

export default {
	data() {
		return {
			loading: false,
			timeRange: 'month',
			stats: {
				totalOrders: 0,
				totalAmount: '0.00',
				totalPoints: 0,
				totalCoupons: 0
			},
			orderStats: {
				unpaid: 0,
				testing: 0,
				completed: 0,
				cancelled: 0
			},
			projectStats: [],
			trendData: [],
			frequentProjects: []
		}
	},
	watch: {
		timeRange() {
			this.loadAllData()
		}
	},
	onLoad() {
		this.loadAllData()
	},
	methods: {
		async loadAllData() {
			this.loading = true
			try {
				await Promise.all([
					this.loadOverview(),
					this.loadOrderStats(),
					this.loadProjectStats(),
					this.loadTrend(),
					this.loadFrequentProjects()
				])
			} catch (e) {
				console.error('加载统计数据失败', e)
			} finally {
				this.loading = false
			}
		},
		
		async loadOverview() {
			try {
				const res = await api.getStatsOverview(this.timeRange)
				if (res.code === 0 && res.data) {
					this.stats = {
						totalOrders: res.data.total_orders || 0,
						totalAmount: this.formatAmount(res.data.total_amount || 0),
						totalPoints: res.data.total_points || 0,
						totalCoupons: res.data.total_coupons || 0
					}
				}
			} catch (e) {
				console.error('加载概览失败', e)
			}
		},
		
		async loadOrderStats() {
			try {
				const res = await api.getOrderStats(this.timeRange)
				if (res.code === 0 && res.data) {
					this.orderStats = res.data
				}
			} catch (e) {
				console.error('加载订单统计失败', e)
			}
		},
		
		async loadProjectStats() {
			try {
				const res = await api.getProjectStats(this.timeRange, 5)
				if (res.code === 0 && res.data?.items) {
					this.projectStats = res.data.items
				}
			} catch (e) {
				console.error('加载项目统计失败', e)
			}
		},
		
		async loadTrend() {
			try {
				const res = await api.getConsumptionTrend(this.timeRange)
				if (res.code === 0 && res.data?.items) {
					this.trendData = res.data.items
				}
			} catch (e) {
				console.error('加载趋势失败', e)
			}
		},
		
		async loadFrequentProjects() {
			try {
				const res = await api.getFrequentProjects(5)
				if (res.code === 0 && res.data?.items) {
					this.frequentProjects = res.data.items
				}
			} catch (e) {
				console.error('加载常用项目失败', e)
			}
		},
		
		formatAmount(amount) {
			return Number(amount).toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
		},
		
		goProjects() {
			uni.switchTab({ url: '/pages/category/category' })
		},
		
		goProjectDetail(item) {
			uni.navigateTo({ url: `/pages/project/detail?id=${item.id}` })
		}
	}
}
</script>

<style lang="scss" scoped>
.stats-page {
	min-height: 100vh;
	background: #f5f5f5;
	padding-bottom: 40rpx;
}

.time-filter {
	display: flex;
	background: #fff;
	padding: 16rpx 24rpx;
	gap: 16rpx;
	
	.filter-item {
		flex: 1;
		text-align: center;
		padding: 16rpx 0;
		border-radius: 8rpx;
		font-size: 26rpx;
		color: #666;
		background: #f5f5f5;
		
		&.active {
			background: #1890ff;
			color: #fff;
		}
	}
}

.stats-cards {
	display: grid;
	grid-template-columns: repeat(2, 1fr);
	gap: 16rpx;
	padding: 16rpx 24rpx;
	
	.stats-card {
		display: flex;
		align-items: center;
		background: #fff;
		padding: 24rpx;
		border-radius: 12rpx;
		
		.card-icon {
			font-size: 48rpx;
			margin-right: 16rpx;
		}
		
		.card-content {
			.card-value {
				display: block;
				font-size: 36rpx;
				font-weight: 700;
				color: #333;
			}
			
			.card-label {
				font-size: 24rpx;
				color: #999;
			}
		}
		
		&.primary { border-left: 6rpx solid #1890ff; }
		&.success { border-left: 6rpx solid #52c41a; }
		&.warning { border-left: 6rpx solid #faad14; }
		&.info { border-left: 6rpx solid #722ed1; }
	}
}

.section {
	background: #fff;
	margin: 16rpx 24rpx;
	border-radius: 12rpx;
	padding: 24rpx;
	
	.section-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 24rpx;
		
		.section-title {
			font-size: 30rpx;
			font-weight: 600;
			color: #333;
		}
		
		.section-more {
			font-size: 26rpx;
			color: #1890ff;
		}
	}
}

.order-stats {
	display: flex;
	justify-content: space-around;
	
	.order-stat-item {
		text-align: center;
		
		.stat-value {
			display: block;
			font-size: 40rpx;
			font-weight: 700;
			color: #1890ff;
			margin-bottom: 8rpx;
		}
		
		.stat-label {
			font-size: 24rpx;
			color: #999;
		}
	}
}

.project-stats {
	.project-item {
		margin-bottom: 20rpx;
		
		&:last-child {
			margin-bottom: 0;
		}
		
		.project-info {
			display: flex;
			justify-content: space-between;
			margin-bottom: 8rpx;
			
			.project-name {
				font-size: 26rpx;
				color: #333;
			}
			
			.project-count {
				font-size: 26rpx;
				color: #666;
			}
		}
		
		.progress-bar {
			height: 16rpx;
			background: #f0f0f0;
			border-radius: 8rpx;
			overflow: hidden;
			
			.progress-fill {
				height: 100%;
				border-radius: 8rpx;
				transition: width 0.3s;
			}
		}
	}
}

.trend-chart {
	.chart-bars {
		display: flex;
		align-items: flex-end;
		height: 200rpx;
		gap: 16rpx;
		
		.bar-item {
			flex: 1;
			display: flex;
			flex-direction: column;
			align-items: center;
			
			.bar {
				width: 100%;
				background: linear-gradient(180deg, #1890ff 0%, #69c0ff 100%);
				border-radius: 8rpx 8rpx 0 0;
				min-height: 8rpx;
			}
			
			.bar-label {
				font-size: 22rpx;
				color: #999;
				margin-top: 8rpx;
			}
		}
	}
}

.frequent-list {
	.frequent-item {
		display: flex;
		align-items: center;
		padding: 20rpx 0;
		border-bottom: 1rpx solid #f0f0f0;
		
		&:last-child {
			border-bottom: none;
		}
		
		.item-icon {
			font-size: 40rpx;
			margin-right: 16rpx;
		}
		
		.item-info {
			flex: 1;
			
			.item-name {
				display: block;
				font-size: 28rpx;
				color: #333;
				margin-bottom: 4rpx;
			}
			
			.item-count {
				font-size: 24rpx;
				color: #999;
			}
		}
		
		.item-arrow {
			font-size: 32rpx;
			color: #ccc;
		}
	}
}
</style>

