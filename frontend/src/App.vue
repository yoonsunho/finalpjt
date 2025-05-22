<template>
  <NavbarComponent />
  <header class="layout">
      <nav>
        <RouterLink :to="{name: 'SignUpView'}">signup</RouterLink> |
        <RouterLink :to="{name: 'LogInView'}">login</RouterLink> |
        <RouterLink :to="{name: 'DepositList'}">Deposits</RouterLink> | 
        <RouterLink :to="{name: 'SavingList'}">Savings</RouterLink>
      </nav>
  </header>
  <RouterView />
  <FooterComponent />
</template>

<script setup>
  import { RouterView, RouterLink } from 'vue-router'
  import NavbarComponent from '@/components/NavbarComponent.vue'
  import FooterComponent from '@/components/FooterComponent.vue'
</script>

<style scoped>
* {
  font-family: Pretendard;
}
.layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh; /* 화면 전체 높이 */
}

.layout > *:last-child {
  margin-top: auto; /* 푸터 바닥에 고정 */
}
</style>