<template>
    <div>
        <h1>Deposit Page</h1>
        <DepositList />
    </div>
</template>

<script setup>
    import DepositList from '@/components/product/DepositList.vue';
    import { useDepositStore } from '@/stores/deposit';
    // import { name } from '@vue/eslint-config-prettier/skip-formatting';
    import { onMounted } from 'vue';
    // import { RouterLink } from 'vue-router';
    const store = useDepositStore()
    onMounted(()=>{
        store.getDepositProducts()
    })
</script>

<style scoped>

</style>