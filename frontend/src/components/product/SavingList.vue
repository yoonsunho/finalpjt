<template>
    <div>
        <h3>Saving List</h3>
        <SavingListItem v-for="product in store.savingProducts" 
        :key="product.id"
        :product = "product"/>
    </div>
</template>

<script setup>
    import SavingListItem from './SavingListItem.vue';
    import { useSavingStore } from '@/stores/saving';
    const store = useSavingStore()

    
</script>

<style scoped>

</style>