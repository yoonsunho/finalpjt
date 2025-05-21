<template>
  <header>
    <div>
      <nav>
        <RouterLink :to="{name: 'DepositList'}">Deposits</RouterLink> | 
        <RouterLink :to="{name: 'SavingList'}">Savings</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<script setup>
  import { RouterView, RouterLink } from 'vue-router'
  

</script>

<style scoped>

</style>
