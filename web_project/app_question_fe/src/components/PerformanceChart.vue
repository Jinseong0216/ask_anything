<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow p-4">
    <h4 class="text-sm font-semibold mb-2">최근 성과</h4>
    <div class="w-full h-32 flex items-end gap-2">
      <div
        v-for="(d, idx) in data"
        :key="idx"
        class="bg-blue-500 rounded-b"
        :style="{ height: d.score + '%' }"
        :title="d.subject + ': ' + d.score + '%'">
      </div>
    </div>
    <div class="flex justify-between text-xs mt-2">
      <span v-for="d in data" :key="d.subject">{{ d.subject }}</span>
    </div>
  </div>
</template>

<script setup>
// eslint-disable-next-line no-undef
defineProps({
  data: Array
})
</script>
