<template>
  <div class="signup-container">
    <div class="signup-card">
      <h1>회원가입</h1>
      
      <form @submit.prevent="handleSignup" class="signup-form">
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
            minlength="6"
            :disabled="authStore.isLoading"
            placeholder="비밀번호를 입력하세요 (최소 6자)"
          />
        </div>

        <div class="form-group">
          <label for="name">이름</label>
          <input
            id="name"
            v-model="form.name"
            type="text"
            required
            :disabled="authStore.isLoading"
            placeholder="이름을 입력하세요"
          />
        </div>

        <div class="form-group">
          <label>역할</label>
          <div class="role-options">
            <label class="role-option">
              <input
                id="role"
                v-model="form.role"
                type="radio"
                value="mentor"
                :disabled="authStore.isLoading"
              />
              <span>멘토</span>
              <small>다른 사람을 가르치고 싶어요</small>
            </label>
            <label class="role-option">
              <input
                v-model="form.role"
                type="radio"
                value="mentee"
                :disabled="authStore.isLoading"
              />
              <span>멘티</span>
              <small>누군가에게 배우고 싶어요</small>
            </label>
          </div>
        </div>

        <div v-if="authStore.error" class="error-message">
          {{ authStore.error }}
        </div>

        <div v-if="successMessage" class="success-message">
          {{ successMessage }}
        </div>

        <button 
          id="signup"
          type="submit" 
          class="signup-btn"
          :disabled="authStore.isLoading || !form.role"
        >
          {{ authStore.isLoading ? '가입 중...' : '회원가입' }}
        </button>
      </form>

      <div class="login-link">
        <p>이미 계정이 있으신가요? <router-link to="/login">로그인</router-link></p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const successMessage = ref('')

const form = reactive({
  email: '',
  password: '',
  name: '',
  role: '' as 'mentor' | 'mentee' | ''
})

const handleSignup = async () => {
  authStore.clearError()
  successMessage.value = ''
  
  if (!form.role) {
    return
  }
  
  const success = await authStore.signup(
    form.email, 
    form.password, 
    form.name, 
    form.role
  )
  
  if (success) {
    successMessage.value = '회원가입이 완료되었습니다! 로그인 페이지로 이동합니다.'
    setTimeout(() => {
      router.push('/login')
    }, 2000)
  }
}

// 이미 로그인된 사용자는 프로필 페이지로 리다이렉트
onMounted(() => {
  if (authStore.isAuthenticated) {
    router.push('/profile')
  }
})
</script>

<style scoped>
.signup-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f5f5;
  padding: 1rem;
}

.signup-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 500px;
}

.signup-card h1 {
  text-align: center;
  margin-bottom: 2rem;
  color: #333;
}

.signup-form {
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

.form-group input[type="email"],
.form-group input[type="password"],
.form-group input[type="text"] {
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

.role-options {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.role-option {
  display: flex;
  flex-direction: column;
  padding: 1rem;
  border: 2px solid #eee;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.role-option:hover {
  border-color: var(--color-primary);
  background-color: #f8fffe;
}

.role-option input[type="radio"] {
  margin-bottom: 0.5rem;
}

.role-option span {
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.role-option small {
  color: #666;
  font-size: 0.875rem;
}

.role-option:has(input:checked) {
  border-color: var(--color-primary);
  background-color: #f0fdf4;
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

.success-message {
  color: #16a085;
  font-size: 0.875rem;
  text-align: center;
  padding: 0.5rem;
  background-color: #f0fdf4;
  border-radius: 4px;
  border: 1px solid #86efac;
}

.signup-btn {
  padding: 0.75rem;
  background-color: var(--color-primary);
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-top: 0.5rem;
}

.signup-btn:hover:not(:disabled) {
  background-color: #369e6b;
}

.signup-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.login-link {
  text-align: center;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #eee;
}

.login-link a {
  color: var(--color-primary);
  text-decoration: none;
  font-weight: 500;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>
