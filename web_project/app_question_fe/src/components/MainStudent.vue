<template>
    <div>
        <!-- 상단 2컬럼: 진행정보 / 오늘 할 일 -->
        <section class="max-w-7xl mx-auto px-4 grid grid-cols-1 lg:grid-cols-2 gap-6 mb-4">

            <!-- 왼쪽: 학생 레벨 + 진행도 -->
            <div class="space-y-6">
                <StudentLevelCard :level="student.level" :progress="student.progress" />
                <ProgressCard title="숙제 이행률" :progress="0.8" color="blue"/>
                <ProgressCard title="출석률" :progress="0.95" color="green"/>
            </div>

            <!-- 오른쪽: 오늘 할 일 -->
            <div class="space-y-4">
                <TodayLesson :lessons="todayLessons" />
                <TodoCard :tasks="todayTodos" />
            </div>

        </section>

        <!-- 하단: 시간표 / 기타 카드 -->
        <section class="max-w-7xl mx-auto px-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-6">
          <ScheduleTable :schedule="schedule" />
          <HomeworkList :homeworks="homeworks" />
          <PerformanceChart :data="performanceData" />
        </section>
        <EnrollmentForm />
    </div>
</template>

<script setup>
import { useAuthStore } from "@/store/auth"
import StudentLevelCard from "@/components/StudentLevelCard.vue"
import TodayLesson from "@/components/TodayLesson.vue"
import HomeworkList from "@/components/HomeworkList.vue"
import ScheduleTable from "@/components/ScheduleTable.vue"

// 추가 컴포넌트
import EnrollmentForm from "@/components/EnrollmentForm.vue"
import ProgressCard from "@/components/ProgressCard.vue"
import TodoCard from "@/components/TodoCard.vue"
import PerformanceChart from "@/components/PerformanceChart.vue"

const auth = useAuthStore()
auth

// 샘플 데이터
const student = { level: 3, progress: 0.65 }

const todayLessons = [
  { subject: "수학", time: "10:00 ~ 11:00", teacher: "김선생님" },
  { subject: "영어", time: "11:30 ~ 12:30", teacher: "이선생님" },
]

const todayTodos = [
  { title: "수학 숙제 제출", done: false },
  { title: "영어 단어 암기", done: true },
  { title: "과학 프로젝트 준비", done: false },
]

const homeworks = [
  { title: "수학 숙제 1", due: "2026-02-12" },
  { title: "영어 숙제 2", due: "2026-02-13" },
]

const schedule = [
  { time: "09:00", subject: "수학" },
  { time: "10:00", subject: "영어" },
  { time: "11:00", subject: "과학" },
]

const performanceData = [
  { subject: "수학", score: 85 },
  { subject: "영어", score: 90 },
  { subject: "과학", score: 78 },
]
</script>
