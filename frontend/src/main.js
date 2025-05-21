import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

// npm install pinia-plugin-persistedstate 이거 해주기!!!

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

const app = createApp(App)
const pinia = createPinia()

pinia.use(piniaPluginPersistedstate)
// app.use(createPinia())
app.use(pinia)
app.use(router)

app.mount('#app')
