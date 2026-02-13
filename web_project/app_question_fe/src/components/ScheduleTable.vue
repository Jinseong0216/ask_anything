<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow p-6 overflow-x-auto">
    <h3 class="text-lg font-semibold mb-4">시간표</h3>
    <table class="min-w-full text-left text-sm">
      <thead>
        <tr>
          <th class="px-4 py-2 border-b border-gray-300 dark:border-gray-600">시간</th>
          <th class="px-4 py-2 border-b border-gray-300 dark:border-gray-600">과목</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(item, idx) in schedule"
          :key="idx"
          class="hover:bg-gray-50 dark:hover:bg-gray-700 transition"
        >
          <td class="px-4 py-2 border-b border-gray-300 dark:border-gray-600">{{ item.time }}</td>
          <td class="px-4 py-2 border-b border-gray-300 dark:border-gray-600">{{ item.subject }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
// eslint-disable-next-line no-undef
defineProps({
  schedule: Array
})
</script>
