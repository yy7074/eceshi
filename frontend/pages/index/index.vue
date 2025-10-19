<template>
	<view class="container">
		<!-- 搜索栏 -->
		<view class="search-bar">
			<view class="search-input" @click="goSearch">
				<text class="icon">🔍</text>
				<text class="placeholder">输入仪器名称/型号，如 XRD、SEM、FT-IR</text>
			</view>
		</view>
		
		<!-- 顶部快捷入口 -->
		<view class="quick-nav">
			<view class="nav-item" v-for="(item, index) in quickNavs" :key="index" @click="handleQuickNav(item)">
				<view class="nav-icon-wrap" :style="{ background: item.bg }">
					<text class="nav-icon" :style="{ color: item.color }">{{ item.icon }}</text>
				</view>
				<text class="nav-text">{{ item.name }}</text>
			</view>
		</view>
		
		<!-- 活动banner -->
		<view class="promo-banner">
			<view class="banner-content">
				<view class="banner-left">
					<text class="banner-title">金秋检测季 测试34元</text>
					<text class="banner-subtitle">XPS 6折 SEM/FT-IR 6折</text>
					<view class="banner-btn">立即参与</view>
				</view>
				<view class="banner-right">
					<text class="banner-emoji">🎉</text>
				</view>
			</view>
		</view>
		
		<!-- 分类导航 -->
		<view class="category-grid">
			<view class="category-item" v-for="item in categories" :key="item.id" @click="goCategory(item)">
				<view class="category-icon" :style="{ background: item.color }">
					<text class="category-emoji">{{ item.emoji }}</text>
				</view>
				<text class="category-name">{{ item.name }}</text>
			</view>
		</view>
		
		<!-- 增值活动区域 -->
		<view class="activity-section">
			<view class="activity-left">
				<view class="activity-card green">
					<text class="activity-title">升级</text>
					<text class="activity-subtitle">打折</text>
				</view>
			</view>
			<view class="activity-right">
				<view class="activity-info">
					<text class="info-title">增值活动</text>
					<view class="info-tags">
						<text class="tag">一键领取</text>
						<text class="tag">现任有礼</text>
						<text class="tag">免费登记</text>
						<text class="tag">新客专区</text>
					</view>
				</view>
				<view class="activity-card orange">
					<text class="activity-title">测试34元</text>
					<text class="activity-subtitle">XPS低至6折</text>
				</view>
				<view class="activity-card blue">
					<text class="activity-title">全屋升级</text>
					<text class="activity-subtitle">金额双倍</text>
				</view>
			</view>
		</view>
		
		<!-- 项目列表 -->
		<view class="project-section">
			<view class="project-grid">
				<view class="project-card" v-for="item in projects" :key="item.id">
					<image :src="item.cover_image" mode="aspectFill" class="project-image" :show-menu-by-longpress="true" @click="goProjectDetail(item)"></image>
					<view class="project-info">
						<text class="project-name" @click="goProjectDetail(item)">{{ item.name }}</text>
						<view class="project-meta">
					<view class="project-meta-row">
						<text class="tested">已测{{ item.order_count || 0 }}次</text>
						<text class="dot">·</text>
						<text class="cycle">{{ item.service_cycle_min || 3 }}-{{ item.service_cycle_max || 5 }}个工作日</text>
					</view>
						</view>
						<view class="project-footer">
							<view class="project-price">
								<text class="price-symbol">¥</text>
								<text class="price-value">{{ item.current_price }}</text>
								<text class="price-unit">起</text>
							</view>
							<view class="book-btn" @click.stop="goBooking(item)">立即预约</view>
						</view>
					</view>
				</view>
			</view>
		</view>
		
		<!-- 底部占位 -->
		<view class="bottom-placeholder"></view>
	</view>
</template>

<script>
	import api from '@/utils/api.js'
	
	export default {
		data() {
			return {
				quickNavs: [
					{ icon: '🤝', name: '邀请好友', bg: '#e6fcf5', color: '#12b886' },
					{ icon: '🎯', name: '优惠券', bg: '#fff4e6', color: '#ff922b' },
					{ icon: '👥', name: '创建团体', bg: '#eef2ff', color: '#667eea' },
					{ icon: '📍', name: '我的积分', bg: '#e7f5ff', color: '#4dabf7' }
				],
				categories: [],
				projects: []
			}
		},
		onLoad() {
			this.loadData()
		},
		methods: {
			async loadData() {
				try {
					// 加载分类
					const categoryRes = await api.getCategories()
					const serverCategories = categoryRes.data || []
					
					// 纯色数组
					const solidColors = [
						'#667eea', // 紫色
						'#f093fb', // 粉红
						'#4facfe', // 蓝色
						'#43e97b', // 绿色
						'#fa709a', // 粉色
						'#30cfd0', // 青色
						'#a8edea', // 浅青
						'#ffecd2'  // 浅橙
					]
					
					// 使用后台返回的分类数据，添加纯色背景
					this.categories = serverCategories.slice(0, 8).map((cat, index) => ({
						id: cat.id,
						name: cat.name,
						emoji: cat.icon || '📦', // 使用后台的icon字段
						color: solidColors[index % solidColors.length]
					}))
					
					// 如果分类不足8个，补充"更多功能"
					if (this.categories.length < 8) {
						this.categories.push({
							id: 999,
							name: '更多功能',
							emoji: '➕',
							color: solidColors[7]
						})
					}
					
					// 加载热门项目
					const projectRes = await api.getProjects({ page: 1, page_size: 20 })
					const projects = projectRes.data?.items || projectRes.data?.list || []
					
					// 使用后台返回的项目数据
					this.projects = projects.map(project => ({
						...project,
						// 直接使用后台返回的cover_image
						cover_image: project.cover_image || `https://picsum.photos/400/300?random=${project.id}`,
						lab_name: project.laboratory?.name || '官方实验室',
						order_count: project.order_count || 0,
						service_cycle_min: project.service_cycle_min || 3,
						service_cycle_max: project.service_cycle_max || 5
					}))
				} catch (e) {
					console.error('加载数据失败', e)
					uni.showToast({
						title: '加载失败，请重试',
						icon: 'none'
					})
				}
			},
		handleQuickNav(item) {
			// 检查登录
			const token = uni.getStorageSync('token')
			
			switch(item.name) {
				case '邀请好友':
					// 检查登录
					if (!token) {
						uni.showModal({
							title: '提示',
							content: '请先登录',
							success: (res) => {
								if (res.confirm) {
									uni.navigateTo({ url: '/pages/login/login' })
								}
							}
						})
						return
					}
					// 跳转到邀请好友页面
					uni.navigateTo({ url: '/pagesA/invite/invite' })
					break
				case '优惠券':
					// 检查登录
					if (!token) {
						uni.showModal({
							title: '提示',
							content: '请先登录',
							success: (res) => {
								if (res.confirm) {
									uni.navigateTo({
										url: '/pages/login/login'
									})
								}
							}
						})
						return
					}
					// 跳转到优惠券页面
					uni.navigateTo({
						url: '/pagesA/coupon/coupon'
					})
					break
				case '创建团体':
					// 检查登录
					if (!token) {
						uni.showModal({
							title: '提示',
							content: '请先登录',
							success: (res) => {
								if (res.confirm) {
									uni.navigateTo({
										url: '/pages/login/login'
									})
								}
							}
						})
						return
					}
					// 跳转到团体页面
					uni.navigateTo({
						url: '/pagesA/group/group'
					})
					break
				case '我的积分':
					// 检查登录
					if (!token) {
						uni.showModal({
							title: '提示',
							content: '请先登录',
							success: (res) => {
								if (res.confirm) {
									uni.navigateTo({
										url: '/pages/login/login'
									})
								}
							}
						})
						return
					}
					// 跳转到积分页面
					uni.navigateTo({
						url: '/pagesA/points/points'
					})
					break
				default:
					uni.showToast({
						title: '功能开发中',
						icon: 'none'
					})
			}
		},
		goSearch() {
			uni.navigateTo({
				url: '/pages/search/search'
			})
		},
		goCategory(item) {
			// 跳转到分类页（tabBar页面使用switchTab）
			uni.switchTab({
				url: `/pages/category/category`
			})
		},
		goProjectDetail(item) {
			uni.navigateTo({
				url: `/pages/project/detail?id=${item.id}`
			})
		},
		goBooking(item) {
			// 跳转到预约页面
			uni.navigateTo({
				url: `/pagesA/booking/booking?projectId=${item.id}&projectName=${encodeURIComponent(item.name)}`
			})
		}
		}
	}
</script>

<style lang="scss" scoped>
	.container {
		min-height: 100vh;
		background: #f5f5f5;
		padding-bottom: 20rpx;
	}
	
	/* 搜索栏 */
	.search-bar {
		background: #ff9500;
		padding: 20rpx 30rpx 30rpx;
		
		.search-input {
			background: white;
			border-radius: 50rpx;
			padding: 18rpx 30rpx;
			display: flex;
			align-items: center;
			
			.icon {
				font-size: 32rpx;
				margin-right: 15rpx;
			}
			
			.placeholder {
				color: #999;
				font-size: 28rpx;
			}
		}
	}
	
	/* 快捷入口 */
	.quick-nav {
		display: flex;
		justify-content: space-around;
		background: white;
		padding: 24rpx 10rpx;
		margin: 0 30rpx 20rpx;
		border-radius: 16rpx;
		
		.nav-item {
			display: flex;
			flex-direction: column;
			align-items: center;
			
			.nav-icon-wrap {
				width: 90rpx;
				height: 90rpx;
				border-radius: 20rpx;
				display: flex;
				align-items: center;
				justify-content: center;
				margin-bottom: 10rpx;
			}
			.nav-icon { font-size: 46rpx; }
			
			.nav-text {
				font-size: 24rpx;
				color: #333;
			}
		}
	}
	
	/* 活动banner */
	.promo-banner {
		background: #ff9500;
		margin: 0 30rpx 20rpx;
		border-radius: 20rpx;
		overflow: hidden;
		
		.banner-content {
			display: flex;
			justify-content: space-between;
			align-items: center;
			padding: 30rpx;
			
			.banner-left {
				flex: 1;
				
				.banner-title {
					display: block;
					font-size: 36rpx;
					font-weight: bold;
					color: #8B4513;
					margin-bottom: 10rpx;
				}
				
				.banner-subtitle {
					display: block;
					font-size: 24rpx;
					color: #8B4513;
					margin-bottom: 20rpx;
				}
				
				.banner-btn {
					background: white;
					color: #ff6b35;
					padding: 12rpx 30rpx;
					border-radius: 30rpx;
					font-size: 26rpx;
					display: inline-block;
					font-weight: bold;
				}
			}
			
			.banner-right {
				.banner-emoji {
					font-size: 100rpx;
				}
			}
		}
	}
	
	/* 分类网格 */
	.category-grid {
		display: grid;
		grid-template-columns: repeat(4, 1fr);
		gap: 20rpx;
		background: white;
		padding: 30rpx;
		margin-bottom: 20rpx;
		
		.category-item {
			display: flex;
			flex-direction: column;
			align-items: center;
			
			.category-icon {
				width: 100rpx;
				height: 100rpx;
				border-radius: 20rpx;
				display: flex;
				align-items: center;
				justify-content: center;
				margin-bottom: 10rpx;
				
				.category-emoji {
					font-size: 50rpx;
				}
			}
			
			.category-name {
				font-size: 24rpx;
				color: #333;
			}
		}
	}
	
	/* 增值活动 */
	.activity-section {
		display: flex;
		gap: 20rpx;
		padding: 0 30rpx 20rpx;
		
		.activity-left {
			.activity-card {
				width: 200rpx;
				height: 400rpx;
				border-radius: 20rpx;
				padding: 30rpx;
				display: flex;
				flex-direction: column;
				justify-content: center;
				
				&.green {
					background: #43e97b;
				}
				
				.activity-title {
					font-size: 40rpx;
					font-weight: bold;
					color: white;
					display: block;
					margin-bottom: 10rpx;
				}
				
				.activity-subtitle {
					font-size: 28rpx;
					color: white;
					display: block;
				}
			}
		}
		
		.activity-right {
			flex: 1;
			display: flex;
			flex-direction: column;
			gap: 20rpx;
			
			.activity-info {
				background: white;
				border-radius: 20rpx;
				padding: 20rpx;
				
				.info-title {
					font-size: 28rpx;
					font-weight: bold;
					color: #333;
					display: block;
					margin-bottom: 15rpx;
				}
				
				.info-tags {
					display: flex;
					flex-wrap: wrap;
					gap: 10rpx;
					
					.tag {
						background: #f0f0f0;
						padding: 8rpx 20rpx;
						border-radius: 30rpx;
						font-size: 22rpx;
						color: #666;
					}
				}
			}
			
			.activity-card {
				flex: 1;
				border-radius: 20rpx;
				padding: 20rpx;
				display: flex;
				flex-direction: column;
				justify-content: center;
				
				&.orange {
					background: #fa709a;
				}
				
				&.blue {
					background: #4facfe;
				}
				
				.activity-title {
					font-size: 32rpx;
					font-weight: bold;
					color: white;
					display: block;
					margin-bottom: 5rpx;
				}
				
				.activity-subtitle {
					font-size: 24rpx;
					color: white;
					display: block;
				}
			}
		}
	}
	
	/* 项目列表 */
	.project-section {
		padding: 0 30rpx;
		
		.project-grid {
			display: grid;
			grid-template-columns: repeat(2, 1fr);
			gap: 20rpx;
			
			.project-card {
				background: white;
				border-radius: 20rpx;
				overflow: hidden;
				
				.project-image {
					width: 100%;
					height: 280rpx;
				}
				
				.project-info {
					padding: 20rpx;
					
					.project-name {
						font-size: 28rpx;
						font-weight: bold;
						color: #333;
						display: block;
						margin-bottom: 10rpx;
						overflow: hidden;
						text-overflow: ellipsis;
						white-space: nowrap;
					}
					
				.project-meta {
						margin-bottom: 15rpx;
					.project-meta-row { display: flex; align-items: center; gap: 8rpx; }
					.tested { font-size: 22rpx; color: #666; }
					.dot { color: #ccc; }
					.cycle { font-size: 22rpx; color: #999; }
					}
					
					.project-footer {
						display: flex;
						justify-content: space-between;
						align-items: center;
						
						.project-price {
							display: flex;
							align-items: baseline;
							
							.price-symbol {
								font-size: 24rpx;
								color: #ff6b35;
							}
							
							.price-value {
								font-size: 32rpx;
								font-weight: bold;
								color: #ff6b35;
							}
							
							.price-unit {
								font-size: 22rpx;
								color: #ff6b35;
								margin-left: 4rpx;
							}
						}
						
						.book-btn {
							background: #667eea;
							color: white;
							padding: 10rpx 20rpx;
							border-radius: 30rpx;
							font-size: 22rpx;
						}
					}
				}
			}
		}
	}
	
	.bottom-placeholder {
		height: 100rpx;
	}
</style>
