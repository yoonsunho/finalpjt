<template>
  <div class="profile-wrapper">
    <!-- <h1 class="profile-name">{{ user?.email }} 님의 프로필</h1> -->
    <h1 class="profile-name"><strong>선호바보개</strong>님의 프로필</h1>
    <div class="profile-container">
      <div class="profile-category">
        <p><strong>회원정보</strong></p>
        <p>찜한 상품</p>
        <p>가입한 상품</p>
      </div>
      <div class="profile-category-detail">
        <ProfileInfo />
      </div>
    </div>
  </div>
</template>

<script setup>
import ProfileInfo from '@/views/authpages/ProfileInfo.vue'
import { computed } from 'vue'
import { useAccountStore } from '@/stores/user'
const accountStore = useAccountStore()
const user = computed(() => accountStore.userInfo)
</script>

<style scoped>
.profile-wrapper {
  display: flex;
  flex-direction: column;
  /* margin: auto; */
  min-width: 300px;
  /* margin: auto; */

  /* 수정해야함.임의설정 */
  margin: 100px;     

  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  gap: 20px;
}

.profile-name {
  font-size: 1.7rem;
  /* font-weight: bold; */
}
.profile-container {
  display: flex;
  /* box-shadow: inset 0 0 3px orange; */
  padding:20px 0 0 0;
  border-top: 1px solid #666;
  
}

.profile-category {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding-right: 20px;
  /* box-shadow: inset 0 0 3px dodgerblue; */
  border-right: 1px solid #666;
}
.profile-category-detail {
  /* box-shadow: inset 0 0 3px pink; */
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}
</style>
