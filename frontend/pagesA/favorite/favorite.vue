<template>
	<view class="favorite-page">
		<!-- 顶部Tab -->
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
		
		<!-- 项目列表 -->
		<view v-if="projects.length > 0" class="projects-list">
			<view v-for="(item, index) in projects" :key="index" class="project-item" @click="goProjectDetail(item.id)">
				<image :src="item.cover_image || 'https://picsum.photos/200/200'" mode="aspectFill" class="project-image"></image>
				<view class="project-info">
					<text class="project-name">{{ item.name }}</text>
					<text class="project-lab">{{ item.lab_name }}</text>
					<view class="project-stats">
						<text class="stat-item">满意度 {{ item.satisfaction }}%</text>
						<text class="stat-item">已测{{ item.order_count }}次</text>
					</view>
					<view class="project-footer">
						<view class="project-price">
							<text class="current-price">¥{{ item.current_price }}</text>
							<text v-if="item.original_price > item.current_price" class="original-price">¥{{ item.original_price }}</text>
						</view>
						<button class="action-btn" @click.stop="handleAction(item)">
							{{ currentTab === 0 ? '立即预约' : '再次预约' }}
						</button>
					</view>
				</view>
				<view class="unfavorite-btn" @click.stop="unfavoriteProject(item)">
					<text class="icon">💔</text>
				</view>
			</view>
		</view>
		
		<!-- 空状态 -->
		<view v-else class="empty-state">
			<text class="empty-icon">⭐</text>
			<text class="empty-text">{{ currentTab === 0 ? '还没有收藏项目' : '还没有浏览历史' }}</text>
			<button class="go-browse-btn" @click="goBrowse">去逛逛</button>
		</view>
	</view>
</template>

<script>
import api from '@/utils/api.js'

export default {
	data() {
		return {
			currentTab: 0,
			tabs: ['我的收藏', '浏览历史'],
			projects: []
		}
	},
	
	onLoad() {
		this.loadProjects()
	},
	
	onShow() {
		// 返回时刷新
		this.loadProjects()
	},
	
	methods: {
		// 切换Tab
		switchTab(index) {
			this.currentTab = index
			this.loadProjects()
		},
		
		// 加载项目列表
		async loadProjects() {
			try {
				uni.showLoading({ title: '加载中...' })
				
				if (this.currentTab === 0) {
					// TODO: 调用API获取收藏列表
					this.projects = []
				} else {
					// TODO: 调用API获取浏览历史
					this.projects = []
				}
				
				uni.hideLoading()
			} catch (error) {
				uni.hideLoading()
				console.error('加载项目失败', error)
				uni.showToast({
					title: '加载失败',
					icon: 'none'
				})
			}
		},
		
		// 跳转项目详情
		goProjectDetail(projectId) {
			uni.navigateTo({
				url: `/pages/project/detail?id=${projectId}`
			})
		},
		
		// 取消收藏
		unfavoriteProject(item) {
			uni.showModal({
				title: '提示',
				content: `确定要取消收藏"${item.name}"吗？`,
				success: (res) => {
					if (res.confirm) {
						// TODO: 调用API取消收藏
						uni.showToast({
							title: '已取消收藏',
							icon: 'success'
						})
						
						// 从列表中移除
						const index = this.projects.findIndex(p => p.id === item.id)
						if (index > -1) {
							this.projects.splice(index, 1)
						}
					}
				}
			})
		},
		
		// 处理操作
		handleAction(item) {
			// 检查登录
			const token = uni.getStorageSync('token')
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
			
			// 跳转预约页面
			uni.navigateTo({
				url: `/pagesA/booking/booking?projectId=${item.id}&projectName=${item.name}`
			})
		},
		
		// 去逛逛
		goBrowse() {
			uni.switchTab({
				url: '/pages/index/index'
			})
		}
	}
}
</script>

<style lang="scss" scoped>
.favorite-page {
	min-height: 100vh;
	background: #f5f5f5;
}

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
			color: #667eea;
			font-weight: bold;
			
			&::after {
				content: '';
				position: absolute;
				bottom: 0;
				left: 50%;
				transform: translateX(-50%);
				width: 60rpx;
				height: 4rpx;
				background: #667eea;
				border-radius: 2rpx;
			}
		}
	}
}

.projects-list {
	padding: 20rpx 30rpx;
	
	.project-item {
		background: white;
		border-radius: 16rpx;
		padding: 20rpx;
		margin-bottom: 20rpx;
		display: flex;
		position: relative;
		
		.project-image {
			width: 200rpx;
			height: 200rpx;
			border-radius: 12rpx;
			flex-shrink: 0;
			margin-right: 20rpx;
		}
		
		.project-info {
			flex: 1;
			display: flex;
			flex-direction: column;
			justify-content: space-between;
			
			.project-name {
				font-size: 28rpx;
				font-weight: bold;
				color: #333;
				margin-bottom: 10rpx;
				overflow: hidden;
				text-overflow: ellipsis;
				white-space: nowrap;
			}
			
			.project-lab {
				font-size: 24rpx;
				color: #999;
				margin-bottom: 10rpx;
			}
			
			.project-stats {
				display: flex;
				gap: 20rpx;
				margin-bottom: 15rpx;
				
				.stat-item {
					font-size: 22rpx;
					color: #999;
				}
			}
			
			.project-footer {
				display: flex;
				justify-content: space-between;
				align-items: center;
				
				.project-price {
					display: flex;
					align-items: baseline;
					gap: 10rpx;
					
					.current-price {
						font-size: 32rpx;
						font-weight: bold;
						color: #ff4444;
					}
					
					.original-price {
						font-size: 24rpx;
						color: #999;
						text-decoration: line-through;
					}
				}
				
				.action-btn {
					background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
					color: white;
					border: none;
					border-radius: 50rpx;
					padding: 15rpx 35rpx;
					font-size: 24rpx;
				}
			}
		}
		
		.unfavorite-btn {
			position: absolute;
			top: 20rpx;
			right: 20rpx;
			width: 60rpx;
			height: 60rpx;
			background: rgba(255, 255, 255, 0.9);
			border-radius: 50%;
			display: flex;
			align-items: center;
			justify-content: center;
			box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.1);
			
			.icon {
				font-size: 32rpx;
			}
		}
	}
}

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
	
	.go-browse-btn {
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		color: white;
		border: none;
		border-radius: 50rpx;
		padding: 25rpx 60rpx;
		font-size: 28rpx;
	}
}
</style>

