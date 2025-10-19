<template>
	<view class="certification-page">
		<!-- 认证状态 -->
		<view class="status-card" v-if="certInfo.status">
			<view class="status-icon" :class="'status-' + certInfo.status">
				<text class="icon">{{ getStatusIcon() }}</text>
			</view>
			<text class="status-text">{{ getStatusText() }}</text>
			<text class="status-desc" v-if="certInfo.reject_reason">{{ certInfo.reject_reason }}</text>
		</view>
		
		<!-- 认证表单 -->
		<view class="form-container" v-if="!certInfo.status || certInfo.status === 'rejected'">
			<!-- 真实姓名 -->
			<view class="form-item">
				<text class="label"><text class="required">*</text>真实姓名</text>
				<input 
					v-model="form.real_name" 
					placeholder="请输入真实姓名"
					class="input"
					maxlength="20"
				/>
			</view>
			
			<!-- 身份证号 -->
			<view class="form-item">
				<text class="label"><text class="required">*</text>身份证号</text>
				<input 
					v-model="form.id_card" 
					placeholder="请输入身份证号"
					class="input"
					maxlength="18"
				/>
			</view>
			
			<!-- 身份证照片 -->
			<view class="upload-section">
				<text class="section-title">身份证照片</text>
				<view class="upload-grid">
					<!-- 身份证正面 -->
					<view class="upload-item">
						<view class="upload-box" @click="chooseIdCardFront">
							<image 
								v-if="form.id_card_front" 
								:src="form.id_card_front" 
								mode="aspectFill" 
								class="upload-image"
							></image>
							<view v-else class="upload-placeholder">
								<text class="upload-icon">📷</text>
								<text class="upload-text">身份证正面</text>
							</view>
						</view>
						<text class="upload-label">身份证正面</text>
					</view>
					
					<!-- 身份证反面 -->
					<view class="upload-item">
						<view class="upload-box" @click="chooseIdCardBack">
							<image 
								v-if="form.id_card_back" 
								:src="form.id_card_back" 
								mode="aspectFill" 
								class="upload-image"
							></image>
							<view v-else class="upload-placeholder">
								<text class="upload-icon">📷</text>
								<text class="upload-text">身份证反面</text>
							</view>
						</view>
						<text class="upload-label">身份证反面</text>
					</view>
				</view>
			</view>
			
			<!-- 提示信息 -->
			<view class="tips-card">
				<text class="tips-title">⚠️ 温馨提示</text>
				<text class="tips-text">1. 请确保身份证照片清晰完整</text>
				<text class="tips-text">2. 请上传本人真实身份证</text>
				<text class="tips-text">3. 您的信息将严格保密</text>
			</view>
			
			<!-- 提交按钮 -->
			<view class="submit-btn-wrap">
				<button class="submit-btn" @click="submitCertification" :disabled="submitting">
					{{ submitting ? '提交中...' : '提交认证' }}
				</button>
			</view>
		</view>
		
		<!-- 已认证信息展示 -->
		<view class="certified-info" v-if="certInfo.status === 'approved'">
			<view class="info-item">
				<text class="info-label">真实姓名</text>
				<text class="info-value">{{ certInfo.real_name }}</text>
			</view>
			<view class="info-item">
				<text class="info-label">身份证号</text>
				<text class="info-value">{{ maskIdCard(certInfo.id_card) }}</text>
			</view>
			<view class="info-item">
				<text class="info-label">认证时间</text>
				<text class="info-value">{{ formatDate(certInfo.approved_at) }}</text>
			</view>
		</view>
	</view>
</template>

<script>
import api from '@/utils/api.js'

export default {
	data() {
		return {
			certInfo: {},
			form: {
				real_name: '',
				id_card: '',
				id_card_front: '',
				id_card_back: ''
			},
			submitting: false
		}
	},
	onLoad() {
		this.loadCertInfo()
	},
	methods: {
		// 加载认证信息
		async loadCertInfo() {
			try {
				const res = await api.getCertification()
				if (res.data) {
					this.certInfo = res.data
					this.form = {
						real_name: res.data.real_name || '',
						id_card: res.data.id_card || '',
						id_card_front: res.data.id_card_front || '',
						id_card_back: res.data.id_card_back || ''
					}
				}
			} catch (e) {
				console.error('加载认证信息失败', e)
			}
		},
		
		// 选择身份证正面
		chooseIdCardFront() {
			this.uploadIdCard('front')
		},
		
		// 选择身份证反面
		chooseIdCardBack() {
			this.uploadIdCard('back')
		},
		
		// 上传身份证
		uploadIdCard(type) {
			uni.chooseImage({
				count: 1,
				sizeType: ['compressed'],
				sourceType: ['album', 'camera'],
				success: (res) => {
					const tempFilePath = res.tempFilePaths[0]
					this.uploadImage(tempFilePath, type)
				}
			})
		},
		
		// 上传图片
		async uploadImage(filePath, type) {
			uni.showLoading({ title: '上传中...' })
			
			try {
				const token = uni.getStorageSync('token')
				
				uni.uploadFile({
					url: 'https://catdog.dachaonet.com/api/v1/upload/image',
					filePath: filePath,
					name: 'file',
					header: {
						'Authorization': `Bearer ${token}`
					},
					success: (uploadRes) => {
						const data = JSON.parse(uploadRes.data)
						if (data.code === 200) {
							if (type === 'front') {
								this.form.id_card_front = data.data.url
							} else {
								this.form.id_card_back = data.data.url
							}
							uni.showToast({
								title: '上传成功',
								icon: 'success'
							})
						} else {
							uni.showToast({
								title: '上传失败',
								icon: 'none'
							})
						}
					},
					fail: () => {
						uni.showToast({
							title: '上传失败',
							icon: 'none'
						})
					},
					complete: () => {
						uni.hideLoading()
					}
				})
			} catch (e) {
				uni.hideLoading()
				console.error('上传图片失败', e)
			}
		},
		
		// 提交认证
		async submitCertification() {
			// 验证
			if (!this.form.real_name) {
				uni.showToast({ title: '请输入真实姓名', icon: 'none' })
				return
			}
			
			if (!this.form.id_card) {
				uni.showToast({ title: '请输入身份证号', icon: 'none' })
				return
			}
			
			// 简单的身份证号验证
			if (!/^[1-9]\d{5}(18|19|20)\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$/.test(this.form.id_card)) {
				uni.showToast({ title: '身份证号格式不正确', icon: 'none' })
				return
			}
			
			if (!this.form.id_card_front) {
				uni.showToast({ title: '请上传身份证正面', icon: 'none' })
				return
			}
			
			if (!this.form.id_card_back) {
				uni.showToast({ title: '请上传身份证反面', icon: 'none' })
				return
			}
			
			this.submitting = true
			
			try {
				await api.submitCertification({
					real_name: this.form.real_name,
					id_card: this.form.id_card,
					id_card_front: this.form.id_card_front,
					id_card_back: this.form.id_card_back
				})
				
				uni.showToast({
					title: '提交成功',
					icon: 'success'
				})
				
				setTimeout(() => {
					this.loadCertInfo()
				}, 1500)
			} catch (e) {
				console.error('提交失败', e)
				uni.showToast({
					title: e.message || '提交失败',
					icon: 'none'
				})
			} finally {
				this.submitting = false
			}
		},
		
		// 获取状态图标
		getStatusIcon() {
			const iconMap = {
				'pending': '⏰',
				'approved': '✅',
				'rejected': '❌'
			}
			return iconMap[this.certInfo.status] || '📝'
		},
		
		// 获取状态文本
		getStatusText() {
			const statusMap = {
				'pending': '审核中',
				'approved': '已认证',
				'rejected': '审核未通过'
			}
			return statusMap[this.certInfo.status] || ''
		},
		
		// 隐藏身份证号
		maskIdCard(idCard) {
			if (!idCard || idCard.length < 14) return idCard
			return idCard.replace(/^(.{6})(?:\d+)(.{4})$/, '$1********$2')
		},
		
		// 格式化日期
		formatDate(dateStr) {
			if (!dateStr) return ''
			const date = new Date(dateStr)
			const Y = date.getFullYear()
			const M = String(date.getMonth() + 1).padStart(2, '0')
			const D = String(date.getDate()).padStart(2, '0')
			return `${Y}-${M}-${D}`
		}
	}
}
</script>

<style lang="scss" scoped>
.certification-page {
	min-height: 100vh;
	background: #f5f5f5;
	padding-bottom: 40rpx;
}

/* 状态卡片 */
.status-card {
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	padding: 60rpx 30rpx;
	display: flex;
	flex-direction: column;
	align-items: center;
	margin-bottom: 20rpx;
	
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

/* 表单容器 */
.form-container {
	padding: 20rpx;
}

.form-item {
	background: white;
	padding: 30rpx;
	margin-bottom: 20rpx;
	border-radius: 12rpx;
	display: flex;
	align-items: center;
	
	.label {
		width: 180rpx;
		font-size: 28rpx;
		color: #333;
		
		.required {
			color: #ff0000;
			margin-right: 5rpx;
		}
	}
	
	.input {
		flex: 1;
		font-size: 28rpx;
		color: #333;
		text-align: right;
	}
}

/* 上传区域 */
.upload-section {
	background: white;
	padding: 30rpx;
	margin-bottom: 20rpx;
	border-radius: 12rpx;
	
	.section-title {
		font-size: 30rpx;
		font-weight: bold;
		color: #333;
		margin-bottom: 30rpx;
		display: block;
	}
	
	.upload-grid {
		display: flex;
		gap: 30rpx;
		
		.upload-item {
			flex: 1;
			
			.upload-box {
				width: 100%;
				height: 300rpx;
				border: 2rpx dashed #ddd;
				border-radius: 12rpx;
				overflow: hidden;
				margin-bottom: 15rpx;
				
				.upload-image {
					width: 100%;
					height: 100%;
				}
				
				.upload-placeholder {
					width: 100%;
					height: 100%;
					display: flex;
					flex-direction: column;
					align-items: center;
					justify-content: center;
					background: #f5f8ff;
					
					.upload-icon {
						font-size: 60rpx;
						margin-bottom: 15rpx;
					}
					
					.upload-text {
						font-size: 24rpx;
						color: #999;
					}
				}
			}
			
			.upload-label {
				font-size: 24rpx;
				color: #666;
				text-align: center;
				display: block;
			}
		}
	}
}

/* 提示卡片 */
.tips-card {
	background: #fff3e0;
	padding: 30rpx;
	margin-bottom: 20rpx;
	border-radius: 12rpx;
	
	.tips-title {
		font-size: 28rpx;
		font-weight: bold;
		color: #ff9500;
		display: block;
		margin-bottom: 15rpx;
	}
	
	.tips-text {
		font-size: 24rpx;
		color: #666;
		line-height: 1.8;
		display: block;
	}
}

/* 提交按钮 */
.submit-btn-wrap {
	padding: 30rpx;
	
	.submit-btn {
		width: 100%;
		height: 90rpx;
		line-height: 90rpx;
		background: #4facfe;
		color: white;
		border-radius: 45rpx;
		font-size: 32rpx;
		font-weight: bold;
		border: none;
		
		&::after {
			border: none;
		}
		
		&[disabled] {
			opacity: 0.6;
		}
	}
}

/* 已认证信息 */
.certified-info {
	background: white;
	margin: 20rpx;
	padding: 30rpx;
	border-radius: 12rpx;
	
	.info-item {
		display: flex;
		justify-content: space-between;
		padding: 20rpx 0;
		border-bottom: 1rpx solid #f0f0f0;
		
		&:last-child {
			border-bottom: none;
		}
		
		.info-label {
			font-size: 28rpx;
			color: #666;
		}
		
		.info-value {
			font-size: 28rpx;
			color: #333;
		}
	}
}
</style>
