import { createRouter, createWebHistory } from 'vue-router'
import MainPage from '@/views/MainPage.vue'
import LoginPage from '@/views/LoginPage.vue'
import SignUpPage from '@/views/SignUpPage.vue'
import ProfilePage from '@/views/ProfilePage.vue'
import ExchangePage from '@/views/ExchangePage.vue'
import MapPage from '@/views/MapPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'main',
      component: MainPage,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginPage
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUpPage
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfilePage
    },
    {
      path: '/exchange',
      name: 'exchangepage',
      component: ExchangePage
    },
    {
      path: '/map',
      name: 'mappage',
      component: MapPage
    },
    {
      path: '/community/articles/:id',
      name: 'articledetail',
      component: ArticleDetail
    },
    {
      path: '/community/articles/create',
      name: 'createview',
      component: CreateView
    },
  ],
})

export default router
