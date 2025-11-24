<template>
	<view class="invite-page">
		<!-- 顶部统计卡片 -->
		<view class="top-card">
			<view class="card-left">
				<text class="card-label">可提现奖励(元)</text>
				<text class="card-amount">{{ withdrawable.toFixed(2) }}</text>
				<text class="card-link" @click="handleWithdraw">立即提现 ›</text>
			</view>
			<view class="card-right">
				<text class="bag-emoji">💰</text>
			</view>
			<view class="rule-badge" @click="showRulesModal">规则</view>
		</view>
		
		<!-- 四项指标 -->
		<view class="stats-grid">
			<view class="stat-item">
				<text class="stat-value">{{ myInvites }}</text>
				<text class="stat-label">我的邀请(人)</text>
			</view>
			<view class="stat-item">
				<text class="stat-value">{{ predictedOrders }}</text>
				<text class="stat-label">预测收益(单)</text>
			</view>
			<view class="stat-item">
				<text class="stat-value">{{ predictedRewards.toFixed(2) }}</text>
				<text class="stat-label">预测奖励(元)</text>
			</view>
			<view class="stat-item">
				<text class="stat-value">{{ earnedRewards.toFixed(2) }}</text>
				<text class="stat-label">已得奖励(元)</text>
			</view>
		</view>
		
		<!-- 邀请奖励 -->
		<view class="reward-panel">
			<view class="panel-header orange">
				<text>邀请奖励</text>
				<text class="header-emoji">🎁</text>
			</view>
			<view class="panel-body">
				<view class="reward-item">
					<text class="reward-tag">奖励一</text>
				</view>
				<text class="reward-text">好友注册30天内下单（不限量），邀请人可获得订单金额的 <text class="highlight orange">8%</text>现金奖励；</text>
				
				<view class="reward-item">
					<text class="reward-tag">奖励二</text>
				</view>
				<text class="reward-text">好友注册31—100天内下单（不限量），邀请人可获得订单金额的 <text class="highlight orange">4%</text>现金奖励；</text>
			</view>
		</view>
		
		<!-- 好友福利 -->
		<view class="reward-panel">
			<view class="panel-header blue">
				<text>好友福利</text>
				<text class="header-emoji">👥</text>
			</view>
			<view class="panel-body">
				<view class="reward-item">
					<text class="reward-tag blue">福利一</text>
				</view>
				<text class="reward-text">好友注册30天内并下单，好友可获得订单金额<text class="highlight blue">2%</text>的现金奖励；好友注册31—100天内并下单，好友可获得订单金额<text class="highlight blue">1%</text>的现金奖励；</text>
				
				<view class="reward-item">
					<text class="reward-tag blue">福利二</text>
				</view>
				<text class="reward-text">注册即得首样免费<text class="highlight orange">200元</text>门槛券 + 新客专区<text class="highlight orange">6折</text>起测试优惠（价值500元）</text>
			</view>
		</view>
		
		<!-- 邀请好友流程 -->
		<view class="flow-section">
			<view class="section-title">邀请好友流程</view>
			<view class="flow-list">
				<view class="flow-item">
					<text class="flow-number">01.</text>
					<view class="flow-content">
						<view class="flow-step">邀请好友完成注册</view>
						<button class="flow-btn" open-type="share">立即分享好友</button>
					</view>
				</view>
				<view class="flow-item">
					<text class="flow-number">02.</text>
					<view class="flow-content">
						<view class="flow-step">好友完成注册</view>
						<text class="flow-desc">好友获得<text class="highlight orange">200元</text>首样优惠券 + 价值<text class="highlight orange">500元</text>新客专区<text class="highlight orange">6折</text>优惠</text>
					</view>
				</view>
				<view class="flow-item">
					<text class="flow-number">03.</text>
					<view class="flow-content">
						<view class="flow-step">好友注册30天内下单（不限量）</view>
						<text class="flow-desc">您可获得订单金额的<text class="highlight orange">8%</text>奖励，好友获得订单金额<text class="highlight blue">2%</text>奖励</text>
					</view>
				</view>
				<view class="flow-item">
					<text class="flow-number">04.</text>
					<view class="flow-content">
						<view class="flow-step">好友注册31—100天内下单（不限量）</view>
						<text class="flow-desc">您可获得订单金额的<text class="highlight orange">4%</text>奖励，好友获得订单金额<text class="highlight blue">1%</text>奖励</text>
					</view>
				</view>
				<view class="flow-item">
					<text class="flow-number">05.</text>
					<view class="flow-content">
						<view class="flow-step">好友订单完成（信用支付需还款）</view>
						<text class="flow-desc">订单奖励全部解冻</text>
					</view>
				</view>
				<view class="flow-item">
					<text class="flow-number">06.</text>
					<view class="flow-content">
						<view class="flow-step">【钱包】里自动提醒</view>
						<button class="flow-btn orange">查看钱包</button>
						<text class="flow-desc">提现需实名认证</text>
					</view>
				</view>
			</view>
		</view>
		
		<!-- 活动规则 -->
		<view class="text-section">
			<view class="section-title">活动规则</view>
			<view class="text-content">
				<text>1. 被邀请人通过邀请人分享的邀请链接注册成功，并在注册后30天内下单（不限平台、不限单量），邀请人即可获得邀请订单金额的现金奖励；被邀请人可获得订单金额2%与1%的现金奖励；</text>
				<text>2. 现金奖励的计算方式：按订单实际支付金额（含使用抵扣后金额）计算；</text>
				<text>3. 若被邀请人订单产生退款，系统将自动扣减对应奖励；若存在恶意刷单行为，平台将取消其奖励资格；</text>
				<text>4. 奖励到账时间为订单完成后T+7日；</text>
			</view>
		</view>
		
		<!-- 提现规则 -->
		<view class="text-section">
			<view class="section-title">提现规则</view>
			<view class="text-content">
				<text>支持在"可提现奖励"处发起提现，需完成实名认证；平台保留规则最终解释权。</text>
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
			withdrawable: 0,
			myInvites: 0,
			predictedOrders: 0,
			predictedRewards: 0,
			earnedRewards: 0
		}
	},
	
	onLoad() {
		this.loadInviteData()
	},
	
	// 分享配置
	onShareAppMessage() {
		const userInfo = uni.getStorageSync('userInfo') || {}
		return {
			title: '我在科研检测服务平台发现了超好用的检测服务！注册即享优惠！',
			path: `/pages/index/index?inviteUserId=${userInfo.id}`
		}
	},
	
	methods: {
		// 加载邀请数据
		async loadInviteData() {
			try {
				const res = await api.getInviteStats()
				this.withdrawable = res.data.withdrawable || 0
				this.myInvites = res.data.my_invites || 0
				this.predictedOrders = res.data.predicted_orders || 0
				this.predictedRewards = res.data.predicted_rewards || 0
				this.earnedRewards = res.data.earned_rewards || 0
			} catch (error) {
				console.error('加载邀请数据失败', error)
				// 如果API调用失败，使用默认值
				this.withdrawable = 0
				this.myInvites = 0
				this.predictedOrders = 0
				this.predictedRewards = 0
				this.earnedRewards = 0
			}
		},
		
		// 提现
		handleWithdraw() {
			if (this.withdrawable <= 0) {
				uni.showToast({
					title: '暂无可提现奖励',
					icon: 'none'
				})
				return
			}
			
			uni.showModal({
				title: '提现',
				content: `确认提现 ¥${this.withdrawable.toFixed(2)} 到钱包吗？需要先完成实名认证。`,
				success: (res) => {
					if (res.confirm) {
						// 检查是否实名
						uni.navigateTo({
							url: '/pagesA/certification/certification'
						})
					}
				}
			})
		},
		
		// 显示规则
		showRulesModal() {
			uni.showModal({
				title: '邀请活动规则',
				content: '好友注册30天内下单奖励8%，31-100天内下单奖励4%；好友现金奖励：30天内2%，31-100天内1%。奖励以实际支付金额计算，退款将扣减奖励。订单完成后T+7日到账。',
				showCancel: false,
				confirmText: '我知道了'
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

/* 四项指标 */
.stats-grid {
	display: grid;
	grid-template-columns: repeat(4, 1fr);
	background: white;
	margin: 0 30rpx 20rpx;
	border-radius: 12rpx;
	padding: 24rpx 0;
	gap: 0;
}

.stat-item {
	display: flex;
	flex-direction: column;
	align-items: center;
	border-right: 1rpx solid #f0f0f0;
}

.stat-item:last-child {
	border-right: none;
}

.stat-value {
	font-size: 36rpx;
	font-weight: 700;
	color: #333;
	margin-bottom: 8rpx;
}

.stat-label {
	font-size: 22rpx;
	color: #666;
	text-align: center;
}

/* 奖励面板 */
.reward-panel {
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

.reward-item {
	margin-bottom: 12rpx;
}

.reward-tag {
	background: #ffedd5;
	color: #ff7e5f;
	padding: 8rpx 20rpx;
	border-radius: 30rpx;
	font-size: 22rpx;
	display: inline-block;
}

.reward-tag.blue {
	background: #e7f5ff;
	color: #4dabf7;
}

.reward-text {
	font-size: 26rpx;
	color: #333;
	line-height: 1.8;
	display: block;
	margin-bottom: 20rpx;
}

.highlight {
	font-weight: 700;
}

.highlight.orange {
	color: #ff7e5f;
}

.highlight.blue {
	color: #4dabf7;
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

.flow-step {
	background: linear-gradient(135deg, #6ec1ff 0%, #4dabf7 100%);
	color: white;
	padding: 12rpx 24rpx;
	border-radius: 40rpx;
	font-size: 24rpx;
	display: inline-block;
	margin-bottom: 8rpx;
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

/* 文字区块 */
.text-section {
	background: white;
	margin: 0 30rpx 20rpx;
	border-radius: 16rpx;
	padding: 24rpx;
}

.text-content {
	text {
		font-size: 24rpx;
		color: #666;
		line-height: 1.8;
		display: block;
		margin-bottom: 12rpx;
	}
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
