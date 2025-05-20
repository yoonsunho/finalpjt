<!-- NavbarComponent.vue -->
<template>
  <section class="navigation">
    <div class="nav-container">
      <div class="logo">
        <a href="#!">선호바보개</a>
      </div>
      <nav>
        <div class="nav-left"></div>
        <div class="nav-center"></div>
        <div class="nav-right"></div>

        <div class="nav-mobile" @click="toggleMobileMenu">
          <a id="navbar-toggle" :class="{ active: isMobileOpen }"><span></span></a>
        </div>
        <ul class="nav-list" v-show="isMobileOpen || isDesktop">
          <li>
            <a href="#!" @click.prevent="toggleDropdown('deposit')">예적금</a>
            <ul v-show="openDropdown === 'deposit'" class="navbar-dropdown">
              <li><a href="#!">예금</a></li>
              <li><a href="#!">적금</a></li>
            </ul>
          </li>
          <li><a href="#!">커뮤니티</a></li>
          <li><a href="#!">저축</a></li>
          <li>
            <a href="#!" @click.prevent="toggleDropdown('etc')">기타</a>
            <ul v-show="openDropdown === 'etc'" class="navbar-dropdown">
              <li><a href="#!">환율</a></li>
              <li><a href="#!">지도</a></li>
            </ul>
          </li>
          <li><a href="#!">로그인</a></li>
          <li><a href="#!">회원가입</a></li>
        </ul>
      </nav>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const isMobileOpen = ref(false)
const openDropdown = ref(null)
const isDesktop = ref(window.innerWidth > 800)

const toggleMobileMenu = () => {
  isMobileOpen.value = !isMobileOpen.value
}

const toggleDropdown = (menuName) => {
  openDropdown.value = openDropdown.value === menuName ? null : menuName
}

const handleResize = () => {
  isDesktop.value = window.innerWidth > 800
  if (isDesktop.value) {
    isMobileOpen.value = true
  }
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
  handleResize()
  document.addEventListener('click', handleOutsideClick)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  document.removeEventListener('click', handleOutsideClick)
})

const handleOutsideClick = (e) => {
  if (!e.target.closest('nav')) {
    openDropdown.value = null
  }
}
</script>

<style scoped>
/* 기본 세팅 */
body {
  margin: 0;
  padding: 0;
  font-family: 'Pretendard', sans-serif;
}
.navigation {
  height: 55px;
  background: linear-gradient(45deg, #4199fe, #74b4fe);
}
.logo {
  position: absolute;
  padding-left: 20px;
  float: left;
  line-height: 55px;
  text-transform: uppercase;
  font-size: 1.4em;
}
.logo a {
  color: #ffffff;
  text-decoration: none;
}
.nav-container {
  max-width: 1000px;
  margin: 0 auto;
}
nav {
  float: right;
}
nav ul {
  list-style: none;
  margin: 0;
  padding: 0;
}
nav ul li {
  float: left;
  position: relative;
}
nav ul li a {
  display: block;
  padding: 0 20px;
  line-height: 55px;
  color: #fff;
  background: transparent;
  text-decoration: none;
}
nav ul li a:hover {
  background: #2581dc;
  color: #ffffff;
}
.navbar-dropdown li a {
  background: #2581dc;
}
nav ul li a:not(:only-child)::after {
  padding-left: 4px;
  content: ' \025BE';
}
nav ul li ul li {
  min-width: 190px;
}
nav ul li ul li a {
  padding: 15px;
  line-height: 20px;
}
.navbar-dropdown {
  position: absolute;
  display: none;
  z-index: 1;
  background: #fff;
  box-shadow: 0 0 35px 0 rgba(0, 0, 0, 0.25);
}
.navbar-dropdown[style*="display: block"] {
  display: block !important;
}

/* Mobile navigation */
.nav-mobile {
  display: none;
  position: absolute;
  top: 0;
  right: 0;
  background: transparent;
  height: 55px;
  width: 70px;
}
@media only screen and (max-width: 800px) {
  .nav-mobile {
    display: block;
  }
  nav {
    width: 100%;
    padding: 55px 0 15px;
  }
  nav ul {
    display: none;
  }
  nav ul li {
    float: none;
  }
  nav ul li a {
    padding: 15px;
    line-height: 20px;
    background: #262626;
  }
  nav ul li ul li a {
    padding-left: 30px;
  }
  .navbar-dropdown {
    position: static;
  }
}
@media screen and (min-width: 801px) {
  .nav-list {
    display: block !important;
  }
}
#navbar-toggle {
  position: absolute;
  left: 18px;
  top: 15px;
  cursor: pointer;
  padding: 10px 35px 16px 0px;
}
#navbar-toggle span,
#navbar-toggle span::before,
#navbar-toggle span::after {
  cursor: pointer;
  border-radius: 1px;
  height: 3px;
  width: 30px;
  background: #ffffff;
  position: absolute;
  display: block;
  content: '';
  transition: all 300ms ease-in-out;
}
#navbar-toggle span::before {
  top: -10px;
}
#navbar-toggle span::after {
  bottom: -10px;
}
#navbar-toggle.active span {
  background-color: transparent;
}
#navbar-toggle.active span::before {
  transform: rotate(45deg);
  top: 0;
}
#navbar-toggle.active span::after {
  transform: rotate(-45deg);
  top: 0;
}
</style>
