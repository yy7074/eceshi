<template>
	<view class="option-node" :class="{ 'nested': level > 0, 'inline': option.display_inline }">
		<!-- ==================== 下拉选择器 ==================== -->
		<view class="option-dropdown" v-if="option.option_type === 'dropdown'">
			<view class="option-label">
				<text class="required-mark" v-if="option.is_required">*</text>
				<text class="label-text">{{ option.name }}</text>
			</view>
			<picker
				class="dropdown-picker"
				:value="dropdownIndex"
				:range="dropdownOptions"
				range-key="name"
				@change="handleDropdownChange"
			>
				<view class="picker-value">
					<text>{{ dropdownValue || option.placeholder || '请选择' }}</text>
					<text class="picker-arrow">▼</text>
				</view>
			</picker>
		</view>

		<!-- ==================== 复选框组（横向平铺多选） ==================== -->
		<view class="option-checkbox-group" v-else-if="option.option_type === 'checkbox_group'">
			<view class="option-label">
				<text class="required-mark" v-if="option.is_required">*</text>
				<text class="label-text">{{ option.name }}</text>
			</view>
			<view class="checkbox-items">
				<view
					class="checkbox-item"
					v-for="child in option.children"
					:key="child.id"
					:class="{ 'checked': isChildSelected(child.id) }"
					@click="toggleCheckbox(child)"
				>
					<view class="checkbox-icon">
						<text v-if="isChildSelected(child.id)">✓</text>
					</view>
					<text class="checkbox-label">{{ child.name }}</text>
					<text class="checkbox-price" v-if="child.hint_text">{{ child.hint_text }}</text>
					<text class="checkbox-price" v-else-if="child.price > 0">+¥{{ formatPrice(child.price) }}</text>
				</view>
			</view>
		</view>

		<!-- ==================== 单选按钮组（横向平铺单选，常用于检测周期） ==================== -->
		<view class="option-radio-group" v-else-if="option.option_type === 'radio_group'">
			<view class="option-label">
				<text class="required-mark" v-if="option.is_required">*</text>
				<text class="label-text">{{ option.name }}</text>
			</view>
			<view class="radio-items">
				<view
					class="radio-item"
					v-for="child in option.children"
					:key="child.id"
					:class="{ 'checked': isChildSelected(child.id) }"
					@click="selectRadio(child)"
				>
					<view class="radio-icon">
						<view class="radio-inner" v-if="isChildSelected(child.id)"></view>
					</view>
					<text class="radio-label">{{ child.name }}</text>
					<text class="radio-price highlight" v-if="child.hint_text">{{ child.hint_text }}</text>
					<text class="radio-price" v-else-if="child.price > 0">+¥{{ formatPrice(child.price) }}</text>
				</view>
			</view>
		</view>

		<!-- ==================== 输入框 ==================== -->
		<view class="option-input-row" v-else-if="option.option_type === 'input'">
			<view class="option-label" v-if="!option.display_inline">
				<text class="required-mark" v-if="option.is_required">*</text>
				<text class="label-text">{{ option.name }}</text>
			</view>
			<view class="input-wrapper" :class="{ 'inline': option.display_inline }">
				<text class="inline-label" v-if="option.display_inline">
					<text class="required-mark" v-if="option.is_required">*</text>
					{{ option.name }}
				</text>
				<input
					class="text-input"
					type="text"
					:placeholder="option.placeholder || '请输入'"
					:value="inputValue"
					@input="handleInput"
					@blur="handleInputBlur"
				/>
			</view>
		</view>

		<!-- ==================== 卡片式单选/多选（原有样式） ==================== -->
		<view class="option-item" v-else :class="{ 'selected': isSelected }">
			<view
				class="option-selector"
				@click="toggleSelect"
			>
				<view
					class="selector-icon"
					:class="{
						'radio': option.option_type === 'single',
						'checkbox': option.option_type === 'multi',
						'checked': isSelected
					}"
				>
					<text v-if="isSelected">{{ option.option_type === 'single' ? '●' : '✓' }}</text>
				</view>
				<view class="option-content">
					<text class="option-name">{{ option.name }}</text>
					<text class="option-price" v-if="isSelected && option.price > 0">
						+¥{{ formatPrice(option.price) }}
						<text class="price-type" v-if="option.price_type !== 'fixed'">
							({{ priceTypeLabel }})
						</text>
					</text>
				</view>
			</view>

			<!-- 必填标记 -->
			<text class="required-mark-inline" v-if="option.is_required">*</text>
		</view>

		<!-- 红色提示文字 -->
		<view class="hint-text" v-if="option.hint_text && (isSelected || option.option_type === 'input')">
			<text>{{ option.hint_text }}</text>
		</view>

		<!-- 子选项（仅对 single/multi 类型，且在父选项选中时显示） -->
		<view class="children-wrapper" v-if="hasChildren && isSelected && isCardType">
			<option-node
				v-for="child in option.children"
				:key="child.id"
				:option="child"
				:siblings="option.children"
				:selections="selections"
				:level="level + 1"
				@select="$emit('select', $event)"
				@input="$emit('input', $event)"
			/>
		</view>
	</view>
</template>

<script>
export default {
	name: 'OptionNode',
	props: {
		// 选项数据
		option: {
			type: Object,
			required: true
		},
		// 同级选项（用于单选互斥）
		siblings: {
			type: Array,
			default: () => []
		},
		// 所有选择状态
		selections: {
			type: Object,
			default: () => ({})
		},
		// 层级深度
		level: {
			type: Number,
			default: 0
		}
	},
	computed: {
		// 是否选中
		isSelected() {
			const sel = this.selections[this.option.id]
			return sel && sel.selected
		},
		// 输入值
		inputValue() {
			const sel = this.selections[this.option.id]
			return sel ? sel.input_value : ''
		},
		// 是否有子选项
		hasChildren() {
			return this.option.children && this.option.children.length > 0
		},
		// 是否为卡片类型（single/multi）
		isCardType() {
			return ['single', 'multi'].includes(this.option.option_type)
		},
		// 价格类型标签
		priceTypeLabel() {
			const typeMap = {
				'per_sample': '每样品',
				'percentage': '比例'
			}
			return typeMap[this.option.price_type] || ''
		},
		// 下拉选项列表
		dropdownOptions() {
			return this.option.children || []
		},
		// 下拉选中索引
		dropdownIndex() {
			if (!this.option.children) return 0
			const selectedChild = this.option.children.find(c => this.isChildSelected(c.id))
			return selectedChild ? this.option.children.indexOf(selectedChild) : 0
		},
		// 下拉选中值
		dropdownValue() {
			if (!this.option.children) return ''
			const selectedChild = this.option.children.find(c => this.isChildSelected(c.id))
			return selectedChild ? selectedChild.name : ''
		}
	},
	methods: {
		// 检查子选项是否选中
		isChildSelected(childId) {
			const sel = this.selections[childId]
			return sel && sel.selected
		},

		// 切换选择状态（卡片式）
		toggleSelect() {
			const newSelected = !this.isSelected
			this.$emit('select', {
				option: this.option,
				selected: newSelected,
				siblings: this.siblings
			})
		},

		// 处理下拉选择变化
		handleDropdownChange(e) {
			const index = e.detail.value
			const selectedChild = this.option.children[index]
			if (selectedChild) {
				// 先取消其他同级选项
				this.option.children.forEach(child => {
					if (child.id !== selectedChild.id && this.isChildSelected(child.id)) {
						this.$emit('select', {
							option: child,
							selected: false,
							siblings: this.option.children
						})
					}
				})
				// 选中当前选项
				this.$emit('select', {
					option: selectedChild,
					selected: true,
					siblings: this.option.children
				})
			}
		},

		// 切换复选框
		toggleCheckbox(child) {
			const newSelected = !this.isChildSelected(child.id)
			this.$emit('select', {
				option: child,
				selected: newSelected,
				siblings: this.option.children
			})
		},

		// 选择单选按钮
		selectRadio(child) {
			// 发送选择事件，标记为单选类型，让父组件处理互斥逻辑
			this.$emit('select', {
				option: child,
				selected: true,
				siblings: this.option.children,
				isRadioGroup: true  // 标记为单选组
			})
		},

		// 处理输入
		handleInput(e) {
			const value = e.detail.value
			this.$emit('input', {
				option: this.option,
				value: value
			})
		},

		// 输入框失焦
		handleInputBlur(e) {
			const value = e.detail.value
			if (value) {
				this.$emit('input', {
					option: this.option,
					value: value
				})
			}
		},

		// 格式化价格
		formatPrice(price) {
			return parseFloat(price).toFixed(2)
		}
	}
}
</script>

<style lang="scss" scoped>
.option-node {
	&.nested {
		margin-left: 40rpx;
		padding-left: 20rpx;
		border-left: 2rpx solid #e0e0e0;
	}

	&.inline {
		display: flex;
		align-items: center;
	}
}

/* 通用标签样式 */
.option-label {
	display: flex;
	align-items: center;
	margin-bottom: 20rpx;

	.required-mark {
		color: #ff0000;
		margin-right: 8rpx;
	}

	.label-text {
		font-size: 28rpx;
		color: #333;
		font-weight: 500;
	}
}

.required-mark {
	color: #ff0000;
	font-size: 28rpx;
}

/* ==================== 下拉选择器样式 ==================== */
.option-dropdown {
	padding: 20rpx 0;
	border-bottom: 1rpx solid #f5f5f5;

	.dropdown-picker {
		width: 100%;
	}

	.picker-value {
		display: flex;
		justify-content: space-between;
		align-items: center;
		height: 80rpx;
		padding: 0 24rpx;
		background: #f5f5f5;
		border-radius: 8rpx;
		font-size: 28rpx;
		color: #333;

		.picker-arrow {
			font-size: 20rpx;
			color: #999;
		}
	}
}

/* ==================== 复选框组样式 ==================== */
.option-checkbox-group {
	padding: 20rpx 0;
	border-bottom: 1rpx solid #f5f5f5;

	.checkbox-items {
		display: flex;
		flex-wrap: wrap;
		gap: 20rpx;
	}

	.checkbox-item {
		display: flex;
		align-items: center;
		padding: 16rpx 24rpx;
		background: #f5f5f5;
		border-radius: 8rpx;
		border: 2rpx solid transparent;
		transition: all 0.2s;

		&.checked {
			background: #e8f4ff;
			border-color: #4facfe;
		}

		.checkbox-icon {
			width: 36rpx;
			height: 36rpx;
			display: flex;
			align-items: center;
			justify-content: center;
			margin-right: 12rpx;
			border: 2rpx solid #ddd;
			border-radius: 6rpx;
			font-size: 24rpx;
			color: #fff;
			background: #fff;

			&:has(text) {
				border-color: #4facfe;
				background: #4facfe;
			}
		}

		.checkbox-label {
			font-size: 26rpx;
			color: #333;
		}

		.checkbox-price {
			margin-left: 12rpx;
			font-size: 24rpx;
			color: #ff6b6b;
		}
	}
}

/* ==================== 单选按钮组样式 ==================== */
.option-radio-group {
	padding: 20rpx 0;
	border-bottom: 1rpx solid #f5f5f5;

	.radio-items {
		display: flex;
		flex-direction: column;
		gap: 16rpx;
	}

	.radio-item {
		display: flex;
		align-items: center;
		padding: 20rpx 24rpx;
		background: #f5f5f5;
		border-radius: 8rpx;
		border: 2rpx solid transparent;
		transition: all 0.2s;

		&.checked {
			background: #e8f4ff;
			border-color: #4facfe;
		}

		.radio-icon {
			width: 36rpx;
			height: 36rpx;
			display: flex;
			align-items: center;
			justify-content: center;
			margin-right: 16rpx;
			border: 2rpx solid #ddd;
			border-radius: 50%;
			background: #fff;

			.radio-inner {
				width: 20rpx;
				height: 20rpx;
				background: #4facfe;
				border-radius: 50%;
			}
		}

		.radio-label {
			flex: 1;
			font-size: 28rpx;
			color: #333;
		}

		.radio-price {
			font-size: 24rpx;
			color: #ff6b6b;

			&.highlight {
				background: linear-gradient(135deg, #ff6b6b 0%, #ff8e53 100%);
				color: #fff;
				padding: 4rpx 12rpx;
				border-radius: 20rpx;
				font-size: 22rpx;
			}
		}
	}
}

/* ==================== 输入框样式 ==================== */
.option-input-row {
	padding: 20rpx 0;
	border-bottom: 1rpx solid #f5f5f5;

	.input-wrapper {
		&.inline {
			display: flex;
			align-items: center;

			.inline-label {
				font-size: 28rpx;
				color: #333;
				margin-right: 20rpx;
				white-space: nowrap;
			}
		}
	}

	.text-input {
		flex: 1;
		height: 80rpx;
		padding: 0 24rpx;
		background: #f5f5f5;
		border-radius: 8rpx;
		font-size: 28rpx;
	}
}

/* ==================== 卡片式选项样式（原有） ==================== */
.option-item {
	display: flex;
	align-items: center;
	padding: 20rpx 0;
	border-bottom: 1rpx solid #f5f5f5;
	position: relative;

	&.selected {
		background: #f8fbff;
	}

	&:last-child {
		border-bottom: none;
	}
}

.option-selector {
	display: flex;
	align-items: center;
	flex: 1;

	.selector-icon {
		width: 40rpx;
		height: 40rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		margin-right: 20rpx;
		border: 2rpx solid #ddd;
		font-size: 24rpx;
		color: #fff;

		&.radio {
			border-radius: 50%;

			&.checked {
				border-color: #4facfe;
				background: #4facfe;
			}
		}

		&.checkbox {
			border-radius: 6rpx;

			&.checked {
				border-color: #4facfe;
				background: #4facfe;
			}
		}
	}

	.option-content {
		flex: 1;
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
}

.option-name {
	font-size: 28rpx;
	color: #333;
}

.option-price {
	font-size: 26rpx;
	color: #ff6b6b;
	margin-left: 20rpx;

	.price-type {
		font-size: 22rpx;
		color: #999;
	}
}

.required-mark-inline {
	position: absolute;
	left: -20rpx;
	top: 50%;
	transform: translateY(-50%);
	color: #ff0000;
	font-size: 28rpx;
}

.hint-text {
	padding: 15rpx 20rpx;
	margin: 10rpx 0;
	background: #fff5f5;
	border-radius: 8rpx;
	border-left: 4rpx solid #ff6b6b;

	text {
		font-size: 24rpx;
		color: #ff6b6b;
		line-height: 1.5;
	}
}

.children-wrapper {
	margin-top: 10rpx;
	padding: 10rpx 0;
}
</style>
