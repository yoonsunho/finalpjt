<template>
  <div class="wrapper">
    <NavbarComponent />
    <div class="inner-wrapper">
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
  /* box-shadow: inset 0 0 13px dodgerblue; */
}

.inner-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  /* box-shadow: inset 0 0 13px rebeccapurple; */

}
</style>
