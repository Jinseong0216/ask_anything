import axios from "axios"
import authEvents from "@/events/authEvents"
import { ref } from "vue"

/*
  인증 전용 axios 인스턴스
  - 다른 API와 분리
  - 설정 한 곳에 집중
*/
const authHttp = axios.create({
  baseURL: "/api/auth",
  headers: { "Content-Type": "application/json"},
  withCredentials: true,
  timeout: 10000,
})

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

/*
  read csrf_access_token from Cookie 
*/
authHttp.interceptors.request.use(config => {
  const csrf = getCookie("csrf_token")
  console.log('===== interceptors.request.use =====')
  if (csrf) config.headers["X-CSRF-TOKEN"] = csrf
  config.withCredentials = true
  return config
})

/*
  =========================
  Response Interceptor
  - 401 → refresh
  - 403 → logout
  =========================
*/
const isRefreshing = ref(false)
const refreshQueue = ref([])



function processQueue(error) {
  refreshQueue.value.forEach((promise) => {
    if (error) promise.reject(error)
    else promise.resolve()
  })
  refreshQueue.value = []
}


authHttp.interceptors.response.use(
  res => res,
  async error => {
    console.log('===== interceptors.response.use =====')
    const status = error.response?.status
    const originalRequest = error.config

    // refresh 요청 자체가 실패한 경우 → 즉시 로그아웃
    if (originalRequest.url?.includes("/refresh")) {
      authEvents.emit("force-logout", {
        reason: "refresh_failed"
      })
      return Promise.reject(error)
    }

    // access token 만료
    if (status === 401 && !originalRequest._retry) {
      // 이미 refresh 중이면 큐에 대기
      if (isRefreshing.value) {
        return new Promise((resolve, reject) => {
          refreshQueue.value.push({ resolve, reject })
        }).then(() => authHttp(originalRequest))
      }

      originalRequest._retry = true
      isRefreshing.value = true

      try {
        await authHttp.post("/refresh") // csrf_refresh_token 사용됨

        processQueue(null)
        isRefreshing.value = false

        // 원래 요청 재시도
        return authHttp(originalRequest)
      } catch (err) {
        processQueue(err)
        isRefreshing.value = false

        // authEvents.emit("force-logout", {
        //   reason: "refresh_failed"
        // })

        return Promise.reject(err)
      }
    }
    console.log(error)
    return Promise.reject(error)
  }
)



/*
  인증 API 모음
*/
export const authApi = {
  login(payload) {
    return authHttp.post("/login", payload)
  },

  logout() {
    return authHttp.post("/logout")
  },

  me() {
    return authHttp.get('/me')
  },

  refresh() {
    return authHttp.post("/refresh")
  },

  register(payload) {
    console.log("register 요청")
    return authHttp.post("/register", payload)
  },
}
