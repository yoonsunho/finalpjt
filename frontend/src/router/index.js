import { createRouter, createWebHistory } from 'vue-router'
import MainPage from '@/views/MainPage.vue'

import LoginPage from '@/views/authpages/LoginPage.vue'
import SignUpPage from '@/views/authpages/SignUpPage.vue'
import ProfilePage from '@/views/authpages/ProfilePage.vue'

import CommunityPage from '@/views/community/CommunityPage.vue'
import ArticleDetail from '@/views/community/ArticleDetail.vue'
import CreateArticle from '@/views/community/CreateArticle.vue'

import EtcPage from '@/views/etcpages/EtcPage.vue'
import ExchangePage from '@/views/etcpages/ExchangePage.vue'
import MapPage from '@/views/etcpages/MapPage.vue'

import DepositView from '@/views/deposit/DepositView.vue'
// import DepositDetail from '@/views/deposit/DepositDetail.vue'

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
      path: '/community/create',
      name: 'createarticle',
      component: CreateArticle,
    },
    {
      path: '/etc',
      name: 'etc',
      component: EtcPage,
    },
    {
      path: '/exchange',
      name: 'exchange',
      component: ExchangePage,
    },
    {
      path: '/map',
      name: 'map',
      component: MapPage,
    },
    {
      path: '/deposits',
      name: 'deposits',
      component: DepositView,
    },
    // {
    //   path: '/deposits/detail/:id',
    //   name: 'depositdetail',
    //   component: DepositDetail,
    // },
  ],
})

export default router
