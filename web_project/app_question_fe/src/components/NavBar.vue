<template>
  <header
    class="h-14 flex items-center px-4 bg-white border-b border-zinc-200 relative"
  >
    <!-- 로고 -->
    <div class="flex items-center gap-2 pr-4 border-r border-zinc-200">
      <router-link to="/"><img :src="logo" alt="Qube" class="h-8" /></router-link>
    </div>

    <!-- 데스크탑 메뉴 -->
    <nav class="hidden md:flex items-center gap-2 ml-6">
      <NavBtn to="/" label="대시보드" />
      <NavBtn to="/" label="시간표" />
      <NavBtn to="/" label="숙제" />
      <NavBtn to="/" label="질문함" />
      <NavBtn to="/" label="자료실" />
    </nav>

    <div class="flex-1" />

    <!-- 우측 아이콘 영역 -->
    <div class="flex items-center gap-2">
      <!-- 이름 + 역할 배지 (데스크탑에서만 표시) -->
      <div
        class="hidden md:flex items-center gap-2 px-3 py-1 bg-zinc-50 rounded-full border border-zinc-200"
      >
        <span class="font-semibold text-zinc-900">{{ auth.user.user_name }}</span>
        <span
          class="text-xs px-2 py-0.5 rounded-full font-medium"
          :class="{
            'bg-blue-100 text-blue-800': auth.user.role === 'student',
            'bg-green-100 text-green-800': auth.user.role === 'teacher'
          }"
        >
          {{ auth.user.role === 'student' ? '학생' : '선생' }}
        </span>
      </div>

      <!-- 전체 메뉴 버튼 (모바일 + 데스크탑 공통) -->
      <button
        @click="toggleMenu"
        class="w-9 h-9 flex items-center justify-center rounded hover:bg-zinc-100 transition"
      >
        ☰
      </button>

      <!-- 마이페이지 버튼 -->
      <router-link
        to=""
        class="w-9 h-9 flex items-center justify-center rounded-full hover:bg-zinc-100 transition"
      >
        👤
      </router-link>
    </div>

    <!-- 사이드 전체 메뉴 (Drawer) -->
    <transition name="slide">
      <div
        v-if="menuOpen"
        class="fixed top-0 right-0 w-64 h-full bg-white shadow-lg border-l border-zinc-200 z-50 p-6 flex flex-col"
      >
        <!-- 헤더 -->
        <div class="flex justify-between items-center mb-6">
          <h2 class="font-semibold text-lg">전체 메뉴</h2>
          <button @click="toggleMenu" class="text-zinc-500 hover:text-zinc-900">✕</button>
        </div>

        <!-- 메뉴 링크 -->
        <div class="flex-1 flex flex-col gap-4 text-sm">
          <router-link @click="toggleMenu" to="/">대시보드</router-link>
          <router-link @click="toggleMenu" to="/">시간표</router-link>
          <router-link @click="toggleMenu" to="/">숙제</router-link>
          <router-link @click="toggleMenu" to="/">질문함</router-link>
          <router-link @click="toggleMenu" to="/">자료실</router-link>
          <router-link @click="toggleMenu" to="/">마이페이지</router-link>
        </div>

        <!-- 로그아웃 버튼 (맨 아래 고정) -->
        <button
          @click="logout"
          class="mt-4 px-4 py-2 text-sm text-zinc-700 hover:bg-zinc-100 rounded transition text-left w-full"
        >
          로그아웃
        </button>
      </div>
    </transition>


    <!-- 어두운 배경 -->
    <div
      v-if="menuOpen"
      @click="toggleMenu"
      class="fixed inset-0 bg-black/30 z-40"
    />
  </header>
</template>

<script setup>
import NavBtn from "@/components/NavBtn.vue"
import { ref } from "vue"
import { useAuthStore } from "@/store/auth.js"
import logo from "@/assets/neoMath.png"


const auth = useAuthStore()
const logout = async () => {
  await auth.logout()
}

const menuOpen = ref(false)

const toggleMenu = () => {
  menuOpen.value = !menuOpen.value
}

</script>

<style>
.slide-enter-from {
  transform: translateX(100%);
}
.slide-enter-active {
  transition: transform 0.2s ease;
}
.slide-leave-to {
  transform: translateX(100%);
}
.slide-leave-active {
  transition: transform 0.2s ease;
}
</style>
