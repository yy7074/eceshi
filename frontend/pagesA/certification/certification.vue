<template>
	<view class="certification-page">
		<!-- 认证状态 -->
		<view class="status-card" v-if="certInfo.status && certInfo.status !== 'not_certified'">
			<view class="status-icon" :class="'status-' + certInfo.status">
				<text class="icon">{{ getStatusIcon() }}</text>
			</view>
			<text class="status-text">{{ getStatusText() }}</text>
			<text class="status-desc" v-if="certInfo.reject_reason">{{ certInfo.reject_reason }}</text>
		</view>

		<!-- 认证表单 -->
		<view class="form-container" v-if="!certInfo.status || certInfo.status === 'rejected' || certInfo.status === 'not_certified'">
			<!-- 基本信息 -->
			<view class="form-section">
				<text class="section-title">基本信息</text>

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

				<!-- 邮箱 -->
				<view class="form-item">
					<text class="label">邮箱</text>
					<input
						v-model="form.email"
						placeholder="请输入邮箱（选填）"
						class="input"
						type="text"
					/>
				</view>
			</view>

			<!-- 身份信息 -->
			<view class="form-section">
				<text class="section-title">身份信息</text>

				<!-- 身份类型 -->
				<picker mode="selector" :range="identityLabels" :value="identityIndex" @change="onIdentityChange">
					<view class="form-item">
						<text class="label"><text class="required">*</text>身份类型</text>
						<view class="picker-value">
							<text :class="form.identity_type ? '' : 'placeholder'">
								{{ getIdentityLabel(form.identity_type) || '请选择身份类型' }}
							</text>
							<text class="arrow">></text>
						</view>
					</view>
				</picker>

				<!-- 学历（学生/老师显示） -->
				<picker
					v-if="['student', 'teacher'].includes(form.identity_type)"
					mode="selector"
					:range="educationLabels"
					:value="educationIndex"
					@change="onEducationChange"
				>
					<view class="form-item">
						<text class="label"><text class="required">*</text>学历</text>
						<view class="picker-value">
							<text :class="form.education_level ? '' : 'placeholder'">
								{{ getEducationLabel(form.education_level) || '请选择学历' }}
							</text>
							<text class="arrow">></text>
						</view>
					</view>
				</picker>

				<!-- 入学年份（学生显示） -->
				<picker
					v-if="form.identity_type === 'student'"
					mode="selector"
					:range="yearOptions"
					:value="enrollmentYearIndex"
					@change="onEnrollmentYearChange"
				>
					<view class="form-item">
						<text class="label">入学年份</text>
						<view class="picker-value">
							<text :class="form.enrollment_year ? '' : 'placeholder'">
								{{ form.enrollment_year || '请选择入学年份' }}
							</text>
							<text class="arrow">></text>
						</view>
					</view>
				</picker>

				<!-- 预计毕业年份（学生显示） -->
				<picker
					v-if="form.identity_type === 'student'"
					mode="selector"
					:range="yearOptions"
					:value="graduationYearIndex"
					@change="onGraduationYearChange"
				>
					<view class="form-item">
						<text class="label">预计毕业</text>
						<view class="picker-value">
							<text :class="form.graduation_year ? '' : 'placeholder'">
								{{ form.graduation_year || '请选择毕业年份' }}
							</text>
							<text class="arrow">></text>
						</view>
					</view>
				</picker>
			</view>

			<!-- 单位信息 -->
			<view class="form-section">
				<text class="section-title">单位信息</text>

				<!-- 省份 -->
				<picker mode="selector" :range="provinceOptions" :value="provinceIndex" @change="onProvinceChange">
					<view class="form-item">
						<text class="label"><text class="required">*</text>所在省份</text>
						<view class="picker-value">
							<text :class="form.province ? '' : 'placeholder'">
								{{ form.province || '请选择省份' }}
							</text>
							<text class="arrow">></text>
						</view>
					</view>
				</picker>

				<!-- 城市 -->
				<view class="form-item">
					<text class="label"><text class="required">*</text>所在城市</text>
					<input
						v-model="form.city"
						placeholder="请输入城市"
						class="input"
					/>
				</view>

				<!-- 学校/单位 -->
				<view class="form-item">
					<text class="label"><text class="required">*</text>{{ ['student', 'teacher'].includes(form.identity_type) ? '所在高校' : '单位名称' }}</text>
					<input
						v-model="form.university"
						:placeholder="['student', 'teacher'].includes(form.identity_type) ? '请输入学校名称' : '请输入单位名称'"
						class="input"
					/>
				</view>

				<!-- 院系/部门 -->
				<view class="form-item">
					<text class="label"><text class="required">*</text>{{ ['student', 'teacher'].includes(form.identity_type) ? '所在院系' : '所在部门' }}</text>
					<input
						v-model="form.department"
						:placeholder="['student', 'teacher'].includes(form.identity_type) ? '请输入院系名称' : '请输入部门名称'"
						class="input"
					/>
				</view>

				<!-- 导师姓名（学生显示） -->
				<view class="form-item" v-if="form.identity_type === 'student'">
					<text class="label">导师姓名</text>
					<input
						v-model="form.supervisor_name"
						placeholder="请输入导师姓名（选填）"
						class="input"
					/>
				</view>
			</view>

			<!-- 证件照片 -->
			<view class="form-section" v-if="['student', 'teacher'].includes(form.identity_type)">
				<text class="section-title">证件照片（选填）</text>
				<!-- 学生证/工作证 -->
				<view class="upload-single">
					<view class="upload-box" @click="chooseStudentCard">
						<image
							v-if="form.student_card_photo"
							:src="form.student_card_photo"
							mode="aspectFill"
							class="upload-image"
						></image>
						<view v-else class="upload-placeholder">
							<text class="upload-icon">📷</text>
							<text class="upload-text">{{ form.identity_type === 'student' ? '上传学生证' : '上传工作证' }}</text>
						</view>
					</view>
					<text class="upload-tip">上传证件有助于加快审核</text>
				</view>
			</view>

			<!-- 提示信息 -->
			<view class="tips-card">
				<text class="tips-title">温馨提示</text>
				<text class="tips-text">1. 请确保填写信息真实有效</text>
				<text class="tips-text">2. 实名认证通过后可获得3000元信用额度</text>
				<text class="tips-text">3. 您的信息将严格保密，仅用于身份验证</text>
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
				<text class="info-label">身份类型</text>
				<text class="info-value">{{ getIdentityLabel(certInfo.identity_type) }}</text>
			</view>
			<view class="info-item" v-if="certInfo.education_level">
				<text class="info-label">学历</text>
				<text class="info-value">{{ getEducationLabel(certInfo.education_level) }}</text>
			</view>
			<view class="info-item">
				<text class="info-label">所在单位</text>
				<text class="info-value">{{ certInfo.university }}</text>
			</view>
			<view class="info-item">
				<text class="info-label">院系/部门</text>
				<text class="info-value">{{ certInfo.department }}</text>
			</view>
			<view class="info-item" v-if="certInfo.supervisor_name">
				<text class="info-label">导师</text>
				<text class="info-value">{{ certInfo.supervisor_name }}</text>
			</view>
			<view class="info-item">
				<text class="info-label">认证时间</text>
				<text class="info-value">{{ formatDate(certInfo.certified_at) }}</text>
			</view>

			<view class="credit-info">
				<text class="credit-label">信用额度</text>
				<text class="credit-value">¥3000.00</text>
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
				email: '',
				identity_type: 'student',
				education_level: '',
				enrollment_year: '',
				graduation_year: '',
				province: '',
				city: '',
				university: '',
				department: '',
				supervisor_name: '',
				student_card_photo: ''
			},
			submitting: false,

			// 选项数据
			identityOptions: [
				{ value: 'student', label: '学生' },
				{ value: 'teacher', label: '老师/教职工' },
				{ value: 'enterprise', label: '企业' },
				{ value: 'research', label: '研究所' },
				{ value: 'hospital', label: '医院' }
			],
			educationOptions: [
				{ value: 'bachelor', label: '本科' },
				{ value: 'master', label: '硕士' },
				{ value: 'doctor', label: '博士' },
				{ value: 'other', label: '其他' }
			],
			provinceOptions: [
				'北京', '天津', '上海', '重庆', '河北', '山西', '辽宁', '吉林',
				'黑龙江', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南',
				'湖北', '湖南', '广东', '海南', '四川', '贵州', '云南', '陕西',
				'甘肃', '青海', '台湾', '内蒙古', '广西', '西藏', '宁夏', '新疆', '香港', '澳门'
			]
		}
	},
	computed: {
		identityLabels() {
			return this.identityOptions.map(item => item.label)
		},
		educationLabels() {
			return this.educationOptions.map(item => item.label)
		},
		identityIndex() {
			return Math.max(0, this.identityOptions.findIndex(item => item.value === this.form.identity_type))
		},
		educationIndex() {
			return Math.max(0, this.educationOptions.findIndex(item => item.value === this.form.education_level))
		},
		provinceIndex() {
			return Math.max(0, this.provinceOptions.findIndex(item => item === this.form.province))
		},
		enrollmentYearIndex() {
			return Math.max(0, this.yearOptions.findIndex(item => item === this.form.enrollment_year))
		},
		graduationYearIndex() {
			return Math.max(0, this.yearOptions.findIndex(item => item === this.form.graduation_year))
		},
		yearOptions() {
			const currentYear = new Date().getFullYear()
			const years = []
			for (let i = currentYear + 6; i >= currentYear - 20; i--) {
				years.push(i.toString())
			}
			return years
		}
	},
	onLoad() {
		this.loadCertInfo()
	},
	methods: {
		onIdentityChange(e) {
			const item = this.identityOptions[Number(e.detail.value)]
			if (!item) return
			this.form.identity_type = item.value
			if (!['student', 'teacher'].includes(item.value)) {
				this.form.education_level = ''
				this.form.enrollment_year = ''
				this.form.graduation_year = ''
				this.form.supervisor_name = ''
				this.form.student_card_photo = ''
			}
		},

		onEducationChange(e) {
			const item = this.educationOptions[Number(e.detail.value)]
			if (item) {
				this.form.education_level = item.value
			}
		},

		onProvinceChange(e) {
			this.form.province = this.provinceOptions[Number(e.detail.value)] || ''
		},

		onEnrollmentYearChange(e) {
			this.form.enrollment_year = this.yearOptions[Number(e.detail.value)] || ''
		},

		onGraduationYearChange(e) {
			this.form.graduation_year = this.yearOptions[Number(e.detail.value)] || ''
		},

		// 加载认证信息
		async loadCertInfo() {
			try {
				const res = await api.getCertification()
				if (res.data) {
					if (res.data.status === 'not_certified') {
						console.log('用户未提交认证信息')
						return
					}
					this.certInfo = res.data
					// 填充表单
					if (res.data.identity_type) {
						this.form.identity_type = res.data.identity_type
					}
					if (res.data.education_level) {
						this.form.education_level = res.data.education_level
					}
				}
			} catch (e) {
				console.error('加载认证信息失败', e)
			}
		},

		// 获取身份类型标签
		getIdentityLabel(value) {
			const item = this.identityOptions.find(o => o.value === value)
			return item ? item.label : ''
		},

		// 获取学历标签
		getEducationLabel(value) {
			const item = this.educationOptions.find(o => o.value === value)
			return item ? item.label : ''
		},

		// 选择身份证正面
		chooseIdCardFront() {
			this.uploadImage('id_card_front')
		},

		// 选择身份证反面
		chooseIdCardBack() {
			this.uploadImage('id_card_back')
		},

		// 选择学生证
		chooseStudentCard() {
			this.uploadImage('student_card_photo')
		},

		// 上传图片
		uploadImage(field) {
			uni.chooseImage({
				count: 1,
				sizeType: ['compressed'],
				sourceType: ['album', 'camera'],
				success: (res) => {
					const tempFilePath = res.tempFilePaths[0]
					this.doUpload(tempFilePath, field)
				}
			})
		},

		// 执行上传
		async doUpload(filePath, field) {
			uni.showLoading({ title: '上传中...' })

			try {
				const token = uni.getStorageSync('token')

				uni.uploadFile({
					url: `${api.baseUrl}/api/v1/upload/image`,
					filePath: filePath,
					name: 'file',
					header: {
						'Authorization': `Bearer ${token}`
					},
					success: (uploadRes) => {
						let data = {}
						try {
							data = JSON.parse(uploadRes.data)
						} catch (e) {
							uni.showToast({ title: '上传响应异常', icon: 'none' })
							return
						}
						if (data.code === 200) {
							this.form[field] = data.data.url
							uni.showToast({ title: '上传成功', icon: 'success' })
						} else {
							uni.showToast({ title: '上传失败', icon: 'none' })
						}
					},
					fail: () => {
						uni.showToast({ title: '上传失败', icon: 'none' })
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
			// 验证必填项
			if (!this.form.real_name) {
				uni.showToast({ title: '请输入真实姓名', icon: 'none' })
				return
			}

			if (!this.form.id_card) {
				uni.showToast({ title: '请输入身份证号', icon: 'none' })
				return
			}

			if (!/^[1-9]\d{5}(18|19|20)\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$/.test(this.form.id_card)) {
				uni.showToast({ title: '身份证号格式不正确', icon: 'none' })
				return
			}

			if (!this.form.identity_type) {
				uni.showToast({ title: '请选择身份类型', icon: 'none' })
				return
			}

			if (['student', 'teacher'].includes(this.form.identity_type) && !this.form.education_level) {
				uni.showToast({ title: '请选择学历', icon: 'none' })
				return
			}

			if (!this.form.province) {
				uni.showToast({ title: '请选择省份', icon: 'none' })
				return
			}

			if (!this.form.city) {
				uni.showToast({ title: '请输入城市', icon: 'none' })
				return
			}

			if (!this.form.university) {
				uni.showToast({ title: '请输入学校/单位名称', icon: 'none' })
				return
			}

			if (!this.form.department) {
				uni.showToast({ title: '请输入院系/部门', icon: 'none' })
				return
			}

			this.submitting = true

			try {
				await api.submitCertification({
					real_name: this.form.real_name,
					id_card: this.form.id_card,
					identity_type: this.form.identity_type,
					education_level: this.form.education_level || null,
					enrollment_year: this.form.enrollment_year || null,
					graduation_year: this.form.graduation_year || null,
					province: this.form.province,
					city: this.form.city,
					university: this.form.university,
					department: this.form.department,
					supervisor_name: this.form.supervisor_name || null,
					student_card_photo: this.form.student_card_photo || null
				})

				uni.showToast({ title: '提交成功', icon: 'success' })

				setTimeout(() => {
					this.loadCertInfo()
				}, 1500)
			} catch (e) {
				console.error('提交失败', e)
				uni.showToast({ title: e.message || e.detail || '提交失败', icon: 'none' })
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

.form-section {
	background: white;
	border-radius: 16rpx;
	padding: 30rpx;
	margin-bottom: 20rpx;

	.section-title {
		font-size: 32rpx;
		font-weight: bold;
		color: #333;
		margin-bottom: 20rpx;
		display: block;
		padding-left: 20rpx;
		border-left: 6rpx solid #667eea;
	}
}

.form-item {
	display: flex;
	align-items: center;
	padding: 25rpx 0;
	border-bottom: 1rpx solid #f0f0f0;

	&:last-child {
		border-bottom: none;
	}

	.label {
		width: 180rpx;
		font-size: 28rpx;
		color: #333;
		flex-shrink: 0;

		.required {
			color: #ff4d4f;
			margin-right: 5rpx;
		}
	}

	.input {
		flex: 1;
		font-size: 28rpx;
		color: #333;
		text-align: right;
	}

	.picker-value {
		flex: 1;
		display: flex;
		align-items: center;
		justify-content: flex-end;

		text {
			font-size: 28rpx;
			color: #333;
		}

		.placeholder {
			color: #999;
		}

		.arrow {
			margin-left: 10rpx;
			color: #ccc;
		}
	}
}

/* 上传区域 */
.upload-grid {
	display: flex;
	gap: 30rpx;
	margin-top: 20rpx;

	.upload-item {
		flex: 1;

		.upload-box {
			width: 100%;
			height: 220rpx;
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
				background: #fafafa;

				.upload-icon {
					font-size: 50rpx;
					margin-bottom: 10rpx;
				}

				.upload-text {
					font-size: 22rpx;
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

.upload-single {
	margin-top: 20rpx;

	.upload-box {
		width: 100%;
		height: 200rpx;
		border: 2rpx dashed #ddd;
		border-radius: 12rpx;
		overflow: hidden;

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
			background: #fafafa;

			.upload-icon {
				font-size: 50rpx;
				margin-bottom: 10rpx;
			}

			.upload-text {
				font-size: 24rpx;
				color: #999;
			}
		}
	}

	.upload-tip {
		display: block;
		text-align: center;
		font-size: 24rpx;
		color: #999;
		margin-top: 16rpx;
	}
}

/* 提示卡片 */
.tips-card {
	background: #fff7e6;
	padding: 30rpx;
	margin-bottom: 20rpx;
	border-radius: 16rpx;
	border: 1rpx solid #ffe7ba;

	.tips-title {
		font-size: 28rpx;
		font-weight: bold;
		color: #fa8c16;
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
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
	border-radius: 16rpx;

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

	.credit-info {
		margin-top: 30rpx;
		padding: 30rpx;
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		border-radius: 12rpx;
		display: flex;
		justify-content: space-between;
		align-items: center;

		.credit-label {
			font-size: 28rpx;
			color: rgba(255, 255, 255, 0.9);
		}

		.credit-value {
			font-size: 40rpx;
			font-weight: bold;
			color: white;
		}
	}
}

</style>
