<!-- src/components/auth/GoogleLoginButton.vue -->
<script setup>
import { googleAuthCodeLogin } from 'vue3-google-login'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/user' // 추가
const accountStore = useAccountStore()

const router = useRouter()
const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL

const handleGoogleLogin = async () => {
  try {
    const { code } = await googleAuthCodeLogin()
    const response = await axios.post(`${apiBaseUrl}/accounts/google/`, {
      code,
      redirect_uri: window.location.origin
    })
    console.log(response.data)

    if (response.data.status === 'additional_info_required') {
  // 신규 유저: 추가 정보 입력
  router.push({
    name: 'GoogleAdditionalInfoView',
    query: {
      token: response.data.key,
      temp_nickname: response.data.temp_nickname
    }
  })
} else if (response.data?.key) {
  // 기존 유저
  if (response.data.has_completed_profile === false || response.data.has_completed_profile === 0) {
    // 기존 유저지만 추가 정보 미입력 → 추가 정보 입력 페이지로 이동
    router.push({
      name: 'GoogleAdditionalInfoView',
      query: {
        token: response.data.key,
        temp_nickname: '' // 기존 닉네임 등 필요시 추가
      }
    })
  } else {
    // 추가 정보 입력 완료 → 정상 로그인 처리
    accountStore.token = response.data.key
    await accountStore.fetchUserInfo()
    router.push({ name: 'MainPage' })
  }
} else {
  alert('서버 응답 오류: 예상치 못한 데이터 형식')
}
  } catch (error) {
    alert(error.response?.data?.detail || '로그인 처리 중 오류 발생')
  }
}
</script>

<template>
<button class="gsi-material-button" @click="handleGoogleLogin">
  <div class="gsi-material-button-state"></div>
  <div class="gsi-material-button-content-wrapper">
    <div class="gsi-material-button-icon">
      <svg version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" xmlns:xlink="http://www.w3.org/1999/xlink" style="display: block;">
        <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"></path>
        <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"></path>
        <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"></path>
        <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"></path>
        <path fill="none" d="M0 0h48v48H0z"></path>
      </svg>
    </div>
    <span style="display: none;">Sign in with Google</span>
  </div>
</button>
</template>

<style scoped>
.social-login-btn {
  width: 100%;
  padding: 12px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-weight: 500;
  transition: filter 0.2s;
}

.social-login-btn:hover {
  filter: brightness(0.95);
}

.google {
  background: #ffffff;
  border: 1px solid #dadce0;
  color: #3c4043;
}

img {
  width: 20px;
  height: 20px;
}
</style>
