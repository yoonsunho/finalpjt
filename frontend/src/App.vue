<template>
  <div>
    <NavbarComponent />
    <Carousel/>
    <BannerComponent />
    <main class="main-content">
      <ArticleDetail/>
      <TableComponent/>
    </main>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import NavbarComponent from './components/NavbarComponent.vue'
import Carousel from './components/Carousel.vue'
import BannerComponent from './components/BannerComponent.vue'
import ArticleDetail from './views/ArticleDetail.vue'
import TableComponent from './components/TableComponent.vue'
</script>

<style scoped>
* {
  /* padding: 2rem; */
  font-family: Pretendard;
}

main {
  padding: 2rem;
}
</style>
