<template>
  <div class="profile-wrapper">
    <h1 class="profile-title">{{ user.nickname }}님의 프로필</h1>
    <div class="profile-container">
      <div class="profile-category">
        <p>회원정보</p>
        <p>찜한 상품</p>
        <p>가입 상품</p>
      </div>
      <div class="profile-category-detail">
        dd
      </div>

    </div>
  </div>

  

</template>

<script setup>
import { onMounted, ref, computed } from 'vue';
import { useAccountStore } from '@/stores/user';

const accountStore = useAccountStore()

const user = computed(() => accountStore.userInfo)

onMounted(() => {
  accountStore.fetchUserInfo()
})

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
}
</style>
