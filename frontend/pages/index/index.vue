<template>
	<view class="container">
		<!-- 搜索栏 -->
		<view class="search-bar">
			<view class="search-input" @click="goSearch">
				<text class="iconfont icon-search"></text>
				<text class="placeholder">搜索检测项目</text>
			</view>
		</view>
		
		<!-- 轮播图 -->
		<view class="banner">
			<swiper class="swiper" indicator-dots circular autoplay>
				<swiper-item v-for="(item, index) in banners" :key="index">
					<image :src="item.image" mode="aspectFill" class="banner-image"></image>
				</swiper-item>
			</swiper>
		</view>
		
		<!-- 分类导航 -->
		<view class="category-nav">
			<view class="category-item" v-for="item in categories" :key="item.id" @click="goCategory(item)">
				<image :src="item.icon" mode="aspectFit" class="category-icon"></image>
				<text class="category-name">{{ item.name }}</text>
			</view>
		</view>
		
		<!-- 热门项目 -->
		<view class="hot-projects">
			<view class="section-title">
				<text class="title-text">热门项目</text>
				<text class="more" @click="goProjectList">查看更多 ></text>
			</view>
			
			<view class="project-list">
				<view class="project-item card" v-for="item in projects" :key="item.id" @click="goProjectDetail(item)">
					<image :src="item.cover_image" mode="aspectFill" class="project-image"></image>
					<view class="project-info">
						<text class="project-name">{{ item.name }}</text>
						<text class="project-lab">{{ item.lab_name }}</text>
						<view class="project-footer">
							<view class="price">
								<text class="current-price">¥{{ item.current_price }}</text>
								<text class="original-price">¥{{ item.original_price }}</text>
							</view>
							<view class="booking">
								<text class="booking-count">{{ item.booking_count }}次预约</text>
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
				banners: [
					{ image: 'https://via.placeholder.com/750x300' },
					{ image: 'https://via.placeholder.com/750x300' },
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
					this.categories = categoryRes.data || []
					
					// 加载热门项目
					const projectRes = await api.getProjects({ page: 1, page_size: 10 })
					this.projects = projectRes.data?.list || []
				} catch (e) {
					console.error('加载数据失败', e)
				}
			},
			goSearch() {
				uni.navigateTo({
					url: '/pages/search/search'
				})
			},
			goCategory(item) {
				uni.navigateTo({
					url: `/pages/category/category?id=${item.id}`
				})
			},
			goProjectList() {
				uni.switchTab({
					url: '/pages/category/category'
				})
			},
			goProjectDetail(item) {
				uni.navigateTo({
					url: `/pages/project/detail?id=${item.id}`
				})
			}
		}
	}
</script>

<style lang="scss" scoped>
	.container {
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
			
			.placeholder {
				margin-left: 12rpx;
				color: #999;
				font-size: 28rpx;
			}
		}
	}
	
	.banner {
		margin: 20rpx 30rpx;
		border-radius: 16rpx;
		overflow: hidden;
		
		.swiper {
			height: 300rpx;
			
			.banner-image {
				width: 100%;
				height: 100%;
			}
		}
	}
	
	.category-nav {
		display: flex;
		justify-content: space-around;
		padding: 40rpx 30rpx;
		background-color: #ffffff;
		margin: 20rpx 30rpx;
		border-radius: 16rpx;
		
		.category-item {
			display: flex;
			flex-direction: column;
			align-items: center;
			
			.category-icon {
				width: 80rpx;
				height: 80rpx;
				margin-bottom: 12rpx;
			}
			
			.category-name {
				font-size: 24rpx;
				color: #333;
			}
		}
	}
	
	.hot-projects {
		padding: 0 30rpx;
		
		.section-title {
			display: flex;
			justify-content: space-between;
			align-items: center;
			padding: 30rpx 0;
			
			.title-text {
				font-size: 36rpx;
				font-weight: bold;
				color: #333;
			}
			
			.more {
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
						
						.booking-count {
							font-size: 22rpx;
							color: #999;
						}
					}
				}
			}
		}
	}
</style>

