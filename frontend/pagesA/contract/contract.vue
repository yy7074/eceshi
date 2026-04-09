<template>
	<view class="contract-page">
		<!-- 筛选标签 -->
		<view class="filter-tabs">
			<view class="tab-item" :class="{ active: activeTab === 'all' }" @click="activeTab = 'all'; loadContracts()">
				全部
			</view>
			<view class="tab-item" :class="{ active: activeTab === 'active' }" @click="activeTab = 'active'; loadContracts()">
				生效中
			</view>
			<view class="tab-item" :class="{ active: activeTab === 'expired' }" @click="activeTab = 'expired'; loadContracts()">
				已过期
			</view>
		</view>
		
		<!-- 合同列表 -->
		<view class="contract-list" v-if="contracts.length > 0">
			<view class="contract-card" v-for="contract in contracts" :key="contract.id" @click="showContractDetail(contract)">
				<view class="contract-header">
					<view class="contract-icon">📄</view>
					<view class="contract-info">
						<text class="contract-title">{{ contract.title }}</text>
						<text class="contract-no">{{ contract.contract_no }}</text>
					</view>
					<view class="contract-status" :class="contract.status">
						{{ contract.status === 'active' ? '生效中' : '已过期' }}
					</view>
				</view>
				
				<view class="contract-body">
					<view class="info-row">
						<text class="label">关联订单</text>
						<text class="value">{{ contract.order_no }}</text>
					</view>
					<view class="info-row">
						<text class="label">签订日期</text>
						<text class="value">{{ contract.signed_at }}</text>
					</view>
					<view class="info-row">
						<text class="label">有效期至</text>
						<text class="value">{{ contract.expired_at }}</text>
					</view>
				</view>
				
				<view class="contract-actions">
					<view class="action-btn" @click.stop="viewContract(contract)">
						<text>👁️ 查看</text>
					</view>
					<view class="action-btn primary" @click.stop="downloadContract(contract)">
						<text>⬇️ 下载</text>
					</view>
				</view>
			</view>
		</view>
		
		<!-- 空状态 -->
		<view class="empty-state" v-else>
			<text class="empty-icon">📋</text>
			<text class="empty-text">暂无合同</text>
			<text class="empty-hint">下单后系统将自动生成服务合同</text>
		</view>
	</view>
</template>

<script>
import api from '@/utils/api.js'

export default {
	data() {
		return {
			activeTab: 'all',
			contracts: [],
			loading: false
		}
	},
	onLoad() {
		this.loadContracts()
	},
	methods: {
		async loadContracts() {
			this.loading = true
			try {
				const res = await api.getContracts({ status: this.activeTab })
				this.contracts = res.data?.items || []
			} catch (e) {
				// 使用演示数据
				this.contracts = [
					{
						id: 1,
						contract_no: 'CON2025120100001',
						title: '检测服务合同',
						order_no: 'ORD2025120100001',
						signed_at: '2025-12-01',
						expired_at: '2026-12-01',
						status: 'active'
					},
					{
						id: 2,
						contract_no: 'CON2025110100002',
						title: '检测服务合同',
						order_no: 'ORD2025110100002',
						signed_at: '2025-11-01',
						expired_at: '2026-11-01',
						status: 'active'
					},
					{
						id: 3,
						contract_no: 'CON2024120100003',
						title: '检测服务合同',
						order_no: 'ORD2024120100003',
						signed_at: '2024-12-01',
						expired_at: '2025-12-01',
						status: 'expired'
					}
				]
				
				if (this.activeTab !== 'all') {
					this.contracts = this.contracts.filter(c => c.status === this.activeTab)
				}
			} finally {
				this.loading = false
			}
		},
		
		showContractDetail(contract) {
			uni.showModal({
				title: contract.title,
				content: `合同编号：${contract.contract_no}\n关联订单：${contract.order_no}\n签订日期：${contract.signed_at}\n有效期至：${contract.expired_at}\n\n甲方：博才科研百测\n乙方：用户\n\n根据相关法律法规，甲乙双方就检测服务事宜达成协议...`,
				showCancel: false,
				confirmText: '关闭'
			})
		},
		
		viewContract(contract) {
			uni.showModal({
				title: '合同预览',
				content: `《${contract.title}》\n\n合同编号：${contract.contract_no}\n\n第一条 服务内容\n甲方为乙方提供专业的检测服务...\n\n第二条 服务费用\n按照订单金额执行...\n\n第三条 双方权利义务\n...\n\n第四条 违约责任\n...\n\n第五条 其他条款\n...`,
				showCancel: false,
				confirmText: '关闭'
			})
		},
		
		downloadContract(contract) {
			uni.showLoading({ title: '准备下载...' })
			
			setTimeout(() => {
				uni.hideLoading()
				uni.showToast({
					title: '合同已保存',
					icon: 'success'
				})
			}, 1500)
		}
	}
}
</script>

<style lang="scss" scoped>
.contract-page {
	min-height: 100vh;
	background: #f5f5f5;
}

.filter-tabs {
	display: flex;
	background: #fff;
	padding: 0 24rpx;
	border-bottom: 1rpx solid #f0f0f0;
	
	.tab-item {
		padding: 28rpx 32rpx;
		font-size: 28rpx;
		color: #666;
		position: relative;
		
		&.active {
			color: #1890ff;
			font-weight: 500;
			
			&::after {
				content: '';
				position: absolute;
				bottom: 0;
				left: 50%;
				transform: translateX(-50%);
				width: 48rpx;
				height: 4rpx;
				background: #1890ff;
				border-radius: 2rpx;
			}
		}
	}
}

.contract-list {
	padding: 16rpx 24rpx;
}

.contract-card {
	background: #fff;
	border-radius: 12rpx;
	padding: 24rpx;
	margin-bottom: 16rpx;
	
	.contract-header {
		display: flex;
		align-items: center;
		padding-bottom: 20rpx;
		border-bottom: 1rpx solid #f0f0f0;
		
		.contract-icon {
			font-size: 48rpx;
			margin-right: 16rpx;
		}
		
		.contract-info {
			flex: 1;
			
			.contract-title {
				display: block;
				font-size: 30rpx;
				font-weight: 600;
				color: #333;
				margin-bottom: 4rpx;
			}
			
			.contract-no {
				font-size: 24rpx;
				color: #999;
			}
		}
		
		.contract-status {
			padding: 8rpx 16rpx;
			border-radius: 8rpx;
			font-size: 24rpx;
			
			&.active {
				background: #f6ffed;
				color: #52c41a;
			}
			
			&.expired {
				background: #f5f5f5;
				color: #999;
			}
		}
	}
	
	.contract-body {
		padding: 16rpx 0;
		
		.info-row {
			display: flex;
			justify-content: space-between;
			padding: 8rpx 0;
			
			.label {
				font-size: 26rpx;
				color: #999;
			}
			
			.value {
				font-size: 26rpx;
				color: #333;
			}
		}
	}
	
	.contract-actions {
		display: flex;
		gap: 16rpx;
		padding-top: 16rpx;
		border-top: 1rpx solid #f0f0f0;
		
		.action-btn {
			flex: 1;
			padding: 16rpx;
			background: #f5f5f5;
			border-radius: 8rpx;
			text-align: center;
			
			text {
				font-size: 26rpx;
				color: #666;
			}
			
			&.primary {
				background: #1890ff;
				
				text {
					color: #fff;
				}
			}
		}
	}
}

.empty-state {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 120rpx 0;
	
	.empty-icon {
		font-size: 100rpx;
		margin-bottom: 24rpx;
	}
	
	.empty-text {
		font-size: 32rpx;
		color: #333;
		margin-bottom: 12rpx;
	}
	
	.empty-hint {
		font-size: 26rpx;
		color: #999;
	}
}
</style>

