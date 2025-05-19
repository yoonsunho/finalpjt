<template>
  <div>
    <input v-model="email" placeholder="이메일" />
    <input v-model="password" placeholder="비밀번호" type="password" />
    <button @click="login">로그인</button>
    <p>{{ result }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const email = ref('')
const password = ref('')
const result = ref('')

const login = async () => {
  try {
    const res = await axios.post('/api/accounts/login/', {
      email: email.value,
      password: password.value
    })
    result.value = res.data.message
  } catch (err) {
    result.value = JSON.stringify(err.response.data)
  }
}
</script>
