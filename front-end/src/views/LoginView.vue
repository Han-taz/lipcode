<template>
  <div class="login-container">
    <div class="login-card">
      <h1>로그인</h1>
      
      <form @submit.prevent="handleLogin" @submit="() => console.log('🔥 [LOGIN] 폼 제출됨!')" class="login-form">
        <div class="form-group">
          <label for="email">이메일</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            required
            :disabled="authStore.isLoading"
            placeholder="이메일을 입력하세요"
          />
        </div>

        <div class="form-group">
          <label for="password">비밀번호</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            required
            :disabled="authStore.isLoading"
            placeholder="비밀번호를 입력하세요"
          />
        </div>

        <div v-if="authStore.error" class="error-message">
          {{ authStore.error }}
        </div>

        <button 
          id="login"
          type="submit" 
          class="login-btn"
          :disabled="authStore.isLoading"
          @click="() => console.log('🔥 [LOGIN] 버튼 클릭됨!')"
        >
          {{ authStore.isLoading ? '로그인 중...' : '로그인' }}
        </button>
      </form>

      <div class="signup-link">
        <p>계정이 없으신가요? <router-link to="/signup">회원가입</router-link></p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

console.log('🔥 [LOGIN] LoginView.vue <script> 실행됨!')

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  email: '',
  password: ''
})

console.log('🔥 [LOGIN] 초기 설정 완료, form:', form)

const handleLogin = async () => {
  console.log('🔥 [LOGIN] handleLogin 함수 호출됨!')
  console.log('🔥 [LOGIN] 폼 데이터:', form)
  
  authStore.clearError()
  
  const success = await authStore.login(form.email, form.password)
  console.log('🔥 [LOGIN] 로그인 결과:', success)
  
  if (success) {
    console.log('✅ [LOGIN] 로그인 성공, 잠시 대기 중...')
    
    // 임시로 리다이렉트 지연
    setTimeout(() => {
      console.log('✅ [LOGIN] 프로필 페이지로 이동')
      router.push('/profile')
    }, 2000) // 2초 후 이동
  } else {
    console.log('❌ [LOGIN] 로그인 실패')
  }
}

// 이미 로그인된 사용자는 프로필 페이지로 리다이렉트
onMounted(() => {
  console.log('🔥 [LOGIN] LoginView 마운트됨!')
  console.log('🔥 [LOGIN] 인증 상태:', authStore.isAuthenticated)
  
  if (authStore.isAuthenticated) {
    console.log('🔥 [LOGIN] 이미 로그인됨, 프로필로 리다이렉트')
    router.push('/profile')
  }
})
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f5f5;
  padding: 1rem;
}

.login-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.login-card h1 {
  text-align: center;
  margin-bottom: 2rem;
  color: #333;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #555;
}

.form-group input {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-group input:focus {
  outline: none;
  border-color: var(--color-primary);
}

.form-group input:disabled {
  background-color: #f9f9f9;
  cursor: not-allowed;
}

.error-message {
  color: #e74c3c;
  font-size: 0.875rem;
  text-align: center;
  padding: 0.5rem;
  background-color: #fdf2f2;
  border-radius: 4px;
  border: 1px solid #fecaca;
}

.login-btn {
  padding: 0.75rem;
  background-color: var(--color-primary);
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.login-btn:hover:not(:disabled) {
  background-color: #369e6b;
}

.login-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.signup-link {
  text-align: center;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #eee;
}

.signup-link a {
  color: var(--color-primary);
  text-decoration: none;
  font-weight: 500;
}

.signup-link a:hover {
  text-decoration: underline;
}
</style>
