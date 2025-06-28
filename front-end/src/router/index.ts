import { createRouter, createWebHistory } from 'vue-router'
import { AuthService } from '@/services/auth'
import HomeView from '@/views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
      meta: { requiresGuest: true }
    },
    {
      path: '/signup',
      name: 'signup', 
      component: () => import('@/views/SignupView.vue'),
      meta: { requiresGuest: true }
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('@/views/ProfileView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/mentors',
      name: 'mentors',
      component: () => import('@/views/MentorsView.vue'),
      meta: { requiresAuth: true, role: 'mentee' }
    },
    {
      path: '/match-requests',
      name: 'match-requests',
      component: () => import('@/views/MatchRequestsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('@/views/NotFoundView.vue')
    }
  ]
})

// 라우터 가드
router.beforeEach((to, from, next) => {
  const hasToken = AuthService.hasToken()
  
  // 인증이 필요한 페이지
  if (to.meta.requiresAuth && !hasToken) {
    next('/login')
    return
  }
  
  // 비인증 사용자만 접근 가능한 페이지 (로그인, 회원가입)
  if (to.meta.requiresGuest && hasToken) {
    next('/')
    return
  }
  
  next()
})

export default router
