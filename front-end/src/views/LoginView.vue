<template>
  <div class="login-container">
    <div class="login-card">
      <h1>로그인</h1>
      
      <form @submit.prevent="actualLogin" class="login-form">
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
          type="button" 
          class="login-btn"
          :disabled="authStore.isLoading"
          @click="actualLogin"
        >
          {{ authStore.isLoading ? '로그인 중...' : '로그인' }}
        </button>
      </form>

      <div class="signup-link">
        <p>계정이 없으신가요? <router-link to="/signup">회원가입</router-link></p>
      </div>

      <!-- 디버그 로그 표시 -->
      <div v-if="debugLogs.length > 0" class="debug-logs">
        <h3>디버그 로그:</h3>
        <div class="log-container">
          <div v-for="(log, index) in debugLogs" :key="index" class="log-item">
            {{ log }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

console.log('🔥 [LOGIN] LoginView.vue <script> 실행됨!')

const router = useRouter()
const authStore = useAuthStore()
const debugLogs = ref<string[]>([])

const addLog = (message: string) => {
  console.log(message)
  debugLogs.value.push(`[${new Date().toLocaleTimeString()}] ${message}`)
  // 최대 20개 로그만 유지
  if (debugLogs.value.length > 20) {
    debugLogs.value.shift()
  }
}

const form = reactive({
  email: '',
  password: ''
})

addLog('🔥 [LOGIN] 초기 설정 완료')
addLog(`🔥 [LOGIN] form: ${JSON.stringify(form)}`)

const testClick = () => {
  addLog('BUTTON CLICKED!')
  addLog(`Current form: ${JSON.stringify(form)}`)
  // 수동으로 actualLogin 호출
  actualLogin()
}

const actualLogin = async () => {
  debugLogs.value.push(`[${new Date().toLocaleTimeString()}] 🔥 [LOGIN] 실제 로그인 시작`)
  debugLogs.value.push(`[${new Date().toLocaleTimeString()}] 🔥 [LOGIN] 폼 데이터: ${JSON.stringify(form)}`)
  
  if (!form.email || !form.password) {
    debugLogs.value.push(`[${new Date().toLocaleTimeString()}] ❌ [LOGIN] 이메일 또는 패스워드가 비어있음`)
    return
  }
  
  try {
    authStore.clearError()
    
    const success = await authStore.login(form.email, form.password)
    debugLogs.value.push(`[${new Date().toLocaleTimeString()}] 🔥 [LOGIN] 로그인 결과: ${success}`)
    
    if (success) {
        debugLogs.value.push(`[${new Date().toLocaleTimeString()}] ✅ [LOGIN] 로그인 성공!`)
        
        // 토큰 확인
        const token = localStorage.getItem('token')
        debugLogs.value.push(`[${new Date().toLocaleTimeString()}] 💾 [LOGIN] 저장된 토큰: ${token ? token.substring(0, 50) + '...' : 'null'}`)
        
        // 사용자 정보 확인
        if (authStore.user) {
          debugLogs.value.push(`[${new Date().toLocaleTimeString()}] ✅ [LOGIN] 사용자 정보: ${JSON.stringify(authStore.user)}`)
          debugLogs.value.push(`[${new Date().toLocaleTimeString()}] 🚀 [LOGIN] 프로필 페이지로 이동합니다`)
          
          // 정상적으로 프로필 페이지로 이동
          setTimeout(() => {
            router.push('/profile')
          }, 1000)
        } else {
          debugLogs.value.push(`[${new Date().toLocaleTimeString()}] ❌ [LOGIN] 사용자 정보가 없음`)
        }
      } else {
      debugLogs.value.push(`[${new Date().toLocaleTimeString()}] ❌ [LOGIN] 로그인 실패`)
    }
  } catch (error: any) {
    debugLogs.value.push(`[${new Date().toLocaleTimeString()}] ❌ [LOGIN] 에러 발생: ${error.message || error}`)
  }
}

// 이미 로그인된 사용자는 프로필 페이지로 리다이렉트
onMounted(() => {
  addLog('🔥 [LOGIN] LoginView 마운트됨!')
  addLog(`🔥 [LOGIN] 인증 상태: ${authStore.isAuthenticated}`)
  
  // 자동 리다이렉트 막음
  // if (authStore.isAuthenticated) {
  //   console.log('🔥 [LOGIN] 이미 로그인됨, 프로필로 리다이렉트')
  //   router.push('/profile')
  // }
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

.debug-logs {
  margin-top: 2rem;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #f9f9f9;
}

.debug-logs h3 {
  margin: 0 0 1rem 0;
  font-size: 1rem;
  color: #333;
}

.log-container {
  max-height: 300px;
  overflow-y: auto;
  font-family: monospace;
  font-size: 0.85rem;
}

.log-item {
  padding: 0.25rem 0;
  border-bottom: 1px solid #eee;
  word-break: break-all;
}

.log-item:last-child {
  border-bottom: none;
}
</style>
