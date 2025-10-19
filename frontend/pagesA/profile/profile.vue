<template>
	<view class="profile-page">
		<!-- 头像 -->
		<view class="form-item">
			<text class="label">头像</text>
			<view class="avatar-wrap" @click="chooseAvatar">
				<image 
					:src="form.avatar || 'https://ui-avatars.com/api/?name=User'" 
					mode="aspectFill" 
					class="avatar"
				></image>
				<text class="change-text">点击更换</text>
			</view>
		</view>
		
		<!-- 昵称 -->
		<view class="form-item">
			<text class="label">昵称</text>
			<input 
				v-model="form.nickname" 
				placeholder="请输入昵称"
				class="input"
				maxlength="20"
			/>
		</view>
		
		<!-- 手机号 -->
		<view class="form-item">
			<text class="label">手机号</text>
			<text class="value">{{ form.phone }}</text>
			<text class="tag">已绑定</text>
		</view>
		
		<!-- 性别 -->
		<view class="form-item">
			<text class="label">性别</text>
			<picker mode="selector" :range="genderOptions" :value="genderIndex" @change="onGenderChange">
				<view class="picker">
					{{ genderOptions[genderIndex] || '请选择' }}
				</view>
			</picker>
		</view>
		
		<!-- 邮箱 -->
		<view class="form-item">
			<text class="label">邮箱</text>
			<input 
				v-model="form.email" 
				placeholder="请输入邮箱"
				class="input"
				type="text"
			/>
		</view>
		
		<!-- 保存按钮 -->
		<view class="save-btn-wrap">
			<button class="save-btn" @click="saveProfile" :disabled="saving">
				{{ saving ? '保存中...' : '保存' }}
			</button>
		</view>
	</view>
</template>

<script>
import api from '@/utils/api.js'

export default {
	data() {
		return {
			form: {
				avatar: '',
				nickname: '',
				phone: '',
				gender: '',
				email: ''
			},
			genderOptions: ['保密', '男', '女'],
			genderIndex: 0,
			saving: false
		}
	},
	onLoad() {
		this.loadUserInfo()
	},
	methods: {
		// 加载用户信息
		async loadUserInfo() {
			try {
				const res = await api.getUserInfo()
				this.form = res.data || {}
				
				// 设置性别索引
				if (this.form.gender === 'male') {
					this.genderIndex = 1
				} else if (this.form.gender === 'female') {
					this.genderIndex = 2
				} else {
					this.genderIndex = 0
				}
			} catch (e) {
				console.error('加载用户信息失败', e)
			}
		},
		
		// 选择头像
		chooseAvatar() {
			uni.chooseImage({
				count: 1,
				sizeType: ['compressed'],
				sourceType: ['album', 'camera'],
				success: (res) => {
					const tempFilePath = res.tempFilePaths[0]
					this.uploadAvatar(tempFilePath)
				}
			})
		},
		
		// 上传头像
		async uploadAvatar(filePath) {
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
							this.form.avatar = data.data.url
							uni.showToast({
								title: '头像上传成功',
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
				console.error('上传头像失败', e)
			}
		},
		
		// 性别选择
		onGenderChange(e) {
			this.genderIndex = e.detail.value
			const genderMap = ['', 'male', 'female']
			this.form.gender = genderMap[this.genderIndex]
		},
		
		// 保存资料
		async saveProfile() {
			// 验证
			if (!this.form.nickname) {
				uni.showToast({
					title: '请输入昵称',
					icon: 'none'
				})
				return
			}
			
			if (this.form.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(this.form.email)) {
				uni.showToast({
					title: '邮箱格式不正确',
					icon: 'none'
				})
				return
			}
			
			this.saving = true
			
			try {
				await api.updateUserInfo({
					avatar: this.form.avatar,
					nickname: this.form.nickname,
					gender: this.form.gender,
					email: this.form.email
				})
				
				uni.showToast({
					title: '保存成功',
					icon: 'success'
				})
				
				setTimeout(() => {
					uni.navigateBack()
				}, 1500)
			} catch (e) {
				console.error('保存失败', e)
				uni.showToast({
					title: e.message || '保存失败',
					icon: 'none'
				})
			} finally {
				this.saving = false
			}
		}
	}
}
</script>

<style lang="scss" scoped>
.profile-page {
	min-height: 100vh;
	background: #f5f5f5;
	padding: 20rpx;
}

.form-item {
	display: flex;
	align-items: center;
	background: white;
	padding: 30rpx;
	margin-bottom: 20rpx;
	border-radius: 12rpx;
	
	.label {
		width: 150rpx;
		font-size: 28rpx;
		color: #333;
	}
	
	.input,
	.picker,
	.value {
		flex: 1;
		font-size: 28rpx;
		color: #333;
		text-align: right;
	}
	
	.input {
		text-align: right;
	}
	
	.value {
		color: #999;
	}
	
	.tag {
		margin-left: 15rpx;
		padding: 5rpx 15rpx;
		background: #4facfe;
		color: white;
		border-radius: 6rpx;
		font-size: 22rpx;
	}
	
	.avatar-wrap {
		flex: 1;
		display: flex;
		align-items: center;
		justify-content: flex-end;
		
		.avatar {
			width: 120rpx;
			height: 120rpx;
			border-radius: 60rpx;
			margin-right: 20rpx;
		}
		
		.change-text {
			font-size: 26rpx;
			color: #4facfe;
		}
	}
}

.save-btn-wrap {
	padding: 60rpx 30rpx;
	
	.save-btn {
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
</style>

