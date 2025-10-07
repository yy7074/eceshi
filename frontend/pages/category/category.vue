<template>
	<view class="category-container">
		<!-- 搜索栏 -->
		<view class="search-bar">
			<view class="search-input" @click="goSearch">
				<text class="icon">🔍</text>
				<text class="placeholder">搜索检测项目</text>
			</view>
		</view>
		
		<!-- 分类列表 -->
		<view class="category-list">
			<view 
				v-for="item in categories" 
				:key="item.id" 
				class="category-item card"
				@click="selectCategory(item)"
			>
				<view class="category-icon">{{ item.icon || '📊' }}</view>
				<view class="category-info">
					<text class="category-name">{{ item.name }}</text>
					<text class="category-desc">{{ item.description }}</text>
				</view>
				<view v-if="item.hot" class="hot-badge">热门</view>
			</view>
		</view>
		
		<!-- 项目列表 -->
		<view v-if="selectedCategory" class="project-section">
			<view class="section-header">
				<text class="title">{{ selectedCategory.name }}</text>
				<text class="count">共{{ projects.length }}个项目</text>
			</view>
			
			<view class="project-list">
				<view 
					v-for="item in projects" 
					:key="item.id" 
					class="project-item card"
					@click="goProjectDetail(item)"
				>
					<image :src="item.cover_image" mode="aspectFill" class="project-image"></image>
					<view class="project-info">
						<text class="project-name">{{ item.name }}</text>
						<text class="project-lab">{{ item.lab_name }}</text>
						<view class="project-footer">
							<view class="price">
								<text class="current-price">¥{{ item.current_price }}</text>
								<text class="original-price">¥{{ item.original_price }}</text>
							</view>
							<view class="stats">
								<text class="satisfaction">满意度{{ item.satisfaction }}%</text>
							</view>
						</view>
					</view>
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
				categories: [],
				selectedCategory: null,
				projects: []
			}
		},
		onLoad(options) {
			this.loadCategories()
			// 如果有传入分类ID，直接加载该分类
			if (options.id) {
				this.loadProjects(options.id)
			}
		},
		methods: {
			// 加载分类
			async loadCategories() {
				try {
					const res = await api.getCategories()
					this.categories = res.data || []
				} catch (error) {
					console.error('加载分类失败', error)
				}
			},
			
			// 选择分类
			async selectCategory(category) {
				this.selectedCategory = category
				await this.loadProjects(category.id)
			},
			
			// 加载项目列表
			async loadProjects(categoryId) {
				try {
					const res = await api.getProjects({
						category_id: categoryId,
						page: 1,
						page_size: 20
					})
					this.projects = res.data?.list || []
				} catch (error) {
					console.error('加载项目失败', error)
				}
			},
			
			// 跳转搜索
			goSearch() {
				uni.navigateTo({
					url: '/pages/search/search'
				})
			},
			
			// 跳转项目详情
			goProjectDetail(item) {
				uni.navigateTo({
					url: `/pages/project/detail?id=${item.id}`
				})
			}
		}
	}
</script>

<style lang="scss" scoped>
	.category-container {
		min-height: 100vh;
		background-color: #f8f8f8;
		padding-bottom: 20rpx;
	}
	
	.search-bar {
		padding: 20rpx 30rpx;
		background-color: #ffffff;
		
		.search-input {
			display: flex;
			align-items: center;
			padding: 16rpx 24rpx;
			background-color: #f5f5f5;
			border-radius: 50rpx;
			
			.icon {
				margin-right: 12rpx;
			}
			
			.placeholder {
				color: #999;
				font-size: 28rpx;
			}
		}
	}
	
	.category-list {
		padding: 20rpx 30rpx;
		
		.category-item {
			display: flex;
			align-items: center;
			padding: 30rpx;
			margin-bottom: 20rpx;
			position: relative;
			
			.category-icon {
				width: 88rpx;
				height: 88rpx;
				background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
				border-radius: 16rpx;
				display: flex;
				align-items: center;
				justify-content: center;
				font-size: 48rpx;
				margin-right: 24rpx;
			}
			
			.category-info {
				flex: 1;
				
				.category-name {
					display: block;
					font-size: 32rpx;
					font-weight: bold;
					color: #333;
					margin-bottom: 12rpx;
				}
				
				.category-desc {
					display: block;
					font-size: 24rpx;
					color: #999;
				}
			}
			
			.hot-badge {
				position: absolute;
				top: 20rpx;
				right: 20rpx;
				padding: 6rpx 16rpx;
				background-color: #ff4d4f;
				color: #ffffff;
				font-size: 20rpx;
				border-radius: 20rpx;
			}
		}
	}
	
	.project-section {
		padding: 0 30rpx;
		
		.section-header {
			display: flex;
			justify-content: space-between;
			align-items: center;
			padding: 30rpx 0;
			
			.title {
				font-size: 36rpx;
				font-weight: bold;
				color: #333;
			}
			
			.count {
				font-size: 26rpx;
				color: #999;
			}
		}
		
		.project-list {
			.project-item {
				display: flex;
				margin-bottom: 24rpx;
				
				.project-image {
					width: 200rpx;
					height: 150rpx;
					border-radius: 12rpx;
					flex-shrink: 0;
				}
				
				.project-info {
					flex: 1;
					margin-left: 24rpx;
					display: flex;
					flex-direction: column;
					justify-content: space-between;
					
					.project-name {
						font-size: 32rpx;
						font-weight: 500;
						color: #333;
						margin-bottom: 8rpx;
					}
					
					.project-lab {
						font-size: 24rpx;
						color: #999;
					}
					
					.project-footer {
						display: flex;
						justify-content: space-between;
						align-items: center;
						
						.price {
							.current-price {
								font-size: 36rpx;
								color: #ff4d4f;
								font-weight: bold;
							}
							
							.original-price {
								margin-left: 12rpx;
								font-size: 24rpx;
								color: #999;
								text-decoration: line-through;
							}
						}
						
						.stats {
							.satisfaction {
								font-size: 22rpx;
								color: #52c41a;
							}
						}
					}
				}
			}
		}
	}
</style>

