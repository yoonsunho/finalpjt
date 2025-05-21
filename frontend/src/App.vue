<script setup>
  import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
      <nav>
        <RouterLink :to="{name: 'SignUpView'}">signup</RouterLink> |
        <RouterLink :to="{name: 'LogInView'}">login</RouterLink> |
        <RouterLink :to="{name: 'DepositList'}">Deposits</RouterLink> | 
        <RouterLink :to="{name: 'SavingList'}">Savings</RouterLink>
      </nav>
  </header>
  <RouterView />
</template>

<script setup>
  import { RouterView, RouterLink } from 'vue-router'
</script>

<style scoped>

</style>
