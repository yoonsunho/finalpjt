import { createRouter, createWebHistory } from 'vue-router'
import MainPage from '@/views/MainPage.vue'
import LoginPage from '@/views/LoginPage.vue'
import SignUpPage from '@/views/SignUpPage.vue'
import ProfilePage from '@/views/ProfilePage.vue'
import ExchangePage from '@/views/ExchangePage.vue'
import MapPage from '@/views/MapPage.vue'
import ArticleDetail from '@/views/ArticleDetail.vue'
import CreateView from '@/views/CreateArticle.vue'
import DepositView from '@/views/DepositView.vue'
import DepositDetail from '@/views/DepositDetail.vue'
import CommunityPage from '@/views/CommunityPage.vue'
import EtcPage from '@/views/EtcPage.vue'

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
      component: LoginPage,
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUpPage,
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfilePage,
    },
    {
      path: '/community',
      name: 'communitypage',
      component: CommunityPage,
    },
    {
      path: '/community/articles/:id',
      name: 'articledetail',
      component: ArticleDetail,
    },
    {
      path: '/community/articles/create',
      name: 'createview',
      component: CreateView,
    },
    {
      path: '/etc',
      name: 'etc',
      component: EtcPage,
    },
    {
      path: '/exchange',
      name: 'exchangepage',
      component: ExchangePage,
    },
    {
      path: '/map',
      name: 'mappage',
      component: MapPage,
    },
    {
      path: '/deposits',
      name: 'deposits',
      component: DepositView,
    },
    {
      path: '/deposits/detail',
      name: 'depositdetail',
      component: DepositView,
    },
    // {
    //   path: '/deposits/예금',
    //   name: '',
    //   component: ,
    // },
    // {
    //   path: '/deposits/적금',
    //   name: '',
    //   component: ,
    // },
  ],
})

export default router
