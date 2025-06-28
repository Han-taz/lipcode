<template>
  <div class="error-page">
    <div class="error-container">
      <div class="error-icon">{{ errorIcon }}</div>
      <h1 class="error-title">{{ title }}</h1>
      <p class="error-message">{{ message }}</p>
      
      <div class="error-actions">
        <button @click="goBack" class="btn btn-primary">
          이전 페이지로
        </button>
        <router-link to="/" class="btn btn-secondary">
          홈으로 가기
        </router-link>
        <button v-if="showRetry" @click="retry" class="btn btn-outline">
          다시 시도
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  type?: 'notFound' | 'forbidden' | 'server' | 'network' | 'generic'
  title?: string
  message?: string
  showRetry?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  type: 'generic',
  showRetry: false
})

const emit = defineEmits<{
  retry: []
}>()

const errorIcon = computed(() => {
  switch (props.type) {
    case 'notFound':
      return '🔍'
    case 'forbidden':
      return '🚫'
    case 'server':
      return '🛠️'
    case 'network':
      return '📡'
    default:
      return '❌'
  }
})

const title = computed(() => {
  if (props.title) return props.title
  
  switch (props.type) {
    case 'notFound':
      return '페이지를 찾을 수 없습니다'
    case 'forbidden':
      return '접근 권한이 없습니다'
    case 'server':
      return '서버 오류가 발생했습니다'
    case 'network':
      return '네트워크 연결을 확인해주세요'
    default:
      return '오류가 발생했습니다'
  }
})

const message = computed(() => {
  if (props.message) return props.message
  
  switch (props.type) {
    case 'notFound':
      return '요청하신 페이지를 찾을 수 없습니다. URL을 확인하거나 홈페이지로 이동해주세요.'
    case 'forbidden':
      return '이 페이지에 접근할 권한이 없습니다. 로그인 상태를 확인해주세요.'
    case 'server':
      return '서버에서 문제가 발생했습니다. 잠시 후 다시 시도해주세요.'
    case 'network':
      return '인터넷 연결을 확인하고 다시 시도해주세요.'
    default:
      return '예상치 못한 오류가 발생했습니다.'
  }
})

const goBack = () => {
  window.history.back()
}

const retry = () => {
  emit('retry')
}
</script>

<style scoped>
.error-page {
  min-height: calc(100vh - 60px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background-color: #f8f9fa;
}

.error-container {
  text-align: center;
  max-width: 500px;
  padding: 3rem 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.error-icon {
  font-size: 4rem;
  margin-bottom: 1.5rem;
}

.error-title {
  font-size: 1.875rem;
  font-weight: 700;
  color: #1a202c;
  margin-bottom: 1rem;
}

.error-message {
  font-size: 1rem;
  color: #718096;
  line-height: 1.6;
  margin-bottom: 2rem;
}

.error-actions {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  align-items: center;
}

@media (min-width: 640px) {
  .error-actions {
    flex-direction: row;
    justify-content: center;
  }
}

.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  font-weight: 500;
  text-decoration: none;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  min-width: 120px;
}

.btn-primary {
  background-color: #3b82f6;
  color: white;
}

.btn-primary:hover {
  background-color: #2563eb;
}

.btn-secondary {
  background-color: #6b7280;
  color: white;
}

.btn-secondary:hover {
  background-color: #4b5563;
}

.btn-outline {
  background-color: transparent;
  color: #3b82f6;
  border: 1px solid #3b82f6;
}

.btn-outline:hover {
  background-color: #3b82f6;
  color: white;
}
</style>
