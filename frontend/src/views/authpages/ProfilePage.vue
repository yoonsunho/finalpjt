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
      <button @click="activeTab = '공동저축방'" :class="{ active: activeTab === '공동저축방' }">
        공동저축방
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
      <div v-if="activeTab === '공동저축방'">
        <MySavingRooms />
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
import MySavingRooms from '@/components/savingroom/MySavingRooms.vue'
const accountStore = useAccountStore()
const user = computed(() => accountStore.userInfo)
const activeTab = ref('회원정보') // 초기메뉴
</script>

<style scoped>
* {
  font-family: Pretendard;
}
.profile-wrapper {
  display: flex;
  flex-direction: column;
  min-width: 300px;
  max-width: 800px;
  margin: 80px auto;
  padding: 40px;
  border-radius: 16px;
  background: #ffffff;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
  gap: 20px;
}

.profile-name {
  font-size: 1.7rem;
  font-weight: 600;
  color: #1f2937;
}

.profile-tab-category {
  display: flex;
  gap: 16px;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 8px;
}

.profile-tab-category button {
  background: none;
  border: none;
  padding: 8px 12px;
  font-weight: 500;
  font-size: 15px;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s ease;
}

.profile-tab-category button.active {
  font-weight: 700;
  color: #111827;
  border-bottom: 2px solid #1f2937;
}

.profile-tab-content {
  margin-top: 20px;
}
</style>
