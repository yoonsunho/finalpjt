import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import axios from 'axios'
import App from './App.vue'
import router from './router'
import SignUp from './views/SignUpView.vue'
import Login from './views/LoginView.vue'

axios.defaults.baseURL = 'http://localhost:8000'
axios.defaults.withCredentials = true
const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
