<template>
  <h1>맞춤추천받기</h1>
  <button @click="getRecommend">맞춤추천받기</button>
  <div></div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/user';
const accountStore = useAccountStore()
const API_URL = 'http://127.0.0.1:8000'


</script>

<style scoped></style>
