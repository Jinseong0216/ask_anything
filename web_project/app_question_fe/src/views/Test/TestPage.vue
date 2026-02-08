<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 px-4">
    <div class="w-full max-w-md bg-white p-8 rounded-lg shadow-md">
      
      <!-- 제목 -->
      <h2 class="text-2xl font-bold mb-6 text-center">회원가입</h2>

      <!-- 회원가입 폼 -->
      <form @submit.prevent="handleSignUp" class="flex flex-col gap-4">
        <input
          v-model.trim="form.login_id"
          type="text"
          placeholder="아이디"
          class="px-4 py-3 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-400"
        />

        <input
          v-model.trim="form.user_name"
          type="text"
          placeholder="이름"
          class="px-4 py-3 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-400"
        />

        <input
          v-model.trim="form.email"
          type="email"
          placeholder="이메일"
          class="px-4 py-3 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-400"
        />

        <input
          v-model.trim="form.password"
          type="password"
          placeholder="비밀번호"
          class="px-4 py-3 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-400"
        />

        <input
          v-model.trim="form.passwordConfirm"
          type="password"
          placeholder="비밀번호 확인"
          class="px-4 py-3 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-400"
        />

        <button
          type="submit"
          :disabled="loading"
          class="bg-blue-500 text-white py-3 rounded-lg hover:bg-blue-600 transition"
        >
          {{ loading ? "가입 중..." : "회원가입" }}
        </button>

        <!-- 에러 메시지 -->
        <p v-if="errorMessage" class="text-red-500 text-sm mt-1">{{ errorMessage }}</p>
      </form>

      <!-- 로그인 링크 -->
      <p class="mt-4 text-sm text-center text-gray-500">
        이미 계정이 있나요? 
        <router-link to="/login" class="text-blue-500 hover:underline">로그인</router-link>
      </p>

      <!-- 소셜 회원가입 -->
      <div class="mt-6 flex justify-center gap-3">
        <button class="w-10 h-10 rounded-full bg-white flex items-center justify-center border hover:bg-gray-100">G</button>
        <button class="w-10 h-10 rounded-full bg-yellow-400 flex items-center justify-center border hover:bg-yellow-500">K</button>
        <button class="w-10 h-10 rounded-full bg-green-500 flex items-center justify-center border hover:bg-green-600">N</button>
      </div>
      
    </div>
  </div>
</template>

<script setup>
import { reactive, computed } from "vue"
import { useAuthStore } from "@/store/auth"
import { useRouter } from "vue-router"

const auth = useAuthStore()
const router = useRouter()

// 회원가입 폼
const form = reactive({
  login_id: "",
  user_name: "",
  email: "",
  password: "",
  passwordConfirm: ""
})

// 에러 메시지 매핑
const errorMessage = computed(() => auth.error || '')

const loading = computed(() => auth.loading)

// 회원가입 처리
const handleSignUp = async () => {

  if (!form.login_id || !form.password) {
    auth.error = "필수 항목을 입력하세요"
    return
  }

  if (form.password.length < 8) {
    auth.error = "비밀번호는 8자 이상이어야 합니다"
    return
  }

  if (form.password !== form.passwordConfirm) {
    auth.error = "비밀번호가 일치하지 않습니다"
    return
  }
  if (form.password !== form.passwordConfirm) {
    auth.error = "비밀번호가 일치하지 않습니다"
    return
  }
  
  try {
    // Pinia store에서 signUp API 연결
    const res = await auth.register(form)
    if (res?.msg === 'registered') {
        router.push({ name: "login" })
        console.log("회원가입 성공", res)
    }
  } catch (err) {
    console.log("실패", err)
  }
  if (auth.user) {
    router.push("/login")  // 가입 후 로그인 페이지로 이동
  }
}
</script>

<style>
/* 필요 시 추가 커스텀 스타일 */
</style>
