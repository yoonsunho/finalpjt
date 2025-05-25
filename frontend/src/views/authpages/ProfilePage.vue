<template>
  <div class="profile-wrapper">
    <h1 class="profile-name">
      <strong>{{ user?.nickname }}</strong
      >님의 프로필
    </h1>
    <div class="profile-container"></div>
    <div class="profile-tab-category">
      <button @click="activeTab = '회원정보'" :class="{ active: activeTab === '회원정보' }">
        회원정보
      </button>
      <button @click="activeTab = '찜한 상품'" :class="{ active: activeTab === '찜한 상품' }">
        찜한 상품
      </button>
      <button @click="activeTab = '가입한 상품'" :class="{ active: activeTab === '가입한 상품' }">
        가입한 상품
      </button>
    </div>

    <div class="profile-tab-content">
      <div v-if="activeTab === '회원정보'">
        <ProfileInfo />
      </div>
      <div v-if="activeTab === '찜한 상품'">
        <MyInterests />
      </div>
      <div v-if="activeTab === '가입한 상품'">
        <MyJoins />
      </div>
    </div>
  </div>
</template>

<script setup>
import ProfileInfo from '@/views/authpages/ProfileInfo.vue'
import { ref, computed } from 'vue'
import { useAccountStore } from '@/stores/user'
import MyInterests from '@/components/product/MyInterests.vue'
import MyJoins from '@/components/product/MyJoins.vue'
const accountStore = useAccountStore()
const user = computed(() => accountStore.userInfo)
const activeTab = ref('회원정보') // 초기메뉴
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
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  gap: 20px;
}

.profile-name {
  font-size: 1.7rem;
  /* font-weight: bold; */
}
.profile-container {
  display: flex;
  /* box-shadow: inset 0 0 3px orange; */
  padding: 20px 0 0 0;
  border-top: 1px solid #191f28;
}

.profile-tab-category {
  display: flex;
  gap: 10px;
  padding-right: 20px;
  /* box-shadow: inset 0 0 3px dodgerblue; */
  border-right: 1px solid #191f28;
  gap: 16px;
}
.profile-category-detail {
  /* box-shadow: inset 0 0 3px pink; */
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.profile-tab-content {
  margin-top: 20px;
  padding: 10px;
}

button.active {
  font-weight: bold;
  border-bottom: 2px solid #191f28;
}
</style>
