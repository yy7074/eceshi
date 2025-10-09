<template>
	<view class="address-container">
		<!-- 地址列表 -->
		<view v-if="mode === 'manage'" class="address-list">
			<view 
				v-for="item in addresses" 
				:key="item.id" 
				class="address-item card"
			>
				<view class="address-content">
					<view class="address-header">
						<text class="receiver">{{ item.receiver_name }}</text>
						<text class="phone">{{ item.phone }}</text>
						<view v-if="item.is_default" class="default-badge">默认</view>
					</view>
					<text class="address-detail">
						{{ item.province }}{{ item.city }}{{ item.district }}{{ item.detail_address }}
					</text>
				</view>
				<view class="address-actions">
					<text class="action-btn" @click="editAddress(item)">编辑</text>
					<text class="action-btn delete" @click="deleteAddress(item.id)">删除</text>
					<text v-if="!item.is_default" class="action-btn" @click="setDefault(item.id)">设为默认</text>
				</view>
			</view>
			
			<!-- 空状态 -->
			<view v-if="addresses.length === 0" class="empty-state">
				<text class="empty-text">暂无收货地址</text>
			</view>
		</view>
		
		<!-- 选择模式 -->
		<view v-else class="address-list">
			<view 
				v-for="item in addresses" 
				:key="item.id" 
				class="address-item card selectable"
				@click="selectAddress(item)"
			>
				<view class="address-content">
					<view class="address-header">
						<text class="receiver">{{ item.receiver_name }}</text>
						<text class="phone">{{ item.phone }}</text>
						<view v-if="item.is_default" class="default-badge">默认</view>
					</view>
					<text class="address-detail">
						{{ item.province }}{{ item.city }}{{ item.district }}{{ item.detail_address }}
					</text>
				</view>
			</view>
		</view>
		
		<!-- 添加按钮 -->
		<button class="btn-add" @click="addAddress">+ 添加新地址</button>
		
		<!-- 编辑/添加弹窗 -->
		<uni-popup ref="popup" type="bottom">
			<view class="form-popup">
				<view class="popup-header">
					<text class="title">{{ editingAddress ? '编辑地址' : '添加地址' }}</text>
					<text class="close" @click="closePopup">×</text>
				</view>
				
				<view class="form-content">
					<view class="form-item">
						<text class="label"><text class="required">*</text>收件人</text>
						<input 
							v-model="form.receiver_name" 
							placeholder="请输入收件人姓名"
							class="input"
						/>
					</view>
					
					<view class="form-item">
						<text class="label"><text class="required">*</text>手机号</text>
						<input 
							v-model="form.phone" 
							type="number"
							maxlength="11"
							placeholder="请输入手机号"
							class="input"
						/>
					</view>
					
					<view class="form-item">
						<text class="label"><text class="required">*</text>所在地区</text>
						<picker 
							mode="multiSelector" 
							:range="regionData" 
							:value="regionIndex"
							@change="onRegionChange"
							@columnchange="onRegionColumnChange"
						>
							<view class="picker">
								{{ regionText || '请选择省市区' }}
							</view>
						</picker>
					</view>
					
					<view class="form-item">
						<text class="label"><text class="required">*</text>详细地址</text>
						<textarea 
							v-model="form.detail_address" 
							placeholder="街道、楼牌号等"
							class="textarea"
							maxlength="100"
						></textarea>
					</view>
					
					<view class="form-item checkbox-item">
						<checkbox 
							:checked="form.is_default" 
							@change="e => form.is_default = e.detail.value"
							color="#007AFF"
						/>
						<text class="checkbox-label">设为默认地址</text>
					</view>
					
					<button class="btn-save" :loading="saving" @click="saveAddress">保存</button>
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
				mode: 'manage', // manage | select
				addresses: [],
				editingAddress: null,
				
				form: {
					receiver_name: '',
					phone: '',
					province: '',
					city: '',
					district: '',
					detail_address: '',
					is_default: false
				},
				
				// 地区数据（简化版）
				regionData: [
					['北京市', '上海市', '广东省', '江苏省', '浙江省'],
					['北京市', '上海市', '广州市', '南京市', '杭州市'],
					['海淀区', '黄浦区', '天河区', '鼓楼区', '西湖区']
				],
				regionIndex: [0, 0, 0],
				regionText: '',
				
				saving: false
			}
		},
		onLoad(options) {
			this.mode = options.mode || 'manage'
			this.loadAddresses()
		},
		methods: {
			// 加载地址列表
			async loadAddresses() {
				try {
					const res = await api.getAddresses()
					this.addresses = res.data || []
				} catch (error) {
					console.error('加载地址失败', error)
				}
			},
			
			// 添加地址
			addAddress() {
				this.editingAddress = null
				this.form = {
					receiver_name: '',
					phone: '',
					province: '',
					city: '',
					district: '',
					detail_address: '',
					is_default: false
				}
				this.regionText = ''
				this.regionIndex = [0, 0, 0]
				this.$refs.popup.open()
			},
			
			// 编辑地址
			editAddress(address) {
				this.editingAddress = address
				this.form = {
					receiver_name: address.receiver_name,
					phone: address.phone,
					province: address.province,
					city: address.city,
					district: address.district,
					detail_address: address.detail_address,
					is_default: address.is_default
				}
				this.regionText = `${address.province} ${address.city} ${address.district || ''}`
				this.$refs.popup.open()
			},
			
			// 地区选择
			onRegionChange(e) {
				const values = e.detail.value
				this.regionIndex = values
				this.form.province = this.regionData[0][values[0]]
				this.form.city = this.regionData[1][values[1]]
				this.form.district = this.regionData[2][values[2]]
				this.regionText = `${this.form.province} ${this.form.city} ${this.form.district}`
			},
			
			// 地区列变化
			onRegionColumnChange(e) {
				// 简化处理，实际应该根据选择动态加载下级
			},
			
			// 保存地址
			async saveAddress() {
				// 验证
				if (!this.form.receiver_name) {
					return uni.showToast({ title: '请输入收件人', icon: 'none' })
				}
				if (!this.form.phone || !/^1[3-9]\d{9}$/.test(this.form.phone)) {
					return uni.showToast({ title: '请输入正确的手机号', icon: 'none' })
				}
				if (!this.form.province || !this.form.city) {
					return uni.showToast({ title: '请选择所在地区', icon: 'none' })
				}
				if (!this.form.detail_address) {
					return uni.showToast({ title: '请输入详细地址', icon: 'none' })
				}
				
				this.saving = true
				try {
					if (this.editingAddress) {
						// 更新
						await api.updateAddress(this.editingAddress.id, this.form)
						uni.showToast({ title: '地址更新成功', icon: 'success' })
					} else {
						// 添加
						await api.addAddress(this.form)
						uni.showToast({ title: '地址添加成功', icon: 'success' })
					}
					
					this.closePopup()
					this.loadAddresses()
					
				} catch (error) {
					console.error('保存地址失败', error)
					uni.showToast({ title: '保存失败', icon: 'none' })
				} finally {
					this.saving = false
				}
			},
			
			// 删除地址
			async deleteAddress(id) {
				uni.showModal({
					title: '确认删除',
					content: '确定要删除这个地址吗？',
					success: async (res) => {
						if (res.confirm) {
							try {
								await api.deleteAddress(id)
								uni.showToast({ title: '删除成功', icon: 'success' })
								this.loadAddresses()
							} catch (error) {
								console.error('删除地址失败', error)
								uni.showToast({ title: '删除失败', icon: 'none' })
							}
						}
					}
				})
			},
			
			// 设为默认
			async setDefault(id) {
				try {
					await api.setDefaultAddress(id)
					uni.showToast({ title: '已设为默认', icon: 'success' })
					this.loadAddresses()
				} catch (error) {
					console.error('设置默认失败', error)
					uni.showToast({ title: '设置失败', icon: 'none' })
				}
			},
			
			// 选择地址（选择模式）
			selectAddress(address) {
				if (this.mode === 'select') {
					// 通过事件返回选中的地址
					const eventChannel = this.getOpenerEventChannel()
					eventChannel.emit('selectAddress', address)
					uni.navigateBack()
				}
			},
			
			// 关闭弹窗
			closePopup() {
				this.$refs.popup.close()
			}
		}
	}
</script>

<style lang="scss" scoped>
	.address-container {
		min-height: 100vh;
		background-color: #f8f8f8;
		padding: 20rpx 30rpx 140rpx;
	}
	
	.address-list {
		.address-item {
			padding: 30rpx;
			margin-bottom: 20rpx;
			
			&.selectable {
				cursor: pointer;
				transition: all 0.3s;
				
				&:active {
					background-color: #f5f5f5;
				}
			}
			
			.address-content {
				.address-header {
					display: flex;
					align-items: center;
					margin-bottom: 16rpx;
					
					.receiver {
						font-size: 32rpx;
						font-weight: bold;
						color: #333;
						margin-right: 20rpx;
					}
					
					.phone {
						font-size: 28rpx;
						color: #666;
						flex: 1;
					}
					
					.default-badge {
						padding: 4rpx 16rpx;
						background-color: #007AFF;
						color: #ffffff;
						font-size: 22rpx;
						border-radius: 20rpx;
					}
				}
				
				.address-detail {
					display: block;
					font-size: 26rpx;
					color: #666;
					line-height: 1.6;
				}
			}
			
			.address-actions {
				display: flex;
				justify-content: flex-end;
				margin-top: 20rpx;
				padding-top: 20rpx;
				border-top: 2rpx solid #f0f0f0;
				
				.action-btn {
					padding: 8rpx 24rpx;
					background-color: #f5f5f5;
					color: #333;
					font-size: 24rpx;
					border-radius: 8rpx;
					margin-left: 16rpx;
					
					&.delete {
						color: #ff4d4f;
					}
				}
			}
		}
		
		.empty-state {
			padding: 200rpx 0;
			text-align: center;
			
			.empty-text {
				font-size: 28rpx;
				color: #999;
			}
		}
	}
	
	.btn-add {
		position: fixed;
		bottom: 40rpx;
		left: 30rpx;
		right: 30rpx;
		height: 88rpx;
		line-height: 88rpx;
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		color: #ffffff;
		border-radius: 44rpx;
		font-size: 32rpx;
		border: none;
	}
	
	.form-popup {
		background-color: #ffffff;
		border-radius: 24rpx 24rpx 0 0;
		
		.popup-header {
			display: flex;
			justify-content: space-between;
			align-items: center;
			padding: 30rpx 40rpx;
			border-bottom: 2rpx solid #f0f0f0;
			
			.title {
				font-size: 36rpx;
				font-weight: bold;
				color: #333;
			}
			
			.close {
				font-size: 60rpx;
				color: #999;
				line-height: 1;
			}
		}
		
		.form-content {
			padding: 40rpx;
			max-height: 1000rpx;
			overflow-y: auto;
			
			.form-item {
				margin-bottom: 30rpx;
				
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
				
				.input, .picker {
					width: 100%;
					height: 80rpx;
					padding: 0 24rpx;
					border: 2rpx solid #e0e0e0;
					border-radius: 12rpx;
					font-size: 28rpx;
				}
				
				.picker {
					line-height: 80rpx;
					color: #333;
				}
				
				.textarea {
					width: 100%;
					min-height: 150rpx;
					padding: 20rpx;
					border: 2rpx solid #e0e0e0;
					border-radius: 12rpx;
					font-size: 28rpx;
				}
				
				&.checkbox-item {
					display: flex;
					align-items: center;
					
					.checkbox-label {
						margin-left: 16rpx;
						font-size: 28rpx;
						color: #333;
					}
				}
			}
			
			.btn-save {
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
	}
</style>

