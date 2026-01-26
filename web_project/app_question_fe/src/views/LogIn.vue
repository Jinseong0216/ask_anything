<template>
  <form @submit.prevent="submit">
    <input v-model="form.username" placeholder="아이디" />
    <input v-model="form.password" type="password" />
    <button>로그인</button>
  </form>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'

const router = useRouter()
const auth = useAuthStore()

const form = reactive({
  username: '',
  password: ''
})

const submit = async () => {
  const res = await auth.login(form)
  if (res.data.success) {
    router.push('/')
  }
}
</script>
