import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import vue3GoogleLogin from 'vue3-google-login'  // ← 이 import가 빠져있었음!
import App from './App.vue'
import router from './router'

// Kakao SDK 로드 후 실행
function loadKakaoMapSdk(callback) {
  const script = document.createElement('script')
  script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${import.meta.env.VITE_KAKAO_API_KEY}&autoload=false&libraries=services`
  script.onload = () => {
    window.kakao.maps.load(callback)
  }
  document.head.appendChild(script)
}

// 환경변수에서 clientId 읽어오기
const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID
if (!clientId) {
  console.error('VITE_GOOGLE_CLIENT_ID가 설정되어 있지 않습니다!')
}

// 카카오맵 로드 후 Vue 앱 시작
loadKakaoMapSdk(() => {
  const app = createApp(App)
  const pinia = createPinia()
  pinia.use(piniaPluginPersistedstate)

  app.use(pinia)
  app.use(router)

  // 구글 로그인 플러그인 등록
  app.use(vue3GoogleLogin, {
    clientId: clientId
  })

  app.mount('#app')
})

