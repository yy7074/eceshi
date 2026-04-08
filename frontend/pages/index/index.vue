<template>
	<view class="container">
		<!-- 顶部栏 -->
		<view class="top-bar">
			<view class="search-input" @click="goSearch">
				<text class="icon">🔍</text>
				<text class="placeholder">输入仪器名称/型号，如 XRD、SEM、FT-IR</text>
			</view>
			<view class="top-icons">
				<view class="icon-item" @click="goNotice">
					<text class="icon-emoji">🔔</text>
					<view class="badge" v-if="unreadCount > 0">{{ unreadCount > 99 ? '99+' : unreadCount }}</view>
				</view>
				<view class="icon-item" @click="goChat">
					<text class="icon-emoji">💬</text>
				</view>
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
		
		<!-- 轮播图Banner -->
		<swiper class="banner-swiper" :autoplay="true" :interval="4000" :circular="true" indicator-dots indicator-color="rgba(255,255,255,0.5)" indicator-active-color="#fff">
			<swiper-item v-for="banner in banners" :key="banner.id" @click="handleBannerClick(banner)">
				<view class="banner-slide" :style="{ background: banner.bgColor }">
					<view class="banner-content">
						<view class="banner-left">
							<text class="banner-title">{{ banner.title }}</text>
							<text class="banner-subtitle">{{ banner.subtitle }}</text>
							<view class="banner-btn" v-if="banner.btnText">{{ banner.btnText }}</view>
						</view>
						<view class="banner-right">
							<text class="banner-emoji">{{ banner.emoji }}</text>
						</view>
					</view>
				</view>
			</swiper-item>
		</swiper>
		
		<!-- 公告栏 -->
		<view class="notice-bar" v-if="announcements.length > 0">
			<text class="notice-icon">📢</text>
			<swiper class="notice-swiper" :autoplay="true" :interval="3000" :circular="true" vertical>
				<swiper-item v-for="ann in announcements" :key="ann.id">
					<text class="notice-text" @click="showAnnouncement(ann)">{{ ann.title }}</text>
				</swiper-item>
			</swiper>
			<text class="notice-more" @click="goNoticeList">更多</text>
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
				unreadCount: 2, // 未读消息数
				banners: [
					{ id: 1, title: '金秋检测季', subtitle: 'XPS 6折 SEM/FT-IR 6折', btnText: '立即参与', emoji: '🎉', bgColor: 'linear-gradient(135deg, #faad14 0%, #fa8c16 100%)' },
					{ id: 2, title: '新用户专享', subtitle: '首单立减50元 注册送100积分', btnText: '领取优惠', emoji: '🎁', bgColor: 'linear-gradient(135deg, #1890ff 0%, #096dd9 100%)' },
					{ id: 3, title: '充值有礼', subtitle: '充1000送150测试费 充5000送1000测试费', btnText: '去充值', emoji: '💰', bgColor: 'linear-gradient(135deg, #52c41a 0%, #389e0d 100%)' }
				],
				announcements: [
					{ id: 1, title: '12月优惠活动火热进行中', content: '金秋检测季活动详情...' },
					{ id: 2, title: '新增检测项目上线通知', content: '新增材料表征、生物科学等检测类目...' }
				],
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
			this.loadBanners()
			this.loadAnnouncements()
		},
		methods: {
			async loadBanners() {
				try {
					const res = await api.getBanners('home')
					if (res.code === 0 && res.data?.items?.length > 0) {
						const bgColors = [
							'linear-gradient(135deg, #faad14 0%, #fa8c16 100%)',
							'linear-gradient(135deg, #1890ff 0%, #096dd9 100%)',
							'linear-gradient(135deg, #52c41a 0%, #389e0d 100%)',
							'linear-gradient(135deg, #722ed1 0%, #531dab 100%)'
						]
						this.banners = res.data.items.map((b, i) => ({
							id: b.id,
							title: b.title,
							subtitle: b.subtitle,
							btnText: b.button_text || '了解详情',
							emoji: '🎉',
							bgColor: bgColors[i % bgColors.length],
							link_type: b.link_type,
							link_value: b.link_value
						}))
					}
				} catch (e) {
					console.error('加载轮播图失败', e)
				}
			},
			
			async loadAnnouncements() {
				try {
					const res = await api.getAnnouncements({ page: 1, page_size: 5 })
					if (res.code === 0 && res.data?.items?.length > 0) {
						this.announcements = res.data.items.map(a => ({
							id: a.id,
							title: a.title,
							content: a.summary || a.content
						}))
					}
				} catch (e) {
					console.error('加载公告失败', e)
				}
			},
			
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
					uni.navigateTo({
						url: '/pagesA/help/help'
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
		},
		goNotice() {
			const token = uni.getStorageSync('token')
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
			uni.navigateTo({ url: '/pagesA/notice/notice' })
		},
		goChat() {
			uni.navigateTo({ url: '/pagesA/chat/chat' })
		},
		handleBannerClick(banner) {
			// 根据banner类型跳转
			if (banner.title.includes('充值')) {
				const token = uni.getStorageSync('token')
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
				uni.navigateTo({ url: '/pagesA/recharge/recharge' })
			} else if (banner.title.includes('新用户')) {
				uni.navigateTo({ url: '/pagesA/coupon/coupon' })
			} else {
				uni.navigateTo({ url: '/pagesA/notice/notice' })
			}
		},
		showAnnouncement(ann) {
			uni.showModal({
				title: ann.title,
				content: ann.content,
				showCancel: false,
				confirmText: '我知道了'
			})
		},
		goNoticeList() {
			uni.navigateTo({ url: '/pagesA/notice/notice' })
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
	
	/* 顶部栏 */
	.top-bar {
		background: #fff;
		padding: 16rpx 24rpx;
		border-bottom: 1rpx solid #f0f0f0;
		display: flex;
		align-items: center;
		gap: 16rpx;
		
		.search-input {
			flex: 1;
			background: #f5f5f5;
			border-radius: 8rpx;
			padding: 16rpx 24rpx;
			display: flex;
			align-items: center;
			
			.icon {
				font-size: 28rpx;
				margin-right: 12rpx;
				color: #8c8c8c;
			}
			
			.placeholder {
				color: #8c8c8c;
				font-size: 26rpx;
			}
		}
		
		.top-icons {
			display: flex;
			gap: 16rpx;
			
			.icon-item {
				position: relative;
				width: 72rpx;
				height: 72rpx;
				display: flex;
				align-items: center;
				justify-content: center;
				background: #f5f5f5;
				border-radius: 50%;
				
				.icon-emoji {
					font-size: 36rpx;
				}
				
				.badge {
					position: absolute;
					top: -4rpx;
					right: -4rpx;
					min-width: 32rpx;
					height: 32rpx;
					padding: 0 8rpx;
					background: #ff4d4f;
					color: #fff;
					font-size: 20rpx;
					border-radius: 16rpx;
					display: flex;
					align-items: center;
					justify-content: center;
				}
			}
		}
	}
	
	/* 轮播图Banner */
	.banner-swiper {
		height: 280rpx;
		margin: 16rpx 24rpx;
		border-radius: 16rpx;
		overflow: hidden;
		
		.banner-slide {
			height: 100%;
			border-radius: 16rpx;
		}
		
		.banner-content {
			display: flex;
			justify-content: space-between;
			align-items: center;
			height: 100%;
			padding: 32rpx;
			
			.banner-left {
				flex: 1;
				
				.banner-title {
					display: block;
					font-size: 36rpx;
					font-weight: 700;
					color: #fff;
					margin-bottom: 12rpx;
				}
				
				.banner-subtitle {
					display: block;
					font-size: 26rpx;
					color: rgba(255,255,255,0.9);
					margin-bottom: 20rpx;
				}
				
				.banner-btn {
					display: inline-block;
					background: rgba(255,255,255,0.95);
					color: #333;
					padding: 12rpx 28rpx;
					border-radius: 8rpx;
					font-size: 26rpx;
					font-weight: 500;
				}
			}
			
			.banner-right {
				.banner-emoji {
					font-size: 100rpx;
				}
			}
		}
	}
	
	/* 公告栏 */
	.notice-bar {
		display: flex;
		align-items: center;
		background: #fffbe6;
		margin: 0 24rpx 16rpx;
		padding: 16rpx 20rpx;
		border-radius: 8rpx;
		border: 1rpx solid #ffe58f;
		
		.notice-icon {
			font-size: 28rpx;
			margin-right: 12rpx;
		}
		
		.notice-swiper {
			flex: 1;
			height: 40rpx;
		}
		
		.notice-text {
			font-size: 26rpx;
			color: #8c6d1f;
			line-height: 40rpx;
		}
		
		.notice-more {
			font-size: 24rpx;
			color: #1890ff;
			margin-left: 12rpx;
		}
	}
	
	/* 快捷入口 */
	.quick-nav {
		display: flex;
		justify-content: space-around;
		background: white;
		padding: 24rpx 16rpx;
		margin-bottom: 2rpx;
		
		.nav-item {
			display: flex;
			flex-direction: column;
			align-items: center;
			
			.nav-icon-wrap {
				width: 88rpx;
				height: 88rpx;
				border-radius: 12rpx;
				display: flex;
				align-items: center;
				justify-content: center;
				margin-bottom: 8rpx;
			}
			.nav-icon { font-size: 40rpx; }
			
			.nav-text {
				font-size: 24rpx;
				color: #595959;
			}
		}
	}
	
	/* 活动banner */
	.promo-banner {
		background: #faad14;
		margin: 0 24rpx 16rpx;
		border-radius: 12rpx;
		overflow: hidden;
		
		.banner-content {
			display: flex;
			justify-content: space-between;
			align-items: center;
			padding: 24rpx;
			
			.banner-left {
				flex: 1;
				
				.banner-title {
					display: block;
					font-size: 32rpx;
					font-weight: 600;
					color: #fff;
					margin-bottom: 8rpx;
				}
				
				.banner-subtitle {
					display: block;
					font-size: 22rpx;
					color: rgba(255,255,255,0.9);
					margin-bottom: 16rpx;
				}
				
				.banner-btn {
					background: white;
					color: #faad14;
					padding: 10rpx 24rpx;
					border-radius: 8rpx;
					font-size: 24rpx;
					display: inline-block;
					font-weight: 500;
				}
			}
			
			.banner-right {
				.banner-emoji {
					font-size: 80rpx;
				}
			}
		}
	}
	
	/* 分类网格 */
	.category-grid {
		display: grid;
		grid-template-columns: repeat(4, 1fr);
		gap: 24rpx 16rpx;
		background: white;
		padding: 24rpx;
		margin-bottom: 2rpx;
		
		.category-item {
			display: flex;
			flex-direction: column;
			align-items: center;
			
			.category-icon {
				width: 88rpx;
				height: 88rpx;
				border-radius: 12rpx;
				display: flex;
				align-items: center;
				justify-content: center;
				margin-bottom: 8rpx;
				
				.category-emoji {
					font-size: 44rpx;
				}
			}
			
			.category-name {
				font-size: 24rpx;
				color: #595959;
			}
		}
	}
	
	/* 项目列表 */
	.project-section {
		padding: 0 24rpx;
		
		.project-grid {
			display: grid;
			grid-template-columns: repeat(2, 1fr);
			gap: 16rpx;
			
			.project-card {
				background: white;
				border-radius: 12rpx;
				overflow: hidden;
				box-shadow: 0 2rpx 8rpx rgba(0,0,0,0.04);
				
				.project-image {
					width: 100%;
					height: 260rpx;
				}
				
				.project-info {
					padding: 16rpx;
					
					.project-name {
						font-size: 26rpx;
						font-weight: 500;
						color: #262626;
						display: block;
						margin-bottom: 8rpx;
						overflow: hidden;
						text-overflow: ellipsis;
						white-space: nowrap;
					}
					
					.project-meta {
						margin-bottom: 12rpx;
						.project-meta-row { display: flex; align-items: center; gap: 6rpx; }
						.tested { font-size: 22rpx; color: #8c8c8c; }
						.dot { color: #d9d9d9; }
						.cycle { font-size: 22rpx; color: #8c8c8c; }
					}
					
					.project-footer {
						display: flex;
						justify-content: space-between;
						align-items: center;
						
						.project-price {
							display: flex;
							align-items: baseline;
							
							.price-symbol {
								font-size: 22rpx;
								color: #ff4d4f;
							}
							
							.price-value {
								font-size: 30rpx;
								font-weight: 600;
								color: #ff4d4f;
							}
							
							.price-unit {
								font-size: 20rpx;
								color: #ff4d4f;
								margin-left: 2rpx;
							}
						}
						
						.book-btn {
							background: #1890ff;
							color: white;
							padding: 8rpx 16rpx;
							border-radius: 8rpx;
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
