<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow p-6">
    <h3 class="text-lg font-semibold mb-4">숙제</h3>
    <ul class="space-y-2">
      <li
        v-for="(hw, idx) in homeworks"
        :key="idx"
        class="flex justify-between p-2 bg-gray-50 dark:bg-gray-700 rounded hover:bg-gray-100 dark:hover:bg-gray-600 transition"
      >
        <span>{{ hw.title }}</span>
        <span class="text-sm text-gray-500 dark:text-gray-300">마감: {{ hw.due }}</span>
      </li>
    </ul>
  </div>
</template>

<script setup>
// eslint-disable-next-line no-undef
defineProps({
  homeworks: Array
})
</script>
