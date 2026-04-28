<template>
	<view class="option-node" :class="{ nested: level > 0 }">
		<view class="option-item" :class="{ selected: isSelected }">
			<view class="option-selector" @click="toggleSelect">
				<view class="selector-icon" :class="{ checked: isSelected }">
					<text v-if="isSelected">✓</text>
				</view>
				<view class="option-content">
					<view class="option-main">
						<text class="required-mark-inline" v-if="option.is_required">*</text>
						<text class="option-name">{{ option.name }}</text>
					</view>
					<text class="option-price" v-if="isSelected && option.price > 0">
						+¥{{ formatPrice(option.price) }}
						<text class="price-type" v-if="option.price_type !== 'fixed'">
							({{ priceTypeLabel }})
						</text>
					</text>
				</view>
			</view>
		</view>

		<view class="hint-text" v-if="option.hint_text && isSelected">
			<text class="hint-content">{{ option.hint_text }}</text>
		</view>

		<view class="input-panel" v-if="requiresInput && isSelected" @click.stop>
			<view class="single-input" v-if="inputMode === 'single'">
				<input
					class="text-input"
					type="text"
					:placeholder="option.placeholder || '请输入'"
					:value="inputValue"
					@input="handleSingleInput"
				/>
			</view>

			<view class="multiple-inputs" v-else>
				<view class="input-line" v-for="(value, index) in displayInputValues" :key="index">
					<input
						class="text-input"
						type="text"
						:placeholder="getInputPlaceholder(index)"
						:value="value"
						@input="handleMultipleInput(index, $event)"
					/>
					<view class="delete-input" v-if="displayInputValues.length > 1" @click.stop="removeInput(index)">删除</view>
				</view>
				<view class="add-input" @click.stop="addInput">+ 添加输入项</view>
			</view>
		</view>

		<view class="children-wrapper" v-if="canShowChildren">
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
		option: {
			type: Object,
			required: true
		},
		siblings: {
			type: Array,
			default: () => []
		},
		selections: {
			type: Object,
			default: () => ({})
		},
		level: {
			type: Number,
			default: 0
		}
	},
	computed: {
		isSelected() {
			const sel = this.selections[this.option.id]
			return !!(sel && sel.selected)
		},
		selection() {
			return this.selections[this.option.id] || {}
		},
		requiresInput() {
			return !!(this.option.requires_input || this.option.option_type === 'input')
		},
		inputMode() {
			const mode = this.option.input_mode || this.selection.input_mode || 'single'
			return ['multiple', 'multi'].includes(mode) ? 'multiple' : 'single'
		},
		inputValue() {
			if (this.selection.input_value) {
				return this.selection.input_value
			}
			const values = this.normalizedInputValues
			return values.length > 0 ? values[0] : ''
		},
		normalizedInputValues() {
			if (Array.isArray(this.selection.input_values)) {
				return this.selection.input_values
			}
			if (this.selection.input_value) {
				const raw = `${this.selection.input_value}`.trim()
				if (raw.startsWith('[')) {
					try {
						const parsed = JSON.parse(raw)
						if (Array.isArray(parsed)) {
							return parsed
						}
					} catch (e) {
						return [raw]
					}
				}
				return [raw]
			}
			return []
		},
		displayInputValues() {
			const values = this.normalizedInputValues
			return values.length > 0 ? values : ['']
		},
		hasChildren() {
			return this.option.children && this.option.children.length > 0
		},
		canShowChildren() {
			return this.hasChildren && this.isSelected && this.option.allow_children !== false
		},
		priceTypeLabel() {
			const typeMap = {
				per_sample: '每样品',
				percentage: '比例'
			}
			return typeMap[this.option.price_type] || ''
		}
	},
	methods: {
		toggleSelect() {
			this.$emit('select', {
				option: this.option,
				selected: !this.isSelected,
				siblings: this.siblings
			})
		},
		handleSingleInput(e) {
			const value = e.detail.value
			this.$emit('input', {
				option: this.option,
				value: {
					input_value: value,
					input_values: value ? [value] : [],
					input_mode: 'single'
				}
			})
		},
		handleMultipleInput(index, e) {
			const values = this.displayInputValues.slice()
			values.splice(index, 1, e.detail.value)
			this.emitMultipleInput(values)
		},
		addInput() {
			const values = this.displayInputValues.slice()
			values.push('')
			this.emitMultipleInput(values)
		},
		removeInput(index) {
			const values = this.displayInputValues.slice()
			values.splice(index, 1)
			this.emitMultipleInput(values.length ? values : [''])
		},
		emitMultipleInput(values) {
			this.$emit('input', {
				option: this.option,
				value: {
					input_value: '',
					input_values: values,
					input_mode: 'multiple'
				}
			})
		},
		getInputPlaceholder(index) {
			return this.option.placeholder || `请输入第${index + 1}项`
		},
		formatPrice(price) {
			return parseFloat(price || 0).toFixed(2)
		}
	}
}
</script>

<style lang="scss" scoped>
.option-node {
	&.nested {
		margin-left: 32rpx;
		padding-left: 18rpx;
		border-left: 2rpx solid #e7edf5;
	}
}

.option-item {
	display: flex;
	align-items: center;
	padding: 20rpx 0;
	border-bottom: 1rpx solid #f2f4f7;

	&.selected {
		background: #f8fbff;
	}
}

.option-selector {
	display: flex;
	align-items: center;
	flex: 1;
	min-width: 0;
}

.selector-icon {
	width: 40rpx;
	height: 40rpx;
	display: flex;
	align-items: center;
	justify-content: center;
	flex-shrink: 0;
	margin-right: 18rpx;
	border: 2rpx solid #cfd7e3;
	border-radius: 6rpx;
	background: #fff;
	color: #fff;
	font-size: 24rpx;

	&.checked {
		border-color: #4facfe;
		background: #4facfe;
	}
}

.option-content {
	flex: 1;
	min-width: 0;
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 16rpx;
}

.option-main {
	display: flex;
	align-items: center;
	min-width: 0;
}

.required-mark-inline {
	color: #ff4d4f;
	font-size: 28rpx;
	margin-right: 6rpx;
}

.option-name {
	font-size: 28rpx;
	color: #333;
	line-height: 1.4;
	word-break: break-all;
}

.option-price {
	flex-shrink: 0;
	font-size: 26rpx;
	color: #ff6b6b;

	.price-type {
		font-size: 22rpx;
		color: #999;
	}
}

.hint-text {
	padding: 14rpx 18rpx;
	margin: 10rpx 0;
	background: #fff5f5;
	border-radius: 8rpx;
	border-left: 4rpx solid #ff6b6b;

	.hint-content {
		font-size: 24rpx;
		color: #ff6b6b;
		line-height: 1.5;
	}
}

.input-panel {
	margin: 12rpx 0 18rpx 58rpx;
	padding: 18rpx;
	background: #f8fafc;
	border: 1rpx solid #e4eaf2;
	border-radius: 8rpx;
}

.input-line {
	display: flex;
	align-items: center;
	gap: 14rpx;
	margin-bottom: 14rpx;

	&:last-child {
		margin-bottom: 0;
	}
}

.text-input {
	flex: 1;
	min-width: 0;
	height: 76rpx;
	padding: 0 22rpx;
	background: #fff;
	border: 1rpx solid #dbe3ee;
	border-radius: 8rpx;
	font-size: 28rpx;
	color: #333;
}

.delete-input {
	width: 84rpx;
	height: 64rpx;
	display: flex;
	align-items: center;
	justify-content: center;
	flex-shrink: 0;
	border: 1rpx solid #ffb3b3;
	border-radius: 8rpx;
	color: #e54d42;
	font-size: 24rpx;
	background: #fff;
}

.add-input {
	height: 68rpx;
	display: flex;
	align-items: center;
	justify-content: center;
	margin-top: 16rpx;
	border: 1rpx dashed #4facfe;
	border-radius: 8rpx;
	color: #2587dc;
	font-size: 26rpx;
	background: #fff;
}

.children-wrapper {
	margin-top: 8rpx;
}
</style>
