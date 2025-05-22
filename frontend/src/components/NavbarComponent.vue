<template>
  <nav class="navbar">
    <div class="container">
      <div class="nav-brand">
        <RouterLink :to="{ name: 'MainPage' }"
          ><img src="" alt="선호바보개_로고" class="nav-logo"
        /></RouterLink>
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
              <RouterLink :to="{ name: 'DepositListView' }">예적금추천</RouterLink>
            </button>
            <ul :class="['dropdown-menu', { active: activeDropdown === 'deposit' }]">
              <li><a href="#" class="dropdown-item">예금</a></li>
              <li><a href="#" class="dropdown-item">적금</a></li>
            </ul>
          </li>

          <li class="nav-item">
            <a href="#" class="nav-link">
              <RouterLink :to="{ name: 'CommunityPage' }">커뮤니티</RouterLink>
            </a>
          </li>
          <li class="nav-item">
            <a href="#" class="nav-link">저축</a>
          </li>

          <li
            class="nav-item dropdown"
            @mouseenter="openDropdown('etc')"
            @mouseleave="closeDropdown"
          >
            <button class="nav-link dropdown-toggle" @click="toggleDropdown('etc')">
              <RouterLink :to="{ name: 'EtcPage' }">기타</RouterLink>
            </button>
            <ul :class="['dropdown-menu', { active: activeDropdown === 'etc' }]">
              <li><a href="#" class="dropdown-item">환율</a></li>
              <li><a href="#" class="dropdown-item">지도</a></li>
            </ul>
          </li>
        </ul>

        <ul class="auth-links">
          <li class="nav-item">
            <a href="#" class="nav-link">
              <RouterLink :to="{ name: 'LogInView' }">로그인</RouterLink>
            </a>
          </li>
          <li class="nav-item">
            <a href="#" class="nav-link sign-up-btn">
              <RouterLink :to="{ name: 'SignUpView' }">회원가입</RouterLink>
            </a>
          </li>
        </ul>

        <!-- 로그인상태에는 프로필 노출 -->
        <!-- <ul class="">
          <li class="nav-item">
            <a href="#" class="nav-link">
              <RouterLink :to="{ name: 'profile' }">프로필</RouterLink>
            </a>
          </li>
        </ul> -->
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const isMenuOpen = ref(false)
const activeDropdown = ref(null)
const isDesktop = ref(window.innerWidth > 768)

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
  if (!isMenuOpen.value) {
    activeDropdown.value = null
  }
}
const openDropdown = (menu) => {
  if (isDesktop.value) {
    activeDropdown.value = menu
  }
}

const closeDropdown = () => {
  if (isDesktop.value) {
    activeDropdown.value = null
  }
}

const toggleDropdown = (menu) => {
  if (!isDesktop.value) {
    activeDropdown.value = activeDropdown.value === menu ? null : menu
  }
}
const checkViewport = () => {
  isDesktop.value = window.innerWidth > 768

  if (isDesktop.value) {
    isMenuOpen.value = false
  }
}

onMounted(() => {
  window.addEventListener('resize', checkViewport)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', checkViewport)
})
</script>

<style scoped>
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
  color: #4b5563;
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
  background-color: #2574e6;
  color: white;
  transition:
    background 0.2s ease,
    color 0.1s ease;
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
  color: #4b5563;
  font-weight: 500;
}

.dropdown-arrow {
  font-size: 0.75rem;
  transition: transform 0.2s ease;
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
  padding: 0.5rem 0;
  margin: 0;
  z-index: 1100;
  opacity: 0;
  visibility: hidden;
  transition:
    opacity 0.2s ease,
    visibility 0.2s ease;
}

.dropdown-menu.active {
  opacity: 1;
  visibility: visible;
}

.dropdown-item {
  padding: 0.5rem 1rem;
  color: #4b5563;
  text-decoration: none;
  display: block;
  transition: background-color 0.2s ease;
}

.dropdown-item:hover {
  background-color: #f3f4f6;
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
    transition: max-height 0.3s ease;
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
    padding-left: 1rem;
    background-color: #f9fafb;
    margin-bottom: 0.5rem;
    opacity: 0;
    visibility: hidden;
    max-height: 0;
    overflow: hidden;
    transition:
      max-height 0.3s ease,
      opacity 0.3s ease,
      visibility 0s linear 0.3s;
  }

  .dropdown-menu.active {
    opacity: 1;
    visibility: visible;
    max-height: 200px;
    transition:
      max-height 0.3s ease,
      opacity 0.3s ease,
      visibility 0s linear 0s;
  }

  .dropdown-item {
    padding: 0.75rem 1rem;
  }
}
</style>
