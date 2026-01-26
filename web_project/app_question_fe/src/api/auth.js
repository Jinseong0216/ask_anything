import axios from "axios"

/*
  인증 전용 axios 인스턴스
  - 다른 API와 분리
  - 설정 한 곳에 집중
*/
const authHttp = axios.create({
  baseURL: "/api/auth",
  withCredentials: true,
  timeout: 10000,
})

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
    return authHttp.get("/me")
  },

  register(payload) {
    console.log("register 요청")
    return authHttp.post("/register", payload)
  },
}
