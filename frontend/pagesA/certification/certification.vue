<template>
	<view class="certification-container">
		<!-- 提示信息 -->
		<view v-if="!certificationInfo || certificationInfo.status === 'pending'" class="tips card">
			<text class="tips-title">📝 实名认证说明</text>
			<text class="tips-text">• 实名认证后可获得初始信用额度</text>
			<text class="tips-text">• 认证信息仅用于平台服务，不会泄露</text>
			<text class="tips-text">• 审核时间：1-2个工作日</text>
		</view>
		
		<!-- 认证状态 -->
		<view v-if="certificationInfo" class="status-card card">
			<view class="status-info">
				<text class="status-icon">
					{{ certificationInfo.status === 'approved' ? '✅' : 
					   certificationInfo.status === 'pending' ? '⏳' : '❌' }}
				</text>
				<view class="status-text">
					<text class="status-title">{{ getStatusText(certificationInfo.status) }}</text>
					<text v-if="certificationInfo.status === 'rejected'" class="reject-reason">
						拒绝原因：{{ certificationInfo.reject_reason }}
					</text>
				</view>
			</view>
		</view>
		
		<!-- 认证表单 -->
		<view v-if="!certificationInfo || certificationInfo.status === 'rejected'" class="form-container">
			<view class="form-section card">
				<text class="section-title">基本信息</text>
				
				<view class="form-item">
					<text class="label"><text class="required">*</text>真实姓名</text>
					<input 
						v-model="form.real_name" 
						placeholder="请输入真实姓名"
						class="input"
					/>
				</view>
				
				<view class="form-item">
					<text class="label"><text class="required">*</text>身份证号</text>
					<input 
						v-model="form.id_card" 
						maxlength="18"
						placeholder="请输入身份证号"
						class="input"
					/>
				</view>
			</view>
			
			<view class="form-section card">
				<text class="section-title">学校信息</text>
				
				<view class="form-item">
					<text class="label"><text class="required">*</text>所在地区</text>
					<picker mode="multiSelector" :range="regionData" @change="onRegionChange">
						<view class="picker">
							{{ form.province && form.city ? `${form.province} ${form.city}` : '请选择省市' }}
						</view>
					</picker>
				</view>
				
				<view class="form-item">
					<text class="label"><text class="required">*</text>所在高校</text>
					<input 
						v-model="form.university" 
						placeholder="请输入高校名称"
						class="input"
					/>
				</view>
				
				<view class="form-item">
					<text class="label"><text class="required">*</text>所在院系</text>
					<input 
						v-model="form.department" 
						placeholder="请输入院系名称"
						class="input"
					/>
				</view>
				
				<view class="form-item">
					<text class="label">入学年份</text>
					<picker mode="date" fields="year" :value="form.enrollment_year" @change="onEnrollmentChange">
						<view class="picker">
							{{ form.enrollment_year || '请选择入学年份' }}
						</view>
					</picker>
				</view>
				
				<view class="form-item">
					<text class="label">预计毕业年份</text>
					<picker mode="date" fields="year" :value="form.graduation_year" @change="onGraduationChange">
						<view class="picker">
							{{ form.graduation_year || '请选择毕业年份' }}
						</view>
					</picker>
				</view>
			</view>
			
			<view class="form-section card">
				<text class="section-title">导师信息（选填）</text>
				
				<view class="form-item">
					<text class="label">导师姓名</text>
					<input 
						v-model="form.supervisor_name" 
						placeholder="请输入导师姓名"
						class="input"
					/>
				</view>
				
				<view class="form-item">
					<text class="label">导师职称</text>
					<picker :range="titleOptions" @change="onTitleChange">
						<view class="picker">
							{{ form.supervisor_title || '请选择导师职称' }}
						</view>
					</picker>
				</view>
			</view>
			
			<view class="form-section card">
				<text class="section-title">证件上传（选填）</text>
				
				<view class="upload-item">
					<text class="label">学生证照片</text>
					<view class="upload-btn" @click="uploadImage('student_card')">
						<image v-if="form.student_card_photo" :src="form.student_card_photo" mode="aspectFill" class="preview-image"></image>
						<view v-else class="upload-placeholder">
							<text class="icon">📷</text>
							<text class="text">点击上传</text>
						</view>
					</view>
				</view>
			</view>
			
			<button class="btn-submit" :loading="loading" @click="submitCertification">
				提交认证
			</button>
		</view>
	</view>
</template>

<script>
	import api from '@/utils/api.js'
	
	export default {
		data() {
			return {
				certificationInfo: null,
				form: {
					real_name: '',
					id_card: '',
					province: '',
					city: '',
					university: '',
					department: '',
					enrollment_year: '',
					graduation_year: '',
					supervisor_name: '',
					supervisor_title: '',
					student_card_photo: ''
				},
				regionData: [
					['北京市', '上海市', '广东省', '江苏省', '浙江省'],
					['北京市', '上海市', '广州市', '南京市', '杭州市']
				],
				titleOptions: ['教授', '副教授', '讲师', '助教', '研究员', '副研究员'],
				loading: false
			}
		},
		onLoad() {
			this.loadCertificationInfo()
		},
		methods: {
			// 加载认证信息
			async loadCertificationInfo() {
				try {
					const res = await api.getCertification()
					this.certificationInfo = res.data
				} catch (error) {
					// 未认证，不做处理
					console.log('未认证')
				}
			},
			
			// 地区选择
			onRegionChange(e) {
				const values = e.detail.value
				this.form.province = this.regionData[0][values[0]]
				this.form.city = this.regionData[1][values[1]]
			},
			
			// 入学年份
			onEnrollmentChange(e) {
				this.form.enrollment_year = e.detail.value
			},
			
			// 毕业年份
			onGraduationChange(e) {
				this.form.graduation_year = e.detail.value
			},
			
			// 职称选择
			onTitleChange(e) {
				this.form.supervisor_title = this.titleOptions[e.detail.value]
			},
			
			// 上传图片
			uploadImage(type) {
				uni.chooseImage({
					count: 1,
					sizeType: ['compressed'],
					sourceType: ['camera', 'album'],
					success: (res) => {
						// TODO: 上传到服务器
						// 这里先使用本地路径
						this.form.student_card_photo = res.tempFilePaths[0]
						uni.showToast({
							title: '图片上传成功',
							icon: 'success'
						})
					}
				})
			},
			
			// 提交认证
			async submitCertification() {
				// 验证
				if (!this.form.real_name) {
					return uni.showToast({ title: '请输入真实姓名', icon: 'none' })
				}
				if (!this.form.id_card) {
					return uni.showToast({ title: '请输入身份证号', icon: 'none' })
				}
				if (!/^\d{17}[\dXx]$/.test(this.form.id_card)) {
					return uni.showToast({ title: '身份证号格式不正确', icon: 'none' })
				}
				if (!this.form.province || !this.form.city) {
					return uni.showToast({ title: '请选择所在地区', icon: 'none' })
				}
				if (!this.form.university) {
					return uni.showToast({ title: '请输入所在高校', icon: 'none' })
				}
				if (!this.form.department) {
					return uni.showToast({ title: '请输入所在院系', icon: 'none' })
				}
				
				this.loading = true
				try {
					await api.submitCertification(this.form)
					
					uni.showToast({
						title: '提交成功，等待审核',
						icon: 'success'
					})
					
					setTimeout(() => {
						uni.navigateBack()
					}, 1500)
					
				} catch (error) {
					console.error('提交认证失败', error)
				} finally {
					this.loading = false
				}
			},
			
			// 获取状态文本
			getStatusText(status) {
				const map = {
					'pending': '审核中',
					'approved': '已通过',
					'rejected': '审核未通过'
				}
				return map[status] || status
			}
		}
	}
</script>

<style lang="scss" scoped>
	.certification-container {
		min-height: 100vh;
		background-color: #f8f8f8;
		padding: 20rpx 30rpx 40rpx;
	}
	
	.tips {
		padding: 30rpx;
		margin-bottom: 20rpx;
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		
		.tips-title {
			display: block;
			font-size: 32rpx;
			font-weight: bold;
			color: #ffffff;
			margin-bottom: 20rpx;
		}
		
		.tips-text {
			display: block;
			font-size: 26rpx;
			color: rgba(255, 255, 255, 0.9);
			line-height: 1.8;
			margin-bottom: 8rpx;
		}
	}
	
	.status-card {
		padding: 40rpx;
		margin-bottom: 20rpx;
		
		.status-info {
			display: flex;
			align-items: center;
			
			.status-icon {
				font-size: 60rpx;
				margin-right: 24rpx;
			}
			
			.status-text {
				flex: 1;
				
				.status-title {
					display: block;
					font-size: 32rpx;
					font-weight: bold;
					color: #333;
					margin-bottom: 12rpx;
				}
				
				.reject-reason {
					display: block;
					font-size: 26rpx;
					color: #ff4d4f;
				}
			}
		}
	}
	
	.form-container {
		.form-section {
			padding: 30rpx;
			margin-bottom: 20rpx;
			
			.section-title {
				display: block;
				font-size: 32rpx;
				font-weight: bold;
				color: #333;
				margin-bottom: 30rpx;
			}
			
			.form-item {
				margin-bottom: 30rpx;
				
				&:last-child {
					margin-bottom: 0;
				}
				
				.label {
					display: block;
					font-size: 28rpx;
					color: #333;
					margin-bottom: 16rpx;
					
					.required {
						color: #ff4d4f;
						margin-right: 4rpx;
					}
				}
				
				.input {
					width: 100%;
					height: 80rpx;
					padding: 0 24rpx;
					border: 2rpx solid #e0e0e0;
					border-radius: 12rpx;
					font-size: 28rpx;
					background-color: #ffffff;
				}
				
				.picker {
					width: 100%;
					height: 80rpx;
					line-height: 80rpx;
					padding: 0 24rpx;
					border: 2rpx solid #e0e0e0;
					border-radius: 12rpx;
					font-size: 28rpx;
					color: #333;
					background-color: #ffffff;
				}
			}
			
			.upload-item {
				.label {
					display: block;
					font-size: 28rpx;
					color: #333;
					margin-bottom: 16rpx;
				}
				
				.upload-btn {
					width: 200rpx;
					height: 200rpx;
					border: 2rpx dashed #ccc;
					border-radius: 12rpx;
					overflow: hidden;
					
					.preview-image {
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
						background-color: #fafafa;
						
						.icon {
							font-size: 60rpx;
							margin-bottom: 12rpx;
						}
						
						.text {
							font-size: 24rpx;
							color: #999;
						}
					}
				}
			}
		}
		
		.btn-submit {
			width: 100%;
			height: 88rpx;
			line-height: 88rpx;
			background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
			color: #ffffff;
			border-radius: 12rpx;
			font-size: 32rpx;
			border: none;
			margin-top: 40rpx;
		}
	}
</style>

