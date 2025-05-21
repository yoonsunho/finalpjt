<template>
<div>
    <RouterLink :to="{name:'DepositDetail', params:{id: product.id}}">
    <p>{{ product.id }}</p>
    </RouterLink>
    <p>금융 회사명: {{ product.deposit_product.kor_co_nm }}</p>
    <p>금융 상품 코드: {{ product.deposit_product.fin_prdt_nm }}</p>
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