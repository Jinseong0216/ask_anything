<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-800 dark:text-white">
    <!-- Header -->
    <header class="flex justify-between items-center px-10 py-6">
      <h1 class="text-2xl font-bold text-primary">AskAnything</h1>

      <div class="flex gap-4">
        <router-link
          to="/login"
          class="px-4 py-2 rounded-lg border hover:bg-gray-100 dark:hover:bg-gray-800"
        >
          로그인
        </router-link>
        <router-link
          to="/register"
          class="px-4 py-2 rounded-lg bg-primary text-white"
        >
          회원가입
        </router-link>
      </div>
    </header>

    <!-- Hero -->
    <section class="flex flex-col items-center text-center mt-24 px-6">
      <h2 class="text-4xl md:text-5xl font-bold leading-tight">
        질문을 남기면,<br />
        답변이 쌓입니다
      </h2>

      <p class="mt-6 text-lg text-gray-500 dark:text-gray-400 max-w-2xl">
        AskAnything은 질문을 기록하고, 답변을 관리하며  
        지식이 자산이 되는 Q&A 플랫폼입니다.
      </p>

      <div class="mt-10 flex gap-4">
        <router-link
          to="/register"
          class="px-6 py-3 bg-primary text-white rounded-xl text-lg"
        >
          지금 시작하기
        </router-link>
        <router-link
          to="/login"
          class="px-6 py-3 border rounded-xl text-lg"
        >
          로그인
        </router-link>
      </div>
    </section>

    <!-- Features -->
    <section class="mt-32 px-10 grid grid-cols-1 md:grid-cols-3 gap-8">
      <FeatureCard
        title="질문 관리"
        desc="질문을 카테고리별로 정리하고 언제든 다시 확인할 수 있습니다."
      />
      <FeatureCard
        title="답변 기록"
        desc="단순한 답변이 아닌, 축적되는 지식으로 관리하세요."
      />
      <FeatureCard
        title="안전한 인증"
        desc="JWT 기반 인증으로 개인 데이터는 안전하게 보호됩니다."
      />
    </section>

    <!-- CTA -->
    <section class="mt-32 bg-primary text-white py-20 text-center">
      <h3 class="text-3xl font-bold">
        지금 질문을 시작해보세요
      </h3>
      <p class="mt-4 text-lg opacity-90">
        계정 생성은 1분이면 충분합니다
      </p>
      <router-link
        to="/register"
        class="inline-block mt-8 px-8 py-4 bg-white text-primary font-semibold rounded-xl"
      >
        무료로 시작하기
      </router-link>
    </section>

    <!-- Footer -->
    <footer class="py-10 text-center text-gray-500 dark:text-gray-400">
      © 2026 AskAnything. All rights reserved.
    </footer>
  </div>
</template>

<script setup>
import FeatureCard from "@/components/FeatureCard.vue"
</script>
