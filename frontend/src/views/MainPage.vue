<template>
  <div>
    <CarouselComponent />
    <BannerComponent />
    <div class="app">
      <RouterView />
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { RouterView, RouterLink } from 'vue-router'
import CarouselComponent from '@/components/CarouselComponent.vue'
import BannerComponent from '@/components/BannerComponent.vue'
export default {
  name: 'App',
  components: {
    CarouselComponent,
    BannerComponent,
  },
}
</script>

<style scoped></style>
