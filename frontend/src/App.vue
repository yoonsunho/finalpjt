<template>
  <div>
    <NavbarComponent />
    <RouterView />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import NavbarComponent from './components/NavbarComponent.vue'
</script>

<style scoped>
* {
  font-family: Pretendard;
}
</style>
