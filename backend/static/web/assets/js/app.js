// 科研检测服务平台 - Web端应用
const { createApp } = Vue
const { ElMessage, ElMessageBox } = ElementPlus

// API基础URL
const API_BASE_URL = 'http://8.148.188.85:3000'

// Axios配置
axios.defaults.baseURL = API_BASE_URL
axios.interceptors.request.use(config => {
    const token = localStorage.getItem('token')
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
})

axios.interceptors.response.use(
    response => response.data,
    error => {
        const message = error.response?.data?.detail || error.message || '请求失败'
        ElMessage.error(message)
        if (error.response?.status === 401) {
            localStorage.removeItem('token')
            localStorage.removeItem('userInfo')
            window.location.reload()
        }
        return Promise.reject(error)
    }
)

// API接口
const api = {
    // 认证
    sendSms: (data) => axios.post('/api/v1/auth/send-sms', data),
    smsLogin: (data) => axios.post('/api/v1/auth/sms-login', data),
    
    // 用户
    getUserInfo: () => axios.get('/api/v1/users/me'),
    getBalance: () => axios.get('/api/v1/users/balance'),
    updateProfile: (data) => axios.put('/api/v1/users/profile', data),
    
    // 项目
    getCategories: () => axios.get('/api/v1/projects/categories'),
    getProjects: (params) => axios.get('/api/v1/projects/list', { params }),
    getProjectDetail: (id) => axios.get(`/api/v1/projects/${id}`),
    
    // 订单
    getOrders: (params) => axios.get('/api/v1/orders/list', { params }),
    getOrderDetail: (id) => axios.get(`/api/v1/orders/${id}`),
    createOrder: (data) => axios.post('/api/v1/orders/create', data),
    cancelOrder: (id, data) => axios.post(`/api/v1/orders/${id}/cancel`, data),
    
    // 支付
    createPayment: (data) => axios.post('/api/v1/payments/create', data),
    payWithBalance: (data) => axios.post('/api/v1/payments/balance-pay', data),
    
    // 地址
    getAddresses: () => axios.get('/api/v1/addresses/list'),
    createAddress: (data) => axios.post('/api/v1/addresses/create', data),
    updateAddress: (id, data) => axios.put(`/api/v1/addresses/${id}`, data),
    deleteAddress: (id) => axios.delete(`/api/v1/addresses/${id}`),
    setDefaultAddress: (id) => axios.put(`/api/v1/addresses/${id}/default`),
    
    // 优惠券
    getCoupons: (params) => axios.get('/api/v1/coupons/list', { params }),
    getAvailableCoupons: (projectId) => axios.get('/api/v1/coupons/available', { params: { project_id: projectId } }),
    
    // 收藏
    getFavorites: (params) => axios.get('/api/v1/favorites/list', { params }),
    addFavorite: (projectId) => axios.post('/api/v1/favorites/add', { project_id: projectId }),
    removeFavorite: (projectId) => axios.delete(`/api/v1/favorites/${projectId}`),
    checkFavorite: (projectId) => axios.get(`/api/v1/favorites/check/${projectId}`),
    
    // 评价
    getReviews: (params) => {
        if (params.project_id) {
            return axios.get(`/api/v1/reviews/project/${params.project_id}`, { params: { page: params.page, page_size: params.page_size } })
        }
        return axios.get('/api/v1/reviews/my', { params })
    },
    createReview: (data) => axios.post('/api/v1/reviews/create', {
        order_id: data.order_id,
        service_rating: data.rating,
        quality_rating: data.rating,
        logistics_rating: data.rating,
        content: data.content
    }),
    
    // 充值
    createRecharge: (data) => axios.post('/api/v1/recharge/create', data),
    getRechargeRecords: (params) => axios.get('/api/v1/recharge/records', { params }),
    
    // 发票
    applyInvoice: (data) => axios.post('/api/v1/invoices/apply', data),
    getInvoices: (params) => axios.get('/api/v1/invoices/list', { params }),
    
    // 积分
    getPointsGoods: (params) => axios.get('/api/v1/points/goods', { params }),
    exchangePoints: (data) => axios.post('/api/v1/points/exchange', data),
    getPointsRecords: (params) => axios.get('/api/v1/points/records', { params }),
    
    // 团队邀请
    getMyGroup: () => axios.get('/api/v1/groups/my'),
    createGroup: (data) => axios.post('/api/v1/groups/create', data),
    getInviteRecords: (params) => axios.get('/api/v1/invites/records', { params }),
    getInviteStats: () => axios.get('/api/v1/invites/stats'),
    applyWithdraw: (data) => axios.post('/api/v1/invites/withdraw', data),
    
    // 轮播图/Banner
    getBanners: () => axios.get('/api/v1/banners/list'),
    
    // 公告
    getAnnouncements: (params) => axios.get('/api/v1/announcements/list', { params }),
    
    // 帮助中心
    getHelpCategories: () => axios.get('/api/v1/help/categories'),
    getHelpArticles: (params) => axios.get('/api/v1/help/articles', { params }),
    
    // 在线客服
    getChatHistory: () => axios.get('/api/v1/chat/history'),
    sendMessage: (data) => axios.post('/api/v1/chat/send', data),
    
    // 报告下载
    getReports: (params) => axios.get('/api/v1/reports/list', { params }),
    downloadReport: (orderId) => axios.get(`/api/v1/reports/${orderId}/download`, { responseType: 'blob' }),
    
    // 样品追踪
    getSampleStatus: (orderId) => axios.get(`/api/v1/samples/order/${orderId}/status`),
    getSampleTimeline: (orderId) => axios.get(`/api/v1/samples/order/${orderId}/timeline`),
    submitLogistics: (orderId, data) => axios.post(`/api/v1/samples/order/${orderId}/logistics`, data),
    
    // 抽奖
    getLotteryInfo: () => axios.get('/api/v1/lottery/info'),
    doLottery: () => axios.post('/api/v1/lottery/draw'),
    getLotteryRecords: (params) => axios.get('/api/v1/lottery/records', { params }),
    
    // 合同管理
    getContracts: (params) => axios.get('/api/v1/contracts/list', { params }),
    getContractDetail: (id) => axios.get(`/api/v1/contracts/${id}`),
    downloadContract: (id) => axios.post(`/api/v1/contracts/${id}/download`),
    
    // 加盟申请
    submitFranchise: (data) => axios.post('/api/v1/franchise/apply', data),
    getFranchiseModes: () => axios.get('/api/v1/franchise/modes'),
    checkFranchiseStatus: (phone) => axios.get('/api/v1/franchise/check', { params: { phone } }),
    
    // 数据统计
    getStatsOverview: (timeRange) => axios.get('/api/v1/statistics/overview', { params: { time_range: timeRange } }),
    getOrderStats: (timeRange) => axios.get('/api/v1/statistics/order-stats', { params: { time_range: timeRange } }),
    getProjectStats: (timeRange, limit) => axios.get('/api/v1/statistics/project-stats', { params: { time_range: timeRange, limit } }),
    getConsumptionTrend: (timeRange) => axios.get('/api/v1/statistics/trend', { params: { time_range: timeRange } }),
    
    // 用户通知
    getNotifications: (params) => axios.get('/api/v1/announcements/notifications/list', { params }),
    markNotificationRead: (id) => axios.post(`/api/v1/announcements/notifications/${id}/read`),
    markAllNotificationsRead: () => axios.post('/api/v1/announcements/notifications/read-all'),
    
    // 快捷回复
    getQuickReplies: () => axios.get('/api/v1/chat/quick-replies'),
    getChatSession: () => axios.get('/api/v1/chat/session')
}

// ==================== Vue组件 ====================

// 首页组件
const HomeView = {
    emits: ['go-projects', 'go-detail', 'go-help', 'go-chat', 'go-lottery', 'go-reports', 'go-announcements', 'go-franchise'],
    template: `
        <div class="home-view">
            <!-- 轮播图Banner -->
            <div class="banner-carousel" v-if="banners.length > 0">
                <el-carousel height="400px" :interval="5000">
                    <el-carousel-item v-for="banner in banners" :key="banner.id">
                        <div class="banner-item" :style="{ backgroundImage: 'url(' + banner.image + ')' }" @click="handleBannerClick(banner)">
                            <div class="banner-content">
                                <h2>{{ banner.title }}</h2>
                                <p>{{ banner.subtitle }}</p>
                                <el-button v-if="banner.button_text" type="primary" size="large">{{ banner.button_text }}</el-button>
                            </div>
                        </div>
                    </el-carousel-item>
                </el-carousel>
            </div>
            
            <!-- 默认英雄区（无Banner时显示） -->
            <div class="hero-section" v-else>
                <h1 class="hero-title">科研检测服务平台</h1>
                <p class="hero-subtitle">专业 · 高效 · 可靠</p>
                <div class="hero-actions">
                    <el-button type="primary" size="large" @click="$emit('go-projects')">浏览检测项目</el-button>
                    <el-button size="large" plain @click="$emit('go-help')">了解更多</el-button>
                </div>
            </div>

            <!-- 公告栏 -->
            <div class="announcement-bar" v-if="announcements.length > 0">
                <div class="announcement-icon">📢</div>
                <el-carousel height="36px" direction="vertical" :autoplay="true" :interval="4000" indicator-position="none">
                    <el-carousel-item v-for="ann in announcements" :key="ann.id">
                        <div class="announcement-item" @click="showAnnouncement(ann)">
                            <span class="announcement-title">{{ ann.title }}</span>
                            <span class="announcement-time">{{ ann.created_at?.slice(0, 10) }}</span>
                        </div>
                    </el-carousel-item>
                </el-carousel>
                <el-button link type="primary" @click="$emit('go-announcements')">更多</el-button>
            </div>
            
            <!-- 快捷入口 -->
            <div class="quick-entry">
                <div class="quick-item" @click="$emit('go-help')">
                    <div class="quick-icon" style="background: #e6f7ff; color: #1890ff;">❓</div>
                    <span>帮助中心</span>
                </div>
                <div class="quick-item" @click="$emit('go-chat')">
                    <div class="quick-icon" style="background: #fff7e6; color: #fa8c16;">💬</div>
                    <span>在线客服</span>
                </div>
                <div class="quick-item" @click="$emit('go-lottery')">
                    <div class="quick-icon" style="background: #fff1f0; color: #f5222d;">🎁</div>
                    <span>抽奖活动</span>
                </div>
                <div class="quick-item" @click="$emit('go-reports')">
                    <div class="quick-icon" style="background: #f6ffed; color: #52c41a;">📊</div>
                    <span>报告下载</span>
                </div>
                <div class="quick-item" @click="$emit('go-franchise')">
                    <div class="quick-icon" style="background: #f9f0ff; color: #722ed1;">🤝</div>
                    <span>加盟合作</span>
                </div>
            </div>

            <!-- 分类展示 -->
            <div class="mb-24">
                <h2 class="section-title">检测分类</h2>
                <div v-if="categoriesLoading" class="loading-container">
                    <el-icon class="is-loading" :size="40"><loading /></el-icon>
                </div>
                <div v-else class="categories-grid">
                    <div v-for="cat in categories" :key="cat.id" class="category-card" @click="goToCategory(cat.id)">
                        <div class="category-icon">{{ cat.icon || '🔬' }}</div>
                        <div class="category-name">{{ cat.name }}</div>
                    </div>
                </div>
            </div>

            <!-- 推荐项目 -->
            <div>
                <h2 class="section-title">推荐项目</h2>
                <div v-if="projectsLoading" class="loading-container">
                    <el-icon class="is-loading" :size="40"><loading /></el-icon>
                </div>
                <div v-else-if="projects.length === 0" class="empty-state">
                    <div class="empty-icon">📝</div>
                    <div class="empty-text">暂无推荐项目</div>
                </div>
                <div v-else class="projects-grid">
                    <div v-for="project in projects" :key="project.id" class="project-card" @click="$emit('go-detail', project.id)">
                        <img :src="project.cover_image || 'https://via.placeholder.com/280x180'" class="project-image" alt="">
                        <div class="project-info">
                            <div class="project-name">{{ project.name }}</div>
                            <div class="project-price">
                                <span class="current-price">¥{{ project.current_price }}</span>
                                <span class="original-price">¥{{ project.original_price }}</span>
                            </div>
                            <div class="project-tags">
                                <el-tag v-if="project.is_hot" type="danger" size="small">热门</el-tag>
                                <el-tag v-if="project.is_recommended" type="warning" size="small">推荐</el-tag>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `,
    data() {
        return {
            banners: [],
            announcements: [],
            categories: [],
            categoriesLoading: false,
            projects: [],
            projectsLoading: false
        }
    },
    mounted() {
        this.loadBanners()
        this.loadAnnouncements()
        this.loadCategories()
        this.loadProjects()
    },
    methods: {
        async loadBanners() {
            try {
                const res = await api.getBanners()
                this.banners = res.data || []
            } catch (error) {
                // 使用默认Banner数据
                this.banners = [
                    { id: 1, title: '金秋检测季', subtitle: 'XPS、SEM、FT-IR等热门检测6折起', image: 'https://picsum.photos/1400/400?random=1', button_text: '立即查看' },
                    { id: 2, title: '新用户专享', subtitle: '首单立减50元，注册即送100积分', image: 'https://picsum.photos/1400/400?random=2', button_text: '领取优惠' }
                ]
            }
        },
        async loadAnnouncements() {
            try {
                const res = await api.getAnnouncements({ page: 1, page_size: 5 })
                this.announcements = res.data?.items || []
            } catch (error) {
                // 使用默认公告数据
                this.announcements = [
                    { id: 1, title: '平台检测服务升级通知', created_at: '2025-12-01' },
                    { id: 2, title: '12月优惠活动火热进行中', created_at: '2025-12-01' }
                ]
            }
        },
        async loadCategories() {
            this.categoriesLoading = true
            try {
                const res = await api.getCategories()
                this.categories = res.data || []
            } catch (error) {
                console.error('加载分类失败', error)
            } finally {
                this.categoriesLoading = false
            }
        },
        async loadProjects() {
            this.projectsLoading = true
            try {
                const res = await api.getProjects({ page: 1, page_size: 8 })
                this.projects = res.data?.items || []
            } catch (error) {
                console.error('加载项目失败', error)
            } finally {
                this.projectsLoading = false
            }
        },
        goToCategory(categoryId) {
            this.$emit('go-projects', { category_id: categoryId })
        },
        handleBannerClick(banner) {
            if (banner.link) window.open(banner.link, '_blank')
        },
        showAnnouncement(ann) {
            ElMessageBox.alert(ann.content || ann.title, ann.title, { confirmButtonText: '我知道了' })
        }
    }
}

// 项目列表组件
const ProjectsView = {
    template: `
        <div class="projects-view">
            <div class="filter-bar">
                <div class="filter-row">
                    <el-input
                        v-model="search"
                        placeholder="搜索项目名称或编号"
                        style="width: 300px"
                        clearable
                        @change="loadProjects">
                        <template #prefix>
                            <el-icon><search /></el-icon>
                        </template>
                    </el-input>
                    <el-select v-model="categoryId" placeholder="选择分类" clearable @change="loadProjects" style="width: 200px">
                        <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id"></el-option>
                    </el-select>
                    <el-button type="primary" @click="loadProjects">搜索</el-button>
                    <el-button @click="handleReset">重置</el-button>
                </div>
            </div>

            <div v-if="loading" class="loading-container">
                <el-icon class="is-loading" :size="40"><loading /></el-icon>
            </div>
            <div v-else-if="projects.length === 0" class="empty-state">
                <div class="empty-icon">📝</div>
                <div class="empty-text">暂无项目</div>
            </div>
            <div v-else>
                <div class="projects-grid">
                    <div v-for="project in projects" :key="project.id" class="project-card" @click="$emit('go-detail', project.id)">
                        <img :src="project.cover_image || 'https://via.placeholder.com/280x180'" class="project-image" alt="">
                        <div class="project-info">
                            <div class="project-name">{{ project.name }}</div>
                            <div class="project-price">
                                <span class="current-price">¥{{ project.current_price }}</span>
                                <span class="original-price">¥{{ project.original_price }}</span>
                            </div>
                            <div class="project-tags">
                                <el-tag v-if="project.is_hot" type="danger" size="small">热门</el-tag>
                                <el-tag v-if="project.is_recommended" type="warning" size="small">推荐</el-tag>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="text-center mt-24">
                    <el-pagination
                        v-model:current-page="page"
                        v-model:page-size="pageSize"
                        :total="total"
                        :page-sizes="[12, 24, 48]"
                        layout="total, sizes, prev, pager, next, jumper"
                        @current-change="loadProjects"
                        @size-change="loadProjects">
                    </el-pagination>
                </div>
            </div>
        </div>
    `,
    data() {
        return {
            search: '',
            categoryId: null,
            categories: [],
            projects: [],
            loading: false,
            page: 1,
            pageSize: 12,
            total: 0
        }
    },
    mounted() {
        this.loadCategories()
        this.loadProjects()
    },
    methods: {
        async loadCategories() {
            try {
                const res = await api.getCategories()
                this.categories = res.data || []
            } catch (error) {
                console.error('加载分类失败', error)
            }
        },
        async loadProjects() {
            this.loading = true
            try {
                const params = {
                    page: this.page,
                    page_size: this.pageSize
                }
                if (this.search) params.search = this.search
                if (this.categoryId) params.category_id = this.categoryId

                const res = await api.getProjects(params)
                this.projects = res.data?.items || []
                this.total = res.data?.total || 0
            } catch (error) {
                console.error('加载项目失败', error)
            } finally {
                this.loading = false
            }
        },
        handleReset() {
            this.search = ''
            this.categoryId = null
            this.page = 1
            this.loadProjects()
        }
    }
}

// 项目详情组件
const ProjectDetail = {
    props: ['projectId'],
    emits: ['go-back', 'show-booking', 'require-login'],
    template: `
        <div class="project-detail">
            <div v-if="loading" class="loading-container">
                <el-icon class="is-loading" :size="40"><loading /></el-icon>
            </div>
            <div v-else-if="project">
                <div class="detail-header">
                    <div class="detail-actions mb-16">
                        <el-button @click="$emit('go-back')">
                            <el-icon><arrow-left /></el-icon> 返回列表
                        </el-button>
                        <el-button :type="isFavorite ? 'warning' : 'default'" @click="toggleFavorite">
                            <el-icon><star-filled v-if="isFavorite" /><star v-else /></el-icon>
                            {{ isFavorite ? '已收藏' : '收藏' }}
                        </el-button>
                    </div>
                    
                    <div class="detail-main">
                        <div class="detail-images">
                            <img :src="project.cover_image || 'https://via.placeholder.com/400x400'" class="detail-image" alt="">
                        </div>
                        <div class="detail-info">
                            <h1>{{ project.name }}</h1>
                            <div class="detail-price">
                                <span class="current">¥{{ project.current_price }}</span>
                                <span class="original">¥{{ project.original_price }}</span>
                            </div>
                            <div class="detail-meta">
                                <div class="meta-item">
                                    <span class="meta-label">项目编号：</span>
                                    <span class="meta-value">{{ project.project_no }}</span>
                                </div>
                                <div class="meta-item">
                                    <span class="meta-label">服务周期：</span>
                                    <span class="meta-value">{{ project.service_cycle_min }}-{{ project.service_cycle_max }}工作日</span>
                                </div>
                                <div class="meta-item">
                                    <span class="meta-label">检测仪器：</span>
                                    <span class="meta-value">{{ project.equipment_name || '-' }}</span>
                                </div>
                                <div class="meta-item">
                                    <span class="meta-label">浏览量：</span>
                                    <span class="meta-value">{{ project.view_count }}</span>
                                </div>
                            </div>
                            <el-button type="primary" size="large" style="width: 100%" @click="handleBooking">立即预约</el-button>
                        </div>
                    </div>
                </div>

                <div class="detail-tabs">
                    <el-tabs v-model="activeTab">
                        <el-tab-pane label="项目介绍" name="intro">
                            <div v-html="project.introduction || '暂无介绍'"></div>
                        </el-tab-pane>
                        <el-tab-pane label="样品要求" name="sample">
                            <div v-html="project.sample_requirements || '暂无要求'"></div>
                        </el-tab-pane>
                        <el-tab-pane label="检测标准" name="standard">
                            <div v-html="project.testing_standards || '暂无标准'"></div>
                        </el-tab-pane>
                        <el-tab-pane label="用户评价" name="reviews">
                            <div v-if="reviews.length === 0" class="empty-state" style="padding: 40px">
                                <div class="empty-icon">💬</div>
                                <div class="empty-text">暂无评价</div>
                            </div>
                            <div v-else class="reviews-list">
                                <div class="review-item" v-for="review in reviews" :key="review.id">
                                    <div class="review-header">
                                        <el-avatar :size="32">{{ review.user_nickname?.[0] || 'U' }}</el-avatar>
                                        <span class="review-user">{{ review.user_nickname || '匿名用户' }}</span>
                                        <el-rate :model-value="Math.round(review.avg_rating || review.service_rating || 5)" disabled size="small"></el-rate>
                                        <span class="review-time">{{ review.created_at?.slice(0, 10) }}</span>
                                    </div>
                                    <div class="review-content">{{ review.content }}</div>
                                </div>
                            </div>
                        </el-tab-pane>
                    </el-tabs>
                </div>
            </div>
        </div>
    `,
    data() {
        return {
            project: null,
            loading: false,
            activeTab: 'intro',
            isFavorite: false,
            reviews: []
        }
    },
    mounted() {
        this.loadProject()
    },
    watch: {
        projectId() {
            this.loadProject()
        }
    },
    methods: {
        async loadProject() {
            this.loading = true
            try {
                const res = await api.getProjectDetail(this.projectId)
                this.project = res.data
                this.checkFavorite()
                this.loadReviews()
            } catch (error) {
                console.error('加载项目详情失败', error)
            } finally {
                this.loading = false
            }
        },
        async checkFavorite() {
            const token = localStorage.getItem('token')
            if (!token) return
            try {
                const res = await api.checkFavorite(this.projectId)
                this.isFavorite = res.data?.is_favorite || false
            } catch (error) {}
        },
        async toggleFavorite() {
            const token = localStorage.getItem('token')
            if (!token) {
                this.$emit('require-login')
                return
            }
            try {
                if (this.isFavorite) {
                    await api.removeFavorite(this.projectId)
                    ElMessage.success('已取消收藏')
                } else {
                    await api.addFavorite(this.projectId)
                    ElMessage.success('收藏成功')
                }
                this.isFavorite = !this.isFavorite
            } catch (error) {
                console.error('操作失败', error)
            }
        },
        async loadReviews() {
            try {
                const res = await api.getReviews({ project_id: this.projectId, page: 1, page_size: 10 })
                this.reviews = res.data?.items || []
            } catch (error) {}
        },
        handleBooking() {
            const token = localStorage.getItem('token')
            if (!token) {
                this.$emit('require-login')
                return
            }
            this.$emit('show-booking', this.project)
        }
    }
}

// 订单列表组件
const OrdersView = {
    emits: ['show-payment', 'show-review', 'show-invoice', 'go-sample-track', 'go-report'],
    template: `
        <div class="orders-view">
            <h2 class="section-title">我的订单</h2>

            <div class="order-filters">
                <el-radio-group v-model="status" @change="loadOrders">
                    <el-radio-button value="">全部</el-radio-button>
                    <el-radio-button value="unpaid">待支付</el-radio-button>
                    <el-radio-button value="paid">已支付</el-radio-button>
                    <el-radio-button value="testing">实验中</el-radio-button>
                    <el-radio-button value="completed">已完成</el-radio-button>
                </el-radio-group>
            </div>

            <div v-if="loading" class="loading-container">
                <el-icon class="is-loading" :size="40"><loading /></el-icon>
            </div>
            <div v-else-if="orders.length === 0" class="empty-state">
                <div class="empty-icon">📦</div>
                <div class="empty-text">暂无订单</div>
            </div>
            <div v-else>
                <div class="order-card" v-for="order in orders" :key="order.id">
                    <div class="order-header">
                        <span class="order-no">订单号：{{ order.order_no }}</span>
                        <el-tag :type="getStatusType(order.status)">{{ getStatusText(order.status) }}</el-tag>
                    </div>
                    <div class="order-content">
                        <div class="order-project">
                            <div><strong>{{ order.project_name }}</strong></div>
                            <div>样品：{{ order.sample_name }} × {{ order.quantity }}</div>
                            <div class="order-amount">金额：<span class="price">¥{{ order.total_amount }}</span></div>
                            <div class="order-time">下单时间：{{ order.created_at?.slice(0, 16).replace('T', ' ') }}</div>
                        </div>
                        <div class="order-actions">
                            <el-button type="primary" v-if="order.status === 'unpaid'" @click="$emit('show-payment', order)">去支付</el-button>
                            <el-button v-if="order.status === 'unpaid'" @click="handleCancel(order.id)">取消订单</el-button>
                            
                            <!-- 样品追踪 - 支付后可用 -->
                            <el-button v-if="['paid', 'confirmed', 'testing', 'completed'].includes(order.status)" @click="$emit('go-sample-track', order.id)">
                                <el-icon><location /></el-icon> 样品追踪
                            </el-button>
                            
                            <!-- 报告下载 - 完成后可用 -->
                            <el-button type="success" v-if="order.status === 'completed'" @click="downloadReport(order)">
                                <el-icon><download /></el-icon> 下载报告
                            </el-button>
                            
                            <el-button type="warning" v-if="order.status === 'completed' && !order.is_reviewed" @click="$emit('show-review', order)">评价</el-button>
                            <el-button v-if="order.status === 'completed'" @click="$emit('show-invoice', order)">申请发票</el-button>
                        </div>
                    </div>
                    
                    <!-- 进度条 -->
                    <div class="order-progress" v-if="['paid', 'confirmed', 'testing'].includes(order.status)">
                        <el-steps :active="getProgressStep(order.status)" finish-status="success" simple>
                            <el-step title="已支付"></el-step>
                            <el-step title="样品送达"></el-step>
                            <el-step title="检测中"></el-step>
                            <el-step title="已完成"></el-step>
                        </el-steps>
                    </div>
                </div>

                <div class="text-center mt-24">
                    <el-pagination
                        v-model:current-page="page"
                        :total="total"
                        :page-size="10"
                        layout="total, prev, pager, next"
                        @current-change="loadOrders">
                    </el-pagination>
                </div>
            </div>
        </div>
    `,
    data() {
        return {
            status: '',
            orders: [],
            loading: false,
            page: 1,
            total: 0
        }
    },
    mounted() {
        this.loadOrders()
    },
    methods: {
        async loadOrders() {
            this.loading = true
            try {
                const params = { page: this.page, page_size: 10 }
                if (this.status) params.status = this.status

                const res = await api.getOrders(params)
                this.orders = res.data?.items || []
                this.total = res.data?.total || 0
            } catch (error) {
                console.error('加载订单失败', error)
            } finally {
                this.loading = false
            }
        },
        async handleCancel(orderId) {
            try {
                await ElMessageBox.confirm('确定要取消订单吗？', '提示', {
                    type: 'warning'
                })
                await api.cancelOrder(orderId, { reason: '用户取消' })
                ElMessage.success('订单已取消')
                this.loadOrders()
            } catch (error) {
                if (error !== 'cancel') {
                    console.error('取消订单失败', error)
                }
            }
        },
        getStatusText(status) {
            const map = {
                'unpaid': '待支付',
                'paid': '已支付',
                'confirmed': '已确认',
                'testing': '实验中',
                'completed': '已完成',
                'cancelled': '已取消'
            }
            return map[status] || status
        },
        getStatusType(status) {
            const map = {
                'unpaid': 'warning',
                'paid': 'info',
                'confirmed': 'primary',
                'testing': 'primary',
                'completed': 'success',
                'cancelled': 'danger'
            }
            return map[status] || 'info'
        },
        getProgressStep(status) {
            const map = { 'paid': 1, 'confirmed': 2, 'testing': 3, 'completed': 4 }
            return map[status] || 0
        },
        async downloadReport(order) {
            ElMessage.info('正在准备下载报告...')
            try {
                const res = await api.downloadReport(order.id)
                const url = window.URL.createObjectURL(new Blob([res]))
                const link = document.createElement('a')
                link.href = url
                link.download = `检测报告_${order.order_no}.pdf`
                link.click()
                window.URL.revokeObjectURL(url)
                ElMessage.success('下载成功')
            } catch (error) {
                ElMessage.warning('报告正在生成中，请稍后再试')
            }
        }
    }
}

// 个人中心组件
const ProfileView = {
    emits: ['go-orders', 'go-favorites', 'go-coupons', 'go-address', 'go-wallet', 'go-points', 'go-invoice', 'go-team', 'go-reports', 'go-help', 'go-chat', 'go-announcements', 'go-contracts', 'go-lottery', 'go-franchise', 'edit-profile'],
    template: `
        <div class="profile-view">
            <div class="profile-header">
                <el-avatar :size="80" :src="userInfo.avatar">{{ userInfo.nickname?.[0] || 'U' }}</el-avatar>
                <div class="profile-info">
                    <h2>{{ userInfo.nickname || '用户' }}</h2>
                    <p>{{ userInfo.phone }}</p>
                    <div class="profile-badges">
                        <el-tag v-if="userInfo.is_certified" type="success" size="small">已实名</el-tag>
                        <el-tag v-else type="info" size="small">未实名</el-tag>
                        <el-tag v-if="userInfo.vip_level" type="warning" size="small">VIP{{ userInfo.vip_level }}</el-tag>
                    </div>
                    <el-button size="small" @click="$emit('edit-profile')">编辑资料</el-button>
                </div>
            </div>

            <div class="profile-stats">
                <div class="stat-card" @click="$emit('go-wallet')">
                    <div class="stat-value">¥{{ balance.credit_limit || 0 }}</div>
                    <div class="stat-label">信用额度</div>
                </div>
                <div class="stat-card" @click="$emit('go-wallet')">
                    <div class="stat-value">¥{{ balance.prepaid_balance || 0 }}</div>
                    <div class="stat-label">预付余额</div>
                </div>
                <div class="stat-card" @click="$emit('go-orders')">
                    <div class="stat-value">{{ userInfo.total_orders || 0 }}</div>
                    <div class="stat-label">订单数量</div>
                </div>
                <div class="stat-card" @click="$emit('go-points')">
                    <div class="stat-value">{{ userInfo.points_balance || 0 }}</div>
                    <div class="stat-label">积分</div>
                </div>
            </div>

            <div class="profile-menu">
                <h3>订单服务</h3>
                <div class="menu-grid">
                    <div class="menu-item" @click="$emit('go-orders')">
                        <el-icon :size="24"><document /></el-icon>
                        <span>我的订单</span>
                    </div>
                    <div class="menu-item highlight" @click="$emit('go-reports')">
                        <el-icon :size="24"><data-analysis /></el-icon>
                        <span>报告下载</span>
                        <div class="menu-badge">NEW</div>
                    </div>
                    <div class="menu-item" @click="$emit('go-contracts')">
                        <el-icon :size="24"><document-checked /></el-icon>
                        <span>合同管理</span>
                    </div>
                    <div class="menu-item" @click="$emit('go-invoice')">
                        <el-icon :size="24"><document-copy /></el-icon>
                        <span>发票管理</span>
                    </div>
                    <div class="menu-item highlight" @click="$emit('go-franchise')">
                        <el-icon :size="24"><promotion /></el-icon>
                        <span>加盟合作</span>
                        <div class="menu-badge hot">HOT</div>
                    </div>
                </div>
            </div>

            <div class="profile-menu">
                <h3>资产管理</h3>
                <div class="menu-grid">
                    <div class="menu-item" @click="$emit('go-wallet')">
                        <el-icon :size="24"><wallet /></el-icon>
                        <span>我的钱包</span>
                    </div>
                    <div class="menu-item" @click="$emit('go-coupons')">
                        <el-icon :size="24"><ticket /></el-icon>
                        <span>优惠券</span>
                    </div>
                    <div class="menu-item" @click="$emit('go-points')">
                        <el-icon :size="24"><medal /></el-icon>
                        <span>积分商城</span>
                    </div>
                    <div class="menu-item" @click="$emit('go-lottery')">
                        <el-icon :size="24"><present /></el-icon>
                        <span>抽奖活动</span>
                    </div>
                </div>
            </div>

            <div class="profile-menu">
                <h3>常用功能</h3>
                <div class="menu-grid">
                    <div class="menu-item" @click="$emit('go-favorites')">
                        <el-icon :size="24"><star /></el-icon>
                        <span>我的收藏</span>
                    </div>
                    <div class="menu-item" @click="$emit('go-address')">
                        <el-icon :size="24"><location /></el-icon>
                        <span>地址管理</span>
                    </div>
                    <div class="menu-item" @click="$emit('go-team')">
                        <el-icon :size="24"><user /></el-icon>
                        <span>团队邀请</span>
                    </div>
                    <div class="menu-item" @click="$emit('go-announcements')">
                        <el-icon :size="24"><bell /></el-icon>
                        <span>消息通知</span>
                    </div>
                </div>
            </div>

            <div class="profile-menu">
                <h3>帮助与服务</h3>
                <div class="menu-grid">
                    <div class="menu-item" @click="$emit('go-help')">
                        <el-icon :size="24"><question-filled /></el-icon>
                        <span>帮助中心</span>
                    </div>
                    <div class="menu-item" @click="$emit('go-chat')">
                        <el-icon :size="24"><chat-dot-round /></el-icon>
                        <span>在线客服</span>
                    </div>
                </div>
            </div>
        </div>
    `,
    data() {
        return {
            userInfo: JSON.parse(localStorage.getItem('userInfo') || '{}'),
            balance: {}
        }
    },
    mounted() {
        this.loadBalance()
        this.loadUserInfo()
    },
    methods: {
        async loadUserInfo() {
            try {
                const res = await api.getUserInfo()
                this.userInfo = res.data
                localStorage.setItem('userInfo', JSON.stringify(res.data))
            } catch (error) {}
        },
        async loadBalance() {
            try {
                const res = await api.getBalance()
                this.balance = res.data
            } catch (error) {
                console.error('加载余额失败', error)
            }
        }
    }
}

// 关于我们组件
const AboutView = {
    template: `
        <div class="about-view">
            <div class="about-section">
                <h2>关于我们</h2>
                <p>科研检测服务平台致力于为广大科研工作者提供专业、高效、可靠的检测服务。</p>
                <p>我们拥有先进的检测设备和专业的技术团队，能够满足各类科研检测需求。</p>
            </div>

            <div class="about-section">
                <h2>联系我们</h2>
                <p><strong>客服电话：</strong>400-123-4567</p>
                <p><strong>邮箱：</strong>service@eceshi.com</p>
                <p><strong>地址：</strong>北京市海淀区科技园</p>
            </div>

            <div class="about-section">
                <h2>关注我们</h2>
                <p><strong>微信公众号：</strong>E测试</p>
                <p><strong>微信小程序：</strong>科研检测服务平台</p>
            </div>
        </div>
    `
}

// 收藏列表组件
const FavoritesView = {
    emits: ['go-back', 'go-detail'],
    template: `
        <div class="favorites-view">
            <div class="page-header">
                <el-button @click="$emit('go-back')"><el-icon><arrow-left /></el-icon> 返回</el-button>
                <h2>我的收藏</h2>
            </div>
            <div v-if="loading" class="loading-container">
                <el-icon class="is-loading" :size="40"><loading /></el-icon>
            </div>
            <div v-else-if="favorites.length === 0" class="empty-state">
                <div class="empty-icon">⭐</div>
                <div class="empty-text">暂无收藏</div>
            </div>
            <div v-else class="projects-grid">
                <div class="project-card" v-for="item in favorites" :key="item.id" @click="$emit('go-detail', item.project_id)">
                    <img :src="item.project?.cover_image || 'https://via.placeholder.com/280x180'" class="project-image" alt="">
                    <div class="project-info">
                        <div class="project-name">{{ item.project?.name }}</div>
                        <div class="project-price">
                            <span class="current-price">¥{{ item.project?.current_price }}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `,
    data() { return { favorites: [], loading: false } },
    mounted() { this.loadFavorites() },
    methods: {
        async loadFavorites() {
            this.loading = true
            try {
                const res = await api.getFavorites({ page: 1, page_size: 50 })
                this.favorites = res.data?.items || []
            } catch (error) {} finally { this.loading = false }
        }
    }
}

// 优惠券组件
const CouponsView = {
    emits: ['go-back'],
    template: `
        <div class="coupons-view">
            <div class="page-header">
                <el-button @click="$emit('go-back')"><el-icon><arrow-left /></el-icon> 返回</el-button>
                <h2>我的优惠券</h2>
            </div>
            <el-tabs v-model="activeTab" @tab-change="loadCoupons">
                <el-tab-pane label="可用" name="available"></el-tab-pane>
                <el-tab-pane label="已使用" name="used"></el-tab-pane>
                <el-tab-pane label="已过期" name="expired"></el-tab-pane>
            </el-tabs>
            <div v-if="loading" class="loading-container"><el-icon class="is-loading" :size="40"><loading /></el-icon></div>
            <div v-else-if="coupons.length === 0" class="empty-state">
                <div class="empty-icon">🎫</div>
                <div class="empty-text">暂无优惠券</div>
            </div>
            <div v-else class="coupons-list">
                <div class="coupon-card" v-for="coupon in coupons" :key="coupon.id" :class="{ disabled: activeTab !== 'available' }">
                    <div class="coupon-left">
                        <div class="coupon-value">¥{{ coupon.discount_value }}</div>
                        <div class="coupon-condition">满{{ coupon.min_amount }}可用</div>
                    </div>
                    <div class="coupon-right">
                        <div class="coupon-name">{{ coupon.name }}</div>
                        <div class="coupon-time">有效期至 {{ coupon.end_time?.slice(0, 10) }}</div>
                    </div>
                </div>
            </div>
        </div>
    `,
    data() { return { activeTab: 'available', coupons: [], loading: false } },
    mounted() { this.loadCoupons() },
    methods: {
        async loadCoupons() {
            this.loading = true
            try {
                const res = await api.getCoupons({ status: this.activeTab, page: 1, page_size: 50 })
                this.coupons = res.data?.items || []
            } catch (error) {} finally { this.loading = false }
        }
    }
}

// 地址管理组件
const AddressView = {
    emits: ['go-back'],
    template: `
        <div class="address-view">
            <div class="page-header">
                <el-button @click="$emit('go-back')"><el-icon><arrow-left /></el-icon> 返回</el-button>
                <h2>地址管理</h2>
                <el-button type="primary" @click="showAddDialog">新增地址</el-button>
            </div>
            <div v-if="loading" class="loading-container"><el-icon class="is-loading" :size="40"><loading /></el-icon></div>
            <div v-else-if="addresses.length === 0" class="empty-state">
                <div class="empty-icon">📍</div>
                <div class="empty-text">暂无地址</div>
            </div>
            <div v-else class="address-list">
                <div class="address-card" v-for="addr in addresses" :key="addr.id">
                    <div class="address-info">
                        <div class="address-name">{{ addr.receiver_name }} <span>{{ addr.receiver_phone }}</span></div>
                        <div class="address-detail">{{ addr.province }}{{ addr.city }}{{ addr.district }}{{ addr.detail }}</div>
                        <el-tag v-if="addr.is_default" size="small" type="success">默认</el-tag>
                    </div>
                    <div class="address-actions">
                        <el-button size="small" @click="editAddress(addr)">编辑</el-button>
                        <el-button size="small" v-if="!addr.is_default" @click="setDefault(addr.id)">设为默认</el-button>
                        <el-button size="small" type="danger" @click="deleteAddress(addr.id)">删除</el-button>
                    </div>
                </div>
            </div>
            <el-dialog v-model="dialogVisible" :title="editingId ? '编辑地址' : '新增地址'" width="500px">
                <el-form :model="form" label-width="80px">
                    <el-form-item label="收货人"><el-input v-model="form.receiver_name" placeholder="请输入收货人姓名"></el-input></el-form-item>
                    <el-form-item label="手机号"><el-input v-model="form.receiver_phone" placeholder="请输入手机号"></el-input></el-form-item>
                    <el-form-item label="省份"><el-input v-model="form.province" placeholder="省份"></el-input></el-form-item>
                    <el-form-item label="城市"><el-input v-model="form.city" placeholder="城市"></el-input></el-form-item>
                    <el-form-item label="区县"><el-input v-model="form.district" placeholder="区县"></el-input></el-form-item>
                    <el-form-item label="详细地址"><el-input v-model="form.detail" type="textarea" placeholder="详细地址"></el-input></el-form-item>
                    <el-form-item label="默认地址"><el-switch v-model="form.is_default"></el-switch></el-form-item>
                </el-form>
                <template #footer>
                    <el-button @click="dialogVisible = false">取消</el-button>
                    <el-button type="primary" @click="saveAddress" :loading="saving">保存</el-button>
                </template>
            </el-dialog>
        </div>
    `,
    data() { return { addresses: [], loading: false, dialogVisible: false, editingId: null, saving: false, form: { receiver_name: '', receiver_phone: '', province: '', city: '', district: '', detail: '', is_default: false } } },
    mounted() { this.loadAddresses() },
    methods: {
        async loadAddresses() {
            this.loading = true
            try {
                const res = await api.getAddresses()
                this.addresses = res.data || []
            } catch (error) {} finally { this.loading = false }
        },
        showAddDialog() { this.editingId = null; this.form = { receiver_name: '', receiver_phone: '', province: '', city: '', district: '', detail: '', is_default: false }; this.dialogVisible = true },
        editAddress(addr) { this.editingId = addr.id; this.form = { ...addr }; this.dialogVisible = true },
        async saveAddress() {
            this.saving = true
            try {
                if (this.editingId) { await api.updateAddress(this.editingId, this.form) } else { await api.createAddress(this.form) }
                ElMessage.success('保存成功'); this.dialogVisible = false; this.loadAddresses()
            } catch (error) {} finally { this.saving = false }
        },
        async setDefault(id) { try { await api.setDefaultAddress(id); ElMessage.success('设置成功'); this.loadAddresses() } catch (error) {} },
        async deleteAddress(id) { try { await ElMessageBox.confirm('确定要删除吗？', '提示'); await api.deleteAddress(id); ElMessage.success('删除成功'); this.loadAddresses() } catch (error) {} }
    }
}

// 钱包组件
const WalletView = {
    emits: ['go-back'],
    template: `
        <div class="wallet-view">
            <div class="page-header">
                <el-button @click="$emit('go-back')"><el-icon><arrow-left /></el-icon> 返回</el-button>
                <h2>我的钱包</h2>
            </div>
            <div class="wallet-card">
                <div class="wallet-item"><div class="wallet-label">信用额度</div><div class="wallet-value">¥{{ balance.credit_limit || 0 }}</div></div>
                <div class="wallet-item"><div class="wallet-label">预付余额</div><div class="wallet-value">¥{{ balance.prepaid_balance || 0 }}</div></div>
            </div>
            <div class="recharge-section">
                <h3>快捷充值</h3>
                <div class="recharge-options">
                    <div class="recharge-item" v-for="amount in rechargeAmounts" :key="amount" :class="{ active: selectedAmount === amount }" @click="selectedAmount = amount">¥{{ amount }}</div>
                </div>
                <el-input v-model="customAmount" placeholder="或输入自定义金额" style="margin-top: 16px"><template #prepend>¥</template></el-input>
                <el-button type="primary" style="width: 100%; margin-top: 16px" :loading="recharging" @click="handleRecharge">立即充值</el-button>
            </div>
            <div class="records-section">
                <h3>充值记录</h3>
                <div v-if="records.length === 0" class="empty-state" style="padding: 40px"><div class="empty-icon">💰</div><div class="empty-text">暂无充值记录</div></div>
                <div v-else class="records-list">
                    <div class="record-item" v-for="record in records" :key="record.id">
                        <div class="record-info"><div class="record-amount">+¥{{ record.amount }}</div><div class="record-time">{{ record.created_at?.slice(0, 16).replace('T', ' ') }}</div></div>
                        <el-tag :type="record.status === 'completed' ? 'success' : 'warning'" size="small">{{ record.status === 'completed' ? '成功' : '处理中' }}</el-tag>
                    </div>
                </div>
            </div>
        </div>
    `,
    data() { return { balance: {}, rechargeAmounts: [100, 200, 500, 1000, 2000, 5000], selectedAmount: 100, customAmount: '', recharging: false, records: [] } },
    mounted() { this.loadBalance(); this.loadRecords() },
    methods: {
        async loadBalance() { try { const res = await api.getBalance(); this.balance = res.data } catch (error) {} },
        async loadRecords() { try { const res = await api.getRechargeRecords({ page: 1, page_size: 20 }); this.records = res.data?.items || [] } catch (error) {} },
        async handleRecharge() {
            const amount = this.customAmount ? parseFloat(this.customAmount) : this.selectedAmount
            if (!amount || amount <= 0) { ElMessage.error('请选择或输入充值金额'); return }
            this.recharging = true
            try { await api.createRecharge({ amount, pay_method: 'alipay' }); ElMessage.success('充值请求已提交'); this.loadRecords() } catch (error) {} finally { this.recharging = false }
        }
    }
}

// 积分商城组件
const PointsView = {
    emits: ['go-back'],
    template: `
        <div class="points-view">
            <div class="page-header">
                <el-button @click="$emit('go-back')"><el-icon><arrow-left /></el-icon> 返回</el-button>
                <h2>积分商城</h2>
            </div>
            <div class="points-balance"><span class="points-value">{{ userInfo.points_balance || 0 }}</span><span class="points-label">可用积分</span></div>
            <h3>积分商品</h3>
            <div v-if="loading" class="loading-container"><el-icon class="is-loading" :size="40"><loading /></el-icon></div>
            <div v-else-if="goods.length === 0" class="empty-state"><div class="empty-icon">🎁</div><div class="empty-text">暂无积分商品</div></div>
            <div v-else class="goods-grid">
                <div class="goods-card" v-for="item in goods" :key="item.id">
                    <img :src="item.image || 'https://via.placeholder.com/200'" class="goods-image" alt="">
                    <div class="goods-info">
                        <div class="goods-name">{{ item.name }}</div>
                        <div class="goods-points">{{ item.points_cost }}积分</div>
                        <el-button type="primary" size="small" @click="exchange(item)" :disabled="(userInfo.points_balance || 0) < item.points_cost">兑换</el-button>
                    </div>
                </div>
            </div>
        </div>
    `,
    data() { return { userInfo: JSON.parse(localStorage.getItem('userInfo') || '{}'), goods: [], loading: false } },
    mounted() { this.loadGoods() },
    methods: {
        async loadGoods() { this.loading = true; try { const res = await api.getPointsGoods({ page: 1, page_size: 50 }); this.goods = res.data?.items || [] } catch (error) {} finally { this.loading = false } },
        async exchange(item) {
            try { 
                await ElMessageBox.confirm('确定使用 ' + item.points_cost + ' 积分兑换 ' + item.name + ' 吗？', '积分兑换')
                await api.exchangePoints({ goods_id: item.id })
                ElMessage.success('兑换成功')
                const res = await api.getUserInfo()
                this.userInfo = res.data
                localStorage.setItem('userInfo', JSON.stringify(res.data)) 
            } catch (error) {}
        }
    }
}

// 发票管理组件
const InvoiceView = {
    emits: ['go-back'],
    template: `
        <div class="invoice-view">
            <div class="page-header">
                <el-button @click="$emit('go-back')"><el-icon><arrow-left /></el-icon> 返回</el-button>
                <h2>发票管理</h2>
            </div>
            <div v-if="loading" class="loading-container"><el-icon class="is-loading" :size="40"><loading /></el-icon></div>
            <div v-else-if="invoices.length === 0" class="empty-state"><div class="empty-icon">📄</div><div class="empty-text">暂无发票记录</div></div>
            <div v-else class="invoice-list">
                <div class="invoice-card" v-for="invoice in invoices" :key="invoice.id">
                    <div class="invoice-info">
                        <div class="invoice-title">{{ invoice.title }}</div>
                        <div class="invoice-amount">¥{{ invoice.amount }}</div>
                        <div class="invoice-time">{{ invoice.created_at?.slice(0, 10) }}</div>
                    </div>
                    <el-tag :type="getStatusType(invoice.status)">{{ getStatusText(invoice.status) }}</el-tag>
                </div>
            </div>
        </div>
    `,
    data() { return { invoices: [], loading: false } },
    mounted() { this.loadInvoices() },
    methods: {
        async loadInvoices() { this.loading = true; try { const res = await api.getInvoices({ page: 1, page_size: 50 }); this.invoices = res.data?.items || [] } catch (error) {} finally { this.loading = false } },
        getStatusText(status) { const map = { pending: '待审核', approved: '已通过', rejected: '已拒绝', issued: '已开票' }; return map[status] || status },
        getStatusType(status) { const map = { pending: 'warning', approved: 'success', rejected: 'danger', issued: 'primary' }; return map[status] || 'info' }
    }
}

// 团队邀请组件
const TeamView = {
    emits: ['go-back'],
    template: `
        <div class="team-view">
            <div class="page-header">
                <el-button @click="$emit('go-back')"><el-icon><arrow-left /></el-icon> 返回</el-button>
                <h2>团队邀请</h2>
            </div>
            <div class="invite-stats">
                <div class="stat-item"><div class="stat-value">{{ stats.total_invites || 0 }}</div><div class="stat-label">邀请人数</div></div>
                <div class="stat-item"><div class="stat-value">¥{{ stats.total_commission || 0 }}</div><div class="stat-label">累计佣金</div></div>
                <div class="stat-item"><div class="stat-value">¥{{ stats.available_commission || 0 }}</div><div class="stat-label">可提现</div></div>
            </div>
            <div class="invite-code-section">
                <h3>我的邀请码</h3>
                <div class="invite-code">{{ group?.invite_code || '暂无' }}</div>
                <el-button type="primary" v-if="!group" @click="createGroup">创建团队</el-button>
                <el-button type="primary" v-else @click="copyInviteCode">复制邀请码</el-button>
            </div>
            <div class="withdraw-section">
                <h3>佣金提现</h3>
                <el-input v-model="withdrawAmount" placeholder="输入提现金额"><template #prepend>¥</template></el-input>
                <el-button type="success" style="margin-top: 12px" @click="applyWithdraw" :disabled="!withdrawAmount || parseFloat(withdrawAmount) <= 0">申请提现</el-button>
            </div>
            <h3>邀请记录</h3>
            <div v-if="records.length === 0" class="empty-state" style="padding: 40px"><div class="empty-icon">👥</div><div class="empty-text">暂无邀请记录</div></div>
            <div v-else class="records-list">
                <div class="record-item" v-for="record in records" :key="record.id">
                    <div class="record-info"><div class="record-user">{{ record.invitee_nickname || '用户' }}</div><div class="record-time">{{ record.created_at?.slice(0, 10) }}</div></div>
                    <div class="record-commission">+¥{{ record.commission || 0 }}</div>
                </div>
            </div>
        </div>
    `,
    data() { return { group: null, stats: {}, records: [], withdrawAmount: '' } },
    mounted() { this.loadData() },
    methods: {
        async loadData() {
            try { const [groupRes, statsRes, recordsRes] = await Promise.all([api.getMyGroup(), api.getInviteStats(), api.getInviteRecords({ page: 1, page_size: 50 })]); this.group = groupRes.data; this.stats = statsRes.data; this.records = recordsRes.data?.items || [] } catch (error) {}
        },
        async createGroup() { try { await api.createGroup({ name: '我的团队' }); ElMessage.success('团队创建成功'); this.loadData() } catch (error) {} },
        copyInviteCode() { navigator.clipboard.writeText(this.group?.invite_code); ElMessage.success('邀请码已复制') },
        async applyWithdraw() { try { await api.applyWithdraw({ amount: parseFloat(this.withdrawAmount) }); ElMessage.success('提现申请已提交'); this.withdrawAmount = ''; this.loadData() } catch (error) {} }
    }
}

// 帮助中心组件
const HelpView = {
    emits: ['go-back'],
    template: `
        <div class="help-view">
            <div class="page-header">
                <el-button @click="$emit('go-back')"><el-icon><arrow-left /></el-icon> 返回</el-button>
                <h2>帮助中心</h2>
                <el-input v-model="searchKeyword" placeholder="搜索问题" style="width: 300px" @change="searchArticles">
                    <template #prefix><el-icon><search /></el-icon></template>
                </el-input>
            </div>
            <div class="help-content">
                <div class="help-sidebar">
                    <h3>常见问题分类</h3>
                    <el-menu :default-active="activeCategory" @select="selectCategory">
                        <el-menu-item v-for="cat in categories" :key="cat.id" :index="String(cat.id)">
                            <span>{{ cat.icon }} {{ cat.name }}</span>
                        </el-menu-item>
                    </el-menu>
                </div>
                <div class="help-main">
                    <div v-if="loading" class="loading-container"><el-icon class="is-loading" :size="40"><loading /></el-icon></div>
                    <div v-else-if="articles.length === 0" class="empty-state"><div class="empty-icon">📚</div><div class="empty-text">暂无相关文章</div></div>
                    <div v-else class="help-articles">
                        <el-collapse v-model="expandedArticles">
                            <el-collapse-item v-for="article in articles" :key="article.id" :name="article.id" :title="article.title">
                                <div class="article-content" v-html="article.content"></div>
                            </el-collapse-item>
                        </el-collapse>
                    </div>
                </div>
            </div>
        </div>
    `,
    data() {
        return {
            searchKeyword: '',
            activeCategory: '1',
            categories: [
                { id: 1, name: '新手指南', icon: '📖' },
                { id: 2, name: '下单流程', icon: '🛒' },
                { id: 3, name: '支付问题', icon: '💳' },
                { id: 4, name: '样品寄送', icon: '📦' },
                { id: 5, name: '报告获取', icon: '📊' },
                { id: 6, name: '发票问题', icon: '🧾' },
                { id: 7, name: '账户相关', icon: '👤' }
            ],
            articles: [],
            expandedArticles: [],
            loading: false
        }
    },
    mounted() { this.loadArticles() },
    methods: {
        async loadArticles() {
            this.loading = true
            try {
                const res = await api.getHelpArticles({ category_id: this.activeCategory })
                this.articles = res.data?.items || []
            } catch (error) {
                // 使用默认数据
                this.articles = [
                    { id: 1, title: '如何注册账号？', content: '<p>1. 点击首页右上角"登录"按钮</p><p>2. 输入手机号获取验证码</p><p>3. 输入验证码完成登录/注册</p>' },
                    { id: 2, title: '如何下单？', content: '<p>1. 浏览检测项目，选择需要的检测服务</p><p>2. 点击"立即预约"填写样品信息</p><p>3. 确认订单并支付</p><p>4. 按照指引寄送样品</p>' },
                    { id: 3, title: '支持哪些支付方式？', content: '<p>目前支持：</p><ul><li>微信支付</li><li>支付宝支付</li><li>账户余额支付</li></ul>' },
                    { id: 4, title: '如何查看检测报告？', content: '<p>1. 登录账号进入"我的订单"</p><p>2. 找到已完成的订单</p><p>3. 点击"下载报告"即可获取检测报告</p>' }
                ]
            } finally { this.loading = false }
        },
        selectCategory(index) {
            this.activeCategory = index
            this.loadArticles()
        },
        searchArticles() {
            this.loadArticles()
        }
    }
}

// 在线客服组件
const ChatView = {
    emits: ['go-back'],
    template: `
        <div class="chat-view">
            <div class="page-header">
                <el-button @click="$emit('go-back')"><el-icon><arrow-left /></el-icon> 返回</el-button>
                <h2>在线客服</h2>
                <el-tag type="success">在线</el-tag>
            </div>
            <div class="chat-container">
                <div class="chat-messages" ref="chatMessages">
                    <div v-for="msg in messages" :key="msg.id" :class="['message', msg.is_user ? 'user' : 'service']">
                        <div class="message-avatar">
                            <el-avatar :size="36">{{ msg.is_user ? '我' : '客' }}</el-avatar>
                        </div>
                        <div class="message-content">
                            <div class="message-text">{{ msg.content }}</div>
                            <div class="message-time">{{ msg.created_at }}</div>
                        </div>
                    </div>
                </div>
                <div class="chat-quick-replies">
                    <span class="quick-label">快捷问题：</span>
                    <el-tag v-for="q in quickQuestions" :key="q" @click="sendQuickQuestion(q)" class="quick-tag" effect="plain">{{ q }}</el-tag>
                </div>
                <div class="chat-input">
                    <el-input v-model="inputMessage" placeholder="输入您的问题..." @keyup.enter="sendMessage">
                        <template #append>
                            <el-button type="primary" @click="sendMessage" :loading="sending">发送</el-button>
                        </template>
                    </el-input>
                </div>
            </div>
        </div>
    `,
    data() {
        return {
            messages: [
                { id: 1, content: '您好！欢迎咨询科研检测服务平台，请问有什么可以帮助您的？', is_user: false, created_at: '刚刚' }
            ],
            inputMessage: '',
            sending: false,
            quickQuestions: ['如何下单？', '检测周期多久？', '如何获取报告？', '发票问题']
        }
    },
    mounted() { this.loadHistory() },
    methods: {
        async loadHistory() {
            try {
                const res = await api.getChatHistory()
                if (res.data?.length) this.messages = res.data
            } catch (error) {}
        },
        async sendMessage() {
            if (!this.inputMessage.trim()) return
            const content = this.inputMessage
            this.messages.push({ id: Date.now(), content, is_user: true, created_at: '刚刚' })
            this.inputMessage = ''
            this.sending = true
            this.scrollToBottom()
            try {
                const res = await api.sendMessage({ content })
                setTimeout(() => {
                    this.messages.push({ id: Date.now() + 1, content: res.data?.reply || '感谢您的咨询，客服正在为您处理，请稍候...', is_user: false, created_at: '刚刚' })
                    this.scrollToBottom()
                }, 500)
            } catch (error) {
                this.messages.push({ id: Date.now() + 1, content: '感谢您的咨询，我们会尽快为您处理。工作时间：9:00-18:00', is_user: false, created_at: '刚刚' })
                this.scrollToBottom()
            } finally { this.sending = false }
        },
        sendQuickQuestion(q) { this.inputMessage = q; this.sendMessage() },
        scrollToBottom() { this.$nextTick(() => { if (this.$refs.chatMessages) this.$refs.chatMessages.scrollTop = this.$refs.chatMessages.scrollHeight }) }
    }
}

// 抽奖活动组件
const LotteryView = {
    emits: ['go-back'],
    template: `
        <div class="lottery-view">
            <div class="page-header">
                <el-button @click="$emit('go-back')"><el-icon><arrow-left /></el-icon> 返回</el-button>
                <h2>🎁 幸运抽奖</h2>
            </div>
            <div class="lottery-main">
                <div class="lottery-wheel">
                    <div class="wheel-container" :style="{ transform: 'rotate(' + rotation + 'deg)' }">
                        <div class="wheel-item" v-for="(prize, index) in prizes" :key="index" :style="getItemStyle(index)">
                            <span class="prize-name">{{ prize.name }}</span>
                        </div>
                    </div>
                    <div class="wheel-center" @click="startLottery" :class="{ disabled: spinning || chances <= 0 }">
                        <span>{{ spinning ? '抽奖中' : '开始' }}</span>
                    </div>
                </div>
                <div class="lottery-info">
                    <div class="chances-info">
                        <span>剩余抽奖次数：</span>
                        <span class="chances-value">{{ chances }}</span>
                    </div>
                    <p class="lottery-tip">下单满100元可获得1次抽奖机会</p>
                </div>
            </div>
            <div class="lottery-prizes">
                <h3>奖品列表</h3>
                <div class="prizes-grid">
                    <div class="prize-card" v-for="prize in prizes" :key="prize.id">
                        <div class="prize-icon">{{ prize.icon }}</div>
                        <div class="prize-name">{{ prize.name }}</div>
                    </div>
                </div>
            </div>
            <div class="lottery-records">
                <h3>中奖记录</h3>
                <div v-if="records.length === 0" class="empty-state" style="padding: 40px"><div class="empty-icon">🎯</div><div class="empty-text">暂无中奖记录</div></div>
                <div v-else class="records-list">
                    <div class="record-item" v-for="record in records" :key="record.id">
                        <div class="record-info"><div class="record-prize">{{ record.prize_name }}</div><div class="record-time">{{ record.created_at?.slice(0, 10) }}</div></div>
                        <el-tag :type="record.claimed ? 'success' : 'warning'" size="small">{{ record.claimed ? '已领取' : '待领取' }}</el-tag>
                    </div>
                </div>
            </div>
        </div>
    `,
    data() {
        return {
            chances: 3,
            spinning: false,
            rotation: 0,
            prizes: [
                { id: 1, name: '10元优惠券', icon: '🎫' },
                { id: 2, name: '50积分', icon: '⭐' },
                { id: 3, name: '谢谢参与', icon: '😊' },
                { id: 4, name: '20元优惠券', icon: '🎟️' },
                { id: 5, name: '100积分', icon: '🌟' },
                { id: 6, name: '免单机会', icon: '🎁' },
                { id: 7, name: '5元红包', icon: '🧧' },
                { id: 8, name: '实物礼品', icon: '📦' }
            ],
            records: []
        }
    },
    mounted() { this.loadData() },
    methods: {
        async loadData() {
            try {
                const [infoRes, recordsRes] = await Promise.all([api.getLotteryInfo(), api.getLotteryRecords({ page: 1, page_size: 20 })])
                this.chances = infoRes.data?.chances || 0
                this.records = recordsRes.data?.items || []
            } catch (error) {}
        },
        getItemStyle(index) {
            const angle = (360 / this.prizes.length) * index
            return { transform: `rotate(${angle}deg)`, background: index % 2 ? '#fff7e6' : '#e6f7ff' }
        },
        async startLottery() {
            if (this.spinning || this.chances <= 0) return
            this.spinning = true
            const prizeIndex = Math.floor(Math.random() * this.prizes.length)
            const extraRotation = 360 * 5 + (360 / this.prizes.length) * prizeIndex
            this.rotation += extraRotation
            try { await api.doLottery() } catch (error) {}
            setTimeout(() => {
                this.spinning = false
                this.chances--
                ElMessage.success('恭喜获得：' + this.prizes[prizeIndex].name)
                this.loadData()
            }, 4000)
        }
    }
}

// 报告下载组件
const ReportsView = {
    emits: ['go-back', 'go-sample-track'],
    template: `
        <div class="reports-view">
            <div class="page-header">
                <el-button @click="$emit('go-back')"><el-icon><arrow-left /></el-icon> 返回</el-button>
                <h2>报告下载</h2>
            </div>
            <div v-if="loading" class="loading-container"><el-icon class="is-loading" :size="40"><loading /></el-icon></div>
            <div v-else-if="reports.length === 0" class="empty-state">
                <div class="empty-icon">📊</div>
                <div class="empty-text">暂无可下载的报告</div>
                <p style="color: #8c8c8c; margin-top: 12px">完成检测后，报告将在此处显示</p>
            </div>
            <div v-else class="reports-list">
                <div class="report-card" v-for="report in reports" :key="report.id">
                    <div class="report-icon">📄</div>
                    <div class="report-info">
                        <div class="report-name">{{ report.project_name }}</div>
                        <div class="report-order">订单号：{{ report.order_no }}</div>
                        <div class="report-time">完成时间：{{ report.completed_at?.slice(0, 10) }}</div>
                    </div>
                    <div class="report-actions">
                        <el-button type="primary" size="small" @click="downloadReport(report)">
                            <el-icon><download /></el-icon> 下载报告
                        </el-button>
                        <el-button size="small" @click="$emit('go-sample-track', report.order_id)">
                            <el-icon><location /></el-icon> 样品追踪
                        </el-button>
                    </div>
                </div>
            </div>
        </div>
    `,
    data() { return { reports: [], loading: false } },
    mounted() { this.loadReports() },
    methods: {
        async loadReports() {
            this.loading = true
            try {
                const res = await api.getReports({ page: 1, page_size: 50 })
                this.reports = res.data?.items || []
            } catch (error) {
                // 使用演示数据
                this.reports = []
            } finally { this.loading = false }
        },
        async downloadReport(report) {
            try {
                ElMessage.info('正在准备下载...')
                const res = await api.downloadReport(report.order_id)
                const url = window.URL.createObjectURL(new Blob([res]))
                const link = document.createElement('a')
                link.href = url
                link.download = `检测报告_${report.order_no}.pdf`
                link.click()
                window.URL.revokeObjectURL(url)
            } catch (error) {
                ElMessage.warning('报告正在生成中，请稍后再试')
            }
        }
    }
}

// 样品追踪组件
const SampleTrackView = {
    props: ['orderId'],
    emits: ['go-back'],
    template: `
        <div class="sample-track-view">
            <div class="page-header">
                <el-button @click="$emit('go-back')"><el-icon><arrow-left /></el-icon> 返回</el-button>
                <h2>样品追踪</h2>
            </div>
            <div class="track-info" v-if="orderInfo">
                <div class="order-brief">
                    <div class="brief-item"><span class="label">订单号：</span><span>{{ orderInfo.order_no }}</span></div>
                    <div class="brief-item"><span class="label">样品名称：</span><span>{{ orderInfo.sample_name }}</span></div>
                    <div class="brief-item"><span class="label">检测项目：</span><span>{{ orderInfo.project_name }}</span></div>
                </div>
            </div>
            <div class="track-timeline">
                <h3>物流状态</h3>
                <el-timeline>
                    <el-timeline-item v-for="step in trackSteps" :key="step.id" :timestamp="step.time" :type="step.active ? 'primary' : ''" :hollow="!step.active">
                        <div class="timeline-content">
                            <div class="timeline-title">{{ step.title }}</div>
                            <div class="timeline-desc">{{ step.description }}</div>
                        </div>
                    </el-timeline-item>
                </el-timeline>
            </div>
            <div class="track-express" v-if="expressInfo">
                <h3>快递信息</h3>
                <div class="express-card">
                    <div class="express-item"><span class="label">快递公司：</span><span>{{ expressInfo.company }}</span></div>
                    <div class="express-item"><span class="label">快递单号：</span><span>{{ expressInfo.tracking_no }}</span></div>
                </div>
            </div>
        </div>
    `,
    data() {
        return {
            orderInfo: null,
            expressInfo: null,
            trackSteps: [
                { id: 1, title: '订单创建', description: '订单已创建，等待支付', time: '2025-12-01 10:00', active: true },
                { id: 2, title: '已支付', description: '订单支付成功', time: '2025-12-01 10:30', active: true },
                { id: 3, title: '样品已寄出', description: '用户已寄出样品', time: '2025-12-02 09:00', active: true },
                { id: 4, title: '样品已签收', description: '实验室已签收样品', time: '2025-12-03 14:00', active: true },
                { id: 5, title: '检测中', description: '样品正在检测中', time: '2025-12-04 09:00', active: false },
                { id: 6, title: '检测完成', description: '检测完成，报告已生成', time: '', active: false }
            ]
        }
    },
    mounted() { this.loadTrackInfo() },
    methods: {
        async loadTrackInfo() {
            if (!this.orderId) return
            try {
                const res = await api.getSampleStatus(this.orderId)
                this.orderInfo = res.data?.order
                this.expressInfo = res.data?.express
                if (res.data?.steps) this.trackSteps = res.data.steps
            } catch (error) {
                // 使用演示数据
                this.orderInfo = { order_no: 'ORD2025120100001', sample_name: 'XRD测试样品', project_name: 'X射线衍射分析' }
                this.expressInfo = { company: '顺丰速运', tracking_no: 'SF1234567890' }
            }
        }
    }
}

// 公告列表组件
const AnnouncementsView = {
    emits: ['go-back'],
    template: `
        <div class="announcements-view">
            <div class="page-header">
                <el-button @click="$emit('go-back')"><el-icon><arrow-left /></el-icon> 返回</el-button>
                <h2>系统公告</h2>
            </div>
            <div v-if="loading" class="loading-container"><el-icon class="is-loading" :size="40"><loading /></el-icon></div>
            <div v-else-if="announcements.length === 0" class="empty-state"><div class="empty-icon">📢</div><div class="empty-text">暂无公告</div></div>
            <div v-else class="announcements-list">
                <div class="announcement-card" v-for="ann in announcements" :key="ann.id" @click="showDetail(ann)">
                    <div class="ann-header">
                        <el-tag v-if="ann.is_important" type="danger" size="small">重要</el-tag>
                        <span class="ann-title">{{ ann.title }}</span>
                    </div>
                    <div class="ann-summary">{{ ann.summary || ann.content?.slice(0, 100) }}</div>
                    <div class="ann-footer">
                        <span class="ann-time">{{ ann.created_at?.slice(0, 10) }}</span>
                        <span class="ann-views">{{ ann.views || 0 }} 次阅读</span>
                    </div>
                </div>
            </div>
        </div>
    `,
    data() { return { announcements: [], loading: false } },
    mounted() { this.loadAnnouncements() },
    methods: {
        async loadAnnouncements() {
            this.loading = true
            try {
                const res = await api.getAnnouncements({ page: 1, page_size: 50 })
                this.announcements = res.data?.items || []
            } catch (error) {
                this.announcements = [
                    { id: 1, title: '平台服务升级通知', content: '为提供更好的服务体验，我们将于12月10日进行系统升级...', is_important: true, created_at: '2025-12-01', views: 1256 },
                    { id: 2, title: '12月优惠活动公告', content: '金秋检测季，多项热门检测项目6折起...', is_important: false, created_at: '2025-12-01', views: 892 },
                    { id: 3, title: '新增检测项目上线', content: '新增材料表征、生物科学等多个检测类目...', is_important: false, created_at: '2025-11-28', views: 645 }
                ]
            } finally { this.loading = false }
        },
        showDetail(ann) {
            ElMessageBox.alert(ann.content, ann.title, { confirmButtonText: '我知道了', dangerouslyUseHTMLString: true })
        }
    }
}

// 合同管理组件
const ContractsView = {
    emits: ['go-back'],
    template: `
        <div class="contracts-view">
            <div class="page-header">
                <el-button @click="$emit('go-back')"><el-icon><arrow-left /></el-icon> 返回</el-button>
                <h2>合同管理</h2>
            </div>
            <div class="contracts-tabs">
                <el-radio-group v-model="activeTab" @change="loadContracts">
                    <el-radio-button value="all">全部合同</el-radio-button>
                    <el-radio-button value="active">生效中</el-radio-button>
                    <el-radio-button value="expired">已过期</el-radio-button>
                </el-radio-group>
            </div>
            <div v-if="loading" class="loading-container"><el-icon class="is-loading" :size="40"><loading /></el-icon></div>
            <div v-else-if="contracts.length === 0" class="empty-state">
                <div class="empty-icon">📋</div>
                <div class="empty-text">暂无合同</div>
                <p style="color: #8c8c8c; margin-top: 12px">下单后系统将自动生成服务合同</p>
            </div>
            <div v-else class="contracts-list">
                <div class="contract-card" v-for="contract in contracts" :key="contract.id">
                    <div class="contract-header">
                        <div class="contract-icon">📄</div>
                        <div class="contract-title">
                            <div class="title-text">{{ contract.title }}</div>
                            <div class="contract-no">合同编号：{{ contract.contract_no }}</div>
                        </div>
                        <el-tag :type="contract.status === 'active' ? 'success' : 'info'" size="small">
                            {{ contract.status === 'active' ? '生效中' : '已过期' }}
                        </el-tag>
                    </div>
                    <div class="contract-info">
                        <div class="info-row">
                            <span class="label">签订日期：</span>
                            <span class="value">{{ contract.signed_at }}</span>
                        </div>
                        <div class="info-row">
                            <span class="label">有效期至：</span>
                            <span class="value">{{ contract.expired_at }}</span>
                        </div>
                        <div class="info-row">
                            <span class="label">关联订单：</span>
                            <span class="value">{{ contract.order_no }}</span>
                        </div>
                    </div>
                    <div class="contract-actions">
                        <el-button size="small" @click="viewContract(contract)">
                            <el-icon><view /></el-icon> 查看合同
                        </el-button>
                        <el-button size="small" @click="downloadContract(contract)">
                            <el-icon><download /></el-icon> 下载PDF
                        </el-button>
                    </div>
                </div>
            </div>
        </div>
    `,
    data() {
        return {
            activeTab: 'all',
            contracts: [],
            loading: false
        }
    },
    mounted() { this.loadContracts() },
    methods: {
        async loadContracts() {
            this.loading = true
            try {
                // 实际API调用
                // const res = await api.getContracts({ status: this.activeTab })
                // this.contracts = res.data?.items || []
                
                // 演示数据
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
                    }
                ]
                
                if (this.activeTab !== 'all') {
                    this.contracts = this.contracts.filter(c => c.status === this.activeTab)
                }
            } catch (error) {
                console.error('加载合同失败', error)
            } finally {
                this.loading = false
            }
        },
        viewContract(contract) {
            ElMessageBox.alert(
                \`<div style="line-height: 2">
                    <p><strong>合同编号：</strong>\${contract.contract_no}</p>
                    <p><strong>合同名称：</strong>\${contract.title}</p>
                    <p><strong>关联订单：</strong>\${contract.order_no}</p>
                    <p><strong>签订日期：</strong>\${contract.signed_at}</p>
                    <p><strong>有效期至：</strong>\${contract.expired_at}</p>
                    <hr style="margin: 16px 0; border-color: #f0f0f0">
                    <p style="color: #8c8c8c">甲方：科研检测服务平台</p>
                    <p style="color: #8c8c8c">乙方：用户</p>
                    <p style="margin-top: 12px">根据《中华人民共和国合同法》及相关法律法规，甲乙双方本着平等互利的原则，就检测服务事宜达成如下协议...</p>
                </div>\`,
                '合同详情',
                { confirmButtonText: '关闭', dangerouslyUseHTMLString: true, customStyle: { width: '600px' } }
            )
        },
        downloadContract(contract) {
            ElMessage.info('正在准备下载合同PDF...')
            // 实际下载逻辑
            setTimeout(() => {
                ElMessage.success('合同下载成功')
            }, 1500)
        }
    }
}

// 加盟合作组件
const FranchiseView = {
    emits: ['go-back'],
    template: `
        <div class="franchise-view">
            <div class="page-header">
                <el-button @click="$emit('go-back')"><el-icon><arrow-left /></el-icon> 返回</el-button>
                <h2>加盟合作</h2>
            </div>
            
            <!-- 加盟Banner -->
            <div class="franchise-banner">
                <div class="banner-content">
                    <h1>🤝 成为合作伙伴</h1>
                    <p>携手共赢，共创科研检测服务新未来</p>
                </div>
            </div>
            
            <!-- 加盟优势 -->
            <div class="franchise-section">
                <h3 class="section-title">加盟优势</h3>
                <div class="advantages-grid">
                    <div class="advantage-item">
                        <div class="adv-icon">💰</div>
                        <div class="adv-title">高额返佣</div>
                        <div class="adv-desc">订单返佣最高可达20%</div>
                    </div>
                    <div class="advantage-item">
                        <div class="adv-icon">🎯</div>
                        <div class="adv-title">专属支持</div>
                        <div class="adv-desc">一对一运营指导服务</div>
                    </div>
                    <div class="advantage-item">
                        <div class="adv-icon">📊</div>
                        <div class="adv-title">资源共享</div>
                        <div class="adv-desc">共享平台客户资源</div>
                    </div>
                    <div class="advantage-item">
                        <div class="adv-icon">🚀</div>
                        <div class="adv-title">快速结算</div>
                        <div class="adv-desc">T+7工作日结算佣金</div>
                    </div>
                </div>
            </div>
            
            <!-- 合作模式 -->
            <div class="franchise-section">
                <h3 class="section-title">合作模式</h3>
                <el-radio-group v-model="selectedMode" class="mode-group">
                    <el-radio-button value="agent">
                        <div class="mode-content">
                            <span class="mode-icon">🏢</span>
                            <span class="mode-name">区域代理</span>
                        </div>
                    </el-radio-button>
                    <el-radio-button value="partner">
                        <div class="mode-content">
                            <span class="mode-icon">🤝</span>
                            <span class="mode-name">项目合作</span>
                        </div>
                    </el-radio-button>
                    <el-radio-button value="lab">
                        <div class="mode-content">
                            <span class="mode-icon">🔬</span>
                            <span class="mode-name">实验室入驻</span>
                        </div>
                    </el-radio-button>
                </el-radio-group>
                <div class="mode-desc-card">
                    <p v-if="selectedMode === 'agent'">获得指定区域独家代理权，享受区域内所有订单的返佣，适合有渠道资源的合作伙伴。</p>
                    <p v-if="selectedMode === 'partner'">针对特定项目进行深度合作，按项目结算佣金，灵活高效。</p>
                    <p v-if="selectedMode === 'lab'">实验室直接入驻平台，承接检测订单获取收益，共享平台流量。</p>
                </div>
            </div>
            
            <!-- 申请表单 -->
            <div class="franchise-section">
                <h3 class="section-title">提交申请</h3>
                <el-form :model="form" :rules="rules" ref="formRef" label-position="top" class="franchise-form">
                    <el-row :gutter="24">
                        <el-col :span="12">
                            <el-form-item label="联系人姓名" prop="name">
                                <el-input v-model="form.name" placeholder="请输入您的姓名" />
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="联系电话" prop="phone">
                                <el-input v-model="form.phone" placeholder="请输入手机号" maxlength="11" />
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row :gutter="24">
                        <el-col :span="12">
                            <el-form-item label="公司/机构名称" prop="company">
                                <el-input v-model="form.company" placeholder="请输入公司或机构名称" />
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="所在城市" prop="city">
                                <el-input v-model="form.city" placeholder="请输入所在城市" />
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-form-item label="合作意向">
                        <el-input type="textarea" v-model="form.intention" :rows="4" placeholder="请简述您的合作意向和优势资源（可选）" maxlength="500" show-word-limit />
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" size="large" @click="submitApplication" :loading="submitting" style="width: 200px">
                            提交申请
                        </el-button>
                        <span style="margin-left: 16px; color: #8c8c8c; font-size: 14px">提交后我们将在3个工作日内与您联系</span>
                    </el-form-item>
                </el-form>
            </div>
            
            <!-- 联系方式 -->
            <div class="franchise-section contact-section">
                <h3 class="section-title">其他联系方式</h3>
                <div class="contact-grid">
                    <div class="contact-item">
                        <div class="contact-icon">📞</div>
                        <div class="contact-label">商务热线</div>
                        <div class="contact-value">400-123-4567</div>
                    </div>
                    <div class="contact-item">
                        <div class="contact-icon">📧</div>
                        <div class="contact-label">商务邮箱</div>
                        <div class="contact-value">business@keyanbaice.com</div>
                    </div>
                    <div class="contact-item">
                        <div class="contact-icon">💬</div>
                        <div class="contact-label">微信客服</div>
                        <div class="contact-value">keyanbaice_service</div>
                    </div>
                </div>
            </div>
        </div>
    `,
    data() {
        return {
            selectedMode: 'agent',
            submitting: false,
            form: {
                name: '',
                phone: '',
                company: '',
                city: '',
                intention: ''
            },
            rules: {
                name: [{ required: true, message: '请输入联系人姓名', trigger: 'blur' }],
                phone: [
                    { required: true, message: '请输入联系电话', trigger: 'blur' },
                    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
                ],
                company: [{ required: true, message: '请输入公司/机构名称', trigger: 'blur' }],
                city: [{ required: true, message: '请输入所在城市', trigger: 'blur' }]
            }
        }
    },
    methods: {
        async submitApplication() {
            try {
                await this.$refs.formRef.validate()
                this.submitting = true
                
                // 实际API调用
                // await api.submitFranchise({ ...this.form, mode: this.selectedMode })
                
                // 模拟提交
                await new Promise(resolve => setTimeout(resolve, 1500))
                
                ElMessageBox.alert(
                    '感谢您的申请！我们将在3个工作日内与您联系，请保持电话畅通。',
                    '提交成功',
                    { type: 'success', confirmButtonText: '我知道了' }
                )
                
                // 重置表单
                this.form = { name: '', phone: '', company: '', city: '', intention: '' }
            } catch (error) {
                if (error !== false) { // 非表单验证错误
                    ElMessage.error('提交失败，请稍后重试')
                }
            } finally {
                this.submitting = false
            }
        }
    }
}

// ==================== 主应用 ====================
createApp({
    components: {
        HomeView,
        ProjectsView,
        ProjectDetail,
        OrdersView,
        ProfileView,
        AboutView,
        FavoritesView,
        CouponsView,
        AddressView,
        WalletView,
        PointsView,
        InvoiceView,
        TeamView,
        HelpView,
        ChatView,
        LotteryView,
        ReportsView,
        SampleTrackView,
        AnnouncementsView,
        ContractsView,
        FranchiseView
    },
    data() {
        return {
            currentView: 'home',
            currentProjectId: null,
            currentOrderId: null,
            isMobile: false,
            isLogin: false,
            userInfo: {},
            showLogin: false,
            loginForm: { phone: '', sms_code: '' },
            countdown: 0,
            loginLoading: false,
            showMobileMenu: false,
            // 预约下单
            showBooking: false,
            bookingProject: null,
            bookingForm: { sample_name: '', quantity: 1, remark: '', address_id: null, coupon_id: null },
            addresses: [],
            availableCoupons: [],
            bookingLoading: false,
            // 支付
            showPayment: false,
            paymentOrder: null,
            payMethod: 'balance',
            paymentLoading: false,
            balance: {},
            // 评价
            showReview: false,
            reviewOrder: null,
            reviewForm: { rating: 5, content: '' },
            reviewLoading: false,
            // 发票
            showInvoice: false,
            invoiceOrder: null,
            invoiceForm: { invoice_type: 'personal', title: '', tax_id: '', email: '' },
            invoiceLoading: false,
            // 编辑资料
            showEditProfile: false,
            profileForm: { nickname: '', avatar: '' },
            profileLoading: false
        }
    },
    computed: {
        orderTotalAmount() {
            if (!this.bookingProject) return 0
            let total = this.bookingProject.current_price * this.bookingForm.quantity
            if (this.bookingForm.coupon_id) {
                const coupon = this.availableCoupons.find(c => c.id === this.bookingForm.coupon_id)
                if (coupon) total -= coupon.discount_value
            }
            return Math.max(0, total).toFixed(2)
        }
    },
    mounted() {
        this.checkDevice()
        window.addEventListener('resize', this.checkDevice)
        this.checkLogin()
    },
    methods: {
        checkDevice() { this.isMobile = window.innerWidth < 768 },
        checkLogin() {
            const token = localStorage.getItem('token')
            const userInfo = localStorage.getItem('userInfo')
            if (token && userInfo) { this.isLogin = true; this.userInfo = JSON.parse(userInfo) }
        },
        handleMenuSelect(index) { this.currentView = index },
        handleMobileMenuSelect(index) { this.currentView = index; this.showMobileMenu = false },
        handleTabClick(view) { if (!this.isLogin && (view === 'orders' || view === 'profile')) { this.showLogin = true } else { this.currentView = view } },
        handleUserCommand(command) { if (command === 'logout') { this.logout() } else { this.currentView = command } },
        goToDetail(projectId) { this.currentProjectId = projectId; this.currentView = 'detail' },
        goToSampleTrack(orderId) { this.currentOrderId = orderId; this.currentView = 'sampletrack' },
        requireLogin() { this.showLogin = true },
        // 预约下单
        async openBooking(project) {
            this.bookingProject = project
            this.bookingForm = { sample_name: '', quantity: 1, remark: '', address_id: null, coupon_id: null }
            try {
                const [addrRes, couponRes] = await Promise.all([api.getAddresses(), api.getAvailableCoupons(project.id)])
                this.addresses = addrRes.data || []
                this.availableCoupons = couponRes.data || []
                if (this.addresses.length > 0) { const def = this.addresses.find(a => a.is_default) || this.addresses[0]; this.bookingForm.address_id = def.id }
            } catch (error) {}
            this.showBooking = true
        },
        async submitBooking() {
            if (!this.bookingForm.sample_name) { ElMessage.error('请输入样品名称'); return }
            if (!this.bookingForm.address_id) { ElMessage.error('请选择收货地址'); return }
            this.bookingLoading = true
            try {
                const res = await api.createOrder({ project_id: this.bookingProject.id, ...this.bookingForm })
                ElMessage.success('订单创建成功')
                this.showBooking = false
                this.paymentOrder = res.data
                this.showPayment = true
                this.loadBalance()
            } catch (error) {} finally { this.bookingLoading = false }
        },
        // 支付
        async loadBalance() { try { const res = await api.getBalance(); this.balance = res.data } catch (error) {} },
        openPayment(order) { this.paymentOrder = order; this.payMethod = 'balance'; this.showPayment = true; this.loadBalance() },
        async submitPayment() {
            this.paymentLoading = true
            try {
                if (this.payMethod === 'balance') {
                    await api.payWithBalance({ order_id: this.paymentOrder.id })
                    ElMessage.success('支付成功')
                    this.showPayment = false
                    this.currentView = 'orders'
                } else {
                    const res = await api.createPayment({ order_id: this.paymentOrder.id, pay_method: this.payMethod })
                    if (res.data?.pay_url) { window.open(res.data.pay_url, '_blank') }
                    ElMessage.info('请在新窗口完成支付')
                    this.showPayment = false
                }
            } catch (error) {} finally { this.paymentLoading = false }
        },
        // 评价
        openReview(order) { this.reviewOrder = order; this.reviewForm = { rating: 5, content: '' }; this.showReview = true },
        async submitReview() {
            if (!this.reviewForm.content) { ElMessage.error('请输入评价内容'); return }
            this.reviewLoading = true
            try {
                await api.createReview({ order_id: this.reviewOrder.id, project_id: this.reviewOrder.project_id, ...this.reviewForm })
                ElMessage.success('评价成功'); this.showReview = false
            } catch (error) {} finally { this.reviewLoading = false }
        },
        // 发票
        openInvoice(order) { this.invoiceOrder = order; this.invoiceForm = { invoice_type: 'personal', title: '', tax_id: '', email: '' }; this.showInvoice = true },
        async submitInvoice() {
            if (!this.invoiceForm.title) { ElMessage.error('请输入发票抬头'); return }
            if (!this.invoiceForm.email) { ElMessage.error('请输入接收邮箱'); return }
            this.invoiceLoading = true
            try {
                await api.applyInvoice({ order_ids: [this.invoiceOrder.id], amount: this.invoiceOrder.total_amount, ...this.invoiceForm })
                ElMessage.success('发票申请已提交'); this.showInvoice = false
            } catch (error) {} finally { this.invoiceLoading = false }
        },
        // 编辑资料
        openEditProfile() { this.profileForm = { nickname: this.userInfo.nickname || '', avatar: this.userInfo.avatar || '' }; this.showEditProfile = true },
        async submitProfile() {
            this.profileLoading = true
            try {
                await api.updateProfile(this.profileForm)
                const res = await api.getUserInfo()
                this.userInfo = res.data
                localStorage.setItem('userInfo', JSON.stringify(res.data))
                ElMessage.success('资料更新成功'); this.showEditProfile = false
            } catch (error) {} finally { this.profileLoading = false }
        },
        // 登录
        async sendSms() {
            if (!this.loginForm.phone || this.loginForm.phone.length !== 11) { ElMessage.error('请输入正确的手机号'); return }
            try {
                const res = await api.sendSms({ phone: this.loginForm.phone, scene: 'login' })
                ElMessage.success(res.message)
                if (res.data?.code) { ElMessage.info(`开发模式验证码：${res.data.code}`) }
                this.countdown = 60
                const timer = setInterval(() => { this.countdown--; if (this.countdown <= 0) { clearInterval(timer) } }, 1000)
            } catch (error) {}
        },
        async handleLogin() {
            if (!this.loginForm.phone || !this.loginForm.sms_code) { ElMessage.error('请填写完整信息'); return }
            this.loginLoading = true
            try {
                const res = await api.smsLogin(this.loginForm)
                localStorage.setItem('token', res.data.access_token)
                const userRes = await api.getUserInfo()
                localStorage.setItem('userInfo', JSON.stringify(userRes.data))
                this.isLogin = true; this.userInfo = userRes.data; this.showLogin = false
                ElMessage.success('登录成功')
            } catch (error) {} finally { this.loginLoading = false }
        },
        logout() {
            localStorage.removeItem('token'); localStorage.removeItem('userInfo')
            this.isLogin = false; this.userInfo = {}; this.currentView = 'home'
            ElMessage.success('已退出登录')
        }
    }
})
.use(ElementPlus)
.mount('#app')


