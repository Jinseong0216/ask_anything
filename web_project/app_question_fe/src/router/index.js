import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/store/auth'

// views
import Home from '@/views/MainHome.vue'
import LogIn from '@/views/LogIn.vue'
import RegisterPage from '@/views/RegisterPage.vue'
import Admin from '@/views/AdminPage.vue'

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
    meta: { guestOnly: true },
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
    meta: { requiresAuth: true, role: 'admin'}
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

  // 최초 진입 / 새로고침 시 사용자 정보 로딩
  if (!auth.initialized) {
    await auth.fetchMe()
  }

  // 로그인 필요한 페이지
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return { name: "login" }
  }

  // 로그인한 사용자가 로그인 페이지 접근 시
  if (to.meta.guestOnly && auth.isAuthenticated) {
    return { name: "home" }
  }

  // 역할 기반 접근 제어
  if (to.meta.role && auth.user?.auth_level !== to.meta.role) {
    return { name: "home" } // 또는 403 페이지
  }
})

export default router