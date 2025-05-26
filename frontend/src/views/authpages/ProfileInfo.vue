<template>
  <div class="profile-category-info">
    <div class="profile-info-title">
      <p>이메일</p>
      <p>닉네임</p>
      <p>성별</p>
      <p>연봉</p>
      <p>성향</p>
      <p>희망 저축 금액</p>
      <p>희망 저축 기간</p>
    </div>
    <div class="profile-info-data">
      <p>{{ user?.email }}</p>
      <p>{{ user?.nickname }}</p>
      <p>
        <span v-if="user?.gender === 'M'">남성</span>
        <span v-else-if="user?.gender === 'F'">여성</span>
        <span v-else>정보 없음</span>
      </p>
      <p>{{ user?.salary }}</p>
      <p>{{ user?.tendency }}</p>
      <p>{{ user?.deposit_amount }}</p>
      <p>{{ user?.deposit_period }}</p>
    </div>
  </div>
  <button class="profile-edit" type="button" @click="$router.push({ name: 'ProfileEdit' })">
    회원정보 수정
  </button>
  <button class="password-edit" type="button" @click="$router.push({ name: 'PasswordEdit' })">
    비밀번호 수정
  </button>
</template>

<script setup>
import { computed } from 'vue'
import { useAccountStore } from '@/stores/user'
const accountStore = useAccountStore()
const user = computed(() => accountStore.userInfo)
</script>

<style scoped>
.profile-category-info {
  /* border: 1px solid red; */
  display: flex;
  flex-direction: row;
  padding-left: 20px;
  gap: 50px;
}
.profile-info-title {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.profile-info-data {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
button {
  background-color: dodgerblue;
  width: 100px;
  margin: 10px auto;
}
</style>
