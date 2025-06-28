import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { AuthService } from '@/services/auth'
import type { UserProfile } from '@/types/api'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<UserProfile | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const isAuthenticated = computed(() => !!user.value)
  const isMentor = computed(() => user.value?.role === 'mentor')
  const isMentee = computed(() => user.value?.role === 'mentee')
  const userName = computed(() => user.value?.profile.name || '')

  // Actions
  const login = async (email: string, password: string) => {
    try {
      isLoading.value = true
      error.value = null
      
      console.log('🔥 [STORE] 로그인 시도:', { email })
      await AuthService.login({ email, password })
      console.log('✅ [STORE] 로그인 성공, 사용자 정보 가져오는 중...')
      
      await fetchCurrentUser()
      console.log('✅ [STORE] 사용자 정보 가져오기 완료:', user.value)
      
      return true
    } catch (err: any) {
      console.error('❌ [STORE] 로그인 실패:', err)
      error.value = err.response?.data?.error || '로그인에 실패했습니다.'
      return false
    } finally {
      isLoading.value = false
    }
  }

  const signup = async (email: string, password: string, name: string, role: 'mentor' | 'mentee') => {
    try {
      isLoading.value = true
      error.value = null
      
      await AuthService.signup({ email, password, name, role })
      return true
    } catch (err: any) {
      error.value = err.response?.data?.error || '회원가입에 실패했습니다.'
      return false
    } finally {
      isLoading.value = false
    }
  }

  const logout = () => {
    console.log('🚪 [STORE] 로그아웃 호출됨!')
    user.value = null
    AuthService.logout()
  }

  const fetchCurrentUser = async () => {
    try {
      if (!AuthService.hasToken()) {
        console.log('🚫 [STORE] 토큰이 없어서 사용자 정보를 가져올 수 없음')
        return
      }
      
      console.log('🔍 [STORE] 현재 사용자 정보 요청 중...')
      isLoading.value = true
      user.value = await AuthService.getCurrentUser()
      console.log('✅ [STORE] 사용자 정보 가져오기 성공:', user.value)
    } catch (err: any) {
      console.error('❌ [STORE] 사용자 정보 가져오기 실패:', err)
      // 토큰이 유효하지 않은 경우 로그아웃
      logout()
    } finally {
      isLoading.value = false
    }
  }

  const updateUserProfile = (updatedUser: UserProfile) => {
    user.value = updatedUser
  }

  const clearError = () => {
    error.value = null
  }

  // 앱 초기화 시 토큰이 있으면 사용자 정보 조회
  const initializeAuth = async () => {
    if (AuthService.hasToken()) {
      await fetchCurrentUser()
    }
  }

  return {
    // State
    user,
    isLoading,
    error,
    
    // Getters
    isAuthenticated,
    isMentor,
    isMentee,
    userName,
    
    // Actions
    login,
    signup,
    logout,
    fetchCurrentUser,
    updateUserProfile,
    clearError,
    initializeAuth
  }
})
