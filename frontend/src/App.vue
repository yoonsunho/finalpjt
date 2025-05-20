<template>
  <header>
    <div>
      <nav>
        <RouterLink :to="{name: 'DepositList'}">Deposits</RouterLink>
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
