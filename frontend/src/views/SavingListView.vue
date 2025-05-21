<template>
    <div>
        <h1>Saving Page</h1>
        <SavingList />
    </div>
</template>

<script setup>
    import SavingList from '@/components/product/SavingList.vue';
    import { useSavingStore } from '@/stores/saving';
    import { onMounted } from 'vue';
    const store = useSavingStore()
    onMounted(()=>{
        store.getSavingProducts()
    })
</script>

<style scoped>

</style>