<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
      <nav>
        <RouterLink to="/signup">signup</RouterLink>
        <RouterLink to="/login">login</RouterLink>
      </nav>
  </header>
  <RouterView />
</template>

<style scoped>
</style>
