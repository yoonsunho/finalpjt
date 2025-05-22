<template>
  <div class="profile-wrapper">
    <h1 class="profile-name">{{ user?.email }} 님의 프로필</h1>
    <div class="profile-container">
      <div class="profile-category">
        <p>회원정보</p>
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
}

.profile-container {
  display: flex;
}

.profile-category {
  box-shadow: inset 0 0 3px dodgerblue;
}
.profile-category-detail {
  box-shadow: inset 0 0 3px pink;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}
</style>
