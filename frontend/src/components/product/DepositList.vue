<template>
    <div>
        <h3>Deposit List</h3>
        <DepositListItem v-for="product in store.depositProducts" 
        :key="product.id"
        :product = "product"/>
    </div>
</template>

<script setup>
    import DepositListItem from './DepositListItem.vue';
    import { useDepositStore } from '@/stores/deposit';
    const store = useDepositStore()
    
</script>

<style scoped>

</style>