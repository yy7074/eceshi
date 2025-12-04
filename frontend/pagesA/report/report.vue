<template>
	<view class="report-page">
		<!-- 搜索栏 -->
		<view class="search-bar">
			<view class="search-input">
				<text class="search-icon">🔍</text>
				<input type="text" v-model="searchKeyword" placeholder="搜索订单号或项目名称" />
			</view>
		</view>
		
		<!-- 筛选标签 -->
		<view class="filter-tabs">
			<view class="tab-item" :class="{ active: filterStatus === 'all' }" @click="filterStatus = 'all'">
				全部
			</view>
			<view class="tab-item" :class="{ active: filterStatus === 'ready' }" @click="filterStatus = 'ready'">
				可下载
			</view>
			<view class="tab-item" :class="{ active: filterStatus === 'pending' }" @click="filterStatus = 'pending'">
				待生成
			</view>
		</view>
		
		<!-- 报告列表 -->
		<view class="report-list" v-if="filteredReports.length > 0">
			<view class="report-card" v-for="report in filteredReports" :key="report.id">
				<view class="report-header">
					<view class="report-icon">📄</view>
					<view class="report-status" :class="report.status">
						{{ report.status === 'ready' ? '可下载' : '生成中' }}
					</view>
				</view>
				
				<view class="report-info">
					<text class="project-name">{{ report.projectName }}</text>
					<view class="info-row">
						<text class="label">订单号：</text>
						<text class="value">{{ report.orderNo }}</text>
					</view>
					<view class="info-row">
						<text class="label">完成时间：</text>
						<text class="value">{{ report.completedAt }}</text>
					</view>
				</view>
				
				<view class="report-actions">
					<view class="action-btn primary" v-if="report.status === 'ready'" @click="downloadReport(report)">
						<text class="btn-icon">⬇️</text>
						<text>下载报告</text>
					</view>
					<view class="action-btn" v-else disabled>
						<text class="btn-icon">⏳</text>
						<text>报告生成中</text>
					</view>
					<view class="action-btn" @click="goSampleTrack(report)">
						<text class="btn-icon">📦</text>
						<text>样品追踪</text>
					</view>
					<view class="action-btn" @click="previewReport(report)" v-if="report.status === 'ready'">
						<text class="btn-icon">👁️</text>
						<text>预览</text>
					</view>
				</view>
			</view>
		</view>
		
		<!-- 空状态 -->
		<view class="empty-state" v-else>
			<text class="empty-icon">📊</text>
			<text class="empty-text">暂无检测报告</text>
			<text class="empty-hint">完成检测后，报告将在此显示</text>
		</view>
	</view>
</template>

<script>
import api from '@/utils/api.js'

export default {
	data() {
		return {
			searchKeyword: '',
			filterStatus: 'all',
			reports: [
				{
					id: 1,
					orderNo: 'ORD2025120100001',
					projectName: 'X射线衍射分析(XRD)',
					completedAt: '2025-12-01',
					status: 'ready',
					reportUrl: ''
				},
				{
					id: 2,
					orderNo: 'ORD2025112800002',
					projectName: '扫描电子显微镜(SEM)',
					completedAt: '2025-11-30',
					status: 'ready',
					reportUrl: ''
				},
				{
					id: 3,
					orderNo: 'ORD2025112500003',
					projectName: '傅里叶变换红外光谱(FT-IR)',
					completedAt: '',
					status: 'pending',
					reportUrl: ''
				}
			],
			loading: false
		}
	},
	computed: {
		filteredReports() {
			let list = this.reports
			
			// 按状态筛选
			if (this.filterStatus !== 'all') {
				list = list.filter(r => r.status === this.filterStatus)
			}
			
			// 按关键词搜索
			if (this.searchKeyword.trim()) {
				const keyword = this.searchKeyword.toLowerCase()
				list = list.filter(r => 
					r.orderNo.toLowerCase().includes(keyword) ||
					r.projectName.toLowerCase().includes(keyword)
				)
			}
			
			return list
		}
	},
	onLoad() {
		this.loadReports()
	},
	methods: {
		async loadReports() {
			this.loading = true
			try {
				// 调用API获取报告列表
				const res = await api.getOrders({ status: 'completed', page: 1, page_size: 50 })
				const orders = res.data?.items || []
				
				this.reports = orders.map(order => ({
					id: order.id,
					orderNo: order.order_no,
					projectName: order.project_name,
					completedAt: order.completed_at?.slice(0, 10) || '',
					status: order.report_generated ? 'ready' : 'pending',
					reportUrl: order.report_url || ''
				}))
			} catch (e) {
				console.error('加载报告失败', e)
				// 保留演示数据
			} finally {
				this.loading = false
			}
		},
		
		downloadReport(report) {
			if (report.reportUrl) {
				// 有报告URL时下载
				uni.downloadFile({
					url: report.reportUrl,
					success: (res) => {
						if (res.statusCode === 200) {
							uni.openDocument({
								filePath: res.tempFilePath,
								showMenu: true
							})
						}
					},
					fail: () => {
						uni.showToast({ title: '下载失败', icon: 'none' })
					}
				})
			} else {
				uni.showModal({
					title: '报告下载',
					content: '报告正在准备中，请稍后再试或联系客服获取。',
					showCancel: false
				})
			}
		},
		
		previewReport(report) {
			uni.showModal({
				title: '报告预览',
				content: `项目：${report.projectName}\n订单号：${report.orderNo}\n完成时间：${report.completedAt}\n\n报告预览功能开发中...`,
				showCancel: false
			})
		},
		
		goSampleTrack(report) {
			uni.navigateTo({
				url: `/pagesA/sample-track/sample-track?orderId=${report.id}&orderNo=${report.orderNo}`
			})
		}
	}
}
</script>

<style lang="scss" scoped>
.report-page {
	min-height: 100vh;
	background: #f5f5f5;
}

.search-bar {
	background: #fff;
	padding: 20rpx 24rpx;
	
	.search-input {
		display: flex;
		align-items: center;
		background: #f5f5f5;
		border-radius: 8rpx;
		padding: 16rpx 24rpx;
		
		.search-icon {
			font-size: 28rpx;
			margin-right: 12rpx;
		}
		
		input {
			flex: 1;
			font-size: 28rpx;
		}
	}
}

.filter-tabs {
	display: flex;
	background: #fff;
	padding: 0 24rpx;
	border-bottom: 1rpx solid #f0f0f0;
	
	.tab-item {
		padding: 24rpx 32rpx;
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

.report-list {
	padding: 16rpx 24rpx;
}

.report-card {
	background: #fff;
	border-radius: 12rpx;
	padding: 24rpx;
	margin-bottom: 16rpx;
	
	.report-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 16rpx;
		
		.report-icon {
			font-size: 48rpx;
		}
		
		.report-status {
			padding: 8rpx 16rpx;
			border-radius: 8rpx;
			font-size: 24rpx;
			
			&.ready {
				background: #f6ffed;
				color: #52c41a;
			}
			
			&.pending {
				background: #fff7e6;
				color: #fa8c16;
			}
		}
	}
	
	.report-info {
		margin-bottom: 20rpx;
		
		.project-name {
			display: block;
			font-size: 32rpx;
			font-weight: 600;
			color: #333;
			margin-bottom: 12rpx;
		}
		
		.info-row {
			display: flex;
			margin-bottom: 8rpx;
			
			.label {
				font-size: 26rpx;
				color: #999;
				width: 140rpx;
			}
			
			.value {
				font-size: 26rpx;
				color: #666;
			}
		}
	}
	
	.report-actions {
		display: flex;
		gap: 16rpx;
		border-top: 1rpx solid #f0f0f0;
		padding-top: 20rpx;
		
		.action-btn {
			flex: 1;
			display: flex;
			align-items: center;
			justify-content: center;
			gap: 8rpx;
			padding: 16rpx;
			background: #f5f5f5;
			border-radius: 8rpx;
			font-size: 26rpx;
			color: #666;
			
			&.primary {
				background: #1890ff;
				color: #fff;
			}
			
			&[disabled] {
				opacity: 0.6;
			}
			
			.btn-icon {
				font-size: 28rpx;
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

