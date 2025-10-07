<template>
	<view class="detail-container">
		<!-- 轮播图 -->
		<swiper class="swiper" indicator-dots circular>
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
					<text class="current-price">¥{{ project.current_price }}</text>
					<text class="original-price">¥{{ project.original_price }}</text>
				</view>
				<text class="booking-count">{{ project.booking_count }}人已预约</text>
			</view>
		</view>
		
		<!-- 服务信息 -->
		<view class="service-info card">
			<view class="info-item">
				<text class="label">仪器型号</text>
				<text class="value">{{ project.equipment_model }}</text>
			</view>
			<view class="info-item">
				<text class="label">服务周期</text>
				<text class="value">{{ project.service_cycle_min }}-{{ project.service_cycle_max }}个工作日</text>
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
				<view v-if="currentTab === 'introduction'" class="content-section">
					<rich-text :nodes="project.introduction"></rich-text>
				</view>
				
				<!-- 预约须知 -->
				<view v-if="currentTab === 'notice'" class="content-section">
					<rich-text :nodes="project.booking_notice"></rich-text>
				</view>
				
				<!-- 样品要求 -->
				<view v-if="currentTab === 'requirements'" class="content-section">
					<rich-text :nodes="project.sample_requirements"></rich-text>
				</view>
				
				<!-- 常见问题 -->
				<view v-if="currentTab === 'faq'" class="content-section">
					<view v-for="(item, index) in project.faq" :key="index" class="faq-item">
						<text class="question">Q: {{ item.question }}</text>
						<text class="answer">A: {{ item.answer }}</text>
					</view>
				</view>
			</view>
		</view>
		
		<!-- 底部操作栏 -->
		<view class="bottom-bar">
			<view class="actions">
				<view class="action-item" @click="collectProject">
					<text class="icon">{{ isCollected ? '❤️' : '🤍' }}</text>
					<text class="text">收藏</text>
				</view>
				<view class="action-item" @click="contactService">
					<text class="icon">💬</text>
					<text class="text">咨询</text>
				</view>
			</view>
			<button class="btn-book" @click="goBooking">立即预约</button>
		</view>
	</view>
</template>

<script>
	import api from '@/utils/api.js'
	
	export default {
		data() {
			return {
				projectId: null,
				project: {
					images: [],
					faq: []
				},
				currentTab: 'introduction',
				tabs: [
					{ key: 'introduction', label: '项目介绍' },
					{ key: 'notice', label: '预约须知' },
					{ key: 'requirements', label: '样品要求' },
					{ key: 'faq', label: '常见问题' }
				],
				isCollected: false
			}
		},
		onLoad(options) {
			this.projectId = options.id
			this.loadProjectDetail()
		},
		methods: {
			// 加载项目详情
			async loadProjectDetail() {
				try {
					const res = await api.getProjectDetail(this.projectId)
					this.project = res.data
				} catch (error) {
					console.error('加载项目详情失败', error)
				}
			},
			
			// 切换Tab
			switchTab(key) {
				this.currentTab = key
			},
			
			// 收藏
			collectProject() {
				this.isCollected = !this.isCollected
				uni.showToast({
					title: this.isCollected ? '收藏成功' : '取消收藏',
					icon: 'success'
				})
			},
			
			// 联系客服
			contactService() {
				uni.showModal({
					title: '联系客服',
					content: '客服电话：400-XXX-XXXX',
					showCancel: false
				})
			},
			
			// 去预约
			goBooking() {
				// 检查登录
				if (!this.$store.state.hasLogin) {
					return uni.navigateTo({
						url: '/pages/login/login'
					})
				}
				
				// 跳转预约页面
				uni.navigateTo({
					url: `/pagesA/booking/booking?project_id=${this.projectId}`
				})
			}
		}
	}
</script>

<style lang="scss" scoped>
	.detail-container {
		min-height: 100vh;
		background-color: #f8f8f8;
		padding-bottom: 140rpx;
	}
	
	.swiper {
		width: 100%;
		height: 500rpx;
		
		.swiper-image {
			width: 100%;
			height: 100%;
		}
	}
	
	.project-info {
		margin: 20rpx 30rpx;
		padding: 30rpx;
		
		.project-name {
			display: block;
			font-size: 36rpx;
			font-weight: bold;
			color: #333;
			margin-bottom: 20rpx;
		}
		
		.project-meta {
			display: flex;
			justify-content: space-between;
			margin-bottom: 24rpx;
			
			.lab-name {
				font-size: 26rpx;
				color: #666;
			}
			
			.satisfaction {
				font-size: 26rpx;
				color: #52c41a;
			}
		}
		
		.price-row {
			display: flex;
			justify-content: space-between;
			align-items: center;
			
			.price {
				.current-price {
					font-size: 40rpx;
					font-weight: bold;
					color: #ff4d4f;
				}
				
				.original-price {
					margin-left: 16rpx;
					font-size: 28rpx;
					color: #999;
					text-decoration: line-through;
				}
			}
			
			.booking-count {
				font-size: 24rpx;
				color: #999;
			}
		}
	}
	
	.service-info {
		margin: 0 30rpx 20rpx;
		padding: 30rpx;
		
		.info-item {
			display: flex;
			justify-content: space-between;
			padding: 20rpx 0;
			border-bottom: 2rpx solid #f5f5f5;
			
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
	
	.detail-tabs {
		margin: 0 30rpx;
		padding: 0;
		
		.tabs {
			display: flex;
			border-bottom: 2rpx solid #f5f5f5;
			
			.tab-item {
				flex: 1;
				text-align: center;
				padding: 30rpx 0;
				font-size: 28rpx;
				color: #666;
				
				&.active {
					color: #007AFF;
					font-weight: bold;
					border-bottom: 4rpx solid #007AFF;
				}
			}
		}
		
		.tab-content {
			padding: 30rpx;
			
			.content-section {
				line-height: 1.8;
				color: #333;
				font-size: 28rpx;
			}
			
			.faq-item {
				margin-bottom: 30rpx;
				
				.question {
					display: block;
					font-size: 28rpx;
					font-weight: bold;
					color: #333;
					margin-bottom: 12rpx;
				}
				
				.answer {
					display: block;
					font-size: 26rpx;
					color: #666;
					line-height: 1.6;
				}
			}
		}
	}
	
	.bottom-bar {
		position: fixed;
		bottom: 0;
		left: 0;
		right: 0;
		display: flex;
		align-items: center;
		padding: 20rpx 30rpx;
		background-color: #ffffff;
		box-shadow: 0 -4rpx 12rpx rgba(0, 0, 0, 0.08);
		
		.actions {
			display: flex;
			gap: 40rpx;
			
			.action-item {
				display: flex;
				flex-direction: column;
				align-items: center;
				
				.icon {
					font-size: 40rpx;
					margin-bottom: 8rpx;
				}
				
				.text {
					font-size: 22rpx;
					color: #666;
				}
			}
		}
		
		.btn-book {
			flex: 1;
			margin-left: 40rpx;
			height: 80rpx;
			line-height: 80rpx;
			background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
			color: #ffffff;
			border-radius: 40rpx;
			font-size: 32rpx;
			border: none;
		}
	}
</style>

