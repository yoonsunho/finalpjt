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
      <p>{{ salaryMap[user?.salary] }}</p>
      <p>{{ tendencyMap[user?.tendency] }}</p>
      <p>{{ depositAmountMap[user?.deposit_amount] }}</p>
      <p>{{ depositPeriodMap[user?.deposit_period] }}</p>
    </div>
  </div>
  <button class="profile-edit" type="button" @click="$router.push({ name: 'ProfileEdit' })">
    회원정보 수정
  </button>
  <button
    v-if="!accountStore.isGoogleUser"
    class="password-edit"
    @click="$router.push({ name: 'PasswordEdit' })"
  >
    비밀번호 수정
  </button>
</template>

<script setup>
import { computed } from 'vue'
import { useAccountStore } from '@/stores/user'
const accountStore = useAccountStore()
const user = computed(() => accountStore.userInfo)

const salaryMap = {
  under_30m: '3천만원 미만',
  '30m_50m': '3천만원~5천만원',
  '50m_100m': '5천만원~1억원',
  over_100m: '1억원 이상',
}

const tendencyMap = {
  safe: '안정형',
  neutral: '중립형',
  aggressive: '공격형',
}

const depositAmountMap = {
  under_100k: '10만원 미만',
  '100k_500k': '10~50만원',
  '500k_1m': '50~100만원',
  over_1m: '100만원 이상',
}

const depositPeriodMap = {
  under_6m: '6개월 미만',
  '6m_12m': '6~12개월',
  '1y_2y': '1~2년',
  over_2y: '2년 이상',
}
</script>

<style scoped>
* {
  font-family: Pretendard;
}
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
