<template>
  <div>
    <Carousel />
    <BannerComponent />
    <div class="app">
    <RouterView />
    </div>  
  </div>
</template>

<script>
import axios from 'axios';
import { RouterView, RouterLink } from 'vue-router'
import Carousel from '@/components/Carousel.vue'
import BannerComponent from '@/components/BannerComponent.vue'
export default {
  name: 'App',
  components: {
    Carousel,
    BannerComponent,
  },
  data() {
    return {
      isLoggedIn: false
    };
  },
  created() {
    this.checkLoginStatus();
  },
  methods: {
    checkLoginStatus() {
      const token = localStorage.getItem('token');
      this.isLoggedIn = !!token;
    },
    async logout() {
      try {
        await axios.post('/api/dj-rest-auth/logout/');
        localStorage.removeItem('token');
        this.isLoggedIn = false;
        
        this.$router.push('/login');
      } catch (error) {
        console.error('로그아웃 실패:', error);
        
        localStorage.removeItem('token');
        this.isLoggedIn = false;
        this.$router.push('/login');
      }
    }
  },
  watch: {
    $route() {
      this.checkLoginStatus();
    }
  }
};
</script>

<style>
#app {
  /* margin: 0 auto; */
}

header {
  padding: 20px 0;
  border-bottom: 1px solid #eee;
  margin-bottom: 20px;
}

nav {
  display: flex;
  gap: 20px;
}

nav a {
  color: #2c3e50;
  text-decoration: none;
  font-weight: bold;
}

nav a.router-link-exact-active {
  color: #42b983;
}

main {
  min-height: 70vh;
}
</style>
