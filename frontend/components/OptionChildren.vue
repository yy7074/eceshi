<template>
	<view class="children-wrapper">
		<option-node
			v-for="child in children"
			:key="child.id"
			:option="child"
			:siblings="children"
			:selections="selections"
			:level="level"
			@select="$emit('select', $event)"
			@input="$emit('input', $event)"
		/>
	</view>
</template>

<script>
import OptionNode from './OptionNode.vue'

export default {
	name: 'OptionChildren',
	components: {
		OptionNode
	},
	props: {
		children: {
			type: Array,
			default: () => []
		},
		selections: {
			type: Object,
			default: () => ({})
		},
		level: {
			type: Number,
			default: 1
		}
	}
}
</script>

<style lang="scss" scoped>
.children-wrapper {
	margin-top: 8rpx;
}
</style>
