<template>
  <div class="signup-container">
    <h2>회원가입</h2>
    <form @submit.prevent="onSignUp">
      <div class="form-group">
        <label for="email">이메일</label>
        <input
          type="email"
          id="email"
          v-model="email"
          @input="
            () => {
              errors.email = ''
            }
          "
          required
        />
        <button type="button" @click="checkEmailDuplicate">중복확인</button>
        <div v-if="emailCheckMessage" :class="{ error: !isEmailAvailable }">
          {{ emailCheckMessage }}
        </div>
        <div v-if="errors.email" class="error">{{ errors.email }}</div>
      </div>

      <div class="form-group">
        <label for="nickname">닉네임</label>
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
        <button type="button" @click="checkNicknameDuplicate">중복확인</button>
        <div v-if="nicknameCheckMessage" :class="{ error: !isNicknameAvailable }">
          {{ nicknameCheckMessage }}
        </div>
        <div v-if="errors.nickname" class="error">{{ errors.nickname }}</div>
      </div>

      <div class="form-group">
        <label for="password1">비밀번호</label>
        <input type="password" id="password1" v-model="password1" required />
        <div class="password-rules">
          <ul>
            <li>최소 8자 이상</li>
            <li>숫자, 영문자, 특수문자 조합 권장</li>
            <li>너무 쉬운 비밀번호(예: 123456, password 등) 불가</li>
          </ul>
        </div>
        <div v-if="errors.password1" class="error">{{ errors.password1 }}</div>
      </div>

      <div class="form-group">
        <label for="password2">비밀번호 확인</label>
        <input type="password" id="password2" v-model="password2" required />
        <div v-if="errors.password2" class="error">{{ errors.password2 }}</div>
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

      <button type="submit">회원가입</button>
      <!-- <div v-if="errors.non_field_errors" class="error general-error">
        {{ errors.non_field_errors }}
      </div> -->
    </form>
    <div class="login-link">
      이미 계정이 있으신가요?
      <RouterLink :to="{ name: 'LoginView' }" class="login-link-text">로그인</RouterLink>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAccountStore } from '@/stores/user'
import { useRouter, RouterLink } from 'vue-router'
const router = useRouter()
const accountStore = useAccountStore()
const { ACCOUNT_API_URL } = accountStore

const email = ref('')
const nickname = ref('')
const password1 = ref('')
const password2 = ref('')
const gender = ref('')
const salary = ref('')
const wealth = ref('')
const tendency = ref('')
const deposit_amount = ref('')
const deposit_period = ref('')

const errors = ref({})

const emailCheckMessage = ref('')
const isEmailAvailable = ref(false)

// 이메일 중복 확인
const checkEmailDuplicate = async () => {
  const isValidEmail = (email) => {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return regex.test(email)
  }
  // 먼저 형식 검사
  if (!isValidEmail(email.value)) {
    errors.value.email = '이메일 형식이 올바르지 않습니다.'
    emailCheckMessage.value = ''
    isEmailAvailable.value = false
    return
  }
  // 이메일 형식이 맞는 경우 에러 초기화
  errors.value.email = ''
  // 형식 맞으면 서버에 요청해서 중복검사
  try {
    const res = await fetch(`${ACCOUNT_API_URL}/check-email/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email.value }),
    })
    const data = await res.json()
    if (data.available) {
      emailCheckMessage.value = '사용 가능한 이메일입니다.'
      isEmailAvailable.value = true
      errors.value.email = ''
    } else {
      emailCheckMessage.value = '이미 사용 중인 이메일입니다.'
      isEmailAvailable.value = false
    }
  } catch (err) {
    emailCheckMessage.value = '중복 확인 중 오류가 발생했습니다.'
    isEmailAvailable.value = false
  }
}

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

const onSignUp = async function () {
  //비동기 처리 해주기

  errors.value = {}

  // 비밀번호 일치 검사
  if (password1.value !== password2.value) {
    errors.value.password2 = '비밀번호가 일치하지 않습니다.'
    return
  }

  // 이메일,닉네임 중복 확인이 안 되었거나 사용 불가일 때
  if (!isEmailAvailable.value) {
    errors.value.email = '이메일 중복 확인을 해주세요.'
    return
  }

  if (!isNicknameAvailable.value) {
    errors.value.nickname = '닉네임 중복 확인을 해주세요.'
    return
  }

  const userInfo = {
    email: email.value,
    nickname: nickname.value,
    password1: password1.value,
    password2: password2.value,
    gender: gender.value,
    salary: salary.value,
    wealth: wealth.value,
    tendency: tendency.value,
    deposit_amount: deposit_amount.value,
    deposit_period: deposit_period.value,
  }
  try {
    await accountStore.signUp(userInfo)
    router.push({ name: 'SignUpSuccessView' })
  } catch (err) {
    if (err.response && err.response.data) {
      const data = err.response.data
      if (data.password1) {
        errors.value.password1 = Array.isArray(data.password1)
          ? data.password1.join(' ')
          : data.password1
      }
      if (data.password2) {
        errors.value.password2 = Array.isArray(data.password2)
          ? data.password2.join(' ')
          : data.password2
      }
      if (data.email) {
        errors.value.email = Array.isArray(data.email) ? data.email.join(' ') : data.email
      }
      if (data.nickname) {
        errors.value.nickname = Array.isArray(data.nickname)
          ? data.nickname.join(' ')
          : data.nickname
      }
    }
  }
}
</script>

<style scoped>
.signup-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

h2 {
  text-align: center;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input,
select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #2196f3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  margin-top: 10px;
}

button:hover {
  background-color: #2574e6;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.error {
  color: red;
  font-size: 12px;
  margin-top: 5px;
}

.general-error {
  margin: 10px 0;
  text-align: center;
}

.login-link {
  text-align: center;
  margin-top: 20px;
}

.login-link-text {
  color: red;
}

a {
  color: #2196f3;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>
