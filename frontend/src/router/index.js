import { createRouter, createWebHistory } from 'vue-router'
import SignUpView from '@/views/SignUpView.vue'
import LogInView from '@/views/LogInView.vue'
import MainPage from '@/views/MainPage.vue'

// import { useAccountStore } from '@/stores/user'
import DepositListView from '@/views/DepositListView.vue'
import DepositDetailView from '@/views/DepositDetailView.vue'
import SavingListView from '@/views/SavingListView.vue'
import SavingDetailView from '@/views/SavingDetailView.vue'

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
      name: 'LogInView',
      component: LogInView,
    },
    {
      path: '/signup',
      name: 'SignUpView',
      component: SignUpView
    },
    {
      path : '/deposits',
      name :'DepositList',
      component:DepositListView
    },
    {
      path:'/deposits/:id',
      name:'DepositDetail',
      component:DepositDetailView
    },
    {
      path:'/savings',
      name:'SavingList',
      component:SavingListView
    },
    {
      path:'/savings/:id',
      name:'SavingDetail',
      component:SavingDetailView
    },
  ],
})

// router.beforeEach((to,from)=>{
//   const accountStore = useAccountStore()
// })

export default router
