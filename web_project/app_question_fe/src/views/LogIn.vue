<template>
    <div class="flex flex-col md:flex-row h-screen">
      <!-- 왼쪽 이미지/홍색 영역 -->
      <div
        class="md:w-1/2 w-full bg-red-500 text-white flex flex-col justify-center items-center p-8 md:p-12
              min-h-[200px] md:min-h-0"
      >
        <h1 class="text-2xl md:text-3xl font-bold mb-4 text-center md:text-left">
          컨텐츠 제작 혁명, 수학OO
        </h1>
        <p class="text-base md:text-lg text-white/80 mb-8 text-center md:text-left leading-relaxed">
          수학 교육의 디지털 전환을 통한
          업무 효율의 혁신을 경험하세요.
        </p>

        <!-- 슬라이더 점 표시 -->
        <div class="flex gap-2 justify-center md:justify-start">
          <span class="w-3 h-3 rounded-full bg-white/80"></span>
          <span class="w-3 h-3 rounded-full bg-white/40"></span>
        </div>
      </div>

        <!-- 오른쪽 로그인 폼 영역 -->
        <div class="md:w-1/2 w-full flex flex-col justify-center items-center bg-white p-8 md:p-12">
        <!-- 로고 -->
        <img src="/logo.png" alt="수학 OO" class="h-10 mb-6" />

    <!-- 로그인 제목 -->
      <h2 class="text-xl font-semibold mb-4">로그인</h2>
      <a href="/register" class="text-sm text-gray-400 mb-6 self-end">이메일 가입</a>

      <!-- 로그인 폼 -->
      <form @submit.prevent="handleLogin" class="w-full flex flex-col gap-4">
        <input
          type="text"
          placeholder="아이디"
          v-model="form.login_id"
          autocomplete="username"
          class="px-4 py-3 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
        <input
          type="password"
          placeholder="비밀번호 입력"
          v-model="form.password"
          autocomplete="current-password"
          class="px-4 py-3 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
        
        <button
          type="submit"
          :disabled="loading"
          class="bg-gray-400 text-white rounded-lg py-3 hover:bg-gray-500 transition disabled:opacity-50"
        >
          {{ loading ? "로그인 중..." : "로그인" }}
        </button>
        <p v-if="errorMessage" class="text-red-500 text-sm mt-1">{{ errorMessage }}</p>
      </form>

      <!-- 소셜 로그인 버튼 -->
      <div class="flex flex-wrap justify-center gap-3 mt-6">
        <button class="w-10 h-10 rounded-full bg-white flex items-center justify-center border">G</button>
        <button class="w-10 h-10 rounded-full bg-yellow-400 flex items-center justify-center border">K</button>
        <button class="w-10 h-10 rounded-full bg-green-500 flex items-center justify-center border">N</button>
        <button class="w-10 h-10 rounded-full bg-black text-white flex items-center justify-center border"></button>
      </div>

      <a href="#" class="mt-4 text-xs text-gray-400 underline">아이디 · 비밀번호 찾기</a>
    </div>
  </div>
</template>

<script setup>
import { reactive, computed } from 'vue'
import { useAuthStore } from '@/store/auth'

const auth = useAuthStore()

const form = reactive({
  login_id: '',
  password: ''
})

const handleLogin = async () => {
  if (!form.login_id || !form.password) {
    auth.error = "아이디와 비밀번호를 모두 입력해주세요."
    return
  }
  await auth.login(form)
}

const loading = computed(() => auth.loading)
const errorMessage = computed(() => {
  switch (auth.error) {
    case "invalid user":
      return "존재하지 않는 사용자입니다."
    case "inactive account":
      return "비활성 사용자입니다."
    case "invalid credentials":
      return "아이디 또는 비밀번호가 잘못되었습니다."
    default:
      return auth.error
  }
})

</script>
