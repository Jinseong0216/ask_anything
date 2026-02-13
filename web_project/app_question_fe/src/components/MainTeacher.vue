<template>
<div>
  <div class="max-w-md mx-auto mt-10 p-6 bg-white rounded-2xl shadow">
    <h2 class="text-2xl font-bold mb-6 text-center">수업 생성</h2>

    <form @submit.prevent="createLecture">
      <!-- 강의명 -->
      <div class="mb-4">
        <label class="block mb-2 font-semibold">수업 이름</label>
        <input
          v-model="title"
          type="text"
          placeholder="예: 고2 정규반"
          required
          class="w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
      </div>

      <!-- 버튼 -->
      <button
        type="submit"
        :disabled="loading"
        class="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition"
      >
        {{ loading ? "생성 중..." : "수업 생성하기" }}
      </button>
    </form>

    <!-- 결과 표시 -->
    <div v-if="result" class="mt-6 p-4 bg-gray-100 rounded-lg text-sm">
      <p><strong>강의 ID:</strong> {{ result.lecture_id }}</p>
      <p>
        <strong>초대 코드:</strong>
        <span class="text-blue-600 font-bold">{{ result.invite_code }}</span>
      </p>
    </div>

    <!-- 에러 -->
    <p v-if="error" class="mt-4 text-red-500 text-sm">
      {{ error }}
    </p>
  </div>

  <div class="max-w-4xl mx-auto mt-10">
    <h2 class="text-2xl font-bold mb-6">내 수업 목록</h2>

    <div v-if="lectures.length === 0" class="text-gray-500">
      아직 생성한 수업이 없습니다.
    </div>

    <div
      v-for="lecture in lectures"
      :key="lecture.lecture_id"
      class="p-4 mb-4 bg-white rounded-xl shadow flex justify-between items-center"
    >
      <div>
        <div class="font-bold text-lg">{{ lecture.title }}</div>
        <div class="text-sm text-gray-500">
          초대코드: 
          <span class="text-blue-600 font-semibold">
            {{ lecture.invite_code }}
          </span>
        </div>
      </div>

      <router-link
        :to="`/lecture/${lecture.lecture_id}`"
        class="bg-blue-600 text-white px-4 py-2 rounded-lg"
      >
        관리하기
      </router-link>
    </div>
  </div>
</div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { lectureApi } from "@/api/lecture"

const title = ref("")
const loading = ref(false)
const result = ref(null)
const error = ref(null)

const createLecture = async () => {
  if (!title.value.trim()) return

  loading.value = true
  error.value = null
  result.value = null

  try {
    const res = await lectureApi.lectureRegister({
      title: title.value,
    })

    // 백엔드에서
    // { lecture_id: 1, invite_code: "ABCD1234" }
    // 이런 식으로 준다고 가정
    result.value = res.data

    title.value = ""
  } catch (err) {
    console.error(err)
    error.value =
      err.response?.data?.msg || "수업 생성 중 오류가 발생했습니다."
  } finally {
    loading.value = false
  }
}

const lectures = ref([])

onMounted(async () => {
  const res = await lectureApi.getMyLectures()
  lectures.value = res.data
})
</script>
