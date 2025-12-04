<template>
	<view class="order-detail-page">
		<view v-if="loading" class="loading-state">
			<text>加载中...</text>
		</view>
		
		<view v-else-if="order.id">
			<!-- 订单状态 -->
			<view class="status-card">
				<view class="status-icon" :class="'status-' + order.status">
					<text class="icon">{{ getStatusIcon() }}</text>
				</view>
				<text class="status-text">{{ getStatusText() }}</text>
				<text class="status-desc">{{ getStatusDesc() }}</text>
			</view>
			
			<!-- 项目信息 -->
			<view class="section-card">
				<view class="section-title">项目信息</view>
				<view class="project-info">
					<image 
						:src="order.cover_image || 'https://picsum.photos/200/200'" 
						mode="aspectFill" 
						class="project-image"
					></image>
					<view class="project-text">
						<text class="project-name">{{ order.project_name }}</text>
						<text class="project-lab">{{ order.lab_name }}</text>
						<text class="sample-count">样品数量：{{ order.sample_count }}</text>
					</view>
				</view>
			</view>
			
			<!-- 样品信息 -->
			<view class="section-card" v-if="order.sample_name">
				<view class="section-title">样品信息</view>
				<view class="info-row">
					<text class="label">样品名称</text>
					<text class="value">{{ order.sample_name }}</text>
				</view>
				<view class="info-row" v-if="order.sample_composition">
					<text class="label">样品成分</text>
					<text class="value">{{ order.sample_composition }}</text>
				</view>
				<view class="info-row" v-if="order.sample_state">
					<text class="label">样品状态</text>
					<text class="value">{{ order.sample_state }}</text>
				</view>
				<view class="info-row" v-if="order.remark">
					<text class="label">备注</text>
					<text class="value">{{ order.remark }}</text>
				</view>
			</view>
			
			<!-- 配送信息 -->
			<view class="section-card" v-if="order.address">
				<view class="section-title">配送信息</view>
				<view class="address-info">
					<view class="address-header">
						<text class="name">{{ order.address.name }}</text>
						<text class="phone">{{ order.address.phone }}</text>
					</view>
					<text class="address-detail">
						{{ order.address.province }}{{ order.address.city }}{{ order.address.district }}{{ order.address.detail }}
					</text>
				</view>
				<view class="info-row" v-if="order.delivery_method">
					<text class="label">寄送方式</text>
					<text class="value">{{ order.delivery_method === 'express' ? '快递' : '自送' }}</text>
				</view>
				<view class="info-row" v-if="order.delivery_date">
					<text class="label">期望送达</text>
					<text class="value">{{ order.delivery_date }}</text>
				</view>
			</view>
			
			<!-- 物流信息 -->
			<view class="section-card" v-if="order.logistics_info">
				<view class="section-title">物流信息</view>
				<view class="info-row">
					<text class="label">物流公司</text>
					<text class="value">{{ order.logistics_company }}</text>
				</view>
				<view class="info-row">
					<text class="label">快递单号</text>
					<text class="value">{{ order.logistics_no }}</text>
					<text class="copy-btn" @click="copyLogisticsNo">复制</text>
				</view>
			</view>
			
			<!-- 费用明细 -->
			<view class="section-card">
				<view class="section-title">费用明细</view>
				<view class="fee-row">
					<text class="label">测试费用</text>
					<text class="value">¥{{ order.service_amount || '0.00' }}</text>
				</view>
				<view class="fee-row" v-if="order.delivery_fee">
					<text class="label">配送费用</text>
					<text class="value">¥{{ order.delivery_fee }}</text>
				</view>
				<view class="fee-row total">
					<text class="label">总计</text>
					<text class="value">¥{{ order.total_amount }}</text>
				</view>
			</view>
			
			<!-- 订单信息 -->
			<view class="section-card">
				<view class="section-title">订单信息</view>
				<view class="info-row">
					<text class="label">订单号</text>
					<text class="value">{{ order.order_no }}</text>
				</view>
				<view class="info-row">
					<text class="label">创建时间</text>
					<text class="value">{{ formatDateTime(order.created_at) }}</text>
				</view>
				<view class="info-row" v-if="order.paid_at">
					<text class="label">支付时间</text>
					<text class="value">{{ formatDateTime(order.paid_at) }}</text>
				</view>
				<view class="info-row" v-if="order.completed_at">
					<text class="label">完成时间</text>
					<text class="value">{{ formatDateTime(order.completed_at) }}</text>
				</view>
			</view>
		</view>
		
		<view v-else class="error-state">
			<text class="error-icon">⚠️</text>
			<text class="error-text">订单不存在</text>
		</view>
		
		<!-- 快捷操作 -->
		<view class="quick-actions" v-if="['paid', 'confirmed', 'testing', 'completed'].includes(order.status)">
			<view class="action-item" @click="goSampleTrack">
				<text class="action-icon">📦</text>
				<text class="action-text">样品追踪</text>
			</view>
			<view class="action-item" v-if="order.status === 'completed'" @click="downloadReport">
				<text class="action-icon">📊</text>
				<text class="action-text">下载报告</text>
			</view>
			<view class="action-item" @click="goChat">
				<text class="action-icon">💬</text>
				<text class="action-text">在线客服</text>
			</view>
			<view class="action-item" v-if="order.status === 'completed'" @click="goReview">
				<text class="action-icon">⭐</text>
				<text class="action-text">评价订单</text>
			</view>
		</view>
		
		<!-- 底部操作栏 -->
		<view class="bottom-bar" v-if="order.id">
			<button 
				v-if="order.status === 'unpaid'" 
				class="btn-action secondary"
				@click="cancelOrder"
			>
				取消订单
			</button>
			<button 
				v-if="order.status === 'unpaid'" 
				class="btn-action primary"
				@click="payOrder"
			>
				立即支付
			</button>
			<button 
				v-if="['paid', 'confirmed'].includes(order.status)" 
				class="btn-action secondary"
				@click="goSampleTrack"
			>
				样品追踪
			</button>
			<button 
				v-if="order.status === 'completed'" 
				class="btn-action secondary"
				@click="downloadReport"
			>
				下载报告
			</button>
			<button 
				v-if="order.status === 'completed'" 
				class="btn-action primary"
				@click="reorder"
			>
				再次预约
			</button>
		</view>
	</view>
</template>

<script>
import api from '@/utils/api.js'

export default {
	data() {
		return {
			orderId: null,
			loading: true,
			order: {}
		}
	},
	onLoad(options) {
		if (options.id) {
			this.orderId = options.id
			this.loadOrderDetail()
		}
	},
	methods: {
		// 加载订单详情
		async loadOrderDetail() {
			this.loading = true
			try {
				const res = await api.getOrderDetail(this.orderId)
				this.order = res.data || {}
			} catch (e) {
				console.error('加载订单详情失败', e)
				uni.showToast({
					title: '加载失败',
					icon: 'none'
				})
			} finally {
				this.loading = false
			}
		},
		
		// 获取状态图标
		getStatusIcon() {
			const iconMap = {
				'unpaid': '💳',
				'paid': '⏰',
				'confirmed': '📝',
				'testing': '🔬',
				'completed': '✅',
				'cancelled': '❌'
			}
			return iconMap[this.order.status] || '📋'
		},
		
		// 获取状态文本
		getStatusText() {
			const statusMap = {
				'unpaid': '待支付',
				'paid': '待确认',
				'confirmed': '待实验',
				'testing': '实验中',
				'completed': '已完成',
				'cancelled': '已取消'
			}
			return statusMap[this.order.status] || this.order.status
		},
		
		// 获取状态描述
		getStatusDesc() {
			const descMap = {
				'unpaid': '请尽快完成支付',
				'paid': '我们正在确认您的订单',
				'confirmed': '您的样品正在排队中',
				'testing': '实验正在进行中，请耐心等待',
				'completed': '订单已完成，感谢您的使用',
				'cancelled': '订单已取消'
			}
			return descMap[this.order.status] || ''
		},
		
		// 格式化日期时间
		formatDateTime(dateStr) {
			if (!dateStr) return ''
			const date = new Date(dateStr)
			const Y = date.getFullYear()
			const M = String(date.getMonth() + 1).padStart(2, '0')
			const D = String(date.getDate()).padStart(2, '0')
			const h = String(date.getHours()).padStart(2, '0')
			const m = String(date.getMinutes()).padStart(2, '0')
			return `${Y}-${M}-${D} ${h}:${m}`
		},
		
		// 复制物流单号
		copyLogisticsNo() {
			uni.setClipboardData({
				data: this.order.logistics_no,
				success: () => {
					uni.showToast({
						title: '已复制',
						icon: 'success'
					})
				}
			})
		},
		
		// 支付订单
		async payOrder() {
			uni.showLoading({ title: '正在跳转...' })
			
			try {
				const res = await api.createPayment({
					order_id: this.order.id,
					payment_method: 'wechat'
				})
				
				uni.hideLoading()
				
				uni.requestPayment({
					provider: 'wxpay',
					timeStamp: res.data.timeStamp,
					nonceStr: res.data.nonceStr,
					package: res.data.package,
					signType: res.data.signType,
					paySign: res.data.paySign,
					success: () => {
						uni.showToast({ title: '支付成功', icon: 'success' })
						setTimeout(() => {
							this.loadOrderDetail()
						}, 1500)
					},
					fail: () => {
						uni.showToast({ title: '支付取消', icon: 'none' })
					}
				})
			} catch (e) {
				uni.hideLoading()
				console.error('支付失败', e)
				uni.showToast({
					title: e.message || '支付失败',
					icon: 'none'
				})
			}
		},
		
		// 取消订单
		async cancelOrder() {
			uni.showModal({
				title: '确认取消',
				content: '确定要取消这个订单吗？',
				success: async (res) => {
					if (res.confirm) {
						try {
							await api.cancelOrder(this.order.id, {
								reason: '不想要了'
							})
							uni.showToast({ title: '订单已取消', icon: 'success' })
							setTimeout(() => {
								this.loadOrderDetail()
							}, 1500)
						} catch (e) {
							console.error('取消订单失败', e)
							uni.showToast({
								title: '取消失败',
								icon: 'none'
							})
						}
					}
				}
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
		
		// 再次预约
		reorder() {
			uni.navigateTo({
				url: `/pagesA/booking/booking?projectId=${this.order.project_id}&projectName=${encodeURIComponent(this.order.project_name)}`
			})
		},
		
		// 样品追踪
		goSampleTrack() {
			uni.navigateTo({
				url: `/pagesA/sample-track/sample-track?orderId=${this.order.id}&orderNo=${this.order.order_no}`
			})
		},
		
		// 下载报告
		downloadReport() {
			uni.showLoading({ title: '准备下载...' })
			
			// 模拟下载过程
			setTimeout(() => {
				uni.hideLoading()
				uni.showModal({
					title: '报告下载',
					content: '检测报告已生成，请选择操作',
					confirmText: '下载',
					cancelText: '预览',
					success: (res) => {
						if (res.confirm) {
							uni.showToast({ title: '报告下载中...', icon: 'loading' })
							setTimeout(() => {
								uni.showToast({ title: '下载成功', icon: 'success' })
							}, 2000)
						} else {
							// 预览
							uni.showModal({
								title: '报告预览',
								content: `项目：${this.order.project_name}\n订单号：${this.order.order_no}\n\n报告内容正在加载...`,
								showCancel: false
							})
						}
					}
				})
			}, 1000)
		},
		
		// 在线客服
		goChat() {
			uni.navigateTo({ url: '/pagesA/chat/chat' })
		},
		
		// 评价订单
		goReview() {
			uni.navigateTo({
				url: `/pagesA/review/review?orderId=${this.order.id}`
			})
		}
	}
}
</script>

<style lang="scss" scoped>
.order-detail-page {
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
	}
}

/* 状态卡片 */
.status-card {
	background: #1890ff;
	padding: 60rpx 30rpx;
	display: flex;
	flex-direction: column;
	align-items: center;
	
	.status-icon {
		width: 120rpx;
		height: 120rpx;
		border-radius: 60rpx;
		background: rgba(255, 255, 255, 0.9);
		display: flex;
		align-items: center;
		justify-content: center;
		margin-bottom: 25rpx;
		
		.icon {
			font-size: 60rpx;
		}
	}
	
	.status-text {
		font-size: 36rpx;
		font-weight: bold;
		color: white;
		margin-bottom: 15rpx;
	}
	
	.status-desc {
		font-size: 26rpx;
		color: rgba(255, 255, 255, 0.9);
	}
}

/* 区块卡片 */
.section-card {
	background: white;
	margin: 20rpx;
	padding: 30rpx;
	border-radius: 12rpx;
	
	.section-title {
		font-size: 32rpx;
		font-weight: bold;
		color: #333;
		margin-bottom: 25rpx;
		padding-bottom: 20rpx;
		border-bottom: 1rpx solid #f0f0f0;
	}
}

/* 项目信息 */
.project-info {
	display: flex;
	
	.project-image {
		width: 160rpx;
		height: 160rpx;
		border-radius: 8rpx;
		margin-right: 20rpx;
	}
	
	.project-text {
		flex: 1;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		
		.project-name {
			font-size: 30rpx;
			font-weight: bold;
			color: #333;
			margin-bottom: 10rpx;
		}
		
		.project-lab,
		.sample-count {
			font-size: 24rpx;
			color: #999;
			margin-bottom: 5rpx;
		}
	}
}

/* 信息行 */
.info-row {
	display: flex;
	justify-content: space-between;
	align-items: center;
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
		flex: 1;
		font-size: 28rpx;
		color: #333;
		text-align: right;
		margin-left: 30rpx;
	}
	
	.copy-btn {
		margin-left: 15rpx;
		padding: 5rpx 15rpx;
		background: #4facfe;
		color: white;
		border-radius: 6rpx;
		font-size: 22rpx;
	}
}

/* 地址信息 */
.address-info {
	padding: 25rpx;
	background: #f5f8ff;
	border-radius: 8rpx;
	margin-bottom: 20rpx;
	
	.address-header {
		display: flex;
		justify-content: space-between;
		margin-bottom: 15rpx;
		
		.name {
			font-size: 30rpx;
			font-weight: bold;
			color: #333;
		}
		
		.phone {
			font-size: 28rpx;
			color: #666;
		}
	}
	
	.address-detail {
		font-size: 26rpx;
		color: #666;
		line-height: 1.6;
		display: block;
	}
}

/* 费用行 */
.fee-row {
	display: flex;
	justify-content: space-between;
	padding: 20rpx 0;
	border-bottom: 1rpx solid #f0f0f0;
	
	&:last-child {
		border-bottom: none;
	}
	
	&.total {
		border-top: 2rpx solid #333;
		margin-top: 10rpx;
		padding-top: 25rpx;
		
		.label,
		.value {
			font-size: 32rpx;
			font-weight: bold;
			color: #ff6b6b;
		}
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

/* 快捷操作 */
.quick-actions {
	display: flex;
	background: #fff;
	margin: 20rpx;
	border-radius: 12rpx;
	padding: 24rpx 0;
	
	.action-item {
		flex: 1;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 12rpx;
		
		.action-icon {
			font-size: 48rpx;
		}
		
		.action-text {
			font-size: 24rpx;
			color: #666;
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
	gap: 20rpx;
	box-shadow: 0 -2rpx 10rpx rgba(0, 0, 0, 0.05);
	z-index: 100;
	
	.btn-action {
		flex: 1;
		height: 80rpx;
		line-height: 80rpx;
		text-align: center;
		border-radius: 40rpx;
		font-size: 30rpx;
		border: none;
		
		&::after {
			border: none;
		}
		
		&.secondary {
			background: #f0f0f0;
			color: #666;
		}
		
		&.primary {
			background: #4facfe;
			color: white;
			font-weight: bold;
		}
	}
}
</style>
