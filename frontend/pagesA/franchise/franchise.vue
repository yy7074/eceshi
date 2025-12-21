<template>
	<view class="franchise-page">
		<!-- 顶部Banner -->
		<view class="banner">
			<view class="banner-content">
				<text class="banner-title">成为合作伙伴</text>
				<text class="banner-subtitle">携手共赢，共创未来</text>
			</view>
		</view>
		
		<!-- 加盟优势 -->
		<view class="section advantages">
			<view class="section-title">加盟优势</view>
			<view class="advantage-grid">
				<view class="advantage-item">
					<text class="advantage-icon">💰</text>
					<text class="advantage-name">高额返佣</text>
					<text class="advantage-desc">订单返佣最高可达20%</text>
				</view>
				<view class="advantage-item">
					<text class="advantage-icon">🎯</text>
					<text class="advantage-name">专属支持</text>
					<text class="advantage-desc">一对一运营指导服务</text>
				</view>
				<view class="advantage-item">
					<text class="advantage-icon">📊</text>
					<text class="advantage-name">资源共享</text>
					<text class="advantage-desc">共享平台客户资源</text>
				</view>
				<view class="advantage-item">
					<text class="advantage-icon">🚀</text>
					<text class="advantage-name">快速结算</text>
					<text class="advantage-desc">T+7工作日结算佣金</text>
				</view>
			</view>
		</view>
		
		<!-- 合作模式 -->
		<view class="section modes">
			<view class="section-title">合作模式</view>
			<view class="mode-list">
				<view class="mode-item" :class="{ active: selectedMode === 'agent' }" @click="selectedMode = 'agent'">
					<view class="mode-header">
						<text class="mode-icon">🏢</text>
						<text class="mode-name">区域代理</text>
					</view>
					<text class="mode-desc">获得指定区域独家代理权，享受区域内所有订单返佣</text>
				</view>
				<view class="mode-item" :class="{ active: selectedMode === 'partner' }" @click="selectedMode = 'partner'">
					<view class="mode-header">
						<text class="mode-icon">🤝</text>
						<text class="mode-name">项目合作</text>
					</view>
					<text class="mode-desc">针对特定项目进行合作，按项目结算佣金</text>
				</view>
				<view class="mode-item" :class="{ active: selectedMode === 'lab' }" @click="selectedMode = 'lab'">
					<view class="mode-header">
						<text class="mode-icon">🔬</text>
						<text class="mode-name">实验室入驻</text>
					</view>
					<text class="mode-desc">实验室入驻平台，承接检测订单获取收益</text>
				</view>
			</view>
		</view>
		
		<!-- 申请表单 -->
		<view class="section form-section">
			<view class="section-title">填写申请信息</view>
			<view class="form-card">
				<view class="form-item">
					<text class="form-label">联系人姓名 <text class="required">*</text></text>
					<input type="text" v-model="form.name" placeholder="请输入您的姓名" />
				</view>
				<view class="form-item">
					<text class="form-label">联系电话 <text class="required">*</text></text>
					<input type="tel" v-model="form.phone" placeholder="请输入手机号" maxlength="11" />
				</view>
				<view class="form-item">
					<text class="form-label">公司/机构名称</text>
					<input type="text" v-model="form.company" placeholder="请输入公司或机构名称" />
				</view>
				<view class="form-item">
					<text class="form-label">所在城市 <text class="required">*</text></text>
					<input type="text" v-model="form.city" placeholder="请输入所在城市" />
				</view>
				<view class="form-item">
					<text class="form-label">合作意向</text>
					<textarea v-model="form.intention" placeholder="请简述您的合作意向和优势资源" :maxlength="500"></textarea>
				</view>
			</view>
		</view>
		
		<!-- 提交按钮 -->
		<view class="submit-section">
			<button class="submit-btn" @click="submitApplication" :disabled="submitting">
				{{ submitting ? '提交中...' : '提交申请' }}
			</button>
			<text class="submit-tip">提交后我们将在3个工作日内与您联系</text>
		</view>
	</view>
</template>

<script>
import api from '@/utils/api.js'

export default {
	data() {
		return {
			selectedMode: 'agent',
			submitting: false,
			form: {
				name: '',
				phone: '',
				company: '',
				city: '',
				intention: ''
			}
		}
	},
	methods: {
		async submitApplication() {
			// 验证表单
			if (!this.form.name.trim()) {
				uni.showToast({ title: '请输入联系人姓名', icon: 'none' })
				return
			}
			if (!this.form.phone.trim() || this.form.phone.length !== 11) {
				uni.showToast({ title: '请输入正确的手机号', icon: 'none' })
				return
			}
			if (!this.form.city.trim()) {
				uni.showToast({ title: '请输入所在城市', icon: 'none' })
				return
			}
			
			this.submitting = true
			
			try {
				const res = await api.submitFranchise({
					...this.form,
					mode: this.selectedMode
				})
				
				if (res.code === 0) {
					uni.showModal({
						title: '提交成功',
						content: res.message || '感谢您的申请！我们将在3个工作日内与您联系，请保持电话畅通。',
						showCancel: false,
						success: () => {
							// 清空表单
							this.form = {
								name: '',
								phone: '',
								company: '',
								city: '',
								intention: ''
							}
						}
					})
				} else {
					uni.showToast({ title: res.message || '提交失败', icon: 'none' })
				}
			} catch (e) {
				console.error('提交加盟申请失败', e)
				uni.showToast({ title: '提交失败，请稍后重试', icon: 'none' })
			} finally {
				this.submitting = false
			}
		}
	}
}
</script>

<style lang="scss" scoped>
.franchise-page {
	min-height: 100vh;
	background: #f5f5f5;
	padding-bottom: 40rpx;
}

.banner {
	background: linear-gradient(135deg, #1890ff 0%, #096dd9 100%);
	padding: 80rpx 40rpx;
	text-align: center;
	
	.banner-content {
		.banner-title {
			display: block;
			font-size: 48rpx;
			font-weight: 700;
			color: #fff;
			margin-bottom: 16rpx;
		}
		
		.banner-subtitle {
			font-size: 28rpx;
			color: rgba(255,255,255,0.9);
		}
	}
}

.section {
	background: #fff;
	margin: 24rpx;
	border-radius: 16rpx;
	padding: 32rpx;
	
	.section-title {
		font-size: 32rpx;
		font-weight: 600;
		color: #333;
		margin-bottom: 24rpx;
	}
}

.advantage-grid {
	display: grid;
	grid-template-columns: repeat(2, 1fr);
	gap: 24rpx;
	
	.advantage-item {
		background: #f9f9f9;
		padding: 24rpx;
		border-radius: 12rpx;
		text-align: center;
		
		.advantage-icon {
			font-size: 48rpx;
			display: block;
			margin-bottom: 12rpx;
		}
		
		.advantage-name {
			display: block;
			font-size: 28rpx;
			font-weight: 600;
			color: #333;
			margin-bottom: 8rpx;
		}
		
		.advantage-desc {
			font-size: 24rpx;
			color: #999;
		}
	}
}

.mode-list {
	.mode-item {
		background: #f9f9f9;
		padding: 24rpx;
		border-radius: 12rpx;
		margin-bottom: 16rpx;
		border: 2rpx solid transparent;
		transition: all 0.3s;
		
		&.active {
			border-color: #1890ff;
			background: #e6f7ff;
		}
		
		.mode-header {
			display: flex;
			align-items: center;
			margin-bottom: 12rpx;
			
			.mode-icon {
				font-size: 36rpx;
				margin-right: 12rpx;
			}
			
			.mode-name {
				font-size: 30rpx;
				font-weight: 600;
				color: #333;
			}
		}
		
		.mode-desc {
			font-size: 26rpx;
			color: #666;
			line-height: 1.5;
		}
	}
}

.form-card {
	.form-item {
		margin-bottom: 24rpx;
		
		.form-label {
			display: block;
			font-size: 28rpx;
			color: #333;
			margin-bottom: 12rpx;
			
			.required {
				color: #ff4d4f;
			}
		}
		
		input, textarea {
			width: 100%;
			background: #f5f5f5;
			border-radius: 8rpx;
			padding: 20rpx 24rpx;
			font-size: 28rpx;
			box-sizing: border-box;
		}
		
		textarea {
			height: 200rpx;
		}
	}
}

.submit-section {
	padding: 0 24rpx;
	margin-top: 32rpx;
	
	.submit-btn {
		width: 100%;
		height: 88rpx;
		line-height: 88rpx;
		background: linear-gradient(135deg, #1890ff 0%, #096dd9 100%);
		color: #fff;
		font-size: 32rpx;
		font-weight: 600;
		border-radius: 44rpx;
		border: none;
		
		&[disabled] {
			opacity: 0.6;
		}
	}
	
	.submit-tip {
		display: block;
		text-align: center;
		font-size: 24rpx;
		color: #999;
		margin-top: 16rpx;
	}
}
</style>

