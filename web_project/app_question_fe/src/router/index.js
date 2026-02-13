import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/store/auth'

// views
import Home from '@/views/MainHome.vue'
import LogIn from '@/views/LogIn.vue'
import RegisterPage from '@/views/RegisterPage.vue'
import Admin from '@/views/AdminPage.vue'

// Admin
import AdminUser from '@/views/AdminUser.vue'

// Test
import TestHome from '@/views/Test/TestHome.vue'
import TestPage from '@/views/Test/TestPage.vue'

const routes = [
  { 
    path: '/', 
    name: 'home',
    component: Home, 
    meta: { requiresAuth: true },
  },
  { 
    path: '/login', 
    name: 'login',
    component: LogIn, 
    meta: { },
  },  
  {
    path: "/register",
    name: "register",
    component: RegisterPage,
    meta: { guestOnly: true }
  },
  { 
    path: '/admin', 
    name: 'admin',
    component: Admin,
    meta: { requiresAuth: true }
  },

  { 
    path: '/admin/users', 
    name: 'adminUser',
    component: AdminUser,
    meta: { requiresAuth: true }
  },

  { 
    path: '/testHome', 
    name: 'testHome',
    component: TestHome,
    meta: { 
      requiresAuth: false, 
      requiresAdumin: false,
    }
   },

  { 
    path: '/test', 
    name: 'testPage',
    component: TestPage, 
    meta: { guestOnly: true },
  },  

]

const router = createRouter({
  history: createWebHistory(),
  routes
})

/*
  전역 인증 가드
*/
router.beforeEach(async (to) => {
  const auth = useAuthStore()

  console.log(auth.error)
  auth.error = ''
  // 최초 진입 / 새로고침 시 사용자 정보 로딩
  if (!auth.initialized) {
    // 비회원 전용 페이지면 그냥 통과
    if (to.meta.guestOnly) {
      auth.initialized = true
      return true
    }
    console.log('최초 진입 fetch호출 - 시간', Date().toLocaleString())
    auth.initialized = true
    await auth.fetchMe()
  }

  // 로그인 필요한 페이지
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return { name: "login" }
  }

  // 로그인한 사용자가 로그인 페이지 접근 시
  if (to.name === 'login' && auth.user) {
    return { name: "home" }
  }

  // 역할 기반 접근 제어
  /////////////////////////////////////////////////////////
  // TODO: 차후 역할관련 기능 server에서 인증받는 걸로 변경 해야함
  /////////////////////////////////////////////////////////
  if (to.meta.role && auth.user?.role !== to.meta.role) {
    return { name: "home" } // 또는 403 페이지
  }
})

export default router