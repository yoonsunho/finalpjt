<template>
  <div class="success-wrapper">
    <h1>🎉 가입이 완료되었습니다!</h1>
    <p>잠시 로그인 페이지로 이동합니다.</p>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

onMounted(() => {
  setTimeout(() => {
    router.push({ name: 'LoginView' })
  }, 8000)
})
</script>

<style scoped>
.success-wrapper {
  max-width: 400px;
  margin: 100px auto;
  padding: 2rem;
  text-align: center;
  font-size: 1.2rem;
  border: 2px solid #00b894;
  border-radius: 12px;
}
</style>
