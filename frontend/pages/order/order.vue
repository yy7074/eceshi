<template>
	<view class="order-container">
		<!-- Tab栏 -->
		<view class="tabs">
			<view 
				v-for="tab in tabs" 
				:key="tab.key"
				class="tab-item"
				:class="{ active: currentTab === tab.key }"
				@click="switchTab(tab.key)"
			>
				<text class="tab-text">{{ tab.label }}</text>
				<view v-if="tab.count > 0" class="badge">{{ tab.count }}</view>
			</view>
		</view>
		
		<!-- 订单列表 -->
		<scroll-view 
			class="order-list" 
			scroll-y
			refresher-enabled
			:refresher-triggered="refreshing"
			@refresherrefresh="onRefresh"
			@scrolltolower="loadMore"
		>
			<view v-if="loading && orders.length === 0" class="loading-state">
				<text>加载中...</text>
			</view>
			
			<view v-else-if="orders.length > 0">
				<view 
					v-for="item in orders" 
					:key="item.id" 
					class="order-item"
					@click="goOrderDetail(item)"
				>
					<!-- 订单头部 -->
					<view class="order-header">
						<text class="order-no">订单号：{{ item.order_no }}</text>
						<text class="order-status" :class="'status-' + item.status">
							{{ getStatusText(item.status) }}
						</text>
					</view>
					
					<!-- 订单内容 -->
					<view class="order-content">
						<image 
							:src="item.cover_image || item.project_image || 'https://picsum.photos/200/200'" 
							mode="aspectFill" 
							class="project-image"
						></image>
						<view class="order-info">
							<text class="project-name">{{ item.project_name }}</text>
							<text class="sample-info">样品数量：{{ item.sample_count }}</text>
							<text class="order-date">{{ formatDate(item.created_at) }}</text>
						</view>
					</view>
					
					<!-- 订单金额 -->
					<view class="order-footer">
						<text class="total-amount">
							总计：<text class="amount">¥{{ formatMoney(getOrderAmount(item)) }}</text>
						</text>
						
						<!-- 操作按钮 -->
						<view class="actions" @click.stop>
							<button 
								v-if="isPendingPayment(item.status)" 
								class="btn-action primary"
								@click="payOrder(item)"
							>
								立即支付
							</button>
							<button 
								v-if="isPendingPayment(item.status)" 
								class="btn-action"
								@click="cancelOrder(item)"
							>
								取消订单
							</button>
							<button 
								v-if="['paid', 'confirmed', 'testing'].includes(item.status)" 
								class="btn-action"
								@click="goSampleTrack(item)"
							>
								样品追踪
							</button>
							<button 
								v-if="item.status === 'completed'" 
								class="btn-action"
								@click="downloadReport(item)"
							>
								下载报告
							</button>
							<button 
								v-if="item.status === 'completed'" 
								class="btn-action primary"
								@click="reorder(item)"
							>
								再来一单
							</button>
						</view>
					</view>
				</view>
			</view>
			
			<view v-else class="empty-state">
				<text class="empty-icon">📋</text>
				<text class="empty-text">暂无订单</text>
				<button class="btn-go-booking" @click="goHome">去预约</button>
			</view>
			
			<!-- 加载更多 -->
			<view v-if="loadingMore" class="loading-more">
				<text>加载中...</text>
			</view>
			<view v-if="!loading && !loadingMore && noMore && orders.length > 0" class="no-more">
				<text>没有更多了</text>
			</view>
		</scroll-view>
	</view>
</template>

<script>
import api from '@/utils/api.js'

export default {
	data() {
		return {
			currentTab: 'all',
			tabs: [
				{ key: 'all', label: '全部', count: 0 },
				{ key: 'unpaid', label: '待支付', count: 0 },
				{ key: 'paid', label: '待确认', count: 0 },
				{ key: 'testing', label: '实验中', count: 0 },
				{ key: 'completed', label: '已完成', count: 0 }
			],
			orders: [],
			loading: false,
			loadingMore: false,
			refreshing: false,
			noMore: false,
			page: 1,
			pageSize: 10
		}
	},
	onLoad(options) {
		// 如果有状态参数，切换到对应tab
		if (options.status) {
			this.currentTab = options.status
		}
		
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
		
		this.loadOrders()
	},
	onShow() {
		// 检查是否有状态筛选参数（从个人中心跳转过来）
		const statusFilter = uni.getStorageSync('order_status_filter')
		if (statusFilter) {
			this.currentTab = statusFilter
			uni.removeStorageSync('order_status_filter') // 使用后删除
		}
		
		// 每次显示页面时刷新
		const token = uni.getStorageSync('token')
		if (token) {
			this.loadOrders(true)
		}
	},
	methods: {
		// 切换Tab
		switchTab(key) {
			if (this.currentTab === key) return
			this.currentTab = key
			this.loadOrders(true)
		},
		
		// 加载订单列表
		async loadOrders(refresh = false) {
			if (refresh) {
				this.page = 1
				this.noMore = false
				this.orders = []
			}
			
			if (this.loading || this.loadingMore) return
			
			if (refresh) {
				this.loading = true
			} else {
				this.loadingMore = true
			}
			
			try {
				const params = {
					page: this.page,
					page_size: this.pageSize
				}
				
				if (this.currentTab !== 'all') {
					params.status = this.currentTab
				}
				
				const res = await api.getOrders(params)
				const newOrders = res.data?.items || res.data?.list || []
				
				if (refresh) {
					this.orders = newOrders
				} else {
					this.orders = [...this.orders, ...newOrders]
				}
				
				if (newOrders.length < this.pageSize) {
					this.noMore = true
				}
				
			} catch (e) {
				console.error('加载订单失败', e)
				uni.showToast({
					title: '加载失败',
					icon: 'none'
				})
			} finally {
				this.loading = false
				this.loadingMore = false
				this.refreshing = false
			}
		},
		
		// 下拉刷新
		onRefresh() {
			this.refreshing = true
			this.loadOrders(true)
		},
		
		// 加载更多
		loadMore() {
			if (!this.noMore && !this.loading && !this.loadingMore) {
				this.page++
				this.loadOrders()
			}
		},
		
		// 获取状态文本
		getStatusText(status) {
			const statusMap = {
				'unpaid': '待支付',
				'pending_payment': '待支付',
				'paid': '待确认',
				'confirmed': '待实验',
				'accepted': '待实验',
				'sample_received': '已签收',
				'testing': '实验中',
				'completed': '已完成',
				'cancelled': '已取消'
			}
			return statusMap[status] || status
		},

		isPendingPayment(status) {
			return ['unpaid', 'pending_payment'].includes(status)
		},

		getOrderAmount(order) {
			const amount = order.total_fee !== undefined && order.total_fee !== null
				? order.total_fee
				: order.total_amount
			return Number(amount || 0)
		},

		formatMoney(amount) {
			const value = Number(amount)
			return Number.isFinite(value) ? value.toFixed(2) : '0.00'
		},
		
		// 格式化日期
		formatDate(dateStr) {
			if (!dateStr) return ''
			const date = new Date(dateStr)
			const Y = date.getFullYear()
			const M = String(date.getMonth() + 1).padStart(2, '0')
			const D = String(date.getDate()).padStart(2, '0')
			return `${Y}-${M}-${D}`
		},
		
		// 跳转订单详情
		goOrderDetail(order) {
			uni.navigateTo({
				url: `/pagesA/order-detail/order-detail?id=${order.id}`
			})
		},
		
		// 支付订单
		async payOrder(order) {
			uni.showLoading({ title: '正在支付...' })
			
			try {
				const res = await api.creditPay({
					order_id: order.id,
					amount: this.getOrderAmount(order)
				})
				
				uni.hideLoading()
				uni.showToast({ title: res.message || '信用支付成功', icon: 'success' })
				this.loadOrders(true)
			} catch (e) {
				uni.hideLoading()
				console.error('支付失败', e)
				uni.showToast({
					title: e.message || e.detail || '支付失败',
					icon: 'none'
				})
			}
		},
		
		// 取消订单
		async cancelOrder(order) {
			uni.showModal({
				title: '确认取消',
				content: '确定要取消这个订单吗？',
				success: async (res) => {
					if (res.confirm) {
						try {
							await api.cancelOrder(order.id, {
								reason: '不想要了'
							})
							uni.showToast({ title: '订单已取消', icon: 'success' })
							this.loadOrders(true)
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
		
		// 评价订单
		reviewOrder(order) {
			uni.navigateTo({
				url: `/pagesA/review/review?orderId=${order.id}`
			})
		},
		
		// 再次预约
		reorder(order) {
			uni.navigateTo({
				url: `/pagesA/booking/booking?projectId=${order.project_id}&projectName=${encodeURIComponent(order.project_name)}`
			})
		},
		
		// 样品追踪
		goSampleTrack(order) {
			uni.navigateTo({
				url: `/pagesA/sample-track/sample-track?orderId=${order.id}&orderNo=${order.order_no}`
			})
		},
		
		// 下载报告
		async downloadReport(order) {
			uni.showLoading({ title: '准备下载...' })
			try {
				const res = await api.getReportByOrder(order.id)
				const report = res.data || {}
				const reportUrl = report.file_url || order.report_url

				if (!reportUrl) {
					uni.hideLoading()
					uni.showModal({
						title: '报告下载',
						content: '当前订单暂未生成可下载的报告。',
						showCancel: false
					})
					return
				}

				const downloadUrl = reportUrl.startsWith('http')
					? reportUrl
					: `${api.baseUrl}${reportUrl}`

				uni.downloadFile({
					url: downloadUrl,
					success: (downloadRes) => {
						uni.hideLoading()
						if (downloadRes.statusCode === 200) {
							uni.openDocument({
								filePath: downloadRes.tempFilePath,
								showMenu: true
							})
							return
						}
						uni.showToast({ title: '下载失败', icon: 'none' })
					},
					fail: () => {
						uni.hideLoading()
						uni.showToast({ title: '下载失败', icon: 'none' })
					}
				})
			} catch (e) {
				uni.hideLoading()
				uni.showToast({
					title: e.message || '报告暂未生成',
					icon: 'none'
				})
			}
		},
		
		// 回到首页
		goHome() {
			uni.switchTab({
				url: '/pages/index/index'
			})
		}
	}
}
</script>

<style lang="scss" scoped>
.order-container {
	display: flex;
	flex-direction: column;
	height: 100vh;
	background: #f5f5f5;
}

/* Tab栏 */
.tabs {
	display: flex;
	background: white;
	padding: 0 20rpx;
	position: sticky;
	top: 0;
	z-index: 10;
	
	.tab-item {
		flex: 1;
		text-align: center;
		padding: 25rpx 0;
		position: relative;
		
		.tab-text {
			font-size: 28rpx;
			color: #666;
		}
		
		.badge {
			position: absolute;
			top: 15rpx;
			right: 15%;
			background: #ff6b6b;
			color: white;
			font-size: 20rpx;
			padding: 2rpx 10rpx;
			border-radius: 20rpx;
			min-width: 30rpx;
			text-align: center;
		}
		
		&.active {
			.tab-text {
				color: #4facfe;
				font-weight: bold;
			}
			
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

/* 订单列表 */
.order-list {
	flex: 1;
	padding: 20rpx;
}

.order-item {
	background: white;
	border-radius: 12rpx;
	margin-bottom: 20rpx;
	overflow: hidden;
	
	.order-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 25rpx 30rpx;
		border-bottom: 1rpx solid #f0f0f0;
		
		.order-no {
			font-size: 26rpx;
			color: #666;
		}
		
		.order-status {
			font-size: 26rpx;
			font-weight: bold;
			
			&.status-unpaid,
			&.status-pending_payment {
				color: #ff9500;
			}
			
			&.status-paid,
			&.status-confirmed {
				color: #4facfe;
			}
			
			&.status-testing {
				color: #9c27b0;
			}
			
			&.status-completed {
				color: #4caf50;
			}
			
			&.status-cancelled {
				color: #999;
			}
		}
	}
	
	.order-content {
		display: flex;
		padding: 25rpx 30rpx;
		
		.project-image {
			width: 160rpx;
			height: 160rpx;
			border-radius: 8rpx;
			margin-right: 20rpx;
		}
		
		.order-info {
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
			
			.sample-info,
			.order-date {
				font-size: 24rpx;
				color: #999;
				margin-bottom: 5rpx;
			}
		}
	}
	
	.order-footer {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 25rpx 30rpx;
		border-top: 1rpx solid #f0f0f0;
		
		.total-amount {
			font-size: 26rpx;
			color: #666;
			
			.amount {
				font-size: 32rpx;
				font-weight: bold;
				color: #ff6b6b;
			}
		}
		
		.actions {
			display: flex;
			gap: 15rpx;
			
			.btn-action {
				height: 60rpx;
				line-height: 60rpx;
				padding: 0 25rpx;
				background: white;
				color: #666;
				border: 2rpx solid #e0e0e0;
				border-radius: 30rpx;
				font-size: 24rpx;
				
				&::after {
					border: none;
				}
				
				&.primary {
					background: #4facfe;
					color: white;
					border-color: #4facfe;
				}
			}
		}
	}
}

/* 空状态 */
.loading-state,
.empty-state {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 150rpx 0;
	
	.empty-icon {
		font-size: 100rpx;
		margin-bottom: 30rpx;
	}
	
	.empty-text {
		font-size: 28rpx;
		color: #999;
		margin-bottom: 40rpx;
	}
	
	.btn-go-booking {
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

.loading-more,
.no-more {
	text-align: center;
	padding: 30rpx 0;
	font-size: 24rpx;
	color: #999;
}
</style>
