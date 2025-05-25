import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
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

// 카카오맵 로드 후 Vue 앱 시작
loadKakaoMapSdk(() => {
  const app = createApp(App)
  const pinia = createPinia()
  pinia.use(piniaPluginPersistedstate)

  app.use(pinia)
  app.use(router)
  app.mount('#app')
})
