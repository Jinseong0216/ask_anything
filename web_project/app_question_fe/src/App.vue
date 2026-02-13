<template>
  <div id="app">
    <!-- 네비바: 현재 경로가 login/register이 아니면 보임 -->
    <NavBar v-if="showNavBar" />
    <main class="content">
      <!-- 라우터가 렌더링되는 위치 -->
      <router-view />
    </main>
  </div>
</template>
<script setup>
/*
  App.vue는 레이아웃 역할만 함
  페이지 전환은 router-view에서 처리
*/

import { computed } from "vue"
import { useRoute } from "vue-router"
import { useAuthStore } from "@/store/auth"
import NavBar from "@/components/NavBar.vue"

const auth = useAuthStore()
auth

const route = useRoute()

// 로그인/회원가입 페이지에서 네비바 숨기기
const showNavBar = computed(() => {
  return !["/login", "/register", "/test"].includes(route.path)
})

</script>

<style>
#app {
  display: flex;
  flex-direction: column;
  height: 100vh;
  font-family: Avenir, Helvetica, Arial, sans-serif;
}

/* 상단 네비바 */
nav {
  position: sticky;
  top: 0;
  z-index: 100;
}

/* 라우터뷰 콘텐츠 영역 */
.content {
  flex: 1;          /* 남은 공간 채우기 */
  overflow-y: auto; /* 스크롤 가능 */
}
</style>