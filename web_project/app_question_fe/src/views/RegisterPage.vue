<template>
  <div class="register">
    <h2>회원가입</h2>

    <form @submit.prevent="submit">
      <input
        v-model.trim="form.login_id"
        placeholder="아이디"
        autocomplete="username"
      />
      <input
        v-model.trim="form.user_name"
        placeholder="이름"
      />
      <input
        v-model.trim="form.email"
        type="email"
        placeholder="이메일"
        autocomplete="email"
      />
      <input
        v-model="form.password"
        type="password"
        placeholder="비밀번호"
        autocomplete="new-password"
      />
      <input
        v-model="passwordConfirm"
        type="password"
        placeholder="비밀번호 확인"
        autocomplete="new-password"
      />

      <button type="submit" :disabled="auth.loading">
        가입
      </button>

      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/store/auth"

const router = useRouter()
const auth = useAuthStore()

const error = ref("")
const form = ref({
  login_id: "",
  user_name: "",
  email: "",
  password: ""
})
const passwordConfirm = ref("")

const submit = async () => {
  error.value = ""

  if (!form.value.login_id || !form.value.password) {
    error.value = "필수 항목을 입력하세요"
    return
  }

  if (form.value.password.length < 8) {
    error.value = "비밀번호는 8자 이상이어야 합니다"
    return
  }

  if (form.value.password !== passwordConfirm.value) {
    error.value = "비밀번호가 일치하지 않습니다"
    return
  }

  try {
    // store를 통해 signup 호출
    const res = await auth.register(form.value)
    if (res?.msg === 'registered') {
      router.push({ name: "login" })
      console.log("성공", res)
    }
  } catch (err) {
    err.value = useAuthStore.error
    console.log("실패", err)
  }
}

</script>

<style scoped>
.register {
  max-width: 400px;
  margin: auto;
}

input {
  display: block;
  margin-bottom: 12px;
  width: 100%;
  padding: 8px;
}

button {
  padding: 8px 16px;
}

.error {
  color: red;
}
</style>
