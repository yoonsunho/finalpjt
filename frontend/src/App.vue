<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
      <nav>
        <RouterLink :to="{name:'SignUpView'}">signup</RouterLink> |
        <RouterLink :to="{name:'LogInView'}">login</RouterLink>
      </nav>
  </header>
  <RouterView />
</template>

<style scoped>
</style>
