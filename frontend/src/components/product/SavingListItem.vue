<template>
    <div>
        <RouterLink :to="{name:'SavingDetail', params:{id: product.id}}">
        <p>{{ product.id }}</p>
        </RouterLink>
        <p>금융 회사명: {{ product.saving_product.kor_co_nm }}</p>
        <p>금융 상품 명: {{ product.saving_product.fin_prdt_nm }}</p>
        <p>적립 유형: {{ product.rsrv_type_nm }}</p>
        <p>최고 우대 금리:{{ product.intr_rate2 }}</p>
        <p>저축 기간: {{ product.save_trm }}개월</p>
    
        <hr>
    </div>
    </template>
    
    <script setup>
        import { RouterLink } from 'vue-router';
        const props = defineProps({
            product:Object
        })
    </script>
    
    <style scoped>
    
    </style>