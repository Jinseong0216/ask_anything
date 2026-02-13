<template>
  <div class="bg-white dark:bg-gray-800 p-8 rounded-xl shadow text-center">
    <h4 class="text-xl font-bold mb-3">{{ title }}</h4>
    <p class="text-gray-500 dark:text-gray-400">
      {{ desc }}
    </p>
  </div>
</template>

<script setup>
import {defineProps} from 'vue'

defineProps({
  title: String,
  desc: String,
})
</script>
