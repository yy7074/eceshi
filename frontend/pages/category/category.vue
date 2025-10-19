<template>
	<view class="category-page">
		<!-- 顶部标题 -->
		<view class="page-header">
			<text class="header-title">仪器预约一e测试</text>
		</view>
		
		<!-- 搜索栏 -->
		<view class="search-bar">
			<view class="search-input" @click="goSearch">
				<text class="search-icon">🔍</text>
				<text class="search-placeholder">输入您想要的仪器名称</text>
			</view>
		</view>
		
		<!-- 顶部分类标签 -->
		<view class="top-filters">
			<scroll-view class="filter-scroll" scroll-x show-scrollbar="false">
				<view class="filter-item" @click="handleTopFilter('recommend')">为您推荐</view>
				<view class="filter-item active" @click="handleTopFilter('structure')">组织形貌</view>
				<view class="filter-item" @click="handleTopFilter('composition')">成分含量</view>
				<view class="filter-item" @click="handleTopFilter('chemical')">
					<text>化学结构</text>
					<text class="arrow">▼</text>
				</view>
			</scroll-view>
		</view>
		
		<!-- 主内容区 -->
		<view class="main-content">
			<!-- 左侧分类菜单 -->
			<scroll-view class="left-menu" scroll-y>
				<view 
					class="menu-item" 
					:class="{ active: activeCategory === category.id }"
					v-for="category in categories" 
					:key="category.id"
					@click="selectCategory(category)"
				>
					{{ category.name }}
				</view>
			</scroll-view>
			
			<!-- 右侧项目列表 -->
			<scroll-view class="right-content" scroll-y @scrolltolower="loadMore">
				<view class="project-list">
					<view class="project-card" v-for="project in projects" :key="project.id">
						<image :src="project.cover_image" mode="aspectFill" class="project-image" @click="goProjectDetail(project)"></image>
						<view class="project-info">
							<text class="project-name" @click="goProjectDetail(project)">{{ project.name }}</text>
							<view class="project-stats">
								<text class="stat-item">已测{{ project.order_count || 0 }}次</text>
								<text class="stat-item">满意度{{ Math.round(project.satisfaction || 100) }}%</text>
							</view>
							<view class="project-footer">
								<button class="btn-book" @click="goBooking(project)">立即预约</button>
							</view>
						</view>
					</view>
				</view>
				
				<!-- 加载状态 -->
				<view class="loading-more" v-if="loading">
					<text>加载中...</text>
				</view>
				<view class="no-more" v-if="!loading && noMore">
					<text>没有更多了</text>
				</view>
			</scroll-view>
		</view>
	</view>
</template>

<script>
import api from '@/utils/api.js'

export default {
	data() {
		return {
			categories: [
				{ id: 0, name: '材料测试' },
				{ id: 1, name: '高端测试' },
				{ id: 2, name: '材料加工' }
			],
			activeCategory: 0,
			projects: [],
			loading: false,
			noMore: false,
			page: 1,
			pageSize: 10
		}
	},
	onLoad(options) {
		this.loadCategories()
		this.loadProjects()
	},
	methods: {
		// 加载分类
		async loadCategories() {
			try {
				const res = await api.getCategories()
				const serverCategories = res.data || []
				
				// 使用后台返回的分类
				if (serverCategories.length > 0) {
					this.categories = serverCategories.map(cat => ({
						id: cat.id,
						name: cat.name
					}))
					this.activeCategory = this.categories[0]?.id || 0
				}
			} catch (e) {
				console.error('加载分类失败', e)
			}
		},
		
		// 加载项目列表
		async loadProjects(isRefresh = false) {
			if (this.loading) return
			
			this.loading = true
			
			try {
				if (isRefresh) {
					this.page = 1
					this.noMore = false
				}
				
				const res = await api.getProjects({ 
					page: this.page, 
					page_size: this.pageSize,
					category_id: this.activeCategory
				})
				
				const newProjects = res.data?.items || res.data?.list || []
				
				if (isRefresh) {
					this.projects = newProjects
				} else {
					this.projects = [...this.projects, ...newProjects]
				}
				
				if (newProjects.length < this.pageSize) {
					this.noMore = true
				}
				
			} catch (e) {
				console.error('加载项目失败', e)
				uni.showToast({
					title: '加载失败',
					icon: 'none'
				})
			} finally {
				this.loading = false
			}
		},
		
		// 选择分类
		selectCategory(category) {
			this.activeCategory = category.id
			this.loadProjects(true)
		},
		
		// 顶部筛选
		handleTopFilter(type) {
			uni.showToast({
				title: '筛选功能开发中',
				icon: 'none'
			})
		},
		
		// 加载更多
		loadMore() {
			if (!this.loading && !this.noMore) {
				this.page++
				this.loadProjects()
			}
		},
		
		// 搜索
		goSearch() {
			uni.showToast({
				title: '搜索功能开发中',
				icon: 'none'
			})
		},
		
		// 跳转项目详情
		goProjectDetail(project) {
			uni.navigateTo({
				url: `/pages/project/detail?id=${project.id}`
			})
		},
		
		// 立即预约
		goBooking(project) {
			uni.navigateTo({
				url: `/pagesA/booking/booking?projectId=${project.id}&projectName=${encodeURIComponent(project.name)}`
			})
		}
	}
}
</script>

<style lang="scss" scoped>
.category-page {
	display: flex;
	flex-direction: column;
	height: 100vh;
	background: #f5f5f5;
}

/* 顶部标题 */
.page-header {
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	padding: 20rpx 30rpx;
	padding-top: calc(20rpx + env(safe-area-inset-top));
	
	.header-title {
		font-size: 36rpx;
		font-weight: bold;
		color: white;
	}
}

/* 搜索栏 */
.search-bar {
	background: white;
	padding: 20rpx 30rpx;
	
	.search-input {
		display: flex;
		align-items: center;
		height: 70rpx;
		padding: 0 20rpx;
		background: #f5f5f5;
		border-radius: 35rpx;
		
		.search-icon {
			font-size: 32rpx;
			margin-right: 15rpx;
		}
		
		.search-placeholder {
			font-size: 28rpx;
			color: #999;
		}
	}
}

/* 顶部筛选标签 */
.top-filters {
	background: white;
	border-bottom: 1rpx solid #e0e0e0;
	
	.filter-scroll {
		white-space: nowrap;
		padding: 0 20rpx;
		
		.filter-item {
			display: inline-block;
			padding: 20rpx 30rpx;
			font-size: 28rpx;
			color: #666;
			position: relative;
			
			&.active {
				color: #4facfe;
				font-weight: bold;
				
				&::after {
					content: '';
					position: absolute;
					bottom: 0;
					left: 30rpx;
					right: 30rpx;
					height: 4rpx;
					background: #4facfe;
					border-radius: 2rpx;
				}
			}
			
			.arrow {
				margin-left: 5rpx;
				font-size: 20rpx;
			}
		}
	}
}

/* 主内容区 */
.main-content {
	display: flex;
	flex: 1;
	overflow: hidden;
}

/* 左侧分类菜单 */
.left-menu {
	width: 180rpx;
	background: white;
	
	.menu-item {
		padding: 30rpx 20rpx;
		text-align: center;
		font-size: 28rpx;
		color: #333;
		position: relative;
		
		&.active {
			background: #f0f8ff;
			color: #4facfe;
			font-weight: bold;
			
			&::before {
				content: '';
				position: absolute;
				left: 0;
				top: 50%;
				transform: translateY(-50%);
				width: 6rpx;
				height: 40rpx;
				background: #4facfe;
				border-radius: 0 3rpx 3rpx 0;
			}
		}
	}
}

/* 右侧内容区 */
.right-content {
	flex: 1;
	background: #f5f5f5;
	
	.project-list {
		padding: 20rpx;
		
		.project-card {
			background: white;
			border-radius: 12rpx;
			margin-bottom: 20rpx;
			overflow: hidden;
			box-shadow: 0 2rpx 10rpx rgba(0,0,0,0.05);
			
			.project-image {
				width: 100%;
				height: 300rpx;
			}
			
			.project-info {
				padding: 20rpx;
				
				.project-name {
					font-size: 32rpx;
					font-weight: bold;
					color: #333;
					display: block;
					margin-bottom: 15rpx;
				}
				
				.project-stats {
					display: flex;
					gap: 30rpx;
					margin-bottom: 20rpx;
					
					.stat-item {
						font-size: 24rpx;
						color: #999;
					}
				}
				
				.project-footer {
					display: flex;
					justify-content: center;
					
					.btn-book {
						width: 200rpx;
						height: 60rpx;
						line-height: 60rpx;
						background: white;
						border: 2rpx solid #4facfe;
						border-radius: 30rpx;
						font-size: 26rpx;
						color: #4facfe;
						padding: 0;
						
						&::after {
							border: none;
						}
					}
				}
			}
		}
	}
	
	.loading-more,
	.no-more {
		padding: 30rpx;
		text-align: center;
		font-size: 24rpx;
		color: #999;
	}
}
</style>
