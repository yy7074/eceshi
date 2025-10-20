<template>
	<view class="create-group-page">
		<!-- 团体名称 -->
		<view class="form-row">
			<view class="row-label">
				<text>团体名称</text>
				<text class="required">*</text>
			</view>
			<view class="row-value">
				<text class="auto-text">系统自动生成</text>
			</view>
		</view>
		
		<!-- 团体头像 -->
		<view class="form-row upload-row">
			<view class="row-label">
				<text>团体头像</text>
			</view>
			<view class="upload-wrapper" @click="chooseAvatar">
				<image v-if="form.avatar" :src="form.avatar" mode="aspectFill" class="avatar-preview"></image>
				<view v-else class="upload-placeholder">
					<text class="upload-icon">⬆</text>
				</view>
			</view>
		</view>
		
		<!-- 单位类型 -->
		<view class="form-row" @click="showUnitTypePicker">
			<view class="row-label">
				<text>单位类型</text>
				<text class="required">*</text>
			</view>
			<view class="row-value">
				<text :class="form.unitType ? 'value-text' : 'placeholder-text'">
					{{ form.unitType || '请选择' }}
				</text>
				<text class="arrow">›</text>
			</view>
		</view>
		
		<!-- 所在地区 -->
		<view class="form-row" @click="showRegionPicker">
			<view class="row-label">
				<text>所在地区</text>
				<text class="required">*</text>
			</view>
			<view class="row-value">
				<text :class="form.region ? 'value-text' : 'placeholder-text'">
					{{ form.region || '山东省-济南市-历下区' }}
				</text>
				<text class="arrow">›</text>
			</view>
		</view>
		
		<!-- 单位名称 -->
		<view class="form-row input-row">
			<view class="row-label">
				<text>单位名称</text>
				<text class="required">*</text>
			</view>
			<input 
				v-model="form.unitName"
				class="row-input"
				placeholder="请输入"
			/>
		</view>
		
		<!-- 详细地址 -->
		<view class="form-row input-row">
			<view class="row-label">
				<text>详细地址</text>
			</view>
			<input 
				v-model="form.address"
				class="row-input"
				placeholder="请输入"
			/>
		</view>
		
		<!-- 团长姓名 -->
		<view class="form-row">
			<view class="row-label">
				<text>团长姓名</text>
				<text class="required">*</text>
			</view>
			<view class="row-value">
				<text class="value-text">{{ leaderName }}</text>
				<button v-if="!isCertified" class="cert-btn" @click="goCertification">立即实名</button>
			</view>
		</view>
		
		<!-- 团长电话 -->
		<view class="form-row">
			<view class="row-label">
				<text>团长电话</text>
				<text class="required">*</text>
			</view>
			<view class="row-value">
				<text class="value-text">{{ leaderPhone }}</text>
			</view>
		</view>
		
		<!-- 团长邮箱 -->
		<view class="form-row input-row">
			<view class="row-label">
				<text>团长邮箱</text>
			</view>
			<input 
				v-model="form.email"
				class="row-input"
				type="text"
				placeholder="请输入"
			/>
		</view>
		
		<!-- 底部按钮 -->
		<view class="footer-btn">
			<button class="btn-submit" @click="submitCreate">立即创建</button>
		</view>
	</view>
</template>

<script>
export default {
	data() {
		return {
			projectId: '',
			projectName: '',
			form: {
				avatar: '',
				unitType: '',
				region: '山东省-济南市-历下区',
				unitName: '',
				address: '',
				email: ''
			},
			unitTypes: ['高校', '科研院所', '企业', '医院', '其他'],
			leaderName: '会员ihC12T',
			leaderPhone: '15634078193',
			isCertified: false
		}
	},
	
	onLoad(options) {
		this.loadUserInfo()
		if (options.projectId) {
			this.projectId = options.projectId
		}
		if (options.projectName) {
			this.projectName = decodeURIComponent(options.projectName)
		}
	},
	
	methods: {
		// 加载用户信息
		async loadUserInfo() {
			try {
				const userInfo = uni.getStorageSync('userInfo') || {}
				this.leaderName = userInfo.nickname || `会员${userInfo.id || ''}`
				this.leaderPhone = userInfo.phone || ''
				this.isCertified = userInfo.is_certified || false
				this.form.email = userInfo.email || ''
			} catch (error) {
				console.error('加载用户信息失败', error)
			}
		},
		
		// 选择头像
		chooseAvatar() {
			uni.chooseImage({
				count: 1,
				sizeType: ['compressed'],
				sourceType: ['album', 'camera'],
				success: (res) => {
					this.form.avatar = res.tempFilePaths[0]
					// TODO: 上传到服务器
				}
			})
		},
		
		// 显示单位类型选择器
		showUnitTypePicker() {
			uni.showActionSheet({
				itemList: this.unitTypes,
				success: (res) => {
					this.form.unitType = this.unitTypes[res.tapIndex]
				}
			})
		},
		
		// 显示地区选择器
		showRegionPicker() {
			uni.showToast({
				title: '地区选择功能开发中',
				icon: 'none'
			})
		},
		
		// 去实名认证
		goCertification() {
			uni.navigateTo({
				url: '/pagesA/certification/certification'
			})
		},
		
		// 提交创建
		submitCreate() {
			// 验证必填项
			if (!this.form.unitType) {
				uni.showToast({
					title: '请选择单位类型',
					icon: 'none'
				})
				return
			}
			
			if (!this.form.unitName) {
				uni.showToast({
					title: '请输入单位名称',
					icon: 'none'
				})
				return
			}
			
			if (!this.isCertified) {
				uni.showModal({
					title: '提示',
					content: '创建团队需要先完成实名认证',
					confirmText: '去认证',
					success: (res) => {
						if (res.confirm) {
							this.goCertification()
						}
					}
				})
				return
			}
			
			uni.showModal({
				title: '确认创建',
				content: '确定要创建团队吗？',
				success: (res) => {
					if (res.confirm) {
						this.doCreate()
					}
				}
			})
		},
		
		// 执行创建
		async doCreate() {
			try {
				uni.showLoading({ title: '创建中...' })
				
			// 调用API创建团队
			await api.createGroup({
				name: this.form.unitName,
				avatar: this.form.avatar,
				unit_type: this.form.unitType,
				region: this.form.region,
				address: this.form.address,
				leader_name: this.form.leaderName,
				leader_phone: this.form.leaderPhone,
				leader_email: this.form.email
			})
			
			uni.hideLoading()
			
			uni.showToast({
				title: '创建成功',
				icon: 'success',
				duration: 2000
			})
			
			setTimeout(() => {
				uni.navigateBack()
			}, 2000)
			} catch (error) {
				uni.hideLoading()
				console.error('创建失败', error)
				uni.showToast({
					title: error.message || '创建失败',
					icon: 'none'
				})
			}
		}
	}
}
</script>

<style lang="scss" scoped>
.create-group-page {
	min-height: 100vh;
	background: #f5f5f5;
	padding-bottom: 140rpx;
}

/* 表单行 */
.form-row {
	background: white;
	padding: 30rpx;
	border-bottom: 1rpx solid #f5f5f5;
	display: flex;
	justify-content: space-between;
	align-items: center;
}

.form-row.upload-row {
	min-height: 150rpx;
}

.form-row.input-row {
	padding-right: 0;
}

.row-label {
	font-size: 28rpx;
	color: #333;
	display: flex;
	align-items: center;
	
	.required {
		color: #ff4444;
		margin-left: 5rpx;
	}
}

.row-value {
	display: flex;
	align-items: center;
	gap: 15rpx;
}

.auto-text {
	font-size: 26rpx;
	color: #999;
}

.value-text {
	font-size: 26rpx;
	color: #333;
}

.placeholder-text {
	font-size: 26rpx;
	color: #ccc;
}

.arrow {
	font-size: 32rpx;
	color: #ccc;
}

/* 上传区域 */
.upload-wrapper {
	width: 120rpx;
	height: 120rpx;
}

.avatar-preview {
	width: 100%;
	height: 100%;
	border-radius: 12rpx;
}

.upload-placeholder {
	width: 100%;
	height: 100%;
	background: #f0f8ff;
	border: 2rpx dashed #4dabf7;
	border-radius: 12rpx;
	display: flex;
	align-items: center;
	justify-content: center;
}

.upload-icon {
	font-size: 50rpx;
	color: #4dabf7;
}

/* 输入框 */
.row-input {
	flex: 1;
	text-align: right;
	font-size: 26rpx;
	color: #333;
	padding: 30rpx;
}

/* 实名按钮 */
.cert-btn {
	background: #eef2ff;
	color: #667eea;
	border: none;
	padding: 8rpx 20rpx;
	border-radius: 8rpx;
	font-size: 24rpx;
}

/* 底部按钮 */
.footer-btn {
	position: fixed;
	bottom: 0;
	left: 0;
	right: 0;
	padding: 20rpx 30rpx;
	background: white;
	box-shadow: 0 -2rpx 10rpx rgba(0, 0, 0, 0.05);
}

.btn-submit {
	width: 100%;
	background: linear-gradient(135deg, #4dabf7 0%, #1890ff 100%);
	color: white;
	border: none;
	border-radius: 50rpx;
	padding: 30rpx;
	font-size: 32rpx;
	font-weight: bold;
}
</style>
