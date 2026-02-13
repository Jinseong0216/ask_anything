<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-800 dark:text-white">
    <!-- Header -->
    <header class="flex justify-between items-center px-10 py-6 border-b border-gray-200 dark:border-gray-700">
      <h1 class="text-2xl font-bold text-primary">AskAnything</h1>

      <div class="flex gap-4 items-center">
        <span class="text-sm opacity-70">
          {{ auth.user.user_name }}님
        </span>

        <router-link
          v-if="auth.user.auth_level === 'admin'"
          to="/admin"
          class="px-4 py-2 rounded-lg bg-primary text-white text-sm"
        >
          회원관리
        </router-link>

        <button
          @click="logout"
          class="px-4 py-2 rounded-lg bg-primary text-white text-sm"
        >
          로그아웃
        </button>
      </div>
    </header>

    <!-- 상단 요약 카드 -->
    <section class="px-10 mt-10 grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-sm">
        <p class="text-sm opacity-60">오늘 수업</p>
        <h2 class="text-3xl font-bold mt-2">1개</h2>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-sm">
        <p class="text-sm opacity-60">미제출 숙제</p>
        <h2 class="text-3xl font-bold mt-2 text-red-500">2개</h2>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-sm">
        <p class="text-sm opacity-60">답변 대기 질문</p>
        <h2 class="text-3xl font-bold mt-2 text-yellow-500">1개</h2>
      </div>
    </section>

    <!-- 오늘 수업 -->
    <section class="px-10 mt-14">
      <h2 class="text-xl font-bold mb-6">📅 오늘 수업</h2>

      <div class="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-sm">
        <div class="flex justify-between items-center flex-col md:flex-row gap-4">
          <div>
            <p class="font-semibold text-lg">공통수학 2</p>
            <p class="text-sm opacity-60 mt-1">19:00 ~ 21:00</p>
            <p class="text-sm opacity-60">김OO 선생님 · 3관 201호</p>
          </div>

          <router-link
            to="/questions"
            class="px-6 py-3 bg-primary text-white rounded-xl text-sm"
          >
            질문하러 가기
          </router-link>
        </div>
      </div>
    </section>

    <!-- 숙제 영역 -->
    <section class="px-10 mt-14">
      <h2 class="text-xl font-bold mb-6">📝 숙제</h2>

      <div class="space-y-4">
        <div class="bg-white dark:bg-gray-800 rounded-2xl p-5 shadow-sm flex justify-between items-center">
          <div>
            <p class="font-medium">RPM p.32~35</p>
            <p class="text-sm text-red-500">D-1</p>
          </div>
          <router-link to="/homework" class="text-primary text-sm">
            확인
          </router-link>
        </div>

        <div class="bg-white dark:bg-gray-800 rounded-2xl p-5 shadow-sm flex justify-between items-center">
          <div>
            <p class="font-medium">함수 단원 문제 10개</p>
            <p class="text-sm text-green-500">D-3</p>
          </div>
          <router-link to="/homework" class="text-primary text-sm">
            확인
          </router-link>
        </div>
      </div>
    </section>

    <!-- 최근 질문 -->
    <section class="px-10 mt-14 mb-20">
      <h2 class="text-xl font-bold mb-6">💬 최근 질문</h2>

      <div class="space-y-4">
        <div class="bg-white dark:bg-gray-800 rounded-2xl p-5 shadow-sm flex justify-between items-center">
          <div>
            <p class="font-medium">함수의 극한이 이해가 안돼요</p>
            <p class="text-sm text-green-500">답변 완료</p>
          </div>
          <router-link to="/questions" class="text-primary text-sm">
            보기
          </router-link>
        </div>

        <div class="bg-white dark:bg-gray-800 rounded-2xl p-5 shadow-sm flex justify-between items-center">
          <div>
            <p class="font-medium">이 문제 왜 이렇게 풀이해요?</p>
            <p class="text-sm text-yellow-500">답변 대기</p>
          </div>
          <router-link to="/questions" class="text-primary text-sm">
            보기
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/store/auth'

const auth = useAuthStore()

const logout = async () => {
  await auth.logout()
}
</script>
