<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-800 dark:text-white">

    <!-- 상단 네비 / 관리자 버튼 -->
    <div class="max-w-7xl mx-auto px-6 py-4 flex justify-end">
      <router-link
        v-if="auth.user && auth.user.auth_level === 'admin'"
        to="/admin"
        class="flex items-center gap-2 text-sm font-medium text-zinc-600 hover:text-zinc-900 hover:bg-zinc-100 rounded px-3 py-2 transition"
      >
        {{ auth.user.name }} (관리자)
        <span>관리자 대시보드</span>
      </router-link>
    </div>

    <!-- MainTeacher 또는 MainStudent -->
    <component :is="currentComponent" />

    <TheFooter />
  </div>
</template>

<script setup>
import { computed } from "vue"
import { useAuthStore } from "@/store/auth"
import MainStudent from "@/components/MainStudent.vue"
import MainTeacher from "@/components/MainTeacher.vue"
import TheFooter from "@/components/TheFooter.vue"


const auth = useAuthStore()

const currentComponent = computed(() => {
  if (auth.user?.role === "student") return MainStudent
  if (auth.user?.role === "teacher") return MainTeacher
  return null
})

</script>
