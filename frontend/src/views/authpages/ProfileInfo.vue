<template>
  <div class="profile-category-info">
    <p>이메일: {{ user?.email }}</p>
    <p>닉네임: {{ user?.nickname }}</p>
    <p>
      성별:
      <span v-if="user?.gender === 'M'">남성</span>
      <span v-else-if="user?.gender === 'F'">여성</span>
      <span v-else>정보 없음</span>
    </p>
    <p>연봉: {{ user?.salary }}</p>
    <p>성향: {{ user?.tendency }}</p>
    <p>저축금액: {{ user?.deposit_amount }}</p>
    <p>저축기간: {{ user?.deposit_period }}</p>
  </div>
  <button class="profile-edit" type="button" @click="$router.push({ name: 'ProfileEdit' })">
    회원정보 수정
  </button>
</template>

<script setup>
import { computed } from 'vue'
import { useAccountStore } from '@/stores/user'
const accountStore = useAccountStore()
const user = computed(() => accountStore.userInfo)
</script>

<style scoped>
button {
  background-color: dodgerblue;
  width: 100px;
  margin: 10px auto;
}
</style>
