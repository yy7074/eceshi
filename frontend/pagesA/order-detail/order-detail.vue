<template>
	<view class="order-detail-container">
		<!-- 订单状态 -->
		<view class="status-card card">
			<view class="status-header">
				<text class="status-icon">{{ getStatusIcon(order.status) }}</text>
				<text class="status-text">{{ getStatusText(order.status) }}</text>
			</view>
			<text class="status-desc">{{ getStatusDesc(order.status) }}</text>
			
			<!-- 状态时间轴 -->
			<view class="timeline">
				<view 
					v-for="(item, index) in statusTimeline" 
					:key="index"
					class="timeline-item"
					:class="{ active: item.completed }"
				>
					<view class="timeline-dot"></view>
					<view class="timeline-content">
						<text class="timeline-status">{{ item.label }}</text>
						<text v-if="item.time" class="timeline-time">{{ item.time }}</text>
					</view>
				</view>
			</view>
		</view>
		
		<!-- 订单信息 -->
		<view class="info-card card">
			<view class="section-title">订单信息</view>
			<view class="info-row">
				<text class="label">订单号</text>
				<view class="value-copy">
					<text class="value">{{ order.order_no }}</text>
					<text class="copy-btn" @click="copyOrderNo">复制</text>
				</view>
			</view>
			<view class="info-row">
				<text class="label">项目名称</text>
				<text class="value">{{ order.project_name }}</text>
			</view>
			<view class="info-row">
				<text class="label">实验室</text>
				<text class="value">{{ order.lab_name }}</text>
			</view>
			<view class="info-row">
				<text class="label">创建时间</text>
				<text class="value">{{ formatTime(order.created_at) }}</text>
			</view>
		</view>
		
		<!-- 样品信息 -->
		<view class="samples-card card">
			<view class="section-title">样品信息</view>
			<view v-for="(sample, index) in order.samples" :key="sample.id" class="sample-item">
				<view class="sample-header">
					<text class="sample-name">{{ sample.sample_name }}</text>
					<text class="sample-qty">×{{ sample.quantity }}</text>
				</view>
				<text v-if="sample.sample_type" class="sample-type">类型：{{ sample.sample_type }}</text>
				<text v-if="sample.sample_desc" class="sample-desc">{{ sample.sample_desc }}</text>
				
				<!-- 样品照片 -->
				<view v-if="sample.photos && sample.photos.length > 0" class="sample-photos">
					<image 
						v-for="(photo, pIndex) in sample.photos" 
						:key="pIndex"
						:src="photo" 
						mode="aspectFill" 
						class="photo"
						@click="previewImage(sample.photos, pIndex)"
					></image>
				</view>
			</view>
		</view>
		
		<!-- 配送信息 -->
		<view v-if="order.shipping_method" class="shipping-card card">
			<view class="section-title">配送信息</view>
			<view class="info-row">
				<text class="label">配送方式</text>
				<text class="value">{{ getShippingText(order.shipping_method) }}</text>
			</view>
			<view v-if="order.receiver_name" class="address-info">
				<text class="receiver">{{ order.receiver_name }} {{ order.receiver_phone }}</text>
				<text class="address">{{ order.receiver_address }}</text>
			</view>
		</view>
		
		<!-- 费用明细 -->
		<view class="fee-card card">
			<view class="section-title">费用明细</view>
			<view class="fee-item">
				<text class="label">检测费用</text>
				<text class="value">¥{{ order.project_fee }}</text>
			</view>
			<view v-if="order.urgent_fee > 0" class="fee-item">
				<text class="label">加急费用</text>
				<text class="value">¥{{ order.urgent_fee }}</text>
			</view>
			<view v-if="order.shipping_fee > 0" class="fee-item">
				<text class="label">运费</text>
				<text class="value">¥{{ order.shipping_fee }}</text>
			</view>
			<view v-if="order.discount_amount > 0" class="fee-item discount">
				<text class="label">优惠</text>
				<text class="value">-¥{{ order.discount_amount }}</text>
			</view>
			<view class="fee-divider"></view>
			<view class="fee-item total">
				<text class="label">实付金额</text>
				<text class="value">¥{{ order.total_fee }}</text>
			</view>
		</view>
		
		<!-- 备注 -->
		<view v-if="order.remark" class="remark-card card">
			<view class="section-title">订单备注</view>
			<text class="remark-text">{{ order.remark }}</text>
		</view>
		
		<!-- 底部操作栏 -->
		<view class="bottom-bar">
			<view class="actions">
				<!-- 待支付 -->
				<button v-if="order.status === 'pending_payment'" class="btn btn-default" @click="cancelOrder">
					取消订单
				</button>
				<button v-if="order.status === 'pending_payment'" class="btn btn-primary" @click="goPay">
					去支付
				</button>
				
				<!-- 已完成 -->
				<button v-if="order.status === 'completed' && !order.evaluated" class="btn btn-primary" @click="goEvaluate">
					评价
				</button>
				
				<!-- 联系客服 -->
				<button class="btn btn-default" @click="contactService">
					联系客服
				</button>
			</view>
		</view>
	</view>
</template>

<script>
	import api from '@/utils/api.js'
	
	export default {
		data() {
			return {
				orderId: null,
				order: {
					order_no: '',
					status: '',
					project_name: '',
					lab_name: '',
					samples: [],
					created_at: '',
					project_fee: 0,
					urgent_fee: 0,
					shipping_fee: 0,
					discount_amount: 0,
					total_fee: 0,
					shipping_method: '',
					receiver_name: '',
					receiver_phone: '',
					receiver_address: '',
					remark: ''
				},
				statusTimeline: []
			}
		},
		onLoad(options) {
			this.orderId = options.id
			this.loadOrderDetail()
		},
		methods: {
			// 加载订单详情
			async loadOrderDetail() {
				try {
					const res = await api.getOrderDetail(this.orderId)
					this.order = res.data
					this.buildTimeline()
				} catch (error) {
					console.error('加载订单失败', error)
					uni.showToast({
						title: '加载失败',
						icon: 'none'
					})
				}
			},
			
			// 构建时间轴
			buildTimeline() {
				const timeline = [
					{ 
						label: '提交订单', 
						time: this.formatTime(this.order.created_at),
						completed: true 
					},
					{ 
						label: '支付完成', 
						time: this.order.paid_at ? this.formatTime(this.order.paid_at) : '',
						completed: this.order.paid_at != null 
					},
					{ 
						label: '实验中', 
						time: this.order.started_at ? this.formatTime(this.order.started_at) : '',
						completed: this.order.started_at != null 
					},
					{ 
						label: '已完成', 
						time: this.order.completed_at ? this.formatTime(this.order.completed_at) : '',
						completed: this.order.completed_at != null 
					}
				]
				this.statusTimeline = timeline
			},
			
			// 获取状态图标
			getStatusIcon(status) {
				const map = {
					'pending_payment': '⏰',
					'confirmed': '✅',
					'waiting_test': '📦',
					'in_progress': '🔬',
					'completed': '🎉',
					'cancelled': '❌'
				}
				return map[status] || '📋'
			},
			
			// 获取状态文本
			getStatusText(status) {
				const map = {
					'pending_payment': '待支付',
					'confirmed': '已确认',
					'waiting_test': '待试验',
					'in_progress': '实验中',
					'completed': '已完成',
					'cancelled': '已取消'
				}
				return map[status] || status
			},
			
			// 获取状态描述
			getStatusDesc(status) {
				const map = {
					'pending_payment': '请尽快完成支付',
					'confirmed': '实验室已确认接单，等待您寄送样品',
					'waiting_test': '样品已送达，等待开始实验',
					'in_progress': '实验正在进行中，请耐心等待',
					'completed': '实验已完成，可以下载数据',
					'cancelled': '订单已取消'
				}
				return map[status] || ''
			},
			
			// 获取配送方式文本
			getShippingText(method) {
				const map = {
					'self': '自送样品',
					'express': '快递寄送',
					'platform': '平台代收'
				}
				return map[method] || method
			},
			
			// 格式化时间
			formatTime(time) {
				if (!time) return ''
				const date = new Date(time)
				const Y = date.getFullYear()
				const M = (date.getMonth() + 1).toString().padStart(2, '0')
				const D = date.getDate().toString().padStart(2, '0')
				const h = date.getHours().toString().padStart(2, '0')
				const m = date.getMinutes().toString().padStart(2, '0')
				return `${Y}-${M}-${D} ${h}:${m}`
			},
			
			// 复制订单号
			copyOrderNo() {
				uni.setClipboardData({
					data: this.order.order_no,
					success: () => {
						uni.showToast({
							title: '已复制',
							icon: 'success'
						})
					}
				})
			},
			
			// 预览图片
			previewImage(photos, index) {
				uni.previewImage({
					urls: photos,
					current: index
				})
			},
			
			// 取消订单
			cancelOrder() {
				uni.showModal({
					title: '确认取消',
					content: '确定要取消这个订单吗？',
					success: async (res) => {
						if (res.confirm) {
							try {
								await api.cancelOrder(this.orderId, {
									reason: '不想买了'
								})
								uni.showToast({
									title: '已取消',
									icon: 'success'
								})
								this.loadOrderDetail()
							} catch (error) {
								console.error('取消失败', error)
								uni.showToast({
									title: '取消失败',
									icon: 'none'
								})
							}
						}
					}
				})
			},
			
			// 去支付
			goPay() {
				uni.navigateTo({
					url: `/pagesA/payment/payment?order_id=${this.orderId}`
				})
			},
			
			// 去评价
			goEvaluate() {
				uni.navigateTo({
					url: `/pagesA/evaluate/evaluate?order_id=${this.orderId}`
				})
			},
			
			// 联系客服
			contactService() {
				uni.showModal({
					title: '联系客服',
					content: '客服电话：400-XXX-XXXX\n工作时间：9:00-18:00',
					showCancel: false
				})
			}
		}
	}
</script>

<style lang="scss" scoped>
	.order-detail-container {
		min-height: 100vh;
		background-color: #f8f8f8;
		padding: 20rpx 30rpx 160rpx;
	}
	
	.status-card {
		padding: 40rpx 30rpx;
		margin-bottom: 20rpx;
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		color: #ffffff;
		
		.status-header {
			display: flex;
			align-items: center;
			margin-bottom: 16rpx;
			
			.status-icon {
				font-size: 48rpx;
				margin-right: 20rpx;
			}
			
			.status-text {
				font-size: 36rpx;
				font-weight: bold;
			}
		}
		
		.status-desc {
			display: block;
			font-size: 26rpx;
			opacity: 0.9;
			margin-bottom: 30rpx;
		}
		
		.timeline {
			.timeline-item {
				display: flex;
				padding-left: 40rpx;
				position: relative;
				padding-bottom: 30rpx;
				
				&:last-child {
					padding-bottom: 0;
				}
				
				&::before {
					content: '';
					position: absolute;
					left: 14rpx;
					top: 30rpx;
					bottom: 0;
					width: 2rpx;
					background-color: rgba(255, 255, 255, 0.3);
				}
				
				&:last-child::before {
					display: none;
				}
				
				.timeline-dot {
					position: absolute;
					left: 0;
					top: 8rpx;
					width: 28rpx;
					height: 28rpx;
					border-radius: 50%;
					background-color: rgba(255, 255, 255, 0.3);
				}
				
				&.active .timeline-dot {
					background-color: #ffffff;
				}
				
				.timeline-content {
					flex: 1;
					
					.timeline-status {
						display: block;
						font-size: 28rpx;
						margin-bottom: 8rpx;
					}
					
					.timeline-time {
						display: block;
						font-size: 24rpx;
						opacity: 0.8;
					}
				}
			}
		}
	}
	
	.info-card, .samples-card, .shipping-card, .fee-card, .remark-card {
		padding: 30rpx;
		margin-bottom: 20rpx;
		
		.section-title {
			font-size: 32rpx;
			font-weight: bold;
			color: #333;
			margin-bottom: 24rpx;
		}
		
		.info-row {
			display: flex;
			justify-content: space-between;
			align-items: center;
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
				text-align: right;
			}
			
			.value-copy {
				display: flex;
				align-items: center;
				
				.copy-btn {
					margin-left: 16rpx;
					padding: 4rpx 16rpx;
					background-color: #f5f5f5;
					color: #007AFF;
					font-size: 24rpx;
					border-radius: 8rpx;
				}
			}
		}
	}
	
	.samples-card {
		.sample-item {
			padding: 24rpx 0;
			border-bottom: 2rpx solid #f5f5f5;
			
			&:last-child {
				border-bottom: none;
			}
			
			.sample-header {
				display: flex;
				justify-content: space-between;
				align-items: center;
				margin-bottom: 12rpx;
				
				.sample-name {
					font-size: 30rpx;
					font-weight: bold;
					color: #333;
				}
				
				.sample-qty {
					font-size: 26rpx;
					color: #999;
				}
			}
			
			.sample-type, .sample-desc {
				display: block;
				font-size: 26rpx;
				color: #666;
				line-height: 1.6;
				margin-bottom: 8rpx;
			}
			
			.sample-photos {
				display: flex;
				flex-wrap: wrap;
				gap: 16rpx;
				margin-top: 16rpx;
				
				.photo {
					width: 150rpx;
					height: 150rpx;
					border-radius: 12rpx;
				}
			}
		}
	}
	
	.shipping-card {
		.address-info {
			padding-top: 16rpx;
			
			.receiver {
				display: block;
				font-size: 28rpx;
				font-weight: bold;
				color: #333;
				margin-bottom: 12rpx;
			}
			
			.address {
				display: block;
				font-size: 26rpx;
				color: #666;
				line-height: 1.6;
			}
		}
	}
	
	.fee-card {
		.fee-item {
			display: flex;
			justify-content: space-between;
			padding: 20rpx 0;
			
			.label {
				font-size: 28rpx;
				color: #666;
			}
			
			.value {
				font-size: 28rpx;
				color: #333;
			}
			
			&.discount .value {
				color: #52c41a;
			}
			
			&.total {
				padding-top: 24rpx;
				
				.label {
					font-size: 30rpx;
					font-weight: bold;
					color: #333;
				}
				
				.value {
					font-size: 36rpx;
					font-weight: bold;
					color: #ff4d4f;
				}
			}
		}
		
		.fee-divider {
			height: 2rpx;
			background-color: #f0f0f0;
			margin: 10rpx 0;
		}
	}
	
	.remark-card {
		.remark-text {
			display: block;
			font-size: 26rpx;
			color: #666;
			line-height: 1.6;
		}
	}
	
	.bottom-bar {
		position: fixed;
		bottom: 0;
		left: 0;
		right: 0;
		padding: 20rpx 30rpx;
		background-color: #ffffff;
		box-shadow: 0 -4rpx 12rpx rgba(0, 0, 0, 0.08);
		
		.actions {
			display: flex;
			justify-content: flex-end;
			gap: 16rpx;
			
			.btn {
				padding: 0 40rpx;
				height: 72rpx;
				line-height: 72rpx;
				border-radius: 36rpx;
				font-size: 28rpx;
				border: none;
				
				&.btn-default {
					background-color: #f5f5f5;
					color: #666;
				}
				
				&.btn-primary {
					background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
					color: #ffffff;
				}
			}
		}
	}
</style>

