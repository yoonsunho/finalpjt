import { createRouter, createWebHistory } from 'vue-router'

import MainPage from '@/views/MainPage.vue'

import SignUpView from '@/views/authpages/SignUpView.vue'
import LoginView from '@/views/authpages/LoginView.vue'
import ProfilePage from '@/views/authpages/ProfilePage.vue'
import ProfileEdit from '@/views/authpages/ProfileEdit.vue'
import GoogleAdditionalInfoView from '@/views/authpages/GoogleAdditionalInfoView.vue'
// import GoogleLoginView from '@/views/authpages/GoogleLoginView.vue'
import PasswordEdit from '@/views/authpages/PasswordEdit.vue'

import DepositListView from '@/views/deposit/DepositListView.vue'
import DepositDetailView from '@/views/deposit/DepositDetailView.vue'
import SavingListView from '@/views/deposit/SavingListView.vue'
import SavingDetailView from '@/views/deposit/SavingDetailView.vue'
import MyInterests from '@/components/product/MyInterests.vue'
import MyJoins from '@/components/product/MyJoins.vue'
import RecommendView from '@/views/deposit/RecommendView.vue'

import CommunityPage from '@/views/community/CommunityPage.vue'
import ArticleDetail from '@/views/community/ArticleDetail.vue'
import CreateArticle from '@/views/community/CreateArticle.vue'

import SharedSavingRoomDetailView from '@/views/savingroom/SharedSavingRoomDetailView.vue'
import SharedSavingRoomListView from '@/views/savingroom/SharedSavingRoomListView.vue'
import SharedSavingRoomCreateView from '@/views/savingroom/SharedSavingRoomCreateView.vue'

import EtcPage from '@/views/etcpages/EtcPage.vue'
import SpotPage from '@/views/etcpages/SpotPage.vue'
import MapPage from '@/views/etcpages/MapPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'MainPage',
      component: MainPage,
    },
    {
      path: '/login',
      name: 'LoginView',
      component: LoginView,
    },
    {
      path: '/signup',
      name: 'SignUpView',
      component: SignUpView,
    },
    {
      path: '/deposits',
      name: 'DepositListView',
      component: DepositListView,
    },
    {
      path: '/deposits/:id',
      name: 'DepositDetailView',
      component: DepositDetailView,
    },
    {
      path: '/savings',
      name: 'SavingListView',
      component: SavingListView,
    },
    {
      path: '/savings/:id',
      name: 'SavingDetailView',
      component: SavingDetailView,
    },
    {
      path: '/finlife/my-interests',
      name: 'MyInterests',
      component: MyInterests,
    },
    {
      path: '/finlife/my-joins',
      name: 'MyJoins',
      component: MyJoins,
    },
    {
      path: '/recommend/',
      name: 'RecommendView',
      component: RecommendView,
    },
    {
      path: '/profile',
      name: 'ProfilePage',
      component: ProfilePage,
    },
    {
      path: '/profile/edit',
      name: 'ProfileEdit',
      component: ProfileEdit,
    },
    {
      path: '/profile/password',
      name: 'PasswordEdit',
      component: PasswordEdit,
    },
    {
      path: '/community/create',
      name: 'CreateArticle',
      component: CreateArticle,
    },
    {
      path: '/community/article/:id',
      name: 'ArticleDetail',
      component: ArticleDetail,
    },
    {
      path: '/community/:category(review|tip|free)?',
      name: 'CommunityPage',
      component: CommunityPage,
    },
    {
      path: '/savingroom/',
      name: 'SharedSavingRoomListView',
      component: SharedSavingRoomListView,
    },
    {
      path: '/savingroom/room/:id',
      name: 'SharedSavingRoomDetailView',
      component: SharedSavingRoomDetailView,
    },
    {
      path: '/savingroom/create',
      name: 'SharedSavingRoomCreateView',
      component: SharedSavingRoomCreateView,
    },
    {
      path: '/spot',
      name: 'SpotPage',
      component: SpotPage,
    },
    {
      path: '/map',
      name: 'MapPage',
      component: MapPage,
    },
    {
      path: '/google-additional-info',
      name: 'GoogleAdditionalInfoView',
      component: GoogleAdditionalInfoView,
    },
    // {
    //   path: '/:pathMatch(.*)*',
    //   name: 'NotFound',
    //   component: NotFoundView,
    // },
  ],
})

export default router
