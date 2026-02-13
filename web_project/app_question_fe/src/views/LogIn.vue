<template>
  <div class="flex flex-col md:flex-row min-h-screen">
    <!-- 왼쪽 영상 슬라이더 -->
    <div
      ref="sliderWrapper"
      class="relative md:w-1/2 w-full overflow-hidden select-none"
      @mousedown="startDrag"
      @mousemove="onDrag"
      @mouseup="endDrag"
      @mouseleave="endDrag"
      @touchstart="startDrag"
      @touchmove="onDrag"
      @touchend="endDrag"
    >
      <!-- 슬라이더 트랙 -->
      <div class="flex h-full" :style="sliderStyle">
        <div
          v-for="(video, i) in videos"
          :key="i"
          class="relative w-full h-[300px] md:h-full overflow-hidden flex-shrink-0"
        >
          <video
            autoplay
            muted
            loop
            playsinline
            class="absolute inset-0 w-full h-full object-cover"
          >
            <source :src="video" type="video/mp4" />
          </video>

          <!-- 오버레이 -->
          <div class="absolute inset-0 bg-red-500/70"></div>
        </div>
      </div>

      <!-- 텍스트 -->
      <div class="absolute inset-0 z-10 flex items-center p-6 md:p-12 text-white">
        <div>
          <h1 class="text-2xl md:text-3xl font-bold mb-4">
            수업의 밀도를 높이는 단 하나의 질문 시스템
          </h1>
          <p class="text-base md:text-lg text-white/80 mb-6">
            Qube는 실시간 질문 환경을 통해<br class="md:hidden"/>
            더 깊이 있는 수업을 만듭니다.
          </p>

          <!-- 인디케이터 -->
          <div class="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-2">
            <span
              v-for="(v, i) in videos"
              :key="i"
              class="w-2.5 h-2.5 rounded-full transition-all"
              :class="i === currentIndex ? 'bg-white scale-110' : 'bg-white/40'"
            ></span>
          </div>
        </div>
      </div>
    </div>


    <!-- 오른쪽 로그인 폼 영역 -->
    <div class="md:w-1/2 w-full flex-1 flex flex-col justify-center items-center bg-white p-6 md:p-12">
      <!-- 로고 -->
      <img
        :src="logo"
        alt="Qube"
        class="w-40 md:w-48 lg:w-56 mb-6 object-contain"
      />

      <!-- 로그인 제목 -->
      <h2 class="text-xl font-semibold mb-4">로그인</h2>
      <a href="/register" class="text-sm text-gray-400 mb-4 self-end">이메일 가입</a>

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
      <div class="flex justify-center gap-3 mt-6">

        <!-- Google -->
        <button class="social-btn bg-white hover:bg-neutral-50" aria-label="Google 로그인">
          <img :src="googleIcon" class="w-5 h-5" />
        </button>

        <!-- Kakao -->
        <button class="social-btn bg-[#FEE500] hover:brightness-95" aria-label="Kakao 로그인">
          <img :src="kakaoIcon" class="w-5 h-5" />
        </button>

        <!-- Naver -->
        <button class="social-btn bg-[#03C75A] hover:brightness-95" aria-label="Naver 로그인">
          <img :src="naverIcon" class="w-6 h-6" />
        </button>

        <!-- Apple -->
        <button class="social-btn bg-black hover:bg-neutral-900" aria-label="Apple 로그인">
          <img :src="appleIcon" class="w-5 h-5 invert" />
        </button>

      </div>

      <a href="#" class="mt-4 text-xs text-gray-400 underline">아이디 · 비밀번호 찾기</a>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from "vue"
import { useAuthStore } from '@/store/auth'

import googleIcon from "@/assets/social_icons/google.svg"
import kakaoIcon from "@/assets/social_icons/kakao.svg"
import naverIcon from "@/assets/social_icons/naver.svg"
import appleIcon from "@/assets/social_icons/apple.svg"
import logo from "@/assets/neoMath.png"
import video1 from "@/assets/videos/bg-loop.mp4"
import video2 from "@/assets/videos/bg-loop2.mp4"

/* ------------------------
   로그인 로직 (기존 유지)
-------------------------*/
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

/* ------------------------
   영상 슬라이더 로직
-------------------------*/
const videos = [video1, video2]
const currentIndex = ref(0)

const sliderWrapper = ref(null)
const startX = ref(0)
const deltaX = ref(0)
const isDragging = ref(false)

const getX = (e) =>
  e.touches ? e.touches[0].clientX : e.clientX

const sliderStyle = computed(() => {
  const width = sliderWrapper.value?.offsetWidth || 0
  return {
    transform: `translateX(${-currentIndex.value * width + deltaX.value}px)`,
    transition: isDragging.value ? "none" : "transform 0.35s ease"
  }
})

const startDrag = (e) => {
  isDragging.value = true
  startX.value = getX(e)
}

const onDrag = (e) => {
  if (!isDragging.value) return
  deltaX.value = getX(e) - startX.value
}

const endDrag = () => {
  if (!isDragging.value) return
  isDragging.value = false

  const width = sliderWrapper.value?.offsetWidth || 0
  const threshold = width / 4

  if (deltaX.value < -threshold && currentIndex.value < videos.length - 1) {
    currentIndex.value++
  } else if (deltaX.value > threshold && currentIndex.value > 0) {
    currentIndex.value--
  }

  deltaX.value = 0
}
</script>

<style scoped>
.social-btn {
  @apply w-11 h-11 rounded-full flex items-center justify-center
         border border-black/10 transition-all;
}
</style>