import { createRouter, createWebHistory } from 'vue-router'
import DepositListView from '@/views/DepositListView.vue'
import DepositDetailView from '@/views/DepositDetailView.vue'
import SavingListView from '@/views/SavingListView.vue'
import SavingDetailView from '@/views/SavingDetailView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path:'/deposits',
      name:'DepositList',
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

export default router
