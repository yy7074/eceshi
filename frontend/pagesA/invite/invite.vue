<template>
	<view class="invite-page">
		<!-- 顶部统计卡片 -->
		<view class="top-card">
			<view class="card-left">
				<text class="card-label">已绑定邀请(人)</text>
				<text class="card-amount">{{ myInvites }}</text>
				<text class="card-link">仅用于订单邀请来源追踪</text>
			</view>
			<view class="card-right">
				<text class="bag-emoji">🔗</text>
			</view>
		</view>

		<!-- 邀请好友流程 -->
		<view class="flow-section">
			<view class="section-title">邀请流程</view>
			<view class="flow-list">
				<view class="flow-item" v-for="(item, index) in flowItems" :key="item.badge">
					<text class="flow-number">{{ String(index + 1).padStart(2, '0') }}.</text>
					<view class="flow-content">
						<view class="flow-bubble">
							<text class="flow-badge">{{ item.badge }}</text>
							<view class="flow-step">{{ item.title }}</view>
							<text class="flow-desc" v-if="item.desc">{{ item.desc }}</text>
							<button v-if="item.share" class="flow-btn" open-type="share">立即分享好友</button>
						</view>
					</view>
				</view>
			</view>
		</view>

			<!-- 邀请二维码 -->
			<view class="invite-panel">
			<view class="panel-header orange">
				<text>邀请链接/二维码</text>
				<text class="header-emoji">📣</text>
			</view>
			<view class="panel-body">
				<view class="qrcode-section">
					<image
						v-if="latestQrcode"
						:src="getQrcodeImage(latestQrcode)"
						class="promo-qrcode"
						mode="aspectFit"
						@click="previewPromotionQrcode"
					/>
					<view v-else class="promo-qrcode empty">
						<text>暂无二维码</text>
					</view>
					<text class="qrcode-desc">好友通过链接或二维码进入并登录后，会记录邀请来源。</text>
					<view v-if="inviteCode" class="invite-code-box">
						<text class="invite-code-label">邀请码</text>
						<text class="invite-code-value">{{ inviteCode }}</text>
					</view>
					<view class="qrcode-actions">
						<button class="flow-btn orange" @click="createPromotionQrcode" :disabled="qrcodeLoading">
							{{ qrcodeLoading ? '生成中...' : latestQrcode ? '重新生成' : '生成二维码' }}
						</button>
						<button class="flow-btn" v-if="latestQrcode" @click="previewPromotionQrcode">查看大图</button>
						<button class="flow-btn" v-if="inviteLink" @click="copyInviteLink">复制链接</button>
					</view>
				</view>
			</view>
		</view>
		
		<!-- 底部分享按钮 -->
		<view class="footer-btn">
			<button class="share-btn" open-type="share">立即分享好友</button>
		</view>
	</view>
</template>

<script>
import api from '@/utils/api.js'

export default {
	data() {
		return {
			myInvites: 0,
			latestQrcode: null,
			qrcodeLoading: false,
			flowItems: [
				{ badge: '生成', title: '生成邀请链接或二维码', desc: '分享给好友后用于记录来源。', share: true },
				{ badge: '绑定', title: '好友打开链接并登录', desc: '系统自动绑定邀请人与被邀请人关系。' },
				{ badge: '溯源', title: '后台按邀请人筛选订单', desc: '订单管理可按邀请人姓名、手机号或ID查询来源订单。' }
			]
		}
	},

	computed: {
		inviteCode() {
			return this.latestQrcode?.invite_code || ''
		},

		inviteLink() {
			if (this.inviteCode) {
				return `/pages/index/index?inviter=${this.inviteCode}`
			}
			const userInfo = this.getStoredUserInfo()
			return userInfo.id ? `/pages/index/index?inviteUserId=${userInfo.id}` : ''
		}
	},
	
	onLoad() {
		this.loadInviteData()
		this.loadInviteQrcodes()
	},
	
	// 分享配置
	onShareAppMessage() {
		return {
			title: '博才科研百测检测服务邀请',
			path: this.inviteLink || '/pages/index/index'
		}
	},
	onShareTimeline() {
		const code = this.inviteCode ? `inviter=${this.inviteCode}` : ''
		return {
			title: '博才科研百测检测服务邀请',
			query: code
		}
	},
	
	methods: {
		getStoredUserInfo() {
			const stored = uni.getStorageSync('userInfo')
			if (!stored) {
				return {}
			}
			if (typeof stored === 'string') {
				try {
					return JSON.parse(stored)
				} catch (error) {
					return {}
				}
			}
			return stored
		},

		// 加载邀请数据
		async loadInviteData() {
			try {
				const res = await api.getInviteStats()
				this.myInvites = res.data.total_invites || res.data.my_invites || 0
			} catch (error) {
				console.error('加载邀请数据失败', error)
				this.myInvites = 0
			}
		},

		async loadInviteQrcodes() {
			try {
				const res = await api.getInviteQrcodes({ page: 1, page_size: 10 })
				this.latestQrcode = (res.data?.items || [])[0] || null
			} catch (error) {
				console.error('加载推广二维码失败', error)
				this.latestQrcode = null
			}
		},

		async createPromotionQrcode() {
			try {
				this.qrcodeLoading = true
				const res = await api.createInviteQrcode({
					name: `邀请二维码-${Date.now()}`,
					scene: 'trace'
				})
				this.latestQrcode = res.data || null
				uni.showToast({
					title: '二维码已生成',
					icon: 'success'
				})
			} catch (error) {
				uni.showToast({
					title: error.message || error.detail || '生成失败',
					icon: 'none'
				})
			} finally {
				this.qrcodeLoading = false
			}
		},

		getQrcodeImage(item) {
			if (!item?.qrcode_url) {
				return ''
			}
			if (/^https?:\/\//.test(item.qrcode_url)) {
				return item.qrcode_url
			}
			return `${api.baseUrl}${item.qrcode_url}`
		},

		previewPromotionQrcode() {
			if (!this.latestQrcode) {
				return
			}
			const url = this.getQrcodeImage(this.latestQrcode)
			uni.previewImage({
				urls: [url],
					current: url
				})
			},

			copyInviteLink() {
				uni.setClipboardData({
					data: this.inviteLink,
					success: () => {
						uni.showToast({
							title: '邀请链接已复制',
							icon: 'success'
						})
					}
				})
			}
		}
}
</script>

<style lang="scss" scoped>
.invite-page {
	min-height: 100vh;
	background: linear-gradient(180deg, #eef5ff 0%, #f5f5f5 20%);
	padding-bottom: 140rpx;
}

/* 顶部统计卡片 */
.top-card {
	background: white;
	margin: 20rpx 30rpx;
	border-radius: 16rpx;
	padding: 30rpx;
	display: flex;
	align-items: center;
	position: relative;
	box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.05);
}

.qrcode-section {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 20rpx;
}

.promo-qrcode {
	width: 320rpx;
	height: 320rpx;
	background: #fff7e8;
	border-radius: 20rpx;
	padding: 20rpx;
}

.promo-qrcode.empty {
	display: flex;
	align-items: center;
	justify-content: center;
	color: #999;
}

.qrcode-desc {
	font-size: 24rpx;
	color: #666;
	text-align: center;
}

	.qrcode-actions {
		display: flex;
		gap: 16rpx;
		flex-wrap: wrap;
		justify-content: center;
	}

	.invite-code-box {
		display: flex;
		align-items: center;
		gap: 12rpx;
		padding: 12rpx 20rpx;
		background: #f6f8fb;
		border-radius: 12rpx;
	}

	.invite-code-label {
		font-size: 24rpx;
		color: #666;
	}

	.invite-code-value {
		font-size: 28rpx;
		color: #333;
		font-weight: 700;
		letter-spacing: 0;
	}

.card-left {
	flex: 1;
}

.card-label {
	font-size: 26rpx;
	color: #666;
	display: block;
	margin-bottom: 10rpx;
}

.card-amount {
	font-size: 72rpx;
	font-weight: 700;
	color: #333;
	display: block;
	line-height: 1.2;
	margin-bottom: 12rpx;
}

.card-link {
	font-size: 24rpx;
	color: #4dabf7;
}

.card-right {
	width: 140rpx;
	display: flex;
	justify-content: center;
	align-items: center;
}

.bag-emoji {
	font-size: 110rpx;
}

.rule-badge {
	position: absolute;
	top: 20rpx;
	right: 20rpx;
	background: #eef2ff;
	color: #667eea;
	padding: 8rpx 20rpx;
	border-radius: 20rpx;
	font-size: 24rpx;
}

	.invite-panel {
		background: white;
		margin: 0 30rpx 20rpx;
		border-radius: 16rpx;
		overflow: hidden;
	}

.panel-header {
	padding: 20rpx 24rpx;
	font-size: 28rpx;
	font-weight: 700;
	color: white;
	display: flex;
	justify-content: space-between;
	align-items: center;
}

.panel-header.orange {
	background: linear-gradient(135deg, #ffb86c 0%, #ff7e5f 100%);
}

.panel-header.blue {
	background: linear-gradient(135deg, #6ec1ff 0%, #4dabf7 100%);
}

.header-emoji {
	font-size: 32rpx;
}

.panel-body {
	padding: 24rpx;
}

/* 邀请流程 */
.flow-section {
	background: white;
	margin: 0 30rpx 20rpx;
	border-radius: 16rpx;
	padding: 24rpx;
}

.section-title {
	font-size: 28rpx;
	font-weight: 700;
	color: #333;
	margin-bottom: 20rpx;
}

.flow-list {
}

.flow-item {
	display: flex;
	padding: 20rpx 0;
	border-bottom: 1rpx dashed #e5e5e5;
}

.flow-item:last-child {
	border-bottom: none;
}

.flow-number {
	color: #4dabf7;
	font-size: 28rpx;
	font-weight: 700;
	width: 70rpx;
	flex-shrink: 0;
}

.flow-content {
	flex: 1;
}

.flow-bubble {
	position: relative;
	background: #f8fbff;
	border-radius: 18rpx;
	padding: 20rpx 22rpx 18rpx;
}

.flow-badge {
	position: absolute;
	right: 18rpx;
	top: 14rpx;
	padding: 4rpx 14rpx;
	border-radius: 999rpx;
	background: #fff0e6;
	color: #ff7e5f;
	font-size: 22rpx;
	font-weight: 700;
}

.flow-step {
	background: linear-gradient(135deg, #6ec1ff 0%, #4dabf7 100%);
	color: white;
	padding: 12rpx 24rpx;
	border-radius: 40rpx;
	font-size: 24rpx;
	display: inline-block;
	margin-bottom: 8rpx;
	margin-right: 92rpx;
}

.flow-btn {
	background: linear-gradient(135deg, #ffb86c 0%, #ff7e5f 100%);
	color: white;
	border: none;
	padding: 12rpx 28rpx;
	border-radius: 40rpx;
	font-size: 24rpx;
	display: inline-block;
	margin-bottom: 8rpx;
}

.flow-btn.orange {
	background: linear-gradient(135deg, #ffb86c 0%, #ff7e5f 100%);
}

.flow-desc {
	font-size: 24rpx;
	color: #666;
	line-height: 1.6;
	display: block;
	margin-top: 8rpx;
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

.share-btn {
	width: 100%;
	background: linear-gradient(135deg, #ffb86c 0%, #ff7e5f 100%);
	color: white;
	border: none;
	border-radius: 50rpx;
	padding: 30rpx;
	font-size: 32rpx;
	font-weight: 700;
}
</style>
