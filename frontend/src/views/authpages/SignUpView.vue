<template>
  <div class="signup-wrapper">
    <!-- STEP 1, 2 -->
    <div class="signup-container" v-if="step === 1 || step === 2">
      <div class="signup-info">
        <h3>회원가입</h3>
        <p v-if="step === 1">기본 정보를 입력해 주세요.</p>
        <p v-else>
          추가 정보를 입력해 주세요.<br />추가 정보는 맞춤 데이터를 제공하는 데 활용됩니다.
        </p>
        <div class="login-link">
          이미 계정이 있으신가요?
          <RouterLink :to="{ name: 'LoginView' }" class="login-link-text">로그인</RouterLink>
        </div>
        <div class="social-signup-section">
          <div class="divider">간편 가입</div>
          <GoogleLoginButton />
        </div>
      </div>

      <div ref="formContainer" class="signup-form">
        <form @submit.prevent="onSignUp">
          <!-- STEP 1 -->
          <div v-if="step === 1">
            <!-- 이메일 -->
            <div class="form-group">
              <label for="email">이메일</label>
              <div class="input-with-button">
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
              </div>
              <div
                v-if="emailCheckMessage"
                :class="{ error: !isEmailAvailable, success: isEmailAvailable }"
              >
                {{ emailCheckMessage }}
              </div>
              <div v-if="errors.email" class="error">{{ errors.email }}</div>
            </div>

            <!-- 닉네임 -->
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
                <button type="button" @click="checkNicknameDuplicate">중복확인</button>
              </div>
              <div
                v-if="nicknameCheckMessage"
                :class="{ error: !isNicknameAvailable, success: isNicknameAvailable }"
              >
                {{ nicknameCheckMessage }}
              </div>
              <div v-if="errors.nickname" class="error">{{ errors.nickname }}</div>
            </div>

            <div class="form-group">
              <label for="password1">비밀번호</label>
              <input type="password" id="password1" v-model="password1" required />
              <div class="password-rules">
                <ul>
                  <li>
                    최소 8자 이상 / 숫자, 영문자, 특수문자 조합 권장 / 너무 쉬운 비밀번호 불가
                  </li>
                </ul>
              </div>
              <div v-if="errors.password1" class="error">{{ errors.password1 }}</div>
            </div>

            <div class="form-group">
              <label for="password2">비밀번호 확인</label>
              <input type="password" id="password2" v-model="password2" required />
              <div v-if="errors.password2" class="error">{{ errors.password2 }}</div>
            </div>
            <!-- 다음 버튼 -->
            <div class="next-button-wrapper">
              <button type="button" @click="goToStep2">다음</button>
            </div>
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
        </form>
      </div>
    </div>

    <!-- STEP 3 -->
    <div v-else-if="step === 3" class="signup-complete">
      <h2>회원가입이 완료되었습니다!</h2>
      <p>이제 로그인하여 서비스를 이용하실 수 있어요.</p>
      <button class="primary-btn" @click="router.push({ name: 'LoginView' })">
        로그인하러 가기
      </button>
    </div>

    <div class="progress-bar">
      <div class="progress" :style="{ width: `${(step / 3) * 100}%` }"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import gsap from 'gsap'
import { useAccountStore } from '@/stores/user'
import { useRouter, RouterLink } from 'vue-router'
import GoogleLoginButton from '@/components/GoogleLoginButton.vue'

const router = useRouter()
const accountStore = useAccountStore()
const { ACCOUNT_API_URL } = accountStore
const step = ref(1)
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

const goToStep1 = () => {
  step.value = 1
}

const goToStep2 = () => {
  errors.value = {}

  // 모든 필드 확인
  if (!email.value || !nickname.value || !password1.value || !password2.value) {
    if (!email.value) errors.value.email = '이메일을 입력해주세요.'
    if (!nickname.value) errors.value.nickname = '닉네임을 입력해주세요.'
    if (!password1.value) errors.value.password1 = '비밀번호를 입력해주세요.'
    if (!password2.value) errors.value.password2 = '비밀번호 확인을 입력해주세요.'
    return
  }

  // 이메일 중복 확인 여부
  if (!isEmailAvailable.value) {
    errors.value.email = '이메일 중복 확인을 해주세요.'
    return
  }

  // 닉네임 중복 확인 여부
  if (!isNicknameAvailable.value) {
    errors.value.nickname = '닉네임 중복 확인을 해주세요.'
    return
  }

  // 비밀번호 유효성 검사
  const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*()\-_=+{};:,<.>]).{8,}$/
  if (!passwordRegex.test(password1.value)) {
    errors.value.password1 = '비밀번호는 8자 이상, 숫자/영문/특수문자를 모두 포함해야 합니다.'
    return
  }

  // 비밀번호 일치 여부
  if (password1.value !== password2.value) {
    errors.value.password2 = '비밀번호가 일치하지 않습니다.'
    return
  }

  step.value = 2
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
  isEmailAvailable.value = data.available
  emailCheckMessage.value = data.available
    ? '사용 가능한 이메일입니다.'
    : '이미 사용 중인 이메일입니다.'
}

const checkNicknameDuplicate = async () => {
  // 닉네임이 공백이거나 비어있는지 확인
  if (!nickname.value || nickname.value.trim() === '') {
    errors.value.nickname = '닉네임을 입력해주세요.'
    nicknameCheckMessage.value = ''
    isNicknameAvailable.value = false
    return
  }

  try {
    const res = await fetch(`${ACCOUNT_API_URL}/check-nickname/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nickname: nickname.value }),
    })
    const data = await res.json()
    isNicknameAvailable.value = data.available
    nicknameCheckMessage.value = data.available
      ? '사용 가능한 닉네임입니다.'
      : '이미 사용 중인 닉네임입니다.'
  } catch (error) {
    errors.value.nickname = '닉네임 확인 중 오류가 발생했습니다.'
    nicknameCheckMessage.value = ''
    isNicknameAvailable.value = false
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
  padding: 80px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  /* background-color: #f9fafb; */
  min-height: 100vh;
}

.signup-container {
  display: flex;
  flex-wrap: wrap;
  gap: 48px;
  width: 100%;
  max-width: 880px;
  background-color: #ffffff;
  border-radius: 20px;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.06);
  padding: 48px 40px;
}

.signup-info {
  flex: 1;
  padding-right: 32px;
}

.signup-info h3 {
  font-size: 1.8rem;
  font-weight: 700;
  color: #212529;
  margin-bottom: 12px;
}

.signup-info p {
  font-size: 1rem;
  color: #495057;
  margin-top: 8px;
  line-height: 1.5;
}

.login-link {
  margin-top: 24px;
  font-size: 0.95rem;
  color: #495057;
}

.login-link-text {
  color: #1c64f2;
  font-weight: 600;
  margin-left: 6px;
  cursor: pointer;
}

.login-link-text:hover {
  text-decoration: underline;
}

.social-signup-section {
  margin-top: 32px;
}

.divider {
  text-align: center;
  color: #adb5bd;
  font-size: 0.9rem;
  margin: 16px 0;
}
.next-button-wrapper {
  text-align: right;
  margin-top: 24px;
}

.signup-form {
  flex: 2;
}
.input-with-button {
  display: flex;
  gap: 8px;
}

.input-with-button input {
  flex: 1;
}
.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 6px;
  font-size: 0.95rem;
  font-weight: 500;
  color: #374151;
}

input,
select {
  width: 100%;
  padding: 12px;
  border: 1px solid #d1d5db;
  border-radius: 10px;
  font-size: 14px;
  transition: all 0.2s ease;
}

input:focus,
select:focus {
  border-color: #3182f6;
  outline: none;
  box-shadow: 0 0 0 2px rgba(49, 130, 246, 0.2);
}

button {
  padding: 12px 20px;
  border: none;
  border-radius: 12px;
  background-color: #3182f6;
  color: white;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

button:hover {
  background-color: #1d4ed8;
}

.button-group {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
}

.error {
  color: #e03131;
  font-size: 0.9rem;
  margin-top: 6px;
}

.success {
  color: #1c64f2;
  font-size: 0.9rem;
  margin-top: 6px;
}

.password-rules ul {
  font-size: 12px;
  color: #6b7280;
  margin-top: 6px;
  padding-left: 18px;
}

.signup-complete {
  max-width: 480px;
  margin: 0 auto;
  padding: 48px 32px;
  background: #ffffff;
  border-radius: 20px;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.06);
  text-align: center;
}

.primary-btn {
  padding: 12px 24px;
  background-color: #3182f6;
  border: none;
  border-radius: 12px;
  color: white;
  font-weight: 600;
  margin-top: 24px;
  cursor: pointer;
}

.primary-btn:hover {
  background-color: #1e4dd8;
}

.progress-bar {
  width: 75%;
  height: 6px;
  background: #e0e7ff;
  margin-top: 32px;
  border-radius: 3px;
  overflow: hidden;
}

.progress {
  height: 100%;
  background-color: #3182f6;
  transition: width 0.3s ease;
}
</style>
