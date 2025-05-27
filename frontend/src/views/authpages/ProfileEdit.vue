<template>
  <div class="profile-category-info">
    <form @submit.prevent="save">
      <label>이메일: <input v-model="form.email" disabled /></label><br />
      <label>닉네임: <input v-model="form.nickname" /></label><br />

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
      <div class="btn">
        <button class="button-back" type="button" @click="$router.back()">취소</button>
        <button class="button-save" type="submit">저장</button>
      </div>
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
  password: '',
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
  if (user) {
    form.email = user.email || ''
    form.nickname = user.nickname || ''
    form.gender = user.gender || ''
    form.salary = user.salary || ''
    form.wealth = user.wealth || ''
    form.tendency = user.tendency || ''
    form.deposit_amount = user.deposit_amount || ''
    form.deposit_period = user.deposit_period || ''
  }
})

const save = async () => {
  try {
    // 1. 프로필 정보 업데이트 (백엔드 URL에 맞춤)
    const profilePayload = {
      email: form.email,
      nickname: form.nickname,
      gender: form.gender,
      salary: form.salary,
      wealth: form.wealth,
      tendency: form.tendency,
      deposit_amount: form.deposit_amount,
      deposit_period: form.deposit_period,
    }

    await axios.put(`${ACCOUNT_API_URL}/myprofile/`, profilePayload, {
      headers: {
        Authorization: `Token ${store.token}`,
      },
    })

    // 2. 비밀번호 변경 요청이 있는 경우

    alert('수정되었습니다!')
    await store.fetchUserInfo() // 수정된 정보로 스토어 업데이트
    router.push({ name: 'ProfilePage' })
  } catch (err) {
    console.error('수정 실패:', err)
    if (err.response?.data) {
      const errors = err.response.data
      if (errors.nickname) {
        alert(`닉네임 오류: ${errors.nickname[0]}`)
      } else {
        alert('수정 중 오류가 발생하였습니다')
      }
    } else {
      alert('수정 중 오류가 발생하였습니다')
    }
  }
}
</script>
<style scoped>
* {
  font-family: Pretendard;
}
.profile-category-info {
  background: #fff;
  padding: 40px;
  border-radius: 20px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
  /* max-width: 600px; */
  width: 100%;
  margin: 40px auto;
}
form label {
  display: block;
  font-weight: 600;
  color: #333;
  margin-bottom: 1.2rem;
}
input,
select {
  border: 1px solid #dcdcdc;
  border-radius: 12px;
  padding: 12px;
  width: 100%;
  max-width: 100%;
  margin-top: 0.4rem;
  font-size: 15px;
  background-color: #fdfdfd;
}
input[disabled] {
  background-color: #f0f0f0;
  color: #888;
}
.button-group {
  margin-top: 2rem;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
.btn {
  display: flex;
  justify-content: end;
  /* width: 100%; */
  gap: 25px;
}
.button-back,
.button-save {
  padding: 10px 20px;
  border: none;
  border-radius: 12px;
  color: white;
  font-weight: bold;
  font-size: 15px;
  cursor: pointer;
  transition: background 0.3s;
}
.button-back {
  background-color: #64748b;
}
.button-save {
  background-color: #191f28;
}
.button-back:hover {
  background-color: #475569;
}
.button-save:hover {
  background-color: #0f172a;
}
</style>
