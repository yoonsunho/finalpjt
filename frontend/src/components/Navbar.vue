<template>
  <nav class="navbar">
    <div class="navbar-left">
      <span class="logo">윤선호바보</span>

      <!-- 햄버거 버튼 -->
      <button class="burger" @click="toggleMenu">
        ☰
      </button>

      <!-- 메뉴 -->
      <div class="nav-links" :class="{ open: isOpen }">
        <a class="nav-item" href="#">예적금추천</a>
        <a class="nav-item" href="#">커뮤니티</a>
        <a class="nav-item" href="#">저축</a>
      </div>
    </div>

    <div class="navbar-right">
      <a class="nav-item" href="#">회원가입</a>
      <a class="nav-item" href="#">로그인</a>
    </div>
  </nav>
</template>

<script>
export default {
  name: "Navbar",
  data() {
    return {
      isOpen: false,
    };
  },
  methods: {
    toggleMenu() {
      this.isOpen = !this.isOpen;
    },
  },
};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: white;
  border-bottom: 1px solid #e5e5e5;
  flex-wrap: wrap;
}

.navbar-left {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.logo {
  font-weight: bold;
  font-size: 1.5rem;
  color: black;
}

.burger {
  display: none;
  font-size: 1.5rem;
  background: none;
  border: none;
  cursor: pointer;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.nav-item {
  text-decoration: none;
  color: #363636;
  font-size: 0.95rem;
}

.nav-item:hover {
  color: #00d1b2;
}

.icon {
  width: 20px;
  height: 20px;
}

.download-btn {
  background-color: #00d1b2;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
}

.download-btn:hover {
  background-color: #00b89c;
}

.navbar-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

/* 반응형 스타일 */
@media (max-width: 768px) {
  .nav-links {
    display: none;
    flex-direction: column;
    width: 100%;
  }

  .nav-links.open {
    display: flex;
    margin-top: 1rem;
  }

  .burger {
    display: block;
  }

  .navbar {
    align-items: flex-start;
  }

  .navbar-right {
    margin-top: 1rem;
    width: 100%;
    justify-content: flex-end;
  }
}
</style>
