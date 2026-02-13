import Http from "@/api/index"

/*
  관리자 API 모음
*/

export const adminApi = {
  async getUsers() {
    return await Http.get("/auth/users")
  },

  async updateUser(user) {
    await Http.put(`/auth/users/${user.user_id}`, {
      user_name: user.user_name,
      email: user.email,
      role: user.role,
      auth_level: user.auth_level,
      is_active: user.is_active,
    })
  }
}