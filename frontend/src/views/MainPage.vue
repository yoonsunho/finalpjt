<template>
  <div>
    <CarouselComponent />
    <BannerComponent />
    <div>
      <div class="app">
        <RouterView />
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { RouterView, RouterLink } from 'vue-router'
import CarouselComponent from '@/components/CarouselComponent.vue'
import BannerComponent from '@/components/BannerComponent.vue'
export default {
  name: 'App',
  components: {
    CarouselComponent,
    BannerComponent,
  },
  data() {
    return {
      isLoggedIn: false,
    }
  },
  created() {
    this.checkLoginStatus()
  },
  methods: {
    checkLoginStatus() {
      const token = localStorage.getItem('token')
      this.isLoggedIn = !!token
    },
    async logout() {
      try {
        await axios.post('/api/dj-rest-auth/logout/')
        localStorage.removeItem('token')
        this.isLoggedIn = false

        this.$router.push('/login')
      } catch (error) {
        console.error('로그아웃 실패:', error)

        localStorage.removeItem('token')
        this.isLoggedIn = false
        this.$router.push('/login')
      }
    },
  },
  watch: {
    $route() {
      this.checkLoginStatus()
    },
  },
}
</script>

<style scoped></style>
