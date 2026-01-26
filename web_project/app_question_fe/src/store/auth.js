import { defineStore } from "pinia"
import { ref, computed } from "vue"
import { authApi } from "@/api/auth"

export const useAuthStore = defineStore("auth", () => {
  const user = ref(null)
  const loading = ref(false)
  const error = ref("")
  

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
    } catch {
      user.value = null
    } finally {
      loading.value = false
    }
  }

  /*
    로그인
  */
  const login = async (payload) => {
    loading.value = true
    try {
      await authApi.login(payload)
      await fetchMe()
    } catch (e) {
        error.value = e.response?.data?.message || "회원가입 실패"
        return false 
    } finally {
      loading.value = false
    }
  }

  /*
    로그아웃
  */
  const logout = async () => {
    await authApi.logout()
    user.value = null
  }

  /*
    회원가입
  */
  const register = async (payload) => {
    loading.value = true
    error.value = ""
    try {
      const res = await authApi.register(payload)
      return res.data
    } catch (e) {
        error.value = e.response?.data?.message || "회원가입 실패"
        return false
    }finally {
      loading.value = false
    }
  }

  return {
    user,
    loading,
    isAuthenticated,
    fetchMe,
    register,
    login,
    logout,
  }
})
