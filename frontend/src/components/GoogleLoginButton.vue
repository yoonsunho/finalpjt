<template>
  <button class="google-login-button" @click="handleGoogleLogin">
    <div class="icon-wrapper">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">
        <path
          fill="#EA4335"
          d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"
        />
        <path
          fill="#4285F4"
          d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"
        />
        <path
          fill="#FBBC05"
          d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"
        />
        <path
          fill="#34A853"
          d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"
        />
      </svg>
    </div>
    <span>Google로<br />로그인 / 회원가입</span>
  </button>
</template>

<script setup>
import { googleAuthCodeLogin } from 'vue3-google-login'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/user'

const router = useRouter()
const accountStore = useAccountStore()
const { ACCOUNT_API_URL } = accountStore

const handleGoogleLogin = async () => {
  try {
    const { code } = await googleAuthCodeLogin()
    const response = await axios.post(`${ACCOUNT_API_URL}/google/`, {
      code,
      redirect_uri: window.location.origin,
    })

    const data = response.data

    if (data.status === 'additional_info_required' || data.has_completed_profile === false) {
      accountStore.token = data.key
      accountStore.isGoogleUser = true
      router.push({
        name: 'GoogleAdditionalInfoView',
        query: {
          token: data.key,
          temp_nickname: data.temp_nickname || '',
        },
      })
    } else if (data?.key) {
      accountStore.token = data.key
      accountStore.isGoogleUser = true
      await accountStore.fetchUserInfo()
      router.push({ name: 'MainPage' })
    } else {
      alert('서버 응답 오류: 예상치 못한 데이터 형식')
    }
  } catch (error) {
    alert(error.response?.data?.detail || '로그인 처리 중 오류 발생')
  }
}
</script>

<style scoped>
.google-login-button {
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  gap: 12px;
  background-color: #ffffff;
  border: 1px solid #dadce0;
  border-radius: 8px;
  padding: 12px 16px;
  width: 100%;
  font-size: 15px;
  font-weight: 500;
  color: #3c4043;
  cursor: pointer;
  transition:
    box-shadow 0.2s ease,
    background-color 0.2s ease;
}

.google-login-button:hover {
  background-color: #f7f8f8;
  box-shadow: 0 2px 8px rgba(60, 64, 67, 0.15);
}

.google-login-button:active {
  background-color: #eee;
}

.icon-wrapper {
  width: 24px;
  height: 24px;
}

.icon-wrapper svg {
  width: 100%;
  height: 100%;
}
</style>
