<template>
  <div class="wrapper">
    <NavbarComponent />
    <div class="inner-wrapper" :class="{ 'with-padding': route.name !== 'MainPage' }">
      <RouterView />
    </div>
    <FooterComponent />
  </div>
</template>

<script setup>
import { useRoute, RouterView } from 'vue-router'
import NavbarComponent from '@/components/NavbarComponent.vue'
import FooterComponent from '@/components/FooterComponent.vue'
const route = useRoute()
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

.inner-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.with-padding {
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}
</style>
