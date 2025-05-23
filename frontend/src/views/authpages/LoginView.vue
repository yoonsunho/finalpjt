<template>
  <div class="login-wrapper">
    <div class="login-container">
      <h2>로그인</h2>
      <!-- <div v-if="successMessage" class="success-message">
        {{ successMessage }}
      </div> -->
      <form @submit.prevent="onLogIn">
        <div class="form-group">
          <label for="email">이메일</label>
          <input type="email" id="email" v-model="email" required />
          <!-- <div v-if="errors.email" class="error">{{ errors.email }}</div> -->
        </div>

        <div class="form-group">
          <label for="password">비밀번호</label>
          <input type="password" id="password" v-model="password" required />
        </div>

        <button type="submit">로그인</button>
      </form>
      <div v-if="showLoginErrorModal" class="modal">
        <div class="modal-content">
          <p>올바른 로그인 정보를 입력하세요!</p>
          <button @click="showLoginErrorModal = false">닫기</button>
        </div>
      </div>
      <!-- <div class="signup-link">
        계정이 없으신가요? <router-link :to="{name:'SignUpView'}">회원가입</router-link>
      </div>
      -->
      <!-- <div v-if="tokenInfo" class="token-info">
        <h3>토큰 정보</h3>
        <pre>{{ tokenInfo }}</pre>
      </div> -->
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAccountStore } from '@/stores/user'

const accountStore = useAccountStore()

const email = ref('')
const password = ref('')
const showLoginErrorModal = ref(false)

const onLogIn = async function () {
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
.login-wrapper {
}

.login-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 40px;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  margin-bottom: 30px;
  font-size: 24px;
  font-weight: 600;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
}

input {
  width: 100%;
  padding: 12px 14px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 14px;
  transition: border 0.2s;
}

input:focus {
  outline: none;
  border-color: #2196f3;
  box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.2);
}

button {
  width: 100%;
  padding: 12px;
  background-color: #2196f3;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
  margin-top: 10px;
}

button:hover {
  background-color: #1976d2;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.error {
  color: #d32f2f;
  font-size: 13px;
  margin-top: 6px;
}

.general-error {
  margin: 16px 0;
  text-align: center;
}

.success-message {
  background-color: #e0f7e9;
  color: #2e7d32;
  padding: 12px;
  margin-bottom: 24px;
  border-radius: 6px;
  text-align: center;
  font-weight: 500;
}

.signup-link {
  text-align: center;
  margin-top: 24px;
  font-size: 14px;
}

a {
  color: #2196f3;
  text-decoration: none;
  font-weight: 500;
}

a:hover {
  text-decoration: underline;
}

.token-info {
  margin-top: 30px;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 6px;
  font-size: 13px;
  color: #555;
}

.token-info pre {
  white-space: pre-wrap;
  word-break: break-word;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4); /* 반투명 검정 배경 */
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal-content {
  background: white;
  padding: 24px 32px;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}
</style>
