<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow p-4">
    <h4 class="text-sm font-semibold mb-2">오늘 할 일</h4>
    <ul class="space-y-2">
      <li
        v-for="(task, idx) in tasks"
        :key="idx"
        class="flex items-center justify-between p-2 bg-gray-50 dark:bg-gray-700 rounded hover:bg-gray-100 dark:hover:bg-gray-600 transition"
      >
        <span :class="{ 'line-through text-gray-400': task.done }">{{ task.title }}</span>
        <input type="checkbox" v-model="task.done" class="accent-blue-500">
      </li>
    </ul>
  </div>
</template>

<script setup>
// eslint-disable-next-line no-undef
defineProps({
  tasks: Array
})
</script>
