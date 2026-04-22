<template>
	<view class="track-page">
		<!-- 订单信息卡片 -->
		<view class="order-card">
			<view class="order-header">
				<text class="order-title">订单信息</text>
				<text class="order-no">{{ orderInfo.orderNo }}</text>
			</view>
			<view class="order-info">
				<view class="info-item">
					<text class="label">检测项目</text>
					<text class="value">{{ orderInfo.projectName }}</text>
				</view>
				<view class="info-item">
					<text class="label">样品名称</text>
					<text class="value">{{ orderInfo.sampleName }}</text>
				</view>
				<view class="info-item">
					<text class="label">下单时间</text>
					<text class="value">{{ orderInfo.createdAt }}</text>
				</view>
			</view>
		</view>
		
		<!-- 物流信息 -->
		<view class="express-card" v-if="expressInfo.trackingNo">
			<view class="express-header">
				<text class="express-title">📦 物流信息</text>
				<text class="express-copy" @click="copyTrackingNo">复制单号</text>
			</view>
			<view class="express-info">
				<view class="info-item">
					<text class="label">快递公司</text>
					<text class="value">{{ expressInfo.company }}</text>
				</view>
				<view class="info-item">
					<text class="label">快递单号</text>
					<text class="value">{{ expressInfo.trackingNo }}</text>
				</view>
			</view>
		</view>
		
		<!-- 追踪时间线 -->
		<view class="timeline-card">
			<view class="timeline-header">
				<text class="timeline-title">📍 样品状态</text>
			</view>
			<view class="timeline-content">
				<view class="timeline-item" v-for="(step, index) in trackSteps" :key="step.id" :class="{ active: step.active, first: index === 0 }">
					<view class="timeline-dot"></view>
					<view class="timeline-line" v-if="index < trackSteps.length - 1"></view>
					<view class="timeline-info">
						<view class="timeline-header-row">
							<text class="timeline-title-text">{{ step.title }}</text>
							<text class="timeline-time">{{ step.time }}</text>
						</view>
						<text class="timeline-desc">{{ step.description }}</text>
					</view>
				</view>
			</view>
		</view>
		
		<!-- 操作按钮 -->
		<view class="action-section">
			<view class="action-btn" @click="refreshStatus">
				<text class="btn-icon">🔄</text>
				<text>刷新状态</text>
			</view>
			<view class="action-btn" @click="contactService">
				<text class="btn-icon">💬</text>
				<text>联系客服</text>
			</view>
		</view>
		
		<!-- 寄送提示 -->
		<view class="tips-card" v-if="needShip">
			<view class="tips-header">
				<text class="tips-icon">💡</text>
				<text class="tips-title">寄送提示</text>
			</view>
			<view class="tips-content">
				<text>1. 请将样品妥善包装，避免运输过程中损坏</text>
				<text>2. 建议选择顺丰或圆通等快递</text>
				<text>3. 收件地址：广州市黄埔区科学大道1号岭南产教融合孵化器科技苑C座502室</text>
				<text>4. 收件人：实验室收样组 / 电话：17819781949</text>
			</view>
			<view class="tips-action" @click="fillExpressNo">
				<text>填写快递单号</text>
			</view>
		</view>
	</view>
</template>

<script>
import api from '@/utils/api.js'

export default {
	data() {
		return {
			orderId: '',
			orderInfo: {
				orderNo: '',
				projectName: '',
				sampleName: '',
				createdAt: ''
			},
			expressInfo: {
				company: '',
				trackingNo: ''
			},
			trackSteps: [
				{ id: 1, title: '订单创建', description: '订单已创建，等待支付', time: '', active: true },
				{ id: 2, title: '已支付', description: '订单支付成功', time: '', active: false },
				{ id: 3, title: '样品已寄出', description: '用户已寄出样品', time: '', active: false },
				{ id: 4, title: '样品已签收', description: '实验室已签收样品', time: '', active: false },
				{ id: 5, title: '检测中', description: '样品正在检测中', time: '', active: false },
				{ id: 6, title: '检测完成', description: '检测完成，报告已生成', time: '', active: false }
			],
			needShip: true
		}
	},
	onLoad(options) {
		if (options.orderId) {
			this.orderId = options.orderId
		}
		if (options.orderNo) {
			this.orderInfo.orderNo = options.orderNo
		}
		this.loadTrackInfo()
	},
	methods: {
		async loadTrackInfo() {
			try {
				if (!this.orderId) return

				const orderRes = await api.getOrderDetail(this.orderId)
				const order = orderRes.data || {}

				this.orderInfo = {
					orderNo: order.order_no || this.orderInfo.orderNo || '',
					projectName: order.project_name || '',
					sampleName: order.sample_name || '',
					createdAt: order.created_at?.slice(0, 16).replace('T', ' ') || ''
				}

				this.updateTimeline(order.status)
				this.needShip = ['paid', 'confirmed'].includes(order.status)

				if (order.express_company && order.express_no) {
					this.expressInfo = {
						company: order.express_company,
						trackingNo: order.express_no
					}
				} else {
					this.expressInfo = {
						company: '',
						trackingNo: ''
					}
				}
			} catch (e) {
				console.error('加载追踪信息失败', e)
				this.orderInfo = {
					orderNo: this.orderInfo.orderNo || '',
					projectName: '',
					sampleName: '',
					createdAt: ''
				}
				this.expressInfo = {
					company: '',
					trackingNo: ''
				}
				this.updateTimeline('unpaid')
				this.needShip = false
			}
		},
		
		updateTimeline(status) {
			const statusMap = {
				'unpaid': 1,
				'paid': 2,
				'confirmed': 2,
				'accepted': 3,
				'sample_received': 4,
				'received': 4,
				'testing': 5,
				'completed': 6
			}
			
			const activeIndex = statusMap[status] || 1
			
			this.trackSteps.forEach((step, index) => {
				step.active = index < activeIndex
			})
		},
		
		copyTrackingNo() {
			uni.setClipboardData({
				data: this.expressInfo.trackingNo,
				success: () => {
					uni.showToast({ title: '单号已复制', icon: 'success' })
				}
			})
		},
		
		refreshStatus() {
			uni.showLoading({ title: '刷新中...' })
			setTimeout(() => {
				uni.hideLoading()
				this.loadTrackInfo()
				uni.showToast({ title: '已刷新', icon: 'success' })
			}, 1000)
		},
		
		contactService() {
			uni.navigateTo({ url: '/pagesA/chat/chat' })
		},
		
		fillExpressNo() {
			uni.showModal({
				title: '填写快递单号',
				editable: true,
				placeholderText: '请输入快递单号',
				success: (res) => {
					if (res.confirm && res.content) {
						uni.showToast({ title: '提交成功', icon: 'success' })
						this.expressInfo.trackingNo = res.content
						this.expressInfo.company = '顺丰速运'
						this.needShip = false
					}
				}
			})
		}
	}
}
</script>

<style lang="scss" scoped>
.track-page {
	min-height: 100vh;
	background: #f5f5f5;
	padding: 16rpx 24rpx;
	padding-bottom: 40rpx;
}

.order-card, .express-card, .timeline-card, .tips-card {
	background: #fff;
	border-radius: 12rpx;
	padding: 24rpx;
	margin-bottom: 16rpx;
}

.order-card {
	.order-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 20rpx;
		padding-bottom: 16rpx;
		border-bottom: 1rpx solid #f0f0f0;
		
		.order-title {
			font-size: 30rpx;
			font-weight: 600;
			color: #333;
		}
		
		.order-no {
			font-size: 26rpx;
			color: #1890ff;
		}
	}
	
	.order-info {
		.info-item {
			display: flex;
			margin-bottom: 12rpx;
			
			&:last-child {
				margin-bottom: 0;
			}
			
			.label {
				width: 140rpx;
				font-size: 26rpx;
				color: #999;
			}
			
			.value {
				flex: 1;
				font-size: 26rpx;
				color: #333;
			}
		}
	}
}

.express-card {
	.express-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 16rpx;
		
		.express-title {
			font-size: 30rpx;
			font-weight: 600;
			color: #333;
		}
		
		.express-copy {
			font-size: 26rpx;
			color: #1890ff;
		}
	}
	
	.express-info {
		.info-item {
			display: flex;
			margin-bottom: 8rpx;
			
			.label {
				width: 140rpx;
				font-size: 26rpx;
				color: #999;
			}
			
			.value {
				font-size: 26rpx;
				color: #333;
			}
		}
	}
}

.timeline-card {
	.timeline-header {
		margin-bottom: 24rpx;
		
		.timeline-title {
			font-size: 30rpx;
			font-weight: 600;
			color: #333;
		}
	}
	
	.timeline-content {
		padding-left: 16rpx;
	}
	
	.timeline-item {
		position: relative;
		padding-left: 40rpx;
		padding-bottom: 32rpx;
		
		&:last-child {
			padding-bottom: 0;
		}
		
		.timeline-dot {
			position: absolute;
			left: 0;
			top: 8rpx;
			width: 20rpx;
			height: 20rpx;
			border-radius: 50%;
			background: #d9d9d9;
			z-index: 1;
		}
		
		.timeline-line {
			position: absolute;
			left: 9rpx;
			top: 28rpx;
			width: 2rpx;
			height: calc(100% - 8rpx);
			background: #f0f0f0;
		}
		
		&.active {
			.timeline-dot {
				background: #52c41a;
			}
			
			.timeline-line {
				background: #52c41a;
			}
			
			.timeline-title-text {
				color: #333;
				font-weight: 500;
			}
		}
		
		&.first.active {
			.timeline-dot {
				background: #1890ff;
				box-shadow: 0 0 0 4rpx rgba(24, 144, 255, 0.2);
			}
		}
		
		.timeline-info {
			.timeline-header-row {
				display: flex;
				justify-content: space-between;
				align-items: center;
				margin-bottom: 4rpx;
			}
			
			.timeline-title-text {
				font-size: 28rpx;
				color: #999;
			}
			
			.timeline-time {
				font-size: 24rpx;
				color: #999;
			}
			
			.timeline-desc {
				font-size: 24rpx;
				color: #999;
			}
		}
	}
}

.action-section {
	display: flex;
	gap: 16rpx;
	margin-bottom: 16rpx;
	
	.action-btn {
		flex: 1;
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 12rpx;
		background: #fff;
		padding: 28rpx;
		border-radius: 12rpx;
		
		.btn-icon {
			font-size: 32rpx;
		}
		
		text {
			font-size: 28rpx;
			color: #333;
		}
	}
}

.tips-card {
	background: #fffbe6;
	border: 1rpx solid #ffe58f;
	
	.tips-header {
		display: flex;
		align-items: center;
		margin-bottom: 16rpx;
		
		.tips-icon {
			font-size: 32rpx;
			margin-right: 8rpx;
		}
		
		.tips-title {
			font-size: 28rpx;
			font-weight: 600;
			color: #d48806;
		}
	}
	
	.tips-content {
		text {
			display: block;
			font-size: 26rpx;
			color: #8c6e00;
			line-height: 1.8;
		}
	}
	
	.tips-action {
		margin-top: 20rpx;
		padding: 20rpx;
		background: #faad14;
		border-radius: 8rpx;
		text-align: center;
		
		text {
			font-size: 28rpx;
			color: #fff;
			font-weight: 500;
		}
	}
}
</style>
