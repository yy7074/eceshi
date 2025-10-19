<template>
	<view class="invoice-page">
		<!-- Tab切换 -->
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
		
		<!-- 发票列表 -->
		<view v-if="invoices.length > 0" class="invoice-list">
			<view v-for="(item, index) in invoices" :key="index" class="invoice-item" @click="viewInvoice(item)">
				<view class="invoice-header">
					<text class="invoice-title">{{ item.title }}</text>
					<text :class="['invoice-status', 'status-' + item.status]">{{ item.statusText }}</text>
				</view>
				<view class="invoice-info">
					<view class="info-row">
						<text class="label">开票金额：</text>
						<text class="value">¥{{ item.amount.toFixed(2) }}</text>
					</view>
					<view class="info-row">
						<text class="label">申请时间：</text>
						<text class="value">{{ item.applyTime }}</text>
					</view>
				</view>
			</view>
		</view>
		
		<!-- 空状态 -->
		<view v-else class="empty-state">
			<text class="empty-icon">🧾</text>
			<text class="empty-text">暂无发票记录</text>
			<button class="apply-btn" @click="applyInvoice">申请开票</button>
		</view>
		
		<!-- 申请开票按钮（有记录时） -->
		<view v-if="invoices.length > 0" class="footer-btn">
			<button class="apply-btn" @click="applyInvoice">申请开票</button>
		</view>
	</view>
</template>

<script>
export default {
	data() {
		return {
			currentTab: 0,
			tabs: ['全部', '待审核', '已开票', '已拒绝'],
			invoices: []
		}
	},
	
	onLoad() {
		this.loadInvoices()
	},
	
	methods: {
		// 加载发票列表
		async loadInvoices() {
			try {
				// TODO: 调用API获取发票列表
				this.invoices = []
			} catch (error) {
				console.error('加载发票失败', error)
			}
		},
		
		// 切换Tab
		switchTab(index) {
			this.currentTab = index
			this.loadInvoices()
		},
		
		// 查看发票详情
		viewInvoice(item) {
			uni.showToast({
				title: '发票详情开发中',
				icon: 'none'
			})
		},
		
		// 申请开票
		applyInvoice() {
			uni.showToast({
				title: '申请开票功能开发中',
				icon: 'none'
			})
		}
	}
}
</script>

<style lang="scss" scoped>
.invoice-page {
	min-height: 100vh;
	background: #f5f5f5;
	padding-bottom: 120rpx;
}

.tabs {
	display: flex;
	background: white;
	
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

.invoice-list {
	padding: 20rpx 30rpx;
	
	.invoice-item {
		background: white;
		border-radius: 16rpx;
		padding: 30rpx;
		margin-bottom: 20rpx;
		
		.invoice-header {
			display: flex;
			justify-content: space-between;
			align-items: center;
			margin-bottom: 20rpx;
			
			.invoice-title {
				font-size: 30rpx;
				font-weight: bold;
				color: #333;
			}
			
			.invoice-status {
				font-size: 24rpx;
				padding: 8rpx 16rpx;
				border-radius: 8rpx;
				
				&.status-pending {
					background: #fff3e0;
					color: #ff9800;
				}
				
				&.status-approved {
					background: #e8f5e9;
					color: #4caf50;
				}
				
				&.status-rejected {
					background: #ffebee;
					color: #f44336;
				}
			}
		}
		
		.invoice-info {
			.info-row {
				display: flex;
				margin-bottom: 15rpx;
				font-size: 26rpx;
				
				&:last-child {
					margin-bottom: 0;
				}
				
				.label {
					color: #999;
				}
				
				.value {
					color: #333;
				}
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
}

.footer-btn,
.empty-state {
	.apply-btn {
		background: #1890ff;
		color: white;
		border: none;
		border-radius: 50rpx;
		padding: 25rpx 60rpx;
		font-size: 28rpx;
	}
}

.footer-btn {
	position: fixed;
	bottom: 0;
	left: 0;
	right: 0;
	padding: 20rpx 30rpx;
	background: white;
	box-shadow: 0 -2rpx 10rpx rgba(0, 0, 0, 0.05);
	
	.apply-btn {
		width: 100%;
	}
}
</style>

