<template>
  <div>
    <input v-model="form.email" placeholder="이메일" />
    <input v-model="form.password" placeholder="비밀번호" type="password" />
    <input v-model="form.nickname" placeholder="닉네임" />
    <input v-model="form.gender" placeholder="성별(1 or 2)" />
    <input v-model="form.salary" placeholder="연봉(1~5)" />
    <input v-model="form.wealth" placeholder="자산(1~5)" />
    <input v-model="form.tendency" placeholder="성향(1~3)" />
    <input v-model="form.deposit_amount" placeholder="저축 금액" />
    <input v-model="form.deposit_period" placeholder="저축 기간" />
    <button @click="signup">가입하기</button>
    <p>{{ result }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const form = ref({
  email: '',
  password: '',
  nickname: '',
  gender: '',
  salary: '',
  wealth: '',
  tendency: '',
  deposit_amount: '',
  deposit_period: '',
})

const result = ref('')

const signup = async () => {
  try {
    const res = await axios.post('/api/accounts/signup/', form.value)
    result.value = res.data.message
  } catch (err) {
    result.value = JSON.stringify(err.response.data)
  }
}
</script>
