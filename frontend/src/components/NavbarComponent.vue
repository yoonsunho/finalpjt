<template>
  <nav class="navbar">
    <div class="container">
      <div class="nav-brand">
        <RouterLink :to="{ name: 'MainPage' }">
          <!-- <img src="" alt="선호바보개_로고" class="nav-logo"/> -->
          <p class="logo-title">sunho.</p>
        </RouterLink>
      </div>

      <button class="menu-toggle" @click="toggleMenu" aria-label="메뉴 열기">
        <span class="menu-icon">☰</span>
      </button>

      <div :class="['nav-menu', { 'nav-menu-active': isMenuOpen }]">
        <ul class="nav-list">
          <li
            class="nav-item dropdown"
            @mouseenter="openDropdown('deposit')"
            @mouseleave="closeDropdown"
          >
            <button class="nav-link dropdown-toggle" @click="toggleDropdown('deposit')">
              <p>예적금추천</p>
            </button>
            <ul :class="['dropdown-menu', { active: activeDropdown === 'deposit' }]">
              <li>
                <RouterLink :to="{ name: 'DepositListView' }" class="dropdown-item"
                  >예금</RouterLink
                >
              </li>
              <li>
                <RouterLink :to="{ name: 'SavingListView' }" class="dropdown-item">적금</RouterLink>
              </li>
            </ul>
          </li>

          <li
            class="nav-item dropdown"
            @mouseenter="openDropdown('community')"
            @mouseleave="closeDropdown"
          >
            <button class="nav-link dropdown-toggle" @click="toggleDropdown('community')">
              <p>커뮤니티</p>
            </button>
            <ul :class="['dropdown-menu', { active: activeDropdown === 'community' }]">
              <li>
                <RouterLink
                  :to="{ name: 'CommunityPage', params: { category: 'review' } }"
                  class="dropdown-item"
                  >예적금 후기</RouterLink
                >
              </li>
              <li>
                <RouterLink
                  :to="{ name: 'CommunityPage', params: { category: 'tip' } }"
                  class="dropdown-item"
                  >절약 꿀팁</RouterLink
                >
              </li>
              <li>
                <RouterLink
                  :to="{ name: 'CommunityPage', params: { category: 'free' } }"
                  class="dropdown-item"
                  >자유 게시판</RouterLink
                >
              </li>
            </ul>
          </li>

          <li class="nav-item">
            <button class="nav-link">
              <RouterLink :to="{ name: 'SharedSavingRoomListView', params: { category: 'review' } }"
                ><p>공유저축</p></RouterLink
              >
            </button>
          </li>
          <li class="nav-item">
            <button class="nav-link">
              <RouterLink :to="{ name: 'SharedSavingRoomListView', params: { category: 'review' } }"
                ><p>주식 정보</p></RouterLink
              >
            </button>
          </li>
          <li class="nav-item">
            <button class="nav-link">
              <RouterLink :to="{ name: 'SpotPage', params: { category: 'review' } }"
                ><p>현물 시세</p></RouterLink
              >
            </button>
          </li>
          <li class="nav-item">
            <button class="nav-link">
              <RouterLink :to="{ name: 'MapPage', params: { category: 'review' } }"
                ><p>지도</p></RouterLink
              >
            </button>
          </li>
          <!-- <li
            class="nav-item dropdown"
            @mouseenter="openDropdown('EtcPage')"
            @mouseleave="closeDropdown"
          > -->
          <!-- <button class="nav-link dropdown-toggle" @click="toggleDropdown('EtcPage')"> -->
          <!-- <RouterLink :to="{ name: 'EtcPage' }">기타</RouterLink> -->
          <!-- <p>기타</p> -->
          <!-- </button> -->
          <!-- <ul :class="['dropdown-menu', { active: activeDropdown === 'EtcPage' }]"> -->
          <!-- <li> -->
          <!-- <RouterLink :to="{ name: 'SpotPage' }" class="dropdown-item">환율</RouterLink> -->
          <!-- </li> -->
          <!-- <li> -->
          <!-- <RouterLink :to="{ name: 'MapPage' }" class="dropdown-item">지도</RouterLink> -->
          <!-- </li> -->
          <!-- </ul> -->
          <!-- </li> -->
        </ul>

        <ul class="auth-links">
          <!-- 로그인 상태  -->
          <template v-if="isLogin">
            <li class="nav-item">
              <RouterLink :to="{ name: 'ProfilePage' }" class="nav-link">마이 페이지</RouterLink>
            </li>
            <li class="nav-item">
              <button class="nav-link" @click="logOut">로그아웃</button>
            </li>
          </template>
          <!-- 로그아웃 상태 -->
          <template v-else>
            <li class="nav-item">
              <RouterLink :to="{ name: 'LoginView' }" class="nav-link">로그인</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink :to="{ name: 'SignUpView' }" class="nav-link sign-up-btn"
                >회원가입</RouterLink
              >
            </li>
          </template>
        </ul>
      </div>
    </div>
  </nav>
</template>
<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/user'
import { storeToRefs } from 'pinia'

const accountStore = useAccountStore()
const { isLogin } = storeToRefs(accountStore)
const { logOut } = accountStore

const isMenuOpen = ref(false)
const activeDropdown = ref(null)
const isDesktop = ref(window.innerWidth > 768)

const router = useRouter()

// 메뉴 열렸는지 초기화하기
const resetMenuState = () => {
  isMenuOpen.value = false
  activeDropdown.value = null
}

// 메뉴 토글
const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
  if (!isMenuOpen.value) {
    activeDropdown.value = null
  }
}

// 드롭다운 열기
const openDropdown = (menu) => {
  if (isDesktop.value) {
    activeDropdown.value = menu
  }
}

// 드롭다운 닫기
const closeDropdown = () => {
  if (isDesktop.value) {
    activeDropdown.value = null
  }
}

// 모바일 드롭다운
const toggleDropdown = (menu) => {
  if (!isDesktop.value) {
    activeDropdown.value = activeDropdown.value === menu ? null : menu
  }
}

// 반응형상태인지 체크
const checkViewport = () => {
  isDesktop.value = window.innerWidth > 768
  if (isDesktop.value) {
    resetMenuState()
  }
}

onMounted(() => {
  window.addEventListener('resize', checkViewport)
  // 라우터가 바뀔때마다 메뉴상태 초기화
  router.afterEach(() => {
    resetMenuState()
  })
})
</script>

<style scoped>
* {
  font-family: Pretendard;
}
.navbar {
  width: 100%;
  background-color: #ffffff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 1000;
}

.container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1.25rem;
  flex-wrap: wrap;
  max-width: 1200px;
  margin: 0 auto;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.nav-logo {
  width: 40px;
  height: 40px;
  object-fit: contain;
}

.logo-title {
  font-weight: 900;
  /* 800 ? */
  font-size: 1.5rem;
}
.brand-text {
  font-size: 1.25rem;
  font-weight: 600;
  color: #3182f6;
}

.menu-toggle {
  display: none;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  font-size: 1.5rem;
}

/* Navigation Menu */
.nav-menu {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-grow: 1;
}

.nav-list,
.auth-links {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
  gap: 1rem;
}

.nav-list {
  margin-left: 2rem;
}

.auth-links {
  margin-left: auto;
}

.nav-item {
  position: relative;
}

.nav-link {
  padding: 0.5rem 0.75rem;
  color: #191f28;
  text-decoration: none;
  font-size: 1rem;
  font-weight: 500;
  transition: color 0.2s ease;
  display: block;
}

.nav-link:hover {
  color: #2574e6;
}

.sign-up-btn {
  background-color: #3182f6;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 5rem;
  font-weight: 500;
}

.sign-up-btn:hover {
  color: white;
  background-color: #2574e6;
}

.dropdown {
  position: relative;
}

.dropdown-toggle {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.5rem 0.75rem;
  color: #191f28;
  font-weight: 500;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  width: 150px;
  background-color: white;
  border-radius: 0.25rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  list-style: none;
  padding: 0;
  margin: 0;
  z-index: 1100;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  pointer-events: none;
  transition: all 0.2s ease;
}

.dropdown-menu.active {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
  pointer-events: auto;
  padding: 0.5rem 0;
}

.dropdown-item {
  padding: 0.5rem 1rem;
  color: #191f28;
  text-decoration: none;
  display: block;
  transition: background-color 0.2s ease;
}

.dropdown-item:hover {
  /* background-color: #f3f4f6; */
  color: #2574e6;
}

@media (max-width: 768px) {
  .container {
    flex-wrap: wrap;
  }

  .menu-toggle {
    display: block;
  }

  .nav-menu {
    display: none;
    flex-direction: column;
    align-items: flex-start;
    width: 100%;
    padding-top: 1rem;
    overflow: hidden;
    max-height: 0;
    transition: max-height 0.2s ease;
  }

  .nav-menu-active {
    display: flex;
    max-height: 500px;
  }

  .nav-list,
  .auth-links {
    flex-direction: column;
    width: 100%;
    margin: 0;
    gap: 0;
  }

  .auth-links {
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid #e5e7eb;
  }

  .nav-link {
    padding: 0.75rem 0;
  }
  .sign-up-btn {
    display: inline-block;
    margin-top: 0.5rem;
    border-radius: 0;
    font-weight: normal;
    background-color: transparent;
    color: #191f28;
  }
  .sign-up-btn:hover {
    color: #2574e6;
    background-color: transparent;
  }

  .dropdown-toggle {
    width: 100%;
    justify-content: space-between;
    padding: 0.75rem 0;
  }

  .dropdown-menu {
    position: static;
    width: 100%;
    box-shadow: none;
    border-radius: 0;
    background-color: #f9fafb;
    margin: 0;
    padding: 0;
    max-height: 0;
    overflow: hidden;
    opacity: 0;
    visibility: hidden;
    transform: none;
    transition: all 0.2s ease;
  }

  .dropdown-menu.active {
    max-height: 200px;
    opacity: 1;
    visibility: visible;
    margin-bottom: 0.5rem;
    padding-left: 1rem;
  }

  .dropdown-item {
    padding: 0.75rem 1rem;
  }
}
</style>
