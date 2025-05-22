<template>
  <div class="wrapper">
    <NavbarComponent />
    <div class="layout">
      <RouterView />
    </div>
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

.wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.layout {
  flex: 1;
  padding: 5rem;
}
</style>
