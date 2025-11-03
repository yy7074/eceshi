// 科研检测服务平台 - Web端应用
const { createApp } = Vue
const { ElMessage, ElMessageBox } = ElementPlus

// API基础URL
const API_BASE_URL = 'https://catdog.dachaonet.com'

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
    createPayment: (data) => axios.post('/api/v1/payments/create', data)
}

// ==================== Vue组件 ====================

// 首页组件
const HomeView = {
    template: `
        <div class="home-view">
            <!-- 英雄区 -->
            <div class="hero-section">
                <h1 class="hero-title">科研检测服务平台</h1>
                <p class="hero-subtitle">专业 · 高效 · 可靠</p>
                <div class="hero-actions">
                    <el-button type="primary" size="large" @click="$emit('go-projects')">
                        浏览检测项目
                    </el-button>
                    <el-button size="large" plain>了解更多</el-button>
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
            categories: [],
            categoriesLoading: false,
            projects: [],
            projectsLoading: false
        }
    },
    mounted() {
        this.loadCategories()
        this.loadProjects()
    },
    methods: {
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
    template: `
        <div class="project-detail">
            <div v-if="loading" class="loading-container">
                <el-icon class="is-loading" :size="40"><loading /></el-icon>
            </div>
            <div v-else-if="project">
                <div class="detail-header">
                    <el-button @click="$emit('go-back')" class="mb-16">
                        <el-icon><arrow-left /></el-icon> 返回列表
                    </el-button>
                    
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
                            <el-button type="primary" size="large" style="width: 100%">立即预约</el-button>
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
                    </el-tabs>
                </div>
            </div>
        </div>
    `,
    data() {
        return {
            project: null,
            loading: false,
            activeTab: 'intro'
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
            } catch (error) {
                console.error('加载项目详情失败', error)
            } finally {
                this.loading = false
            }
        }
    }
}

// 订单列表组件
const OrdersView = {
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
                            <div>金额：¥{{ order.total_amount }}</div>
                        </div>
                        <div class="order-actions">
                            <el-button type="primary" v-if="order.status === 'unpaid'">去支付</el-button>
                            <el-button v-if="order.status === 'unpaid'" @click="handleCancel(order.id)">取消订单</el-button>
                        </div>
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
        }
    }
}

// 个人中心组件
const ProfileView = {
    template: `
        <div class="profile-view">
            <div class="profile-header">
                <el-avatar :size="80" :src="userInfo.avatar">{{ userInfo.nickname?.[0] || 'U' }}</el-avatar>
                <div>
                    <h2>{{ userInfo.nickname || '用户' }}</h2>
                    <p>{{ userInfo.phone }}</p>
                </div>
            </div>

            <div class="profile-stats">
                <div class="stat-card">
                    <div class="stat-value">¥{{ balance.credit_limit || 0 }}</div>
                    <div class="stat-label">信用额度</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">¥{{ balance.prepaid_balance || 0 }}</div>
                    <div class="stat-label">预付余额</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{{ userInfo.total_orders || 0 }}</div>
                    <div class="stat-label">订单数量</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{{ userInfo.points_balance || 0 }}</div>
                    <div class="stat-label">积分</div>
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
    },
    methods: {
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

// ==================== 主应用 ====================
createApp({
    components: {
        HomeView,
        ProjectsView,
        ProjectDetail,
        OrdersView,
        ProfileView,
        AboutView
    },
    data() {
        return {
            currentView: 'home',
            currentProjectId: null,
            isMobile: false,
            isLogin: false,
            userInfo: {},
            showLogin: false,
            loginForm: {
                phone: '',
                sms_code: ''
            },
            countdown: 0,
            loginLoading: false,
            showMobileMenu: false
        }
    },
    mounted() {
        // 检测设备类型
        this.checkDevice()
        window.addEventListener('resize', this.checkDevice)
        
        // 检查登录状态
        this.checkLogin()
    },
    methods: {
        checkDevice() {
            this.isMobile = window.innerWidth < 768
        },
        checkLogin() {
            const token = localStorage.getItem('token')
            const userInfo = localStorage.getItem('userInfo')
            if (token && userInfo) {
                this.isLogin = true
                this.userInfo = JSON.parse(userInfo)
            }
        },
        handleMenuSelect(index) {
            this.currentView = index
        },
        handleMobileMenuSelect(index) {
            this.currentView = index
            this.showMobileMenu = false
        },
        handleTabClick(view) {
            if (!this.isLogin && (view === 'orders' || view === 'profile')) {
                this.showLogin = true
            } else {
                this.currentView = view
            }
        },
        handleUserCommand(command) {
            if (command === 'logout') {
                this.logout()
            } else {
                this.currentView = command
            }
        },
        goToDetail(projectId) {
            this.currentProjectId = projectId
            this.currentView = 'detail'
        },
        async sendSms() {
            if (!this.loginForm.phone || this.loginForm.phone.length !== 11) {
                ElMessage.error('请输入正确的手机号')
                return
            }
            try {
                const res = await api.sendSms({
                    phone: this.loginForm.phone,
                    scene: 'login'
                })
                ElMessage.success(res.message)
                if (res.data?.code) {
                    ElMessage.info(`开发模式验证码：${res.data.code}`)
                }
                this.countdown = 60
                const timer = setInterval(() => {
                    this.countdown--
                    if (this.countdown <= 0) {
                        clearInterval(timer)
                    }
                }, 1000)
            } catch (error) {
                console.error('发送验证码失败', error)
            }
        },
        async handleLogin() {
            if (!this.loginForm.phone || !this.loginForm.sms_code) {
                ElMessage.error('请填写完整信息')
                return
            }
            this.loginLoading = true
            try {
                const res = await api.smsLogin(this.loginForm)
                localStorage.setItem('token', res.data.access_token)
                
                // 获取用户信息
                const userRes = await api.getUserInfo()
                localStorage.setItem('userInfo', JSON.stringify(userRes.data))
                
                this.isLogin = true
                this.userInfo = userRes.data
                this.showLogin = false
                ElMessage.success('登录成功')
            } catch (error) {
                console.error('登录失败', error)
            } finally {
                this.loginLoading = false
            }
        },
        logout() {
            localStorage.removeItem('token')
            localStorage.removeItem('userInfo')
            this.isLogin = false
            this.userInfo = {}
            this.currentView = 'home'
            ElMessage.success('已退出登录')
        }
    }
})
.use(ElementPlus)
.mount('#app')


