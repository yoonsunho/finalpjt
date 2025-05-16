<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <div class="wrapper">
      <nav>
        <!-- <RouterLink to="/main">Main</RouterLink> -->
        <!-- <RouterLink to="/login">Login</RouterLink>
        <RouterLink to="/signup">SignUp</RouterLink>
        <RouterLink to="/profile">Profile</RouterLink> -->
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>
* {
  font-family: 'Pretendard';
}
</style>
