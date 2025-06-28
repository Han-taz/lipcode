<template>
  <nav class="navbar">
    <div class="container">
      <div class="navbar-brand">
        <router-link to="/" class="brand-link">
          <span class="brand-icon">🎯</span>
          <span class="brand-text">멘토링 플랫폼</span>
        </router-link>
      </div>

      <div class="navbar-menu">
        <div v-if="!authStore.isAuthenticated" class="navbar-nav">
          <router-link to="/login" class="nav-link">로그인</router-link>
          <router-link to="/signup" class="nav-link btn-primary">회원가입</router-link>
        </div>

        <div v-else class="navbar-nav">
          <span class="user-greeting">{{ authStore.userName }}님</span>
          
          <router-link to="/profile" class="nav-link">
            <span class="nav-icon">👤</span>
            프로필
          </router-link>

          <router-link 
            v-if="authStore.isMentee" 
            to="/mentors" 
            class="nav-link"
          >
            <span class="nav-icon">🎓</span>
            멘토 찾기
          </router-link>

          <router-link to="/match-requests" class="nav-link">
            <span class="nav-icon">📋</span>
            {{ authStore.isMentor ? '요청 관리' : '내 요청' }}
          </router-link>

          <button @click="authStore.logout" class="nav-link logout-btn">
            <span class="nav-icon">🚪</span>
            로그아웃
          </button>
        </div>
      </div>

      <!-- 모바일 메뉴 버튼 -->
      <button 
        class="mobile-menu-btn"
        @click="toggleMobileMenu"
        :class="{ active: showMobileMenu }"
      >
        <span></span>
        <span></span>
        <span></span>
      </button>
    </div>

    <!-- 모바일 메뉴 -->
    <div v-if="showMobileMenu" class="mobile-menu">
      <div v-if="!authStore.isAuthenticated" class="mobile-nav">
        <router-link to="/login" class="mobile-nav-link" @click="closeMobileMenu">
          로그인
        </router-link>
        <router-link to="/signup" class="mobile-nav-link" @click="closeMobileMenu">
          회원가입
        </router-link>
      </div>

      <div v-else class="mobile-nav">
        <div class="mobile-user-info">
          <span>{{ authStore.userName }}님</span>
          <span class="user-role">{{ authStore.isMentor ? '멘토' : '멘티' }}</span>
        </div>
        
        <router-link to="/profile" class="mobile-nav-link" @click="closeMobileMenu">
          👤 프로필
        </router-link>

        <router-link 
          v-if="authStore.isMentee" 
          to="/mentors" 
          class="mobile-nav-link"
          @click="closeMobileMenu"
        >
          🎓 멘토 찾기
        </router-link>

        <router-link to="/match-requests" class="mobile-nav-link" @click="closeMobileMenu">
          📋 {{ authStore.isMentor ? '요청 관리' : '내 요청' }}
        </router-link>

        <button @click="handleLogout" class="mobile-nav-link logout-btn">
          🚪 로그아웃
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const showMobileMenu = ref(false)

const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value
}

const closeMobileMenu = () => {
  showMobileMenu.value = false
}

const handleLogout = () => {
  authStore.logout()
  closeMobileMenu()
}
</script>

<style scoped>
.navbar {
  background: white;
  border-bottom: 1px solid var(--color-border);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1rem;
  max-width: 1200px;
  margin: 0 auto;
}

/* 브랜드 */
.navbar-brand {
  flex-shrink: 0;
}

.brand-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: var(--color-text);
  font-weight: 600;
  font-size: 1.25rem;
}

.brand-icon {
  margin-right: 0.5rem;
  font-size: 1.5rem;
}

.brand-text {
  color: var(--color-primary);
}

/* 네비게이션 메뉴 */
.navbar-menu {
  display: flex;
  align-items: center;
}

.navbar-nav {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-greeting {
  color: var(--color-text-soft);
  font-size: 0.875rem;
  margin-right: 0.5rem;
}

.nav-link {
  display: flex;
  align-items: center;
  padding: 0.5rem 0.75rem;
  text-decoration: none;
  color: var(--color-text);
  font-size: 0.875rem;
  font-weight: 500;
  border-radius: 4px;
  transition: all 0.2s;
  background: none;
  border: none;
  cursor: pointer;
}

.nav-link:hover {
  color: var(--color-primary);
  background-color: rgba(62, 175, 124, 0.1);
}

.nav-link.router-link-active {
  color: var(--color-primary);
  background-color: rgba(62, 175, 124, 0.15);
}

.nav-link.btn-primary {
  background-color: var(--color-primary);
  color: white;
}

.nav-link.btn-primary:hover {
  background-color: var(--color-primary-dark);
  color: white;
}

.nav-icon {
  margin-right: 0.25rem;
  font-size: 0.875rem;
}

.logout-btn {
  color: var(--color-danger) !important;
}

.logout-btn:hover {
  background-color: rgba(231, 76, 60, 0.1) !important;
  color: var(--color-danger) !important;
}

/* 모바일 메뉴 버튼 */
.mobile-menu-btn {
  display: none;
  flex-direction: column;
  justify-content: space-around;
  width: 24px;
  height: 24px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
}

.mobile-menu-btn span {
  width: 100%;
  height: 2px;
  background-color: var(--color-text);
  transition: all 0.3s;
}

.mobile-menu-btn.active span:nth-child(1) {
  transform: rotate(45deg) translate(5px, 5px);
}

.mobile-menu-btn.active span:nth-child(2) {
  opacity: 0;
}

.mobile-menu-btn.active span:nth-child(3) {
  transform: rotate(-45deg) translate(7px, -6px);
}

/* 모바일 메뉴 */
.mobile-menu {
  display: none;
  background: white;
  border-top: 1px solid var(--color-border);
  padding: 1rem;
}

.mobile-nav {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.mobile-user-info {
  display: flex;
  flex-direction: column;
  padding: 1rem;
  background-color: var(--color-background-soft);
  border-radius: 4px;
  margin-bottom: 0.5rem;
}

.user-role {
  font-size: 0.75rem;
  color: var(--color-text-soft);
  text-transform: uppercase;
}

.mobile-nav-link {
  display: flex;
  align-items: center;
  padding: 0.75rem;
  text-decoration: none;
  color: var(--color-text);
  font-weight: 500;
  border-radius: 4px;
  transition: background-color 0.2s;
  background: none;
  border: none;
  cursor: pointer;
  text-align: left;
  width: 100%;
}

.mobile-nav-link:hover {
  background-color: var(--color-background-soft);
}

/* 반응형 */
@media (max-width: 768px) {
  .navbar-menu {
    display: none;
  }

  .mobile-menu-btn {
    display: flex;
  }

  .mobile-menu {
    display: block;
  }
}

@media (max-width: 640px) {
  .brand-text {
    display: none;
  }
}
</style>
