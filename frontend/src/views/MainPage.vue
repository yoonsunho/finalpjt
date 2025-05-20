<template>
  <div id="app">
    <header>
      <nav>
        <router-link to="/">홈</router-link>
        <router-link v-if="!isLoggedIn" to="/signup">회원가입</router-link>
        <router-link v-if="!isLoggedIn" to="/login">로그인</router-link>
        <a v-if="isLoggedIn" href="#" @click.prevent="logout">로그아웃</a>
      </nav>
    </header>
    <main>
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'App',
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
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
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