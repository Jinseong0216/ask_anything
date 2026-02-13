<template>
  <div class="bg-white p-6 rounded-2xl shadow-md max-w-md w-full">
    <h2 class="text-xl font-bold mb-4 text-gray-800">
      강의 등록
    </h2>

    <form @submit.prevent="handleEnroll" class="space-y-4">

      <!-- 초대코드 입력 -->
      <div>
        <label class="block text-sm font-medium text-gray-600 mb-1">
          초대코드
        </label>
        <input
          v-model="inviteCode"
          type="text"
          placeholder="초대코드를 입력하세요"
          class="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 outline-none"
          required
        />
      </div>

      <!-- 버튼 -->
      <button
        type="submit"
        :disabled="loading"
        class="w-full bg-blue-600 text-white py-2 rounded-lg font-medium
               hover:bg-blue-700 transition disabled:opacity-50"
      >
        {{ loading ? "등록 중..." : "등록하기" }}
      </button>

      <!-- 메시지 -->
      <p
        v-if="message"
        class="text-sm text-center mt-2"
        :class="success ? 'text-green-600' : 'text-red-500'"
      >
        {{ message }}
      </p>

    </form>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { lectureApi } from "@/api/lecture"

const inviteCode = ref("")
const loading = ref(false)
const message = ref("")
const success = ref(false)

const handleEnroll = async () => {
  if (!inviteCode.value.trim()) return

  loading.value = true
  message.value = ""

  try {
    await lectureApi.enrollLecture(inviteCode.value.trim())

    success.value = true
    message.value = "강의 등록이 완료되었습니다"
    inviteCode.value = ""

  } catch (err) {
    success.value = false

    if (err.response?.status === 404) {
      message.value = "존재하지 않는 초대코드입니다."
    } else if (err.response?.status === 409) {
      message.value = "이미 등록된 강의입니다."
    } else {
      message.value = "등록 중 오류가 발생했습니다."
    }

  } finally {
    loading.value = false
  }
}
</script>
