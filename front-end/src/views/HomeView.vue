<template>
  <div class="home">
    <!-- 헤로 섹션 -->
    <section class="hero">
      <div class="hero-content">
        <h1 class="hero-title">멘토-멘티 매칭 플랫폼</h1>
        <p class="hero-subtitle">
          전문가와 학습자를 연결하여 함께 성장하는 공간입니다
        </p>
        <div class="hero-buttons" v-if="!authStore.isAuthenticated">
          <router-link to="/signup" class="btn btn-primary btn-lg">시작하기</router-link>
          <router-link to="/login" class="btn btn-secondary btn-lg">로그인</router-link>
        </div>
      </div>
    </section>

    <!-- 로그인된 사용자 대시보드 -->
    <section v-if="authStore.isAuthenticated" class="dashboard">
      <div class="welcome-card card">
        <h2>안녕하세요, {{ authStore.user?.profile?.name }}님!</h2>
        <p v-if="authStore.user?.role === 'mentor'">
          멘티들의 요청을 확인하고 멘토링을 시작해보세요.
        </p>
        <p v-else>
          관심 있는 멘토를 찾아서 멘토링을 요청해보세요.
        </p>
      </div>

      <!-- 멘토용 대시보드 -->
      <div v-if="authStore.user?.role === 'mentor'" class="mentor-dashboard">
        <div class="stats-grid">
          <div class="stat-card card">
            <h3>대기중인 요청</h3>
            <p class="stat-number">{{ pendingRequests }}</p>
          </div>
          <div class="stat-card card">
            <h3>수락한 요청</h3>
            <p class="stat-number">{{ acceptedRequests }}</p>
          </div>
        </div>
        <div class="quick-actions">
          <router-link to="/match-requests" class="btn btn-primary">
            요청 관리하기
          </router-link>
          <router-link to="/profile" class="btn btn-secondary">
            프로필 수정
          </router-link>
        </div>
      </div>

      <!-- 멘티용 대시보드 -->
      <div v-if="authStore.user?.role === 'mentee'" class="mentee-dashboard">
        <div class="stats-grid">
          <div class="stat-card card">
            <h3>보낸 요청</h3>
            <p class="stat-number">{{ sentRequests }}</p>
          </div>
          <div class="stat-card card">
            <h3>매칭된 멘토</h3>
            <p class="stat-number">{{ matchedMentors }}</p>
          </div>
        </div>
        <div class="quick-actions">
          <router-link to="/mentors" class="btn btn-primary">
            멘토 찾기
          </router-link>
          <router-link to="/match-requests" class="btn btn-secondary">
            요청 현황
          </router-link>
          <router-link to="/profile" class="btn btn-secondary">
            프로필 수정
          </router-link>
        </div>
      </div>
    </section>

    <!-- 기능 소개 섹션 -->
    <section class="features" v-if="!authStore.isAuthenticated">
      <h2>주요 기능</h2>
      <div class="features-grid">
        <div class="feature-card card">
          <h3>🎯 전문가 매칭</h3>
          <p>관심 분야의 전문가와 직접 연결되어 1:1 멘토링을 받아보세요.</p>
        </div>
        <div class="feature-card card">
          <h3>📚 스킬 기반 검색</h3>
          <p>React, Vue, Spring Boot 등 원하는 기술 스택으로 멘토를 찾을 수 있습니다.</p>
        </div>
        <div class="feature-card card">
          <h3>💬 실시간 소통</h3>
          <p>매칭 요청과 수락/거절을 실시간으로 확인하고 소통할 수 있습니다.</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

// 통계 데이터
const pendingRequests = ref(0)
const acceptedRequests = ref(0)
const sentRequests = ref(0)
const matchedMentors = ref(0)

const loadStats = async () => {
  if (!authStore.isAuthenticated) return

  try {
    if (authStore.user?.role === 'mentor') {
      // 멘토용 통계 로드
      // TODO: API 연결
    } else {
      // 멘티용 통계 로드  
      // TODO: API 연결
    }
  } catch (error) {
    console.error('통계 로드 실패:', error)
  }
}

onMounted(() => {
  loadStats()
})
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
}

/* 헤로 섹션 */
.hero {
  text-align: center;
  padding: 60px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 12px;
  margin-bottom: 40px;
}

.hero-title {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 20px;
}

.hero-subtitle {
  font-size: 1.2rem;
  margin-bottom: 30px;
  opacity: 0.9;
}

.hero-buttons {
  display: flex;
  gap: 15px;
  justify-content: center;
  flex-wrap: wrap;
}

.btn-lg {
  padding: 15px 30px;
  font-size: 16px;
}

/* 대시보드 */
.dashboard {
  margin-bottom: 40px;
}

.welcome-card {
  text-align: center;
  margin-bottom: 30px;
}

.welcome-card h2 {
  color: #333;
  margin-bottom: 10px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  text-align: center;
}

.stat-card h3 {
  color: #666;
  margin-bottom: 10px;
  font-size: 1rem;
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: #007bff;
}

.quick-actions {
  display: flex;
  gap: 15px;
  justify-content: center;
  flex-wrap: wrap;
}

/* 기능 소개 */
.features {
  padding: 40px 20px;
}

.features h2 {
  text-align: center;
  margin-bottom: 40px;
  color: #333;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
}

.feature-card {
  text-align: center;
}

.feature-card h3 {
  color: #333;
  margin-bottom: 15px;
}

.feature-card p {
  color: #666;
  line-height: 1.6;
}

/* 반응형 */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-buttons {
    flex-direction: column;
    align-items: center;
  }
  
  .quick-actions {
    flex-direction: column;
  }
}
</style>
