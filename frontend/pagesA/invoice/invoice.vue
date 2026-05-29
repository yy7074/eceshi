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
					<text :class="['invoice-status', 'status-' + item.status]">{{ item.status_text }}</text>
				</view>
				<view class="invoice-info">
					<view class="info-row">
						<text class="label">开票金额：</text>
						<text class="value amount">¥{{ item.amount.toFixed(2) }}</text>
					</view>
					<view class="info-row">
						<text class="label">发票内容：</text>
						<text class="value">{{ item.content }}</text>
					</view>
					<view class="info-row">
						<text class="label">申请时间：</text>
						<text class="value">{{ formatTime(item.created_at) }}</text>
					</view>
				</view>
				<!-- 电子发票下载 -->
				<view v-if="item.status === 'issued' && item.invoice_url" class="invoice-actions">
					<button class="download-btn" @click.stop="downloadInvoice(item)">下载电子发票</button>
					<button class="download-btn secondary" v-if="item.report_url" @click.stop="copyFileUrl(item.report_url, '测试报告')">测试报告</button>
					<button class="download-btn secondary" v-if="item.checklist_url" @click.stop="copyFileUrl(item.checklist_url, '测试清单')">测试清单</button>
				</view>
				<!-- 拒绝原因 -->
				<view v-if="item.status === 'rejected' && item.reject_reason" class="reject-reason">
					<text>拒绝原因：{{ item.reject_reason }}</text>
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
		
		<!-- 申请开票弹窗 -->
		<uni-popup ref="applyPopup" type="bottom">
			<view class="apply-popup">
				<view class="popup-header">
					<text class="popup-title">申请开票</text>
					<text class="popup-close" @click="closeApplyPopup">×</text>
				</view>
				<scroll-view scroll-y class="popup-content">
					<view class="form-group">
						<text class="form-label">抬头类型</text>
						<view class="type-switch">
							<view :class="['type-item', applyForm.title_type === 'personal' ? 'active' : '']" @click="applyForm.title_type = 'personal'">个人</view>
							<view :class="['type-item', applyForm.title_type === 'company' ? 'active' : '']" @click="applyForm.title_type = 'company'">企业</view>
						</view>
					</view>
					<view class="form-group">
						<text class="form-label">发票抬头 <text class="required">*</text></text>
						<input v-model="applyForm.title" placeholder="请输入发票抬头" class="form-input" />
					</view>
					<view class="form-group" v-if="applyForm.title_type === 'company'">
						<text class="form-label">税号 <text class="required">*</text></text>
						<input v-model="applyForm.tax_number" placeholder="请输入税号" class="form-input" />
					</view>
					<view class="form-group">
						<text class="form-label">关联订单</text>
						<view v-if="invoiceableOrders.length > 0" class="order-select-list">
							<view
								v-for="order in invoiceableOrders"
								:key="order.id"
								class="order-select-item"
								:class="{ active: applyForm.order_ids.includes(order.id) }"
								@click="toggleOrder(order)"
							>
								<view>
									<text class="order-no">{{ order.order_no }}</text>
									<text class="order-project">{{ order.project_name }}</text>
								</view>
								<text class="order-amount">¥{{ Number(order.total_fee || 0).toFixed(2) }}</text>
							</view>
						</view>
						<view v-else class="order-empty">暂无可开票订单</view>
					</view>
					<view class="form-group">
						<text class="form-label">开票金额 <text class="required">*</text></text>
						<input v-model="applyForm.amount" type="digit" placeholder="选择订单后自动合计，也可手动填写" class="form-input" />
					</view>
					<view class="form-group">
						<text class="form-label">接收邮箱 <text class="required">*</text></text>
						<input v-model="applyForm.receiver_email" placeholder="电子发票将发送至此邮箱" class="form-input" />
					</view>
					<view class="form-group">
						<text class="form-label">联系电话</text>
						<input v-model="applyForm.receiver_phone" placeholder="请输入联系电话" class="form-input" />
					</view>
				</scroll-view>
				<view class="popup-footer">
					<button class="submit-btn" @click="submitApply" :loading="submitting">提交申请</button>
				</view>
			</view>
		</uni-popup>
	</view>
</template>

<script>
import api from '@/utils/api.js'

export default {
	data() {
		return {
			currentTab: 0,
			tabs: ['全部', '待审核', '已开票', '已拒绝'],
			invoices: [],
			loading: false,
			submitting: false,
			applyForm: {
				title_type: 'personal',
				title: '',
				tax_number: '',
				amount: '',
				order_ids: [],
				receiver_email: '',
				receiver_phone: '',
				content: '检测服务费'
			},
			invoiceableOrders: []
		}
	},
	
	onLoad() {
		this.loadInvoices()
	},
	
	onPullDownRefresh() {
		this.loadInvoices().finally(() => {
			uni.stopPullDownRefresh()
		})
	},
	
	methods: {
		// 加载发票列表
		async loadInvoices() {
			this.loading = true
			try {
				const statusMap = ['', 'pending', 'issued', 'rejected']
				const status = statusMap[this.currentTab] || ''
				
				const res = await api.getInvoices({ status, page: 1, page_size: 50 })
				this.invoices = res.data.items || []
			} catch (error) {
				console.error('加载发票失败', error)
			} finally {
				this.loading = false
			}
		},
		
		// 切换Tab
		switchTab(index) {
			this.currentTab = index
			this.loadInvoices()
		},
		
		// 格式化时间
		formatTime(timeStr) {
			if (!timeStr) return ''
			return timeStr.replace('T', ' ').substring(0, 16)
		},
		
		// 查看发票详情
		viewInvoice(item) {
			uni.showModal({
				title: '发票详情',
				content: `抬头：${item.title}\n金额：¥${item.amount}\n状态：${item.status_text}\n申请时间：${this.formatTime(item.created_at)}`,
				showCancel: false
			})
		},
		
		// 下载电子发票
		downloadInvoice(item) {
			if (item.invoice_url) {
				// #ifdef H5
				window.open(item.invoice_url, '_blank')
				// #endif
				// #ifndef H5
				uni.showToast({
					title: '发票链接已复制',
					icon: 'success'
				})
				uni.setClipboardData({
					data: item.invoice_url
				})
				// #endif
			}
		},
		copyFileUrl(url, name) {
			if (!url) return
			uni.setClipboardData({
				data: url,
				success: () => uni.showToast({ title: `${name}链接已复制`, icon: 'success' })
			})
		},
		
		// 申请开票
		applyInvoice() {
			this.loadInvoiceableOrders()
			this.$refs.applyPopup.open()
		},
		async loadInvoiceableOrders() {
			try {
				const res = await api.getInvoiceableOrders()
				this.invoiceableOrders = res.data?.items || []
			} catch (error) {
				this.invoiceableOrders = []
			}
		},
		toggleOrder(order) {
			const index = this.applyForm.order_ids.indexOf(order.id)
			if (index >= 0) {
				this.applyForm.order_ids.splice(index, 1)
			} else {
				this.applyForm.order_ids.push(order.id)
			}
			const amount = this.invoiceableOrders
				.filter(item => this.applyForm.order_ids.includes(item.id))
				.reduce((sum, item) => sum + Number(item.total_fee || 0), 0)
			if (amount > 0) {
				this.applyForm.amount = amount.toFixed(2)
			}
		},
		
		// 关闭申请弹窗
		closeApplyPopup() {
			this.$refs.applyPopup.close()
		},
		
		// 提交申请
		async submitApply() {
			// 验证
			if (!this.applyForm.title) {
				uni.showToast({ title: '请输入发票抬头', icon: 'none' })
				return
			}
			if (this.applyForm.title_type === 'company' && !this.applyForm.tax_number) {
				uni.showToast({ title: '请输入税号', icon: 'none' })
				return
			}
			if (!this.applyForm.amount || parseFloat(this.applyForm.amount) <= 0) {
				uni.showToast({ title: '请输入正确的开票金额', icon: 'none' })
				return
			}
			if (!this.applyForm.receiver_email) {
				uni.showToast({ title: '请输入接收邮箱', icon: 'none' })
				return
			}
			
			this.submitting = true
			try {
				await api.applyInvoice({
					...this.applyForm,
					amount: parseFloat(this.applyForm.amount)
				})
				uni.showToast({ title: '申请提交成功', icon: 'success' })
				this.closeApplyPopup()
				this.loadInvoices()
				// 重置表单
				this.applyForm = {
					title_type: 'personal',
					title: '',
					tax_number: '',
					amount: '',
					order_ids: [],
					receiver_email: '',
					receiver_phone: '',
					content: '检测服务费'
				}
			} catch (error) {
				uni.showToast({ title: error.message || '申请失败', icon: 'none' })
			} finally {
				this.submitting = false
			}
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
				flex: 1;
				overflow: hidden;
				text-overflow: ellipsis;
				white-space: nowrap;
			}
			
			.invoice-status {
				font-size: 24rpx;
				padding: 8rpx 16rpx;
				border-radius: 8rpx;
				margin-left: 20rpx;
				
				&.status-pending {
					background: #fff3e0;
					color: #ff9800;
				}
				
				&.status-approved, &.status-issued {
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
					width: 160rpx;
				}
				
				.value {
					color: #333;
					flex: 1;
					
					&.amount {
						color: #ff4d4f;
						font-weight: bold;
					}
				}
			}
		}
		
		.invoice-actions {
			margin-top: 20rpx;
			padding-top: 20rpx;
			border-top: 1rpx solid #f5f5f5;
			display: flex;
			gap: 12rpx;
			flex-wrap: wrap;
			
			.download-btn {
				background: #667eea;
				color: white;
				border: none;
				border-radius: 50rpx;
				padding: 15rpx 40rpx;
				font-size: 26rpx;

				&.secondary {
					background: #edf2ff;
					color: #667eea;
				}
			}
		}
		
		.reject-reason {
			margin-top: 15rpx;
			padding: 15rpx;
			background: #fff5f5;
			border-radius: 8rpx;
			font-size: 24rpx;
			color: #f44336;
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
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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

/* 申请弹窗 */
.apply-popup {
	background: white;
	border-radius: 30rpx 30rpx 0 0;
	max-height: 80vh;
	display: flex;
	flex-direction: column;
	
	.popup-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 30rpx;
		border-bottom: 1rpx solid #f5f5f5;
		
		.popup-title {
			font-size: 32rpx;
			font-weight: bold;
			color: #333;
		}
		
		.popup-close {
			font-size: 48rpx;
			color: #999;
			line-height: 1;
		}
	}
	
	.popup-content {
		flex: 1;
		padding: 30rpx;
		max-height: 60vh;
		
		.form-group {
			margin-bottom: 30rpx;
			
			.form-label {
				font-size: 28rpx;
				color: #333;
				margin-bottom: 15rpx;
				display: block;
				
				.required {
					color: #f44336;
				}
			}
			
			.form-input {
				width: 100%;
				height: 80rpx;
				background: #f5f5f5;
				border-radius: 12rpx;
				padding: 0 20rpx;
				font-size: 28rpx;
			}

			.order-select-list {
				display: flex;
				flex-direction: column;
				gap: 12rpx;
			}

			.order-select-item {
				display: flex;
				align-items: center;
				justify-content: space-between;
				padding: 18rpx;
				background: #f7f8fb;
				border-radius: 12rpx;
				border: 2rpx solid transparent;

				&.active {
					border-color: #667eea;
					background: #eef2ff;
				}

				.order-no,
				.order-project {
					display: block;
					font-size: 24rpx;
					color: #333;
				}

				.order-project {
					color: #777;
					margin-top: 6rpx;
				}

				.order-amount {
					font-size: 26rpx;
					color: #f56c6c;
					font-weight: 700;
				}
			}

			.order-empty {
				color: #999;
				font-size: 26rpx;
				padding: 20rpx;
				background: #f7f8fb;
				border-radius: 12rpx;
			}
			
			.type-switch {
				display: flex;
				gap: 20rpx;
				
				.type-item {
					flex: 1;
					text-align: center;
					padding: 20rpx;
					background: #f5f5f5;
					border-radius: 12rpx;
					font-size: 28rpx;
					color: #666;
					
					&.active {
						background: #667eea;
						color: white;
					}
				}
			}
		}
	}
	
	.popup-footer {
		padding: 20rpx 30rpx 40rpx;
		
		.submit-btn {
			width: 100%;
			background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
			color: white;
			border: none;
			border-radius: 50rpx;
			padding: 25rpx 0;
			font-size: 30rpx;
		}
	}
}
</style>
