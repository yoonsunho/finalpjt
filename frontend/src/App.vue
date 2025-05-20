<template>
  <div>
    <NavbarComponent />
    <main class="main-content">
      <h1>내용</h1>
    </main>
  </div>
</template>

<script setup>
import NavbarComponent from './components/NavbarComponent.vue'
</script>

<style scoped>
.main-content {
  padding: 2rem;
  font-family: Pretendard;
}
</style>
