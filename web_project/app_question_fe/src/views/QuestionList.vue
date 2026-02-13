<template>
  <div>
    <h2>질문 목록</h2>
    <div v-for="q in questions" :key="q.id">
      {{ q.title }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const questions = ref([])

onMounted(async () => {
  const res = await axios.get('/api/questions')
  questions.value = res.data
})
</script>
