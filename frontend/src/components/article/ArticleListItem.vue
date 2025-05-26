<template>
  <div>
    <RouterLink :to="{ name: '', params: {} }">
      <p></p>
    </RouterLink>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>

<style scoped>
* {
  font-family: Pretendard;
}
</style>
