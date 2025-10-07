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
			@scrolltolower="loadMore"
		>
			<view v-if="orders.length > 0">
				<view 
					v-for="item in orders" 
					:key="item.id" 
					class="order-item card"
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
							:src="item.project_image || '/static/default-project.png'" 
							mode="aspectFill" 
							class="project-image"
						></image>
						<view class="order-info">
							<text class="project-name">{{ item.project_name }}</text>
							<text class="lab-name">{{ item.lab_name }}</text>
							<text class="sample-count">样品数量：{{ item.sample_count }}</text>
						</view>
					</view>
					
					<!-- 订单底部 -->
					<view class="order-footer">
						<view class="price-info">
							<text class="label">实付金额：</text>
							<text class="price">¥{{ item.total_fee }}</text>
						</view>
						<view class="actions">
							<button 
								v-if="item.status === 'pending_payment'"
								class="btn btn-primary"
								@click.stop="goPay(item)"
							>
								去支付
							</button>
							<button 
								v-if="item.status === 'completed'"
								class="btn btn-default"
								@click.stop="downloadData(item)"
							>
								下载数据
							</button>
							<button 
								v-if="item.status === 'completed'"
								class="btn btn-primary"
								@click.stop="applyInvoice(item)"
							>
								申请开票
							</button>
						</view>
					</view>
				</view>
			</view>
			
			<!-- 空状态 -->
			<view v-else class="empty-state">
				<image src="/static/empty-order.png" mode="aspectFit" class="empty-image"></image>
				<text class="empty-text">暂无订单</text>
				<button class="btn-goto" @click="goIndex">去看看</button>
			</view>
		</scroll-view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				currentTab: 'all',
				tabs: [
					{ key: 'all', label: '全部', count: 0 },
					{ key: 'pending_payment', label: '待支付', count: 0 },
					{ key: 'in_progress', label: '进行中', count: 0 },
					{ key: 'completed', label: '已完成', count: 0 }
				],
				orders: [],
				page: 1,
				hasMore: true
			}
		},
		onLoad() {
			this.loadOrders()
		},
		onPullDownRefresh() {
			this.page = 1
			this.loadOrders().then(() => {
				uni.stopPullDownRefresh()
			})
		},
		methods: {
			// 切换Tab
			switchTab(key) {
				this.currentTab = key
				this.page = 1
				this.orders = []
				this.loadOrders()
			},
			
			// 加载订单列表
			async loadOrders() {
				// TODO: 调用API
				// 临时模拟数据
				this.orders = [
					{
						id: 1,
						order_no: '202401010001',
						status: 'pending_payment',
						project_name: '场发射扫描电镜（SEM）',
						project_image: 'https://via.placeholder.com/200x150',
						lab_name: '某985高校材料实验室',
						sample_count: 3,
						total_fee: 936.00,
						created_at: '2024-01-01 10:00:00'
					}
				]
			},
			
			// 加载更多
			loadMore() {
				if (!this.hasMore) return
				this.page++
				this.loadOrders()
			},
			
			// 获取状态文本
			getStatusText(status) {
				const map = {
					'pending_payment': '待支付',
					'confirmed': '待确认',
					'waiting_test': '待试验',
					'in_progress': '实验中',
					'completed': '已完成',
					'cancelled': '已取消'
				}
				return map[status] || status
			},
			
			// 跳转订单详情
			goOrderDetail(item) {
				uni.navigateTo({
					url: `/pagesA/order-detail/order-detail?id=${item.id}`
				})
			},
			
			// 去支付
			goPay(item) {
				uni.navigateTo({
					url: `/pagesA/payment/payment?order_id=${item.id}`
				})
			},
			
			// 下载数据
			downloadData(item) {
				uni.showToast({
					title: '下载功能开发中',
					icon: 'none'
				})
			},
			
			// 申请开票
			applyInvoice(item) {
				uni.navigateTo({
					url: `/pagesA/invoice-apply/invoice-apply?order_id=${item.id}`
				})
			},
			
			// 去首页
			goIndex() {
				uni.switchTab({
					url: '/pages/index/index'
				})
			}
		}
	}
</script>

<style lang="scss" scoped>
	.order-container {
		min-height: 100vh;
		background-color: #f8f8f8;
		display: flex;
		flex-direction: column;
	}
	
	.tabs {
		display: flex;
		background-color: #ffffff;
		padding: 20rpx 30rpx;
		box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
		
		.tab-item {
			position: relative;
			flex: 1;
			text-align: center;
			padding: 20rpx 0;
			
			.tab-text {
				font-size: 28rpx;
				color: #666;
			}
			
			.badge {
				position: absolute;
				top: 10rpx;
				right: 20rpx;
				min-width: 32rpx;
				height: 32rpx;
				line-height: 32rpx;
				padding: 0 8rpx;
				background-color: #ff4d4f;
				color: #ffffff;
				font-size: 20rpx;
				border-radius: 16rpx;
				text-align: center;
			}
			
			&.active {
				.tab-text {
					color: #007AFF;
					font-weight: bold;
					border-bottom: 4rpx solid #007AFF;
					padding-bottom: 8rpx;
				}
			}
		}
	}
	
	.order-list {
		flex: 1;
		padding: 20rpx 30rpx;
		
		.order-item {
			margin-bottom: 20rpx;
			
			.order-header {
				display: flex;
				justify-content: space-between;
				align-items: center;
				padding: 24rpx;
				border-bottom: 2rpx solid #f5f5f5;
				
				.order-no {
					font-size: 26rpx;
					color: #666;
				}
				
				.order-status {
					font-size: 26rpx;
					font-weight: bold;
					
					&.status-pending_payment {
						color: #ff4d4f;
					}
					
					&.status-in_progress {
						color: #007AFF;
					}
					
					&.status-completed {
						color: #52c41a;
					}
				}
			}
			
			.order-content {
				display: flex;
				padding: 24rpx;
				
				.project-image {
					width: 160rpx;
					height: 120rpx;
					border-radius: 12rpx;
					flex-shrink: 0;
				}
				
				.order-info {
					flex: 1;
					margin-left: 20rpx;
					display: flex;
					flex-direction: column;
					justify-content: space-between;
					
					.project-name {
						font-size: 30rpx;
						font-weight: 500;
						color: #333;
						margin-bottom: 12rpx;
					}
					
					.lab-name {
						font-size: 24rpx;
						color: #999;
						margin-bottom: 8rpx;
					}
					
					.sample-count {
						font-size: 24rpx;
						color: #666;
					}
				}
			}
			
			.order-footer {
				display: flex;
				justify-content: space-between;
				align-items: center;
				padding: 24rpx;
				border-top: 2rpx solid #f5f5f5;
				
				.price-info {
					.label {
						font-size: 26rpx;
						color: #666;
					}
					
					.price {
						font-size: 36rpx;
						font-weight: bold;
						color: #ff4d4f;
					}
				}
				
				.actions {
					display: flex;
					gap: 16rpx;
					
					.btn {
						padding: 12rpx 32rpx;
						border-radius: 8rpx;
						font-size: 26rpx;
						border: none;
						
						&.btn-default {
							background-color: #f5f5f5;
							color: #666;
						}
						
						&.btn-primary {
							background-color: #007AFF;
							color: #ffffff;
						}
					}
				}
			}
		}
		
		.empty-state {
			display: flex;
			flex-direction: column;
			align-items: center;
			padding-top: 200rpx;
			
			.empty-image {
				width: 400rpx;
				height: 300rpx;
				margin-bottom: 40rpx;
			}
			
			.empty-text {
				font-size: 28rpx;
				color: #999;
				margin-bottom: 40rpx;
			}
			
			.btn-goto {
				padding: 16rpx 60rpx;
				background-color: #007AFF;
				color: #ffffff;
				border-radius: 50rpx;
				border: none;
			}
		}
	}
</style>

