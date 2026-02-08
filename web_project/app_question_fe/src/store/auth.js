import { defineStore } from "pinia"
import { ref, computed } from "vue"
import { authApi } from "@/api/auth"
import { useRouter } from "vue-router"
import authEvents from "@/events/authEvents"

export const useAuthStore = defineStore("auth", () => {
  const router = useRouter()
  const user = ref('')
  const loading = ref(false)
  const error = ref('')
  
  const initialized = ref(false)
  const isAuthenticated = computed(() => !!user.value)

  /*
    현재 로그인 사용자 조회
    - App 시작
    - 새로고침
    - 필요 시 재호출 가능
  */
  const fetchMe = async () => {
    loading.value = true
    try {
      const res = await authApi.me()
      user.value = res.data
      console.log('fetchMe 새로 받은 결과', user.value)
      console.log('fetchMe 새로 받은 결과', user.value.auth_level)
      console.log('fetchMe 새로 받은 결과', user.value.email)
      console.log('fetchMe 새로 받은 결과', user.value.login_id)
      console.log('fetchMe 새로 받은 결과', user.value.role)      
      console.log('fetchMe 새로 받은 결과', user.value.user_id)      
      console.log('fetchMe 새로 받은 결과', user.value.user_name)     
    } catch (e) {
      user.value = ''
    } finally {
      loading.value = false
      initialized.value = true
    }
  }

  /* 
    리프레시토큰 요청
  */
  const refreshToken = async () => {
    console.log('refresh 요청 시작')
    return await authApi.refresh()
  }

  /* 
    강제 로그아웃 + 쿠키 정리
  */
  const forceLogout = async (payload) => {
    console.log("강제 로그아웃 사유:", payload?.reason)
    user.value =''
    initialized.value = true
    if (router.currentRoute.value.name !== 'login') {
      router.replace({ name: "login" })
    }
  }


  /*
    로그인
  */
  const login = async (payload) => {
    loading.value = true
    error.value = ''
    try {
      const res = await authApi.login(payload) 
      console.log(res)
      console.log('fetchMe 실행')
      await fetchMe()
      router.push({ name: "home"})
      return true
    } catch (e) {
        error.value = e.response?.data?.msg || "로그인 실패"
        return false 
    } finally {
      loading.value = false
      initialized.value = true
    }
  }

  /*
    로그아웃
  */
  const logout = async () => {
    const res = await authApi.logout()
    user.value = ''
    initialized.value = false
    console.log('로그아웃요청 들어감 res', res)
    console.log('로그아웃요청 들어감 res.data', res.data)
    router.push({ name: "login"})
  }

  /*
    회원가입
  */
  const register = async (payload) => {
    loading.value = true
    error.value = ''
    try {
      const res = await authApi.register(payload)
      return res.data
    } catch (e) {
        error.value = e.response?.data?.msg || "회원가입 실패"
        return false
    }finally {
      loading.value = false
    }
  }

  const bindEvents = () => {
    authEvents.on("force-logout", forceLogout)
  }

  return {
    user, loading, error, isAuthenticated, initialized,
    fetchMe, register, login, logout, refreshToken, forceLogout,
    bindEvents,
  }
})


