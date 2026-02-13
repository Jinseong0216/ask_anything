<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow p-4 space-y-4">
    <h3 class="text-sm font-semibold text-gray-700 dark:text-gray-200">학생 레벨</h3>

    <!-- 레벨 + 경험치 -->
    <div>
      <div class="flex justify-between mb-1">
        <span>레벨 {{ level }}</span>
        <span>{{ Math.round(progress*100) }}%</span>
      </div>
      <div class="w-full h-3 bg-gray-200 dark:bg-gray-700 rounded-full">
        <div
          class="h-3 rounded-full bg-blue-500"
          :style="{ width: progress * 100 + '%' }"
        ></div>
      </div>
    </div>

    <!-- 숙제 이행률 -->
    <div>
      <div class="flex justify-between mb-1 text-xs">
        <span>숙제 이행률</span>
        <span>{{ Math.round(homeworkProgress*100) }}%</span>
      </div>
      <div class="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-full">
        <div class="h-2 rounded-full bg-green-500" :style="{ width: homeworkProgress*100 + '%' }"></div>
      </div>
    </div>

    <!-- 출석률 -->
    <div>
      <div class="flex justify-between mb-1 text-xs">
        <span>출석률</span>
        <span>{{ Math.round(attendance*100) }}%</span>
      </div>
      <div class="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-full">
        <div class="h-2 rounded-full bg-indigo-500" :style="{ width: attendance*100 + '%' }"></div>
      </div>
    </div>

    <!-- 간단한 막대 그래프 (최근 7일 숙제/출석) -->
    <div class="mt-4">
      <h4 class="text-xs font-semibold mb-1 text-gray-600 dark:text-gray-300">최근 진행</h4>
      <div class="flex items-end gap-1 h-16">
        <div
          v-for="(val, idx) in weeklyProgress"
          :key="idx"
          class="w-3 bg-blue-400 rounded"
          :style="{ height: val*100 + '%' }"
          :title="val*100 + '%'"
        ></div>
      </div>
      <div class="flex justify-between text-[10px] mt-1 text-gray-500 dark:text-gray-400">
        <span v-for="d in weekDays" :key="d">{{ d }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
// eslint-disable-next-line no-undef
defineProps({
  level: Number,
  progress: Number,
  homeworkProgress: { type: Number, default: 0.75 },
  attendance: { type: Number, default: 0.9 },
  weeklyProgress: { type: Array, default: () => [0.6,0.7,0.8,0.5,0.9,0.85,0.7] },
  weekDays: { type: Array, default: () => ['월','화','수','목','금','토','일'] }
})
</script>
