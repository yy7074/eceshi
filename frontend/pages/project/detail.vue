<template>
	<view class="detail-container">
		<view v-if="loading" class="loading-state">
			<text>加载中...</text>
		</view>
		
		<view v-else-if="project.id">
			<!-- 轮播图 -->
			<swiper class="swiper" indicator-dots circular autoplay>
				<swiper-item v-for="(img, index) in project.images" :key="index">
					<image :src="img" mode="aspectFill" class="swiper-image"></image>
				</swiper-item>
			</swiper>
			
			<!-- 项目基本信息 -->
			<view class="project-info card">
				<text class="project-name">{{ project.name }}</text>
				<view class="project-meta">
					<text class="lab-name">{{ project.lab_name }}</text>
					<text class="satisfaction">满意度{{ project.satisfaction }}%</text>
				</view>
				<view class="price-row">
					<view class="price">
						<text class="price-symbol">¥</text>
						<text class="current-price">{{ project.current_price }}</text>
						<text class="original-price">¥{{ project.original_price }}</text>
					</view>
					<text class="order-count">{{ project.order_count }}人已预约</text>
				</view>
			</view>
			
			<!-- 服务信息 -->
			<view class="service-info card">
				<view class="info-item">
					<text class="label">项目编号</text>
					<text class="value">{{ project.project_no }}</text>
				</view>
				<view class="info-item" v-if="project.equipment_model">
					<text class="label">仪器型号</text>
					<text class="value">{{ project.equipment_model }}</text>
				</view>
				<view class="info-item" v-if="project.service_cycle_min && project.service_cycle_max">
					<text class="label">服务周期</text>
					<text class="value">{{ project.service_cycle_min }}-{{ project.service_cycle_max }}个工作日</text>
				</view>
				<view class="info-item">
					<text class="label">计费单位</text>
					<text class="value">{{ project.unit || '样品' }}</text>
				</view>
			</view>
			
			<!-- Tab详情 -->
			<view class="detail-tabs card">
				<view class="tabs">
					<view 
						v-for="tab in tabs" 
						:key="tab.key"
						class="tab-item"
						:class="{ active: currentTab === tab.key }"
						@click="switchTab(tab.key)"
					>
						<text>{{ tab.label }}</text>
					</view>
				</view>
				
				<view class="tab-content">
					<!-- 项目介绍 -->
					<view v-if="currentTab === 'intro'" class="content-section">
						<text class="content-text">{{ project.introduction }}</text>
					</view>
					
					<!-- 样品要求 -->
					<view v-if="currentTab === 'sample'" class="content-section">
						<text class="content-text">{{ project.sample_requirements }}</text>
					</view>
					
					<!-- 预约须知 -->
					<view v-if="currentTab === 'notice'" class="content-section">
						<text class="content-text">{{ project.booking_notice }}</text>
					</view>
					
					<!-- 常见问题 -->
					<view v-if="currentTab === 'faq'" class="content-section">
						<view v-if="project.faq && project.faq.length > 0">
							<view v-for="(item, index) in project.faq" :key="index" class="faq-item">
								<text class="faq-question">Q{{ index + 1 }}：{{ item.question }}</text>
								<text class="faq-answer">A：{{ item.answer }}</text>
							</view>
						</view>
						<view v-else class="empty-tip">
							<text>暂无常见问题</text>
						</view>
					</view>
				</view>
			</view>
		</view>
		
		<view v-else class="error-state">
			<text class="error-icon">⚠️</text>
			<text class="error-text">项目不存在或已下架</text>
			<button class="btn-back" @click="goBack">返回</button>
		</view>
		
		<!-- 底部操作栏 -->
		<view class="bottom-bar" v-if="project.id">
			<view class="bar-left">
				<view class="icon-btn" @click="toggleFavorite">
					<text class="icon">{{ isFavorite ? '❤️' : '🤍' }}</text>
					<text class="text">收藏</text>
				</view>
				<view class="icon-btn" @click="contactService">
					<text class="icon">💬</text>
					<text class="text">客服</text>
				</view>
			</view>
			<button class="btn-group" @click="createGroup">发起团购</button>
			<button class="btn-booking" @click="goBooking">立即预约</button>
		</view>
	</view>
</template>

<script>
import api from '@/utils/api.js'

export default {
	data() {
		return {
			projectId: null,
			loading: true,
			project: {},
			currentTab: 'intro',
			tabs: [
				{ key: 'intro', label: '项目介绍' },
				{ key: 'sample', label: '样品要求' },
				{ key: 'notice', label: '预约须知' },
				{ key: 'faq', label: '常见问题' }
			],
			isFavorite: false
		}
	},
	onLoad(options) {
		if (options.id) {
			this.projectId = options.id
			this.loadProject()
		}
	},
	methods: {
		// 加载项目详情
		async loadProject() {
			this.loading = true
			try {
				const res = await api.getProjectDetail(this.projectId)
				this.project = res.data || {}
				
				// 如果没有图片，使用封面图
				if (!this.project.images || this.project.images.length === 0) {
					this.project.images = [this.project.cover_image || 'https://picsum.photos/750/400']
				}
			} catch (e) {
				console.error('加载项目详情失败', e)
				uni.showToast({
					title: '加载失败',
					icon: 'none'
				})
			} finally {
				this.loading = false
			}
		},
		
		// 切换Tab
		switchTab(key) {
			this.currentTab = key
		},
		
		// 收藏/取消收藏
		toggleFavorite() {
			this.isFavorite = !this.isFavorite
			uni.showToast({
				title: this.isFavorite ? '已收藏' : '已取消收藏',
				icon: 'success'
			})
		},
		
		// 联系客服
		contactService() {
			uni.showModal({
				title: '联系客服',
				content: '客服电话：400-123-4567',
				confirmText: '拨打电话',
				success: (res) => {
					if (res.confirm) {
						uni.makePhoneCall({
							phoneNumber: '400-123-4567'
						})
					}
				}
			})
		},
		
		// 立即预约
		goBooking() {
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
			
		uni.navigateTo({
			url: `/pagesA/booking/booking?projectId=${this.projectId}&projectName=${encodeURIComponent(this.project.name)}`
		})
	},
	
	// 创建团购
	createGroup() {
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
		
		// 跳转到创建团购页面
		uni.navigateTo({
			url: `/pagesA/create-group/create-group?projectId=${this.projectId}&projectName=${encodeURIComponent(this.project.name)}&price=${this.project.current_price}`
		})
	},
	
	// 返回
	goBack() {
		uni.navigateBack()
	}
	}
}
</script>

<style lang="scss" scoped>
.detail-container {
	min-height: 100vh;
	background: #f5f5f5;
	padding-bottom: 150rpx;
}

/* 加载/错误状态 */
.loading-state,
.error-state {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 200rpx 0;
	
	.error-icon {
		font-size: 100rpx;
		margin-bottom: 30rpx;
	}
	
	.error-text {
		font-size: 28rpx;
		color: #999;
		margin-bottom: 40rpx;
	}
	
	.btn-back {
		width: 200rpx;
		height: 70rpx;
		line-height: 70rpx;
		background: #4facfe;
		color: white;
		border-radius: 35rpx;
		font-size: 28rpx;
		border: none;
		
		&::after {
			border: none;
		}
	}
}

/* 轮播图 */
.swiper {
	height: 500rpx;
	
	.swiper-image {
		width: 100%;
		height: 100%;
	}
}

/* 卡片通用样式 */
.card {
	background: white;
	margin: 16rpx 24rpx;
	padding: 24rpx;
	border-radius: 12rpx;
	box-shadow: 0 2rpx 8rpx rgba(0,0,0,0.04);
}

/* 项目信息 */
.project-info {
	.project-name {
		font-size: 32rpx;
		font-weight: 600;
		color: #262626;
		display: block;
		margin-bottom: 12rpx;
	}
	
	.project-meta {
		display: flex;
		align-items: center;
		margin-bottom: 16rpx;
		
		.lab-name {
			font-size: 24rpx;
			color: #595959;
			margin-right: 24rpx;
		}
		
		.satisfaction {
			font-size: 24rpx;
			color: #faad14;
		}
	}
	
	.price-row {
		display: flex;
		justify-content: space-between;
		align-items: center;
		
		.price {
			display: flex;
			align-items: baseline;
			
			.price-symbol {
				font-size: 28rpx;
				color: #ff6b6b;
				margin-right: 5rpx;
			}
			
			.current-price {
				font-size: 48rpx;
				font-weight: bold;
				color: #ff6b6b;
				margin-right: 15rpx;
			}
			
			.original-price {
				font-size: 24rpx;
				color: #999;
				text-decoration: line-through;
			}
		}
		
		.order-count {
			font-size: 24rpx;
			color: #999;
		}
	}
}

/* 服务信息 */
.service-info {
	.info-item {
		display: flex;
		justify-content: space-between;
		padding: 20rpx 0;
		border-bottom: 1rpx solid #f0f0f0;
		
		&:last-child {
			border-bottom: none;
		}
		
		.label {
			font-size: 28rpx;
			color: #666;
		}
		
		.value {
			font-size: 28rpx;
			color: #333;
		}
	}
}

/* Tab详情 */
.detail-tabs {
	.tabs {
		display: flex;
		border-bottom: 2rpx solid #f0f0f0;
		margin-bottom: 30rpx;
		
		.tab-item {
			flex: 1;
			text-align: center;
			padding: 20rpx 0;
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
					left: 25%;
					right: 25%;
					height: 4rpx;
					background: #4facfe;
					border-radius: 2rpx;
				}
			}
		}
	}
	
	.tab-content {
		.content-section {
			.content-text {
				font-size: 28rpx;
				color: #666;
				line-height: 1.8;
				display: block;
				white-space: pre-wrap;
			}
			
			.faq-item {
				margin-bottom: 30rpx;
				padding-bottom: 30rpx;
				border-bottom: 1rpx solid #f0f0f0;
				
				&:last-child {
					border-bottom: none;
				}
				
				.faq-question {
					font-size: 28rpx;
					color: #333;
					font-weight: bold;
					display: block;
					margin-bottom: 15rpx;
				}
				
				.faq-answer {
					font-size: 26rpx;
					color: #666;
					line-height: 1.6;
					display: block;
				}
			}
			
			.empty-tip {
				text-align: center;
				padding: 60rpx 0;
				font-size: 26rpx;
				color: #999;
			}
		}
	}
}

/* 底部操作栏 */
.bottom-bar {
	position: fixed;
	bottom: 0;
	left: 0;
	right: 0;
	background: white;
	padding: 20rpx 30rpx;
	padding-bottom: calc(20rpx + env(safe-area-inset-bottom));
	display: flex;
	align-items: center;
	box-shadow: 0 -2rpx 10rpx rgba(0, 0, 0, 0.05);
	z-index: 100;
	
	.bar-left {
		display: flex;
		gap: 30rpx;
		
		.icon-btn {
			display: flex;
			flex-direction: column;
			align-items: center;
			
			.icon {
				font-size: 40rpx;
				margin-bottom: 5rpx;
			}
			
			.text {
				font-size: 22rpx;
				color: #666;
			}
		}
	}
	
	.btn-group {
		margin-left: 20rpx;
		height: 80rpx;
		line-height: 80rpx;
		padding: 0 30rpx;
		background: white;
		color: #667eea;
		border: 2rpx solid #667eea;
		border-radius: 40rpx;
		font-size: 26rpx;
		font-weight: bold;
		
		&::after {
			border: none;
		}
	}
	
	.btn-booking {
		flex: 1;
		margin-left: 20rpx;
		height: 80rpx;
		line-height: 80rpx;
		background: #1890ff;
		color: white;
		border-radius: 40rpx;
		font-size: 30rpx;
		font-weight: bold;
		text-align: center;
		border: none;
		
		&::after {
			border: none;
		}
	}
}
</style>
