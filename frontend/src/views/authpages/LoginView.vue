<template>
  <div class="signup-wrapper">
    <div class="signup-container">
      <!-- 왼쪽 설명 영역 -->
      <div class="signup-info">
        <h3>로그인</h3>
        <p>이메일과 비밀번호를 입력해 주세요.</p>
        <div class="social-login-section">
          <div class="divider">또는</div>
          <GoogleLoginButton />
        </div>
        <div class="signup-router">
          <p>계정이 없으신가요?</p>
          <RouterLink :to="{ name: 'SignUpView' }"><p class="signup-link">회원가입</p></RouterLink>
        </div>
      </div>

      <!-- 오른쪽 폼 영역 -->
      <div class="signup-form">
        <form @submit.prevent="onLogIn">
          <div class="form-group">
            <label for="email">이메일</label>
            <input type="email" id="email" v-model="email" required />
          </div>

          <div class="form-group">
            <label for="password">비밀번호</label>
            <input type="password" id="password" v-model="password" required />
          </div>

          <div class="button-group">
            <button type="submit">로그인</button>
          </div>

          <div v-if="showLoginErrorModal" class="error general-error">
            올바른 로그인 정보를 입력하세요!
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAccountStore } from '@/stores/user'
import { RouterLink } from 'vue-router'
import GoogleLoginButton from '@/components/GoogleLoginButton.vue'

const accountStore = useAccountStore()

const email = ref('')
const password = ref('')
const showLoginErrorModal = ref(false)

const onLogIn = async () => {
  const userInfo = {
    email: email.value,
    password: password.value,
  }
  try {
    await accountStore.logIn(userInfo)
    showLoginErrorModal.value = false
  } catch (error) {
    showLoginErrorModal.value = true
  }
}
</script>

<style scoped>
.signup-wrapper {
  padding: 80px 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  /* background-color: #f9fafb; */
}

.signup-container {
  display: flex;
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
  border-right: 1px solid #e9ecef;
  padding-right: 32px;
}

.signup-info h3 {
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 12px;
  color: #212529;
}

.signup-info p {
  font-size: 1rem;
  color: #495057;
  margin-top: 8px;
  line-height: 1.5;
}

.social-login-section {
  margin-top: 32px;
}

.divider {
  text-align: center;
  color: #adb5bd;
  font-size: 0.9rem;
  margin: 16px 0;
}

.signup-router {
  margin-top: 32px;
  text-align: center;
  font-size: 0.95rem;
  color: #495057;
}

.signup-link {
  color: #1c64f2;
  font-weight: 600;
  margin-left: 6px;
  cursor: pointer;
}

.signup-link:hover {
  text-decoration: underline;
}

.signup-form {
  flex: 2;
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

input {
  width: 100%;
  padding: 12px;
  border: 1px solid #d1d5db;
  border-radius: 10px;
  font-size: 14px;
  transition: all 0.2s ease;
}

input:focus {
  border-color: #3182f6;
  outline: none;
  box-shadow: 0 0 0 2px rgba(49, 130, 246, 0.2);
}

.button-group {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
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

.error {
  color: #e03131;
  font-size: 0.9rem;
  margin-top: 6px;
}

.general-error {
  margin-top: 16px;
  text-align: center;
}
</style>
