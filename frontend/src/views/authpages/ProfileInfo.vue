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
  <div class="btn">
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
  </div>
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
  font-family: Pretendard, sans-serif;
}

.profile-category-info {
  display: flex;
  /* justify-content: center; */
  align-items: flex-start;
  gap: 60px;
  padding: 26px 15px;
  background-color: #ffffff;
  border-radius: 16px;
  /* box-shadow: 0 6px 20px rgba(0, 0, 0, 0.04); */
}

.profile-info-title p,
.profile-info-data p {
  margin: 6px 0;
  gap: 10px;
  font-size: 15px;
  color: #343a40;
  line-height: 1.6;
}

.profile-info-title {
  font-weight: 600;
  color: #495057;
}

.profile-info-data {
  font-weight: 500;
  color: #212529;
}
.btn {
  display: flex;
}
/* 버튼 공통 스타일 */
button {
  display: block;
  width: 100%;
  max-width: 180px;
  padding: 12px 16px;
  margin: 12px auto 0;
  border: none;
  border-radius: 12px;
  background-color: #f1f3f5;
  font-size: 0.95rem;
  font-weight: 600;
  color: #495057;
  text-align: center;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
  transition:
    background-color 0.2s ease,
    color 0.2s ease;
  cursor: pointer;
}

button:hover {
  background-color: #1c64f2;
  color: white;
}
</style>
