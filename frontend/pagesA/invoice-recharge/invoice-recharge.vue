<template>
	<view class="invoice-recharge-page">
		<!-- 页面标题 -->
		<view class="page-header">
			<view class="header-title">开票充值</view>
			<view class="header-desc">大额充值可开发票，享受同等优惠</view>
		</view>

		<!-- 充值金额 -->
		<view class="form-section">
			<view class="section-title">充值金额</view>
			<view class="amount-input-wrapper">
				<text class="amount-prefix">¥</text>
				<input
					type="digit"
					v-model="form.amount"
					placeholder="请输入充值金额（100元起）"
					class="amount-input"
				/>
			</view>
			<view class="bonus-preview" v-if="bonusAmount > 0">
				<text class="bonus-label">预计赠送：</text>
				<text class="bonus-value">¥{{ bonusAmount }}</text>
				<text class="bonus-total">，到账 ¥{{ totalAmount }}</text>
			</view>
		</view>

		<!-- 发票信息 -->
		<view class="form-section">
			<view class="section-title">发票信息</view>

			<view class="form-item">
				<view class="form-label required">发票抬头</view>
				<input
					type="text"
					v-model="form.invoice_title"
					placeholder="请输入公司名称"
					class="form-input"
				/>
			</view>

			<view class="form-item">
				<view class="form-label">税号</view>
				<input
					type="text"
					v-model="form.invoice_tax_no"
					placeholder="请输入纳税人识别号"
					class="form-input"
				/>
			</view>

			<view class="form-item">
				<view class="form-label">发票类型</view>
				<view class="type-options">
					<view
						class="type-option"
						:class="{ active: form.invoice_type === 'normal' }"
						@click="form.invoice_type = 'normal'"
					>
						普通发票
					</view>
					<view
						class="type-option"
						:class="{ active: form.invoice_type === 'special' }"
						@click="form.invoice_type = 'special'"
					>
						增值税专票
					</view>
				</view>
			</view>

			<view class="form-item">
				<view class="form-label">接收邮箱</view>
				<input
					type="text"
					v-model="form.invoice_email"
					placeholder="电子发票将发送至此邮箱"
					class="form-input"
				/>
			</view>

			<view class="form-item">
				<view class="form-label">发票备注</view>
				<textarea
					v-model="form.invoice_remark"
					placeholder="如有特殊要求请备注"
					class="form-textarea"
				/>
			</view>
		</view>

		<!-- 汇款信息 -->
		<view class="form-section">
			<view class="section-title">汇款信息</view>
			<view class="bank-info">
				<view class="bank-item">
					<view class="bank-label">收款户名</view>
					<view class="bank-value">XX检测科技有限公司</view>
				</view>
				<view class="bank-item">
					<view class="bank-label">开户银行</view>
					<view class="bank-value">中国银行XX支行</view>
				</view>
				<view class="bank-item">
					<view class="bank-label">银行账号</view>
					<view class="bank-value">1234 5678 9012 3456</view>
				</view>
			</view>

			<view class="form-item">
				<view class="form-label">汇款银行</view>
				<input
					type="text"
					v-model="form.bank_name"
					placeholder="您的汇款银行名称"
					class="form-input"
				/>
			</view>

			<view class="form-item">
				<view class="form-label">账号后四位</view>
				<input
					type="text"
					v-model="form.bank_account"
					placeholder="汇款账号后4位，用于核对"
					class="form-input"
					maxlength="4"
				/>
			</view>

			<view class="form-item">
				<view class="form-label">汇款日期</view>
				<picker mode="date" :value="form.transfer_date" @change="onDateChange">
					<view class="picker-input">
						<text>{{ form.transfer_date || '请选择汇款日期' }}</text>
						<text class="picker-arrow">▶</text>
					</view>
				</picker>
			</view>

			<view class="form-item">
				<view class="form-label">汇款凭证</view>
				<view class="upload-area" @click="chooseVoucher">
					<image
						v-if="form.transfer_voucher"
						:src="form.transfer_voucher"
						class="voucher-preview"
						mode="aspectFit"
					/>
					<view v-else class="upload-placeholder">
						<text class="upload-icon">📷</text>
						<text class="upload-text">点击上传汇款凭证</text>
					</view>
				</view>
			</view>
		</view>

		<!-- 提交按钮 -->
		<view class="submit-section">
			<button class="submit-btn" @click="submitApplication" :disabled="submitting">
				{{ submitting ? '提交中...' : '提交申请' }}
			</button>
			<view class="submit-tip">提交后，我们将在1-2个工作日内确认到账</view>
		</view>

		<!-- 申请记录入口 -->
		<view class="records-entry" @click="goToRecords">
			<text>开票充值记录</text>
			<text class="arrow">→</text>
		</view>
	</view>
</template>

<script>
import api from '@/utils/api.js'

export default {
	data() {
		return {
			form: {
				amount: '',
				invoice_title: '',
				invoice_tax_no: '',
				invoice_type: 'normal',
				invoice_email: '',
				invoice_remark: '',
				bank_name: '',
				bank_account: '',
				transfer_date: '',
				transfer_voucher: ''
			},
			submitting: false
		}
	},

	computed: {
		bonusAmount() {
			const amount = parseFloat(this.form.amount) || 0
			if (amount < 100) return 0
			if (amount < 500) return Math.floor(amount * 0.05)
			if (amount < 1000) return Math.floor(amount * 0.10)
			if (amount < 5000) return Math.floor(amount * 0.15)
			return Math.floor(amount * 0.20)
		},

		totalAmount() {
			return (parseFloat(this.form.amount) || 0) + this.bonusAmount
		}
	},

	methods: {
		onDateChange(e) {
			this.form.transfer_date = e.detail.value
		},

		chooseVoucher() {
			uni.chooseImage({
				count: 1,
				sizeType: ['compressed'],
				sourceType: ['album', 'camera'],
				success: async (res) => {
					const tempFilePath = res.tempFilePaths[0]
					try {
						uni.showLoading({ title: '上传中...' })
						const uploadRes = await this.uploadImage(tempFilePath)
						this.form.transfer_voucher = uploadRes
						uni.hideLoading()
						uni.showToast({ title: '上传成功', icon: 'success' })
					} catch (e) {
						uni.hideLoading()
						uni.showToast({ title: '上传失败', icon: 'none' })
					}
				}
			})
		},

		uploadImage(filePath) {
			return new Promise((resolve, reject) => {
				const token = uni.getStorageSync('token')
				uni.uploadFile({
					url: 'https://catdog.dachaonet.com/api/v1/upload/image',
					filePath: filePath,
					name: 'file',
					header: {
						'Authorization': `Bearer ${token}`
					},
					success: (res) => {
						const data = JSON.parse(res.data)
						if (data.code === 200) {
							resolve(data.data.url)
						} else {
							reject(new Error(data.message))
						}
					},
					fail: reject
				})
			})
		},

		async submitApplication() {
			// 验证
			const amount = parseFloat(this.form.amount) || 0
			if (amount < 100) {
				uni.showToast({ title: '充值金额最低100元', icon: 'none' })
				return
			}

			if (!this.form.invoice_title) {
				uni.showToast({ title: '请输入发票抬头', icon: 'none' })
				return
			}

			this.submitting = true

			try {
				const res = await api.applyInvoiceRecharge(this.form)

				if (res.code === 200) {
					uni.showModal({
						title: '提交成功',
						content: `充值金额：¥${amount}，预计赠送：¥${this.bonusAmount}，到账：¥${this.totalAmount}。我们将在1-2个工作日内确认到账。`,
						showCancel: false,
						success: () => {
							uni.navigateBack()
						}
					})
				}
			} catch (e) {
				uni.showToast({
					title: e.data?.message || '提交失败',
					icon: 'none'
				})
			} finally {
				this.submitting = false
			}
		},

		goToRecords() {
			uni.navigateTo({
				url: '/pagesA/invoice-recharge-records/invoice-recharge-records'
			})
		}
	}
}
</script>

<style scoped>
.invoice-recharge-page {
	min-height: 100vh;
	background: #f5f5f5;
	padding-bottom: 50rpx;
}

.page-header {
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	padding: 48rpx 32rpx;
	color: white;
}

.header-title {
	font-size: 40rpx;
	font-weight: bold;
	margin-bottom: 12rpx;
}

.header-desc {
	font-size: 28rpx;
	opacity: 0.9;
}

.form-section {
	background: white;
	margin: 24rpx;
	padding: 32rpx;
	border-radius: 16rpx;
}

.section-title {
	font-size: 32rpx;
	font-weight: bold;
	color: #333;
	margin-bottom: 24rpx;
}

.amount-input-wrapper {
	display: flex;
	align-items: center;
	background: #f8f8f8;
	border-radius: 12rpx;
	padding: 0 24rpx;
	height: 100rpx;
}

.amount-prefix {
	font-size: 40rpx;
	font-weight: bold;
	color: #333;
	margin-right: 16rpx;
}

.amount-input {
	flex: 1;
	font-size: 40rpx;
	font-weight: bold;
	color: #333;
}

.bonus-preview {
	margin-top: 16rpx;
	padding: 16rpx 20rpx;
	background: #fff5eb;
	border-radius: 8rpx;
	display: flex;
	align-items: center;
}

.bonus-label {
	font-size: 26rpx;
	color: #666;
}

.bonus-value {
	font-size: 30rpx;
	font-weight: bold;
	color: #ff6b00;
}

.bonus-total {
	font-size: 26rpx;
	color: #666;
}

.form-item {
	margin-bottom: 24rpx;
}

.form-label {
	font-size: 28rpx;
	color: #333;
	margin-bottom: 12rpx;
}

.form-label.required::before {
	content: '*';
	color: #ff4d4f;
	margin-right: 4rpx;
}

.form-input {
	width: 100%;
	height: 88rpx;
	background: #f8f8f8;
	border-radius: 12rpx;
	padding: 0 24rpx;
	font-size: 28rpx;
	color: #333;
}

.form-textarea {
	width: 100%;
	height: 160rpx;
	background: #f8f8f8;
	border-radius: 12rpx;
	padding: 20rpx 24rpx;
	font-size: 28rpx;
	color: #333;
}

.type-options {
	display: flex;
	gap: 20rpx;
}

.type-option {
	flex: 1;
	height: 80rpx;
	line-height: 80rpx;
	text-align: center;
	background: #f8f8f8;
	border-radius: 12rpx;
	font-size: 28rpx;
	color: #666;
	border: 2rpx solid transparent;
}

.type-option.active {
	background: #f0f7ff;
	border-color: #667eea;
	color: #667eea;
}

.bank-info {
	background: #f8f8f8;
	border-radius: 12rpx;
	padding: 24rpx;
	margin-bottom: 24rpx;
}

.bank-item {
	display: flex;
	justify-content: space-between;
	padding: 12rpx 0;
}

.bank-label {
	font-size: 26rpx;
	color: #999;
}

.bank-value {
	font-size: 28rpx;
	color: #333;
	font-weight: 500;
}

.picker-input {
	display: flex;
	justify-content: space-between;
	align-items: center;
	height: 88rpx;
	background: #f8f8f8;
	border-radius: 12rpx;
	padding: 0 24rpx;
	font-size: 28rpx;
	color: #333;
}

.picker-arrow {
	font-size: 24rpx;
	color: #999;
}

.upload-area {
	width: 100%;
	height: 240rpx;
	background: #f8f8f8;
	border-radius: 12rpx;
	border: 2rpx dashed #ddd;
	display: flex;
	align-items: center;
	justify-content: center;
	overflow: hidden;
}

.upload-placeholder {
	display: flex;
	flex-direction: column;
	align-items: center;
}

.upload-icon {
	font-size: 60rpx;
	margin-bottom: 12rpx;
}

.upload-text {
	font-size: 26rpx;
	color: #999;
}

.voucher-preview {
	width: 100%;
	height: 100%;
}

.submit-section {
	padding: 32rpx;
}

.submit-btn {
	width: 100%;
	height: 96rpx;
	line-height: 96rpx;
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	color: white;
	border: none;
	border-radius: 48rpx;
	font-size: 34rpx;
	font-weight: bold;
}

.submit-btn[disabled] {
	opacity: 0.6;
}

.submit-tip {
	text-align: center;
	font-size: 24rpx;
	color: #999;
	margin-top: 16rpx;
}

.records-entry {
	background: white;
	margin: 0 24rpx 24rpx;
	padding: 32rpx;
	border-radius: 16rpx;
	display: flex;
	align-items: center;
	justify-content: space-between;
	font-size: 30rpx;
	color: #333;
}

.arrow {
	color: #999;
	font-size: 36rpx;
}
</style>
