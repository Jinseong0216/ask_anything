import Http from "@/api/index"

/*
  인증 API 모음
*/
export const authApi = {
  login(payload) {
    return Http.post("/auth/login", payload)
  },

  logout() {
    return Http.post("/auth/logout")
  },

  me() {
    return Http.get('/auth/me')
  },

  refresh() {
    return Http.post("/auth/refresh")
  },

  register(payload) {
    console.log("register 요청")
    return Http.post("/auth/register", payload)
  },
}
