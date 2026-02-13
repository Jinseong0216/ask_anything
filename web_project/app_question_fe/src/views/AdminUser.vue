<template>
  <div class="p-6">
    <h2 class="text-2xl font-bold mb-4">회원 관리</h2>

    <table class="w-full bg-white dark:bg-gray-800 rounded-lg">
      <thead>
        <tr>
          <th class="p-2">이름</th>
          <th class="p-2">이메일</th>
          <th class="p-2">권한</th>
          <th class="p-2">역할</th>
          <th class="p-2">상태</th>
          <th class="p-2">변경</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.user_id">
          <td class="p-2">{{ user.user_name }}</td>
          <td class="p-2">{{ user.email }}</td>
          <td class="p-2">
            <select v-model="user.auth_level">
              <option value="general">일반회원</option>
              <option value="admin">관리자</option>
            </select>
          </td>
          <td class="p-2">
            <select v-model="user.role">
              <option value="student">student</option>
              <option value="teacher">teacher</option>
            </select>
          </td>
          <td class="p-2">
            <input type="checkbox" v-model="user.is_active" />
          </td>
          <td class="p-2">
            <button
              @click="updateUser(user)"
              class="px-3 py-1 bg-primary text-white rounded"
            >
              저장
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { adminApi } from "@/api/admin.js"

const users = ref([])

onMounted(() => {
  adminApi.getUsers()
    .then(res => {
      users.value = res.data
    })
    .catch(err => {
      console.error(err)
    })
})


const updateUser = (user) => {
    adminApi.updateUser(user)
}
</script>
