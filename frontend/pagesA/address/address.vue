<template>
	<view class="address-container">
		<!-- 地址列表 -->
		<view class="address-list">
			<view 
				v-for="item in addresses" 
				:key="item.id" 
				class="address-item"
				@click="handleAddressClick(item)"
			>
				<view class="address-content">
					<view class="address-header">
						<text class="receiver">{{ item.name || item.receiver_name }}</text>
						<text class="phone">{{ item.phone }}</text>
						<view v-if="item.is_default" class="default-badge">默认</view>
					</view>
					<text class="address-detail">
						{{ item.province }}{{ item.city }}{{ item.district }}{{ item.detail || item.detail_address }}
					</text>
				</view>
				<view class="address-actions" v-if="mode === 'manage'" @click.stop>
					<button class="action-btn" @click="editAddress(item)">编辑</button>
					<button class="action-btn delete" @click="deleteAddress(item.id)">删除</button>
					<button v-if="!item.is_default" class="action-btn" @click="setDefault(item.id)">设为默认</button>
				</view>
			</view>
			
			<!-- 空状态 -->
			<view v-if="addresses.length === 0" class="empty-state">
				<text class="empty-icon">📍</text>
				<text class="empty-text">暂无收货地址</text>
			</view>
		</view>
		
		<!-- 添加按钮 -->
		<view class="btn-add" @click="addAddress">+ 添加新地址</view>
		
		<!-- 编辑/添加弹窗 -->
		<view class="form-popup" v-if="showPopup" @click="closePopup">
			<view class="popup-content" @click.stop>
				<view class="popup-header">
					<text class="title">{{ editingAddress ? '编辑地址' : '添加地址' }}</text>
					<text class="close" @click="closePopup">×</text>
				</view>
				
				<scroll-view class="form-content" scroll-y>
					<view class="form-item">
						<text class="label"><text class="required">*</text>收件人</text>
						<input 
							v-model="form.name" 
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
						<view class="region-input" @click="selectRegion">
							<text :class="{ placeholder: !regionText }">{{ regionText || '请选择省市区' }}</text>
							<text class="arrow">▶</text>
						</view>
					</view>
					
					<view class="form-item">
						<text class="label"><text class="required">*</text>详细地址</text>
						<textarea 
							v-model="form.detail" 
							placeholder="如道路、门牌号、小区、楼栋号、单元等"
							class="textarea"
							maxlength="200"
						/>
					</view>
					
					<view class="form-item checkbox">
						<label>
							<checkbox :checked="form.is_default" @click="form.is_default = !form.is_default" />
							<text>设为默认地址</text>
						</label>
					</view>
				</scroll-view>
				
				<view class="popup-footer">
					<button class="btn-cancel" @click="closePopup">取消</button>
					<button class="btn-save" @click="saveAddress" :disabled="saving">
						{{ saving ? '保存中...' : '保存' }}
					</button>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
import api from '@/utils/api.js'

export default {
	data() {
		return {
			mode: 'manage', // manage 或 select
			addresses: [],
			showPopup: false,
			editingAddress: null,
			saving: false,
			form: {
				name: '',
				phone: '',
				province: '',
				city: '',
				district: '',
				detail: '',
				is_default: false
			}
		}
	},
	computed: {
		regionText() {
			if (this.form.province && this.form.city && this.form.district) {
				return `${this.form.province} ${this.form.city} ${this.form.district}`
			}
			return ''
		}
	},
	onLoad(options) {
		if (options.mode) {
			this.mode = options.mode
		}
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
				uni.showToast({ title: '加载失败', icon: 'none' })
			}
		},
		
		// 添加地址
		addAddress() {
			this.editingAddress = null
			this.form = {
				name: '',
				phone: '',
				province: '',
				city: '',
				district: '',
				detail: '',
				is_default: false
			}
			this.showPopup = true
		},
		
		// 编辑地址
		editAddress(address) {
			this.editingAddress = address
			this.form = {
				name: address.name || address.receiver_name || '',
				phone: address.phone || '',
				province: address.province || '',
				city: address.city || '',
				district: address.district || '',
				detail: address.detail || address.detail_address || '',
				is_default: address.is_default || false
			}
			this.showPopup = true
		},
		
		// 选择地区
		selectRegion() {
			uni.showActionSheet({
				itemList: ['北京市 北京市 东城区', '北京市 北京市 西城区', '上海市 上海市 黄浦区', '广东省 广州市 天河区', '浙江省 杭州市 西湖区'],
				success: (res) => {
					const selected = ['北京市 北京市 东城区', '北京市 北京市 西城区', '上海市 上海市 黄浦区', '广东省 广州市 天河区', '浙江省 杭州市 西湖区'][res.tapIndex]
					const parts = selected.split(' ')
					this.form.province = parts[0]
					this.form.city = parts[1]
					this.form.district = parts[2]
				}
			})
		},
		
		// 保存地址
		async saveAddress() {
			// 验证表单
			if (!this.form.name) {
				uni.showToast({ title: '请输入收件人', icon: 'none' })
				return
			}
			if (!this.form.phone || !/^1[3-9]\d{9}$/.test(this.form.phone)) {
				uni.showToast({ title: '请输入正确的手机号', icon: 'none' })
				return
			}
			if (!this.form.province || !this.form.city || !this.form.district) {
				uni.showToast({ title: '请选择所在地区', icon: 'none' })
				return
			}
			if (!this.form.detail) {
				uni.showToast({ title: '请输入详细地址', icon: 'none' })
				return
			}
			
			this.saving = true
			
			try {
				const data = {
					receiver_name: this.form.name,
					name: this.form.name,
					phone: this.form.phone,
					province: this.form.province,
					city: this.form.city,
					district: this.form.district,
					detail_address: this.form.detail,
					detail: this.form.detail,
					is_default: this.form.is_default
				}
				
				if (this.editingAddress) {
					// 更新
					await api.updateAddress(this.editingAddress.id, data)
					uni.showToast({ title: '地址更新成功', icon: 'success' })
				} else {
					// 添加
					await api.addAddress(data)
					uni.showToast({ title: '地址添加成功', icon: 'success' })
				}
				
				this.closePopup()
				this.loadAddresses()
				
			} catch (error) {
				console.error('保存地址失败', error)
				uni.showToast({ title: error.message || '保存失败', icon: 'none' })
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
		
		// 处理地址点击
		handleAddressClick(address) {
			if (this.mode === 'select') {
				this.selectAddress(address)
			}
		},
		
		// 选择地址（选择模式）
		selectAddress(address) {
			// 通过事件返回选中的地址
			const eventChannel = this.getOpenerEventChannel()
			if (eventChannel) {
				eventChannel.emit('selectAddress', address)
			}
			uni.navigateBack()
		},
		
		// 关闭弹窗
		closePopup() {
			this.showPopup = false
		}
	}
}
</script>

<style lang="scss" scoped>
.address-container {
	min-height: 100vh;
	background: #f5f5f5;
	padding-bottom: 120rpx;
}

/* 地址列表 */
.address-list {
	padding: 20rpx;
	
	.address-item {
		background: white;
		border-radius: 12rpx;
		padding: 30rpx;
		margin-bottom: 20rpx;
		box-shadow: 0 2rpx 10rpx rgba(0,0,0,0.05);
		
		&.selectable {
			border: 2rpx solid transparent;
			
			&:active {
				border-color: #4facfe;
				background: #f5f8ff;
			}
		}
		
		.address-content {
			.address-header {
				display: flex;
				align-items: center;
				margin-bottom: 15rpx;
				
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
					padding: 5rpx 15rpx;
					background: #ff6b6b;
					color: white;
					border-radius: 6rpx;
					font-size: 22rpx;
				}
			}
			
			.address-detail {
				font-size: 26rpx;
				color: #999;
				line-height: 1.6;
				display: block;
			}
		}
		
		.address-actions {
			display: flex;
			gap: 20rpx;
			margin-top: 20rpx;
			padding-top: 20rpx;
			border-top: 1rpx solid #f0f0f0;
			
			.action-btn {
				flex: 1;
				height: 60rpx;
				line-height: 60rpx;
				text-align: center;
				background: #f5f5f5;
				color: #666;
				border-radius: 8rpx;
				font-size: 26rpx;
				border: none;
				padding: 0;
				
				&::after {
					border: none;
				}
				
				&.delete {
					color: #ff6b6b;
				}
			}
		}
	}
}

/* 空状态 */
.empty-state {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 150rpx 0;
	
	.empty-icon {
		font-size: 100rpx;
		margin-bottom: 30rpx;
	}
	
	.empty-text {
		font-size: 28rpx;
		color: #999;
	}
}

/* 添加按钮 */
.btn-add {
	position: fixed;
	bottom: 30rpx;
	left: 30rpx;
	right: 30rpx;
	height: 90rpx;
	line-height: 90rpx;
	text-align: center;
	background: #4facfe;
	color: white;
	border-radius: 45rpx;
	font-size: 32rpx;
	box-shadow: 0 4rpx 20rpx rgba(79, 172, 254, 0.3);
}

/* 表单弹窗 */
.form-popup {
	position: fixed;
	top: 0;
	left: 0;
	right: 0;
	bottom: 0;
	background: rgba(0, 0, 0, 0.5);
	display: flex;
	align-items: flex-end;
	z-index: 999;
	
	.popup-content {
		width: 100%;
		max-height: 80vh;
		background: white;
		border-radius: 20rpx 20rpx 0 0;
		display: flex;
		flex-direction: column;
	}
	
	.popup-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 30rpx;
		border-bottom: 1rpx solid #f0f0f0;
		
		.title {
			font-size: 32rpx;
			font-weight: bold;
		}
		
		.close {
			font-size: 60rpx;
			color: #999;
			line-height: 1;
		}
	}
	
	.form-content {
		flex: 1;
		padding: 30rpx;
		overflow-y: auto;
		
		.form-item {
			margin-bottom: 30rpx;
			
			.label {
				font-size: 28rpx;
				color: #333;
				margin-bottom: 15rpx;
				display: block;
				
				.required {
					color: #ff0000;
					margin-right: 5rpx;
				}
			}
			
			.input,
			.textarea {
				width: 100%;
				padding: 20rpx;
				background: #f5f5f5;
				border-radius: 8rpx;
				font-size: 28rpx;
				box-sizing: border-box;
			}
			
			.textarea {
				height: 150rpx;
			}
			
			.region-input {
				display: flex;
				justify-content: space-between;
				align-items: center;
				padding: 20rpx;
				background: #f5f5f5;
				border-radius: 8rpx;
				font-size: 28rpx;
				
				.placeholder {
					color: #999;
				}
				
				.arrow {
					color: #999;
					font-size: 24rpx;
				}
			}
			
			&.checkbox {
				label {
					display: flex;
					align-items: center;
					font-size: 28rpx;
					color: #666;
					
					checkbox {
						margin-right: 15rpx;
					}
				}
			}
		}
	}
	
	.popup-footer {
		display: flex;
		gap: 20rpx;
		padding: 30rpx;
		border-top: 1rpx solid #f0f0f0;
		
		.btn-cancel,
		.btn-save {
			flex: 1;
			height: 80rpx;
			line-height: 80rpx;
			text-align: center;
			border-radius: 40rpx;
			font-size: 30rpx;
			border: none;
			
			&::after {
				border: none;
			}
		}
		
		.btn-cancel {
			background: #f0f0f0;
			color: #666;
		}
		
		.btn-save {
			background: #4facfe;
			color: white;
			
			&[disabled] {
				opacity: 0.5;
			}
		}
	}
}
</style>
