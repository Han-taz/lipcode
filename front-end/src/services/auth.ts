import { apiClient } from './api'
import type { 
  LoginRequest, 
  LoginResponse, 
  SignupRequest, 
  UserProfile 
} from '@/types/api'

export class AuthService {
  // 회원가입
  static async signup(data: SignupRequest): Promise<void> {
    console.log('🔥 [AUTH] 회원가입 요청:', data)
    try {
      const response = await apiClient.post('/signup', data)
      console.log('✅ [AUTH] 회원가입 성공:', response)
    } catch (error) {
      console.error('❌ [AUTH] 회원가입 실패:', error)
      throw error
    }
  }

  // 로그인
  static async login(data: LoginRequest): Promise<LoginResponse> {
    console.log('🔥 [AUTH] 로그인 요청:', data)
    try {
      const response = await apiClient.post<LoginResponse>('/login', data)
      console.log('✅ [AUTH] 로그인 성공:', response)
      
      // 토큰을 로컬 스토리지에 저장
      localStorage.setItem('token', response.token)
      console.log('💾 [AUTH] 토큰 저장됨:', response.token)
      console.log('🔍 [AUTH] 저장된 토큰 확인:', localStorage.getItem('token'))
      
      return response
    } catch (error) {
      console.error('❌ [AUTH] 로그인 실패:', error)
      throw error
    }
  }

  // 로그아웃
  static logout(): void {
    console.log('🚪 [AUTH] 로그아웃 처리 중...')
    localStorage.removeItem('token')
    console.log('🗑️ [AUTH] 토큰 삭제됨')
    console.log('🔍 [AUTH] 로그아웃 완료 - 강제 리다이렉트 막음')
    // window.location.href = '/login'
  }

  // 현재 사용자 정보 조회
  static async getCurrentUser(): Promise<UserProfile> {
    console.log('🔍 [AUTH] 현재 사용자 정보 요청 중...')
    try {
      const user = await apiClient.get<UserProfile>('/me')
      console.log('✅ [AUTH] 현재 사용자 정보 가져오기 성공:', user)
      return user
    } catch (error) {
      console.error('❌ [AUTH] 현재 사용자 정보 가져오기 실패:', error)
      throw error
    }
  }

  // 토큰 존재 여부 확인
  static hasToken(): boolean {
    return !!localStorage.getItem('token')
  }

  // 토큰 가져오기
  static getToken(): string | null {
    return localStorage.getItem('token')
  }
}
