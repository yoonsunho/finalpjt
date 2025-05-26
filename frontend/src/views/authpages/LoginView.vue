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
  padding: 100px;
  /* layout wrapper */
}

.signup-container {
  display: flex;
  gap: 40px;
  align-items: flex-start;
  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  padding: 40px;
}

.signup-info {
  flex: 1;
  border-right: 1px solid #e5e7eb;
  padding-right: 20px;
}

.signup-info h3 {
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 12px;
}

.signup-info p {
  font-size: 1rem;
}

.signup-form {
  flex: 2;
}

.form-group {
  font-size: 1rem;
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 6px;
  font-weight: 500;
  color: #374151;
}

input {
  width: 100%;
  padding: 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  transition: border 0.2s;
}

input:focus {
  border-color: #3182f6;
  outline: none;
  box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
}

button {
  margin-top: 10px;
  padding: 10px 16px;
  border: none;
  border-radius: 8px;
  background-color: #3182f6;
  color: white;
  font-weight: 600;
  cursor: pointer;
}

button:hover {
  background-color: #2563eb;
}

.button-group {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

.error {
  color: #bd0000;
  font-size: 0.9rem;
  margin-top: 6px;
}

.general-error {
  margin-top: 12px;
  text-align: center;
}

.signup-router {
  margin-top: 24px;
  text-align: center;
}

.signup-link {
  color: #3182f6;
  font-weight: 600;
  margin-left: 6px;
  cursor: pointer;
}
.signup-link:hover {
  text-decoration: underline;
}
</style>
