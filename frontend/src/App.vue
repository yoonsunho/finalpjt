<template>
  <div class="layout">
    <NavbarComponent />
    <RouterView />
    <FooterComponent />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
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
