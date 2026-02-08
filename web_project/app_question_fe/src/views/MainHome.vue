<template>
  <div>
    <button @click="logout">로그아웃</button>
    <h1 class="text-4xl font-bold text-primary">
      Tailwind 살아있다
    </h1>
    <p>Main Home</p>

    <div v-if="auth.isAuthenticated">
      {{ auth.user.user_name }} 님 환영합니다  
      <div>
      user.value {{ auth.user }}
      </div>
    </div>

  </div>
</template>

<script setup>
import { useAuthStore } from '@/store/auth'

const auth = useAuthStore()
const logout = async () => {
  await auth.logout()
}
</script>