<script>
	export default {
		onLaunch: function() {
			console.log('App Launch');
			// 初始化配置
			this.initApp();
		},
		onShow: function() {
			console.log('App Show');
		},
		onHide: function() {
			console.log('App Hide');
		},
		methods: {
			initApp() {
				// 检查登录状态
				const token = uni.getStorageSync('token');
				if (token) {
					this.$store.commit('SET_TOKEN', token);
				}
			}
		}
	};
</script>

<style lang="scss">
	/*每个页面公共css */
	
	/* 全局样式 */
	page {
		background-color: #f8f8f8;
		font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Helvetica, Segoe UI, Arial, Roboto, 'PingFang SC', 'miui', 'Hiragino Sans GB', 'Microsoft Yahei', sans-serif;
	}
	
	/* 全局按钮样式 */
	.btn-primary {
		background-color: #007AFF;
		color: #ffffff;
		border-radius: 8rpx;
		padding: 24rpx;
		text-align: center;
		font-size: 32rpx;
	}
	
	.btn-primary:active {
		opacity: 0.8;
	}
	
	/* 全局卡片样式 */
	.card {
		background-color: #ffffff;
		border-radius: 16rpx;
		padding: 24rpx;
		margin-bottom: 24rpx;
		box-shadow: 0 2rpx 12rpx rgba(0,0,0,0.05);
	}
	
	/* 全局文本样式 */
	.text-primary {
		color: #007AFF;
	}
	
	.text-secondary {
		color: #8f9396;
	}
	
	.text-danger {
		color: #dd524d;
	}
	
	.text-success {
		color: #18bc37;
	}
</style>

