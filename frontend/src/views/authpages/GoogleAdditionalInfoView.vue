<template>
  <div class="signup-container">
    <h2>추가 정보 기입</h2>
    <form @submit.prevent="onSubmit">
      <div class="form-group">
        <label for="nickname">닉네임</label>
        <div class="input-with-button">
          <input
            type="text"
            id="nickname"
            v-model="nickname"
            @input="
              () => {
                errors.nickname = ''
              }
            "
            required
          />
          <button type="button" class="check-btn" @click="checkNicknameDuplicate">중복확인</button>
        </div>
        <div v-if="nicknameCheckMessage" :class="{ error: !isNicknameAvailable }">
          {{ nicknameCheckMessage }}
        </div>
        <div v-if="errors.nickname" class="error">{{ errors.nickname }}</div>
      </div>

      <div class="form-group">
        <label for="gender">성별</label>
        <select id="gender" v-model="gender" required>
          <option value="">선택하세요</option>
          <option value="M">남성</option>
          <option value="F">여성</option>
        </select>
      </div>

      <!-- 연봉 -->
      <div class="form-group">
        <label for="salary">연봉</label>
        <select id="salary" v-model="salary" required>
          <option value="">선택하세요</option>
          <option value="under_30m">3천만원 미만</option>
          <option value="30m_50m">3천만원~5천만원</option>
          <option value="50m_100m">5천만원~1억원</option>
          <option value="over_100m">1억원 이상</option>
        </select>
      </div>

      <!-- 자산 범위 -->
      <div class="form-group">
        <label for="wealth">자산 범위</label>
        <select id="wealth" v-model="wealth" required>
          <option value="">선택하세요</option>
          <option value="under_10m">1천만원 미만</option>
          <option value="10m_30m">1천~3천만원</option>
          <option value="30m_50m">3천~5천만원</option>
          <option value="50m_100m">5천~1억원</option>
          <option value="over_100m">1억원 이상</option>
        </select>
      </div>

      <div class="form-group">
        <label for="tendency">투자 성향</label>
        <select id="tendency" v-model="tendency" required>
          <option value="">선택하세요</option>
          <option value="safe">안정형</option>
          <option value="neutral">중립형</option>
          <option value="aggressive">공격형</option>
        </select>
      </div>

      <!-- 희망 저축 금액 -->
      <div class="form-group">
        <label for="deposit_amount">희망 저축 금액</label>
        <select id="deposit_amount" v-model="deposit_amount" required>
          <option value="">선택하세요</option>
          <option value="under_100k">10만원 미만</option>
          <option value="100k_500k">10~50만원</option>
          <option value="500k_1m">50~100만원</option>
          <option value="over_1m">100만원 이상</option>
        </select>
      </div>

      <!-- 희망 저축 기간 -->
      <div class="form-group">
        <label for="deposit_period">희망 저축 기간</label>
        <select id="deposit_period" v-model="deposit_period" required>
          <option value="">선택하세요</option>
          <option value="under_6m">6개월 미만</option>
          <option value="6m_12m">6~12개월</option>
          <option value="1y_2y">1~2년</option>
          <option value="over_2y">2년 이상</option>
        </select>
      </div>

      <div class="submit-btn-wrapper">
        <button type="submit">제출</button>
      </div>
    </form>
    <div class="login-link">
      이미 계정이 있으신가요?
      <RouterLink :to="{ name: 'LoginView' }" class="login-link-text">로그인</RouterLink>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import { useAccountStore } from '@/stores/user'
const accountStore = useAccountStore()
const { ACCOUNT_API_URL } = accountStore

const route = useRoute()
const router = useRouter()
const token = route.query.token // 구글 로그인에서 받은 토큰

const nickname = ref('')
const gender = ref('')
const salary = ref('')
const wealth = ref('')
const tendency = ref('')
const deposit_amount = ref('')
const deposit_period = ref('')

const errors = ref({})

// 닉네임 중복 확인
const nicknameCheckMessage = ref('')
const isNicknameAvailable = ref(false)

const checkNicknameDuplicate = async () => {
  try {
    const res = await fetch(`${ACCOUNT_API_URL}/check-nickname/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nickname: nickname.value }),
    })
    const data = await res.json()
    if (data.available) {
      nicknameCheckMessage.value = '사용 가능한 닉네임입니다.'
      isNicknameAvailable.value = true
      errors.value.nickname = ''
    } else {
      nicknameCheckMessage.value = '이미 사용 중인 닉네임입니다.'
      isNicknameAvailable.value = false
    }
  } catch (err) {
    nicknameCheckMessage.value = '중복 확인 중 오류가 발생했습니다.'
    isNicknameAvailable.value = false
  }
}

const onSubmit = async () => {
  //비동기 처리 해주기

  errors.value = {}

  if (!isNicknameAvailable.value) {
    errors.value.nickname = '닉네임 중복 확인을 해주세요.'
    return
  }

  try {
    const response = await axios.post(
      `${ACCOUNT_API_URL}/complete-social-signup/`,
      {
        nickname: nickname.value,
        gender: gender.value,
        salary: salary.value,
        wealth: wealth.value,
        tendency: tendency.value,
        deposit_amount: deposit_amount.value,
        deposit_period: deposit_period.value,
      },
      {
        headers: { Authorization: `Token ${token}` },
      },
    )
    // console.log('성공응답:',response.data)
    // ✅ 1. 토큰을 Pinia store에 저장 (이미 있다면 생략 가능)
    accountStore.token = token

    // ✅ 2. 사용자 정보 불러오기
    await accountStore.fetchUserInfo()
    router.push({ name: 'MainPage' })
  } catch (err) {
    // console.log('에러 전체:',err)
    // console.log('에러 응답 데이터:',err.response?.data)
    if (err.response?.data?.detail) {
      alert(err.response.data.detail)
      // const data = err.response.data

      // if (data.nickname) {
      // errors.value.nickname = Array.isArray(data.nickname)
      //   ? data.nickname.join(' ')
      //   : data.nickname
      // }
    }
  }
}
</script>

<style scoped>
.signup-container {
  max-width: 500px;
  margin: 0 auto;
  padding: 32px 24px;
  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

h2 {
  text-align: center;
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 32px;
}

.form-group {
  margin-bottom: 24px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

input,
select {
  width: 100%;
  padding: 12px 16px;
  font-size: 14px;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  background-color: #fafafa;
  transition: border 0.2s ease;
}

input:focus,
select:focus {
  border-color: #007aff;
  outline: none;
  background-color: #fff;
}

.input-with-button {
  display: flex;
  gap: 8px;
}

.input-with-button input {
  flex: 1;
}

.check-btn {
  padding: 12px 16px;
  font-size: 14px;
  border-radius: 12px;
  background-color: #f2f3f5;
  color: #333;
  border: none;
  transition: background-color 0.2s ease;
}

.check-btn:hover {
  background-color: #e4e6ea;
}

.submit-btn-wrapper {
  text-align: center;
  width: 100%;
  margin-top: 32px;
}

.submit-btn-wrapper button {
  padding: 12px 24px;
  width: 100%;
  font-size: 16px;
  background-color: #007aff;
  color: white;
  border-radius: 12px;
  border: none;
  transition: background-color 0.2s ease;
}

.submit-btn-wrapper button:hover {
  background-color: #005fcc;
}

button:disabled {
  background-color: #dcdcdc;
  color: #999;
  cursor: not-allowed;
}

.error {
  color: #ff3b30;
  font-size: 13px;
  margin-top: 6px;
}

.login-link {
  text-align: center;
  margin-top: 40px;
  font-size: 14px;
}

.login-link-text {
  color: #007aff;
  font-weight: 500;
  margin-left: 4px;
}

a {
  color: #007aff;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>
