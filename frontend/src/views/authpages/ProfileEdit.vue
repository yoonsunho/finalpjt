<template>
  <div class="profile-category-info">
    <form @submit.prevent="save">
      <label>이메일: <input v-model="form.email" /></label><br />
      <label>닉네임: <input v-model="form.nickname" /></label><br />
      <label>비밀번호: <input type="password" v-model="form.password1" /></label><br />
      <label>비밀번호 확인: <input type="password" v-model="form.password2" /></label><br />
      <label
        >성별:
        <select v-model="form.gender">
          <option value="">선택하세요</option>
          <option value="M">남성</option>
          <option value="F">여성</option>
        </select> </label
      ><br />
      <label
        >연봉:
        <select v-model="form.salary">
          <option value="">선택하세요</option>
          <option value="under_30m">3천만원 미만</option>
          <option value="30m_50m">3천만원~5천만원</option>
          <option value="50m_100m">5천만원~1억원</option>
          <option value="over_100m">1억원 이상</option>
        </select> </label
      ><br /><label
        >자산 범위:
        <select v-model="form.wealth">
          <option value="">선택하세요</option>
          <option value="under_10m">1천만원 미만</option>
          <option value="10m_30m">1천~3천만원</option>
          <option value="30m_50m">3천~5천만원</option>
          <option value="50m_100m">5천~1억원</option>
          <option value="over_100m">1억원 이상</option>
        </select> </label
      ><br /><label
        >투자 성향:
        <select v-model="form.tendency">
          <option value="">선택하세요</option>
          <option value="safe">안정형</option>
          <option value="neutral">중립형</option>
          <option value="aggressive">공격형</option>
        </select> </label
      ><br /><label
        >희망 저축 금액:
        <select v-model="form.deposit_amount">
          <option value="">선택하세요</option>
          <option value="under_100k">10만원 미만</option>
          <option value="100k_500k">10~50만원</option>
          <option value="500k_1m">50~100만원</option>
          <option value="over_1m">100만원 이상</option>
        </select> </label
      ><br /><label
        >희망 저축 기간:
        <select v-model="form.deposit_period">
          <option value="">선택하세요</option>
          <option value="under_6m">6개월 미만</option>
          <option value="6m_12m">6~12개월</option>
          <option value="1y_2y">1~2년</option>
          <option value="over_2y">2년 이상</option>
        </select> </label
      ><br />
      <button class="button-back" type="button" @click="$router.back()">취소</button>
      <button class="button-save" type="submit">저장</button>
    </form>
  </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/user'
import axios from 'axios'

const router = useRouter()
const ACCOUNT_API_URL = 'http://127.0.0.1:8000/accounts'
const store = useAccountStore()
const form = reactive({
  email: '',
  nickname: '',
  password1: '',
  password2: '',
  gender: '',
  salary: '',
  wealth: '',
  tendency: '',
  deposit_amount: '',
  deposit_period: '',
})

onMounted(() => {
  const user = store.userInfo
  form.email = user.email || ''
  form.nickname = user.nickname || ''
  form.gender = user.gender || ''
  form.salary = user.salary || ''
  form.wealth = user.wealth || ''
  form.tendency = user.tendency || ''
  form.deposit_amount = user.deposit_amount || ''
  form.deposit_period = user.deposit_period || ''
})

const save = async () => {
  await axios({
    method: 'PUT',
    url: `${ACCOUNT_API_URL}/user/`,
    data: form,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((res) => {
      console.log(res.data)
      console.log(res.status)
      alert('수정되었습니다.')
      store.fetchUserInfo()
      router.push({ name: 'ProfilePage' })
    })
    .catch((err) => {
      console.error('수정실패', err)
      alert('수정 중 오류가 발생하였습니다')
    })
}
</script>

<style>
.button-back {
  background-color: dodgerblue;
}
.button-save {
  background-color: #666;
}
input {
  border: 1px solid black;
}
</style>
