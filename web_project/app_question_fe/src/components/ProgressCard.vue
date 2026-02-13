<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow p-4">
    <h4 class="text-sm font-semibold mb-2">{{ props.title }}</h4>
    <div class="w-full h-3 bg-gray-200 dark:bg-gray-700 rounded-full">
      <div
        class="h-3 rounded-full"
        :class="progressBarColor"
        :style="{ width: props.progress * 100 + '%' }"
      ></div>
    </div>
    <p class="mt-1 text-xs text-gray-500 dark:text-gray-300">{{ Math.round(props.progress*100) }}%</p>
  </div>
</template>

<script setup>
import { computed } from "vue"

// eslint-disable-next-line no-undef
const props = defineProps({
  title: String,
  progress: Number,
  color: { type: String, default: "blue" }
})

const progressBarColor = computed(() => {
  switch (props.color) {
    case "green": return "bg-green-500"
    case "red": return "bg-red-500"
    default: return "bg-blue-500"
  }
})
</script>
