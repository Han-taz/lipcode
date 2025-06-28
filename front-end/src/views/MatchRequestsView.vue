<template>
  <div class="match-requests-container">
    <div class="container">
      <div class="page-header">
        <h1>{{ authStore.isMentor ? '받은 매칭 요청' : '내 매칭 요청' }}</h1>
        <p class="subtitle">
          {{ authStore.isMentor 
            ? '멘티들의 매칭 요청을 확인하고 응답하세요' 
            : '보낸 매칭 요청의 상태를 확인하세요' 
          }}
        </p>
      </div>

      <!-- 탭 메뉴 (멘토용) -->
      <div v-if="authStore.isMentor" class="tabs">
        <button 
          @click="activeTab = 'incoming'"
          :class="['tab-button', { active: activeTab === 'incoming' }]"
        >
          📥 받은 요청 ({{ incomingRequests.length }})
        </button>
      </div>

      <!-- 로딩 -->
      <div v-if="loading" class="loading">
        <div class="loading-spinner"></div>
        <p>요청 목록을 불러오는 중...</p>
      </div>

      <!-- 에러 -->
      <div v-else-if="error" class="error-section">
        <div class="error-card">
          <h3>❌ 오류가 발생했습니다</h3>
          <p>{{ error }}</p>
          <button @click="loadRequests" class="btn btn-primary">다시 시도</button>
        </div>
      </div>

      <!-- 멘토: 받은 요청 목록 -->
      <div v-else-if="authStore.isMentor" class="requests-content">
        <div v-if="incomingRequests.length === 0" class="empty-state">
          <div class="empty-card">
            <div class="empty-icon">📭</div>
            <h3>받은 매칭 요청이 없습니다</h3>
            <p>아직 멘티들로부터 매칭 요청을 받지 못했습니다.<br>프로필을 업데이트하여 더 많은 멘티들이 찾을 수 있도록 해보세요.</p>
            <router-link to="/profile" class="btn btn-primary">프로필 업데이트</router-link>
          </div>
        </div>

        <div v-else class="requests-grid">
          <div 
            v-for="request in incomingRequests"
            :key="request.id"
            class="request-card"
          >
            <div class="request-header">
              <div class="request-info">
                <h3>매칭 요청 #{{ request.id }}</h3>
                <span :class="['status-badge', request.status]">
                  {{ getStatusText(request.status) }}
                </span>
              </div>
              <div class="request-date">
                <!-- 실제로는 요청 날짜를 표시해야 함 -->
                <small class="text-muted">{{ formatDate(new Date()) }}</small>
              </div>
            </div>

            <div class="request-content">
              <div class="mentee-info">
                <h4>멘티 정보</h4>
                <p><strong>ID:</strong> {{ request.menteeId }}</p>
              </div>

              <div class="request-message">
                <h4>요청 메시지</h4>
                <p class="message-text">{{ request.message }}</p>
              </div>
            </div>

            <div v-if="request.status === 'pending'" class="request-actions">
              <button 
                @click="acceptRequest(request.id)"
                class="btn btn-success"
                :disabled="processingRequestId === request.id"
              >
                {{ processingRequestId === request.id ? '처리 중...' : '✅ 수락' }}
              </button>
              <button 
                @click="rejectRequest(request.id)"
                class="btn btn-danger"
                :disabled="processingRequestId === request.id"
              >
                {{ processingRequestId === request.id ? '처리 중...' : '❌ 거절' }}
              </button>
            </div>

            <div v-else class="request-result">
              <p class="result-text">
                {{ request.status === 'accepted' ? '✅ 수락한 요청입니다' : '❌ 거절한 요청입니다' }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- 멘티: 보낸 요청 목록 -->
      <div v-else class="requests-content">
        <div v-if="outgoingRequests.length === 0" class="empty-state">
          <div class="empty-card">
            <div class="empty-icon">📤</div>
            <h3>보낸 매칭 요청이 없습니다</h3>
            <p>아직 멘토에게 매칭 요청을 보내지 않았습니다.<br>멘토 목록에서 원하는 멘토를 찾아 요청을 보내보세요.</p>
            <router-link to="/mentors" class="btn btn-primary">멘토 찾기</router-link>
          </div>
        </div>

        <div v-else class="requests-grid">
          <div 
            v-for="request in outgoingRequests"
            :key="request.id"
            class="request-card"
          >
            <div class="request-header">
              <div class="request-info">
                <h3>매칭 요청 #{{ request.id }}</h3>
                <span :class="['status-badge', request.status]">
                  {{ getStatusText(request.status) }}
                </span>
              </div>
              <div class="request-date">
                <small class="text-muted">{{ formatDate(new Date()) }}</small>
              </div>
            </div>

            <div class="request-content">
              <div class="mentor-info">
                <h4>멘토 정보</h4>
                <p><strong>ID:</strong> {{ request.mentorId }}</p>
              </div>
            </div>

            <div v-if="request.status === 'pending'" class="request-actions">
              <button 
                @click="cancelRequest(request.id)"
                class="btn btn-danger"
                :disabled="processingRequestId === request.id"
              >
                {{ processingRequestId === request.id ? '취소 중...' : '🗑️ 요청 취소' }}
              </button>
            </div>

            <div v-else class="request-result">
              <p class="result-text">
                <span v-if="request.status === 'accepted'">✅ 멘토가 수락했습니다!</span>
                <span v-else-if="request.status === 'rejected'">❌ 멘토가 거절했습니다</span>
                <span v-else-if="request.status === 'cancelled'">🗑️ 취소된 요청입니다</span>
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- 성공 메시지 -->
      <div v-if="successMessage" class="success-toast">
        {{ successMessage }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { MatchRequestService } from '@/services/mentor'
import type { MatchRequest, MatchRequestOutgoing } from '@/types/api'

const authStore = useAuthStore()

// 데이터
const loading = ref(false)
const error = ref('')
const successMessage = ref('')
const activeTab = ref('incoming')
const processingRequestId = ref<number | null>(null)

const incomingRequests = ref<MatchRequest[]>([])
const outgoingRequests = ref<MatchRequestOutgoing[]>([])

// 요청 목록 로드
const loadRequests = async () => {
  try {
    loading.value = true
    error.value = ''

    if (authStore.isMentor) {
      incomingRequests.value = await MatchRequestService.getIncomingRequests()
    } else {
      outgoingRequests.value = await MatchRequestService.getOutgoingRequests()
    }
  } catch (err: any) {
    error.value = err.response?.data?.error || '요청 목록을 불러오는데 실패했습니다.'
  } finally {
    loading.value = false
  }
}

// 상태 텍스트 변환
const getStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    'pending': '대기 중',
    'accepted': '수락됨',
    'rejected': '거절됨',
    'cancelled': '취소됨'
  }
  return statusMap[status] || status
}

// 날짜 포맷
const formatDate = (date: Date) => {
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 요청 수락 (멘토용)
const acceptRequest = async (requestId: number) => {
  try {
    processingRequestId.value = requestId
    
    await MatchRequestService.acceptRequest(requestId)
    
    // 로컬 상태 업데이트
    const request = incomingRequests.value.find(r => r.id === requestId)
    if (request) {
      request.status = 'accepted'
    }
    
    showSuccess('매칭 요청을 수락했습니다!')
  } catch (err: any) {
    error.value = err.response?.data?.error || '요청 수락에 실패했습니다.'
  } finally {
    processingRequestId.value = null
  }
}

// 요청 거절 (멘토용)
const rejectRequest = async (requestId: number) => {
  try {
    processingRequestId.value = requestId
    
    await MatchRequestService.rejectRequest(requestId)
    
    // 로컬 상태 업데이트
    const request = incomingRequests.value.find(r => r.id === requestId)
    if (request) {
      request.status = 'rejected'
    }
    
    showSuccess('매칭 요청을 거절했습니다.')
  } catch (err: any) {
    error.value = err.response?.data?.error || '요청 거절에 실패했습니다.'
  } finally {
    processingRequestId.value = null
  }
}

// 요청 취소 (멘티용)
const cancelRequest = async (requestId: number) => {
  if (!confirm('정말 이 요청을 취소하시겠습니까?')) {
    return
  }

  try {
    processingRequestId.value = requestId
    
    await MatchRequestService.cancelRequest(requestId)
    
    // 로컬 상태 업데이트
    const request = outgoingRequests.value.find(r => r.id === requestId)
    if (request) {
      request.status = 'cancelled'
    }
    
    showSuccess('매칭 요청을 취소했습니다.')
  } catch (err: any) {
    error.value = err.response?.data?.error || '요청 취소에 실패했습니다.'
  } finally {
    processingRequestId.value = null
  }
}

// 성공 메시지 표시
const showSuccess = (message: string) => {
  successMessage.value = message
  setTimeout(() => {
    successMessage.value = ''
  }, 3000)
}

// 컴포넌트 마운트
onMounted(() => {
  loadRequests()
})
</script>

<style scoped>
.match-requests-container {
  min-height: calc(100vh - 60px);
  padding: 2rem 0;
}

.page-header {
  text-align: center;
  margin-bottom: 2rem;
}

.page-header h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  color: var(--color-text);
}

.subtitle {
  color: var(--color-text-soft);
  font-size: 1.125rem;
}

/* 탭 */
.tabs {
  display: flex;
  justify-content: center;
  margin-bottom: 2rem;
}

.tab-button {
  padding: 0.75rem 1.5rem;
  border: none;
  background: transparent;
  color: var(--color-text-soft);
  cursor: pointer;
  border-bottom: 3px solid transparent;
  font-weight: 600;
  transition: all 0.3s;
}

.tab-button.active {
  color: var(--color-primary);
  border-bottom-color: var(--color-primary);
}

.tab-button:hover {
  color: var(--color-primary);
}

/* 로딩 */
.loading {
  text-align: center;
  padding: 4rem 0;
  color: var(--color-text-soft);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--color-border);
  border-top: 4px solid var(--color-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 에러 */
.error-section {
  display: flex;
  justify-content: center;
  padding: 4rem 0;
}

.error-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid #fecaca;
}

.error-card h3 {
  color: var(--color-danger);
  margin-bottom: 1rem;
}

/* 빈 상태 */
.empty-state {
  display: flex;
  justify-content: center;
  padding: 4rem 0;
}

.empty-card {
  background: white;
  padding: 3rem;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  max-width: 500px;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.empty-card h3 {
  margin-bottom: 1rem;
  color: var(--color-text);
}

.empty-card p {
  color: var(--color-text-soft);
  margin-bottom: 2rem;
  line-height: 1.6;
}

/* 요청 그리드 */
.requests-content {
  margin-top: 2rem;
}

.requests-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 1.5rem;
}

.request-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  border: 1px solid var(--color-border);
  transition: all 0.3s;
}

.request-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.request-header {
  padding: 1.5rem;
  border-bottom: 1px solid var(--color-border);
  background: var(--color-background-soft);
}

.request-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.request-info h3 {
  margin: 0;
  color: var(--color-text);
  font-size: 1.125rem;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.status-badge.pending {
  background: #fef3c7;
  color: #92400e;
}

.status-badge.accepted {
  background: #d1fae5;
  color: #065f46;
}

.status-badge.rejected {
  background: #fecaca;
  color: #991b1b;
}

.status-badge.cancelled {
  background: #e5e7eb;
  color: #374151;
}

.request-date {
  text-align: right;
}

.request-content {
  padding: 1.5rem;
}

.mentee-info,
.mentor-info {
  margin-bottom: 1.5rem;
}

.mentee-info h4,
.mentor-info h4 {
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: var(--color-text);
  text-transform: uppercase;
}

.request-message h4 {
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
  color: var(--color-text);
  text-transform: uppercase;
}

.message-text {
  background: var(--color-background-soft);
  padding: 1rem;
  border-radius: 8px;
  border-left: 4px solid var(--color-primary);
  line-height: 1.5;
  color: var(--color-text);
  font-style: italic;
}

.request-actions {
  padding: 1rem 1.5rem;
  background: var(--color-background-soft);
  display: flex;
  gap: 1rem;
  border-top: 1px solid var(--color-border);
}

.request-result {
  padding: 1rem 1.5rem;
  background: var(--color-background-soft);
  border-top: 1px solid var(--color-border);
}

.result-text {
  text-align: center;
  font-weight: 600;
  margin: 0;
}

/* 버튼 */
.btn {
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex: 1;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background: var(--color-primary);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: var(--color-primary-dark);
}

.btn-success {
  background: var(--color-success);
  color: white;
}

.btn-success:hover:not(:disabled) {
  background: #138d75;
}

.btn-danger {
  background: var(--color-danger);
  color: white;
}

.btn-danger:hover:not(:disabled) {
  background: #c0392b;
}

/* 성공 토스트 */
.success-toast {
  position: fixed;
  top: 20px;
  right: 20px;
  background: var(--color-success);
  color: white;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

/* 반응형 */
@media (max-width: 768px) {
  .match-requests-container {
    padding: 1rem 0;
  }

  .page-header h1 {
    font-size: 2rem;
  }

  .requests-grid {
    grid-template-columns: 1fr;
  }

  .request-actions {
    flex-direction: column;
  }

  .success-toast {
    right: 10px;
    left: 10px;
  }
}
</style>
