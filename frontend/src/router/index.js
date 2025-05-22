import { createRouter, createWebHistory } from 'vue-router'

import MainPage from '@/views/MainPage.vue'

import SignUpView from '@/views/authpages/SignUpView.vue'
import LoginView from '@/views/authpages/LoginView.vue'
import ProfilePage from '@/views/authpages/ProfilePage.vue'

// import { useAccountStore } from '@/stores/user'
import DepositListView from '@/views/deposit/DepositListView.vue'
import DepositDetailView from '@/views/deposit/DepositDetailView.vue'
import SavingListView from '@/views/deposit/SavingListView.vue'
import SavingDetailView from '@/views/deposit/SavingDetailView.vue'


import CommunityPage from '@/views/community/CommunityPage.vue'
import ArticleDetail from '@/views/community/ArticleDetail.vue'
import CreateArticle from '@/views/community/CreateArticle.vue'

import EtcPage from '@/views/etcpages/EtcPage.vue'
import ExchangePage from '@/views/etcpages/ExchangePage.vue'
import MapPage from '@/views/etcpages/MapPage.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path:'/',
      name: 'MainPage',
      component: MainPage
    },
    {
      path: '/login',
      name: 'LoginView',
      component: LoginView,
    },
    {
      path: '/signup',
      name: 'SignUpView',
      component: SignUpView
    },
    {
      path : '/deposits',
      name :'DepositListView',
      component:DepositListView
    },
    {
      path:'/deposits/:id',
      name:'DepositDetailView',
      component:DepositDetailView
    },
    {
      path:'/savings',
      name:'SavingListView',
      component:SavingListView
    },
    {
      path:'/savings/:id',
      name:'SavingDetailView',
      component:SavingDetailView

    },
    {
      path: '/profile',
      name: 'ProfilePage',
      component: ProfilePage,
    },
    {
      path: '/community',
      name: 'CommunityPage',
      component: CommunityPage,
    },
    {
      path: '/community/articles/:id',
      name: 'ArticleDetail',
      component: ArticleDetail,
    },
    {
      path: '/community/create',
      name: 'CreateArticle',
      component: CreateArticle,
    },
    {
      path: '/etc',
      name: 'EtcPage',
      component: EtcPage,
    },
    {
      path: '/exchange',
      name: 'ExchangePage',
      component: ExchangePage,
    },
    {
      path: '/map',
      name: 'MapPage',
      component: MapPage,
    },
  
    // {
    //   path: '/deposits/detail/:id',
    //   name: 'depositdetail',
    //   component: DepositDetail,
    // },
  ],
})

// router.beforeEach((to,from)=>{
//   const accountStore = useAccountStore()
// })

export default router
