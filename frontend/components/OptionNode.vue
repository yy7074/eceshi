<template>
	<view class="option-node" :class="{ 'nested': level > 0 }">
		<!-- 选项主体 -->
		<view class="option-item" :class="{ 'selected': isSelected }">
			<!-- 单选/多选按钮 -->
			<view
				class="option-selector"
				v-if="option.option_type !== 'input'"
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
					<!-- 价格显示（选中后才显示） -->
					<text class="option-price" v-if="isSelected && option.price > 0">
						+¥{{ formatPrice(option.price) }}
						<text class="price-type" v-if="option.price_type !== 'fixed'">
							({{ priceTypeLabel }})
						</text>
					</text>
				</view>
			</view>

			<!-- 输入类型 -->
			<view class="option-input-wrapper" v-else>
				<text class="option-name">{{ option.name }}</text>
				<input
					class="option-input"
					type="text"
					:placeholder="option.placeholder || '请输入'"
					:value="inputValue"
					@input="handleInput"
					@blur="handleInputBlur"
				/>
				<!-- 价格显示（有输入值时才显示） -->
				<text class="option-price" v-if="inputValue && option.price > 0">
					+¥{{ formatPrice(option.price) }}
				</text>
			</view>

			<!-- 必填标记 -->
			<text class="required-mark" v-if="option.is_required">*</text>
		</view>

		<!-- 红色提示文字 -->
		<view class="hint-text" v-if="option.hint_text && isSelected">
			<text>{{ option.hint_text }}</text>
		</view>

		<!-- 子选项（仅在父选项选中时显示） -->
		<view class="children-wrapper" v-if="hasChildren && isSelected">
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
		// 价格类型标签
		priceTypeLabel() {
			const typeMap = {
				'per_sample': '每样品',
				'percentage': '比例'
			}
			return typeMap[this.option.price_type] || ''
		}
	},
	methods: {
		// 切换选择状态
		toggleSelect() {
			const newSelected = !this.isSelected
			this.$emit('select', {
				option: this.option,
				selected: newSelected,
				siblings: this.siblings
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
}

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

.option-input-wrapper {
	flex: 1;
	display: flex;
	align-items: center;
	gap: 20rpx;

	.option-name {
		flex-shrink: 0;
	}

	.option-input {
		flex: 1;
		height: 60rpx;
		padding: 0 20rpx;
		background: #f5f5f5;
		border-radius: 8rpx;
		font-size: 28rpx;
	}
}

.required-mark {
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
