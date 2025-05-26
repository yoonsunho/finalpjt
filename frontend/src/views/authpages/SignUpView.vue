<template>
  <div class="signup-wrapper">
    <h2>회원가입</h2>
    <div class="signup-container">
      <div ref="formContainer" class="">
        <form @submit.prevent="onSignUp">
          <!-- STEP 1 -->
          <div v-if="step === 1">
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
                  <li>너무 쉬운 비밀번호 불가</li>
                </ul>
              </div>
              <div v-if="errors.password1" class="error">{{ errors.password1 }}</div>
            </div>

            <div class="form-group">
              <label for="password2">비밀번호 확인</label>
              <input type="password" id="password2" v-model="password2" required />
              <div v-if="errors.password2" class="error">{{ errors.password2 }}</div>
            </div>

            <button type="button" @click="goToStep2">다음</button>
          </div>

          <!-- STEP 2 -->
          <div v-else-if="step === 2">
            <div class="form-group">
              <label for="gender">성별</label>
              <select id="gender" v-model="gender" required>
                <option value="">선택하세요</option>
                <option value="M">남성</option>
                <option value="F">여성</option>
              </select>
            </div>

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

            <div class="form-group">
              <label for="wealth">자산</label>
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

            <div class="button-group">
              <button type="button" @click="goToStep1">이전</button>
              <button type="submit">회원가입</button>
            </div>
          </div>
          <!-- STEP 3 -->
          <div v-else-if="step === 3" class="complete-message">
            <h2>회원가입이 완료되었습니다!</h2>
            <p>이제 로그인하여 서비스를 이용하실 수 있어요.</p>
            <button class="primary-btn" @click="router.push({ name: 'LoginView' })">
              로그인하러 가기
            </button>
          </div>
        </form>
      </div>
    </div>
    <div class="progress-bar">
      <div class="progress" :style="{ width: `${(step / 3) * 100}%` }"></div>
    </div>
  </div>
</template>
<script setup>
import { ref, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import gsap from 'gsap'
import { useAccountStore } from '@/stores/user'
import { useRouter, RouterLink } from 'vue-router'
import GoogleLoginButton from '@/components/GoogleLoginButton.vue'
const router = useRouter()
const accountStore = useAccountStore()
const { ACCOUNT_API_URL } = accountStore

const step = ref(1) // <-- 여기가 빠져있어서 warning 발생했던 거야!
const formContainer = ref(null)

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
const nicknameCheckMessage = ref('')
const isNicknameAvailable = ref(false)

const animateStepChange = () => {
  if (!formContainer.value) return
  gsap.fromTo(
    formContainer.value,
    { opacity: 0, x: 50 },
    { opacity: 1, x: 0, duration: 0.5, ease: 'power2.out' },
  )
}

watch(step, () => nextTick(animateStepChange))

const goToStep2 = () => {
  errors.value = {}
  if (!email.value || !nickname.value || !password1.value || !password2.value) {
    errors.value.email = '모든 필드를 입력해주세요.'
    return
  }
  if (!isEmailAvailable.value) {
    errors.value.email = '이메일 중복 확인을 해주세요.'
    return
  }
  if (!isNicknameAvailable.value) {
    errors.value.nickname = '닉네임 중복 확인을 해주세요.'
    return
  }
  if (password1.value !== password2.value) {
    errors.value.password2 = '비밀번호가 일치하지 않아요.'
    return
  }
  step.value = 2
}

const goToStep1 = () => {
  step.value = 1
}

const checkEmailDuplicate = async () => {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!regex.test(email.value)) {
    errors.value.email = '이메일 형식이 올바르지 않습니다.'
    return
  }
  const res = await fetch(`${ACCOUNT_API_URL}/check-email/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: email.value }),
  })
  const data = await res.json()
  if (data.available) {
    isEmailAvailable.value = true
    emailCheckMessage.value = '사용 가능한 이메일입니다.'
  } else {
    isEmailAvailable.value = false
    emailCheckMessage.value = '이미 사용 중인 이메일입니다.'
  }
}

const checkNicknameDuplicate = async () => {
  const res = await fetch(`${ACCOUNT_API_URL}/check-nickname/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nickname: nickname.value }),
  })
  const data = await res.json()
  if (data.available) {
    isNicknameAvailable.value = true
    nicknameCheckMessage.value = '사용 가능한 닉네임입니다.'
  } else {
    isNicknameAvailable.value = false
    nicknameCheckMessage.value = '이미 사용 중인 닉네임입니다.'
  }
}
const onSignUp = async () => {
  errors.value = {}
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
    step.value = 3
  } catch (err) {
    const data = err.response?.data || {}
    errors.value = data
  }
}
</script>

<style scoped>
.signup-wrapper {
  max-width: 600px;
  margin: 40px auto;
  padding: 20px;
  font-family: 'Segoe UI', sans-serif;
}

.progress-bar {
  width: 100%;
  height: 6px;
  background: #e0e7ff;
  margin-bottom: 24px;
  border-radius: 3px;
  overflow: hidden;
}

.progress {
  height: 100%;
  background-color: #6366f1;
  transition: width 0.3s ease;
}

.signup-container {
  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  padding: 40px;
}

.form-title {
  text-align: center;
  font-size: 24px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 32px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 6px;
  font-weight: 500;
  color: #374151;
}

input,
select {
  width: 100%;
  padding: 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  transition: border 0.2s;
}

input:focus,
select:focus {
  border-color: #6366f1;
  outline: none;
  box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
}

.input-with-button {
  display: flex;
  gap: 8px;
}

.check-btn {
  background-color: #e5e7eb;
  border: none;
  padding: 0 16px;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.check-btn:hover {
  background-color: #d1d5db;
}

.primary-btn {
  background-color: #6366f1;
  color: white;
  border: none;
  padding: 12px;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 600;
  width: 100%;
  transition: background-color 0.2s;
}

.primary-btn:hover {
  background-color: #4f46e5;
}

.secondary-btn {
  background-color: #e5e7eb;
  color: #374151;
  border: none;
  padding: 12px;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 600;
  width: 100%;
  transition: background-color 0.2s;
}

.secondary-btn:hover {
  background-color: #d1d5db;
}

.button-group {
  display: flex;
  gap: 12px;
  margin-top: 20px;
}

.error {
  color: #dc2626;
  font-size: 13px;
  margin-top: 6px;
}

.success {
  color: #16a34a;
  font-size: 13px;
  margin-top: 6px;
}

.password-rules ul {
  font-size: 12px;
  color: #6b7280;
  margin-top: 6px;
  padding-left: 18px;
}
.complete-message {
  text-align: center;
  padding: 40px 20px;
}

.complete-message h2 {
  color: #4f46e5;
  font-size: 24px;
  margin-bottom: 16px;
}
</style>
