<template>
  <div class="mentors-container">
    <div class="container">
      <div class="mentors-header">
        <h1>멘토 찾기</h1>
        <p class="subtitle">원하는 기술을 가진 멘토를 찾아 매칭 요청을 보내보세요</p>
      </div>

      <!-- 검색 및 필터 -->
      <div class="search-section">
        <div class="search-card">
          <div class="search-controls">
            <div class="search-group">
              <label class="search-label">기술 스택으로 검색</label>
              <div class="search-input-group">
                <input 
                  v-model="searchSkill"
                  type="text"
                  class="search-input"
                  placeholder="예: React, Vue, Python..."
                  @keydown.enter="searchMentors"
                />
                <button 
                  @click="searchMentors"
                  class="search-btn"
                  :disabled="loading"
                >
                  🔍 검색
                </button>
              </div>
            </div>

            <div class="filter-group">
              <label class="search-label">정렬</label>
              <select 
                v-model="sortBy"
                class="sort-select"
                @change="searchMentors"
              >
                <option value="">기본순</option>
                <option value="name">이름순</option>
                <option value="skill">기술순</option>
              </select>
            </div>

            <button 
              @click="clearFilters"
              class="clear-btn"
              :disabled="loading"
            >
              초기화
            </button>
          </div>
        </div>
      </div>

      <!-- 로딩 -->
      <div v-if="loading" class="loading">
        <div class="loading-spinner"></div>
        <p>멘토 목록을 불러오는 중...</p>
      </div>

      <!-- 에러 메시지 -->
      <div v-else-if="error" class="error-section">
        <div class="error-card">
          <h3>❌ 오류가 발생했습니다</h3>
          <p>{{ error }}</p>
          <button @click="loadMentors" class="btn btn-primary">다시 시도</button>
        </div>
      </div>

      <!-- 멘토 목록 -->
      <div v-else class="mentors-content">
        <div class="mentors-info">
          <p class="mentors-count">
            총 <strong>{{ mentors.length }}</strong>명의 멘토를 찾았습니다
          </p>
        </div>

        <div v-if="mentors.length === 0" class="empty-state">
          <div class="empty-card">
            <div class="empty-icon">🔍</div>
            <h3>검색 결과가 없습니다</h3>
            <p>다른 기술 스택으로 검색해보시거나, 필터를 초기화해보세요.</p>
            <button @click="clearFilters" class="btn btn-primary">전체 멘토 보기</button>
          </div>
        </div>

        <div v-else class="mentors-grid">
          <div 
            v-for="mentor in mentors"
            :key="mentor.id"
            class="mentor-card"
          >
            <!-- 프로필 이미지 -->
            <div class="mentor-image">
              <img 
                :src="getMentorImageUrl(mentor.id)"
                :alt="`${mentor.profile.name}의 프로필`"
                @error="handleImageError"
              />
            </div>

            <!-- 멘토 정보 -->
            <div class="mentor-info">
              <h3 class="mentor-name">{{ mentor.profile.name }}</h3>
              <p class="mentor-email">{{ mentor.email }}</p>
              
              <div class="mentor-bio">
                <p>{{ mentor.profile.bio || '소개글이 없습니다.' }}</p>
              </div>

              <!-- 기술 스택 -->
              <div class="mentor-skills">
                <h4>보유 기술</h4>
                <div class="skills-list">
                  <span 
                    v-for="skill in mentor.profile.skills"
                    :key="skill"
                    class="skill-tag"
                  >
                    {{ skill }}
                  </span>
                  <span v-if="mentor.profile.skills.length === 0" class="no-skills">
                    등록된 기술이 없습니다
                  </span>
                </div>
              </div>

              <!-- 매칭 요청 버튼 -->
              <div class="mentor-actions">
                <button 
                  @click="openMatchRequestModal(mentor)"
                  class="btn btn-primary match-btn"
                  :disabled="isRequestPending || requestingMentorId === mentor.id"
                >
                  {{ requestingMentorId === mentor.id ? '요청 중...' : '매칭 요청' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 매칭 요청 모달 -->
    <div v-if="showMatchModal" class="modal-overlay" @click="closeMatchModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ selectedMentor?.profile.name }}님에게 매칭 요청</h3>
          <button @click="closeMatchModal" class="modal-close">×</button>
        </div>

        <div class="modal-body">
          <div v-if="selectedMentor" class="mentor-summary">
            <img 
              :src="getMentorImageUrl(selectedMentor.id)"
              :alt="`${selectedMentor.profile.name}의 프로필`"
              class="modal-mentor-image"
            />
            <div>
              <h4>{{ selectedMentor.profile.name }}</h4>
              <p class="modal-mentor-skills">
                {{ selectedMentor.profile.skills.join(', ') || '등록된 기술 없음' }}
              </p>
            </div>
          </div>

          <div class="message-group">
            <label class="form-label">메시지</label>
            <textarea 
              v-model="matchMessage"
              class="form-textarea"
              rows="4"
              placeholder="멘토님께 전하고 싶은 메시지를 작성해주세요..."
              required
            ></textarea>
          </div>

          <div v-if="matchError" class="error-message">
            {{ matchError }}
          </div>
        </div>

        <div class="modal-footer">
          <button 
            @click="closeMatchModal"
            class="btn btn-secondary"
            :disabled="sendingRequest"
          >
            취소
          </button>
          <button 
            @click="sendMatchRequest"
            class="btn btn-primary"
            :disabled="!matchMessage.trim() || sendingRequest"
          >
            {{ sendingRequest ? '전송 중...' : '요청 보내기' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { MentorService, MatchRequestService } from '@/services/mentor'
import { UserService } from '@/services/user'
import type { MentorListItem } from '@/types/api'

const authStore = useAuthStore()

// 데이터
const loading = ref(false)
const error = ref('')
const mentors = ref<MentorListItem[]>([])
const searchSkill = ref('')
const sortBy = ref('')

// 매칭 요청 모달
const showMatchModal = ref(false)
const selectedMentor = ref<MentorListItem | null>(null)
const matchMessage = ref('')
const matchError = ref('')
const sendingRequest = ref(false)
const requestingMentorId = ref<number | null>(null)

// 현재 사용자가 이미 요청을 보낸 상태인지 확인
const isRequestPending = computed(() => {
  // 실제로는 보낸 요청 목록을 확인해야 하지만, 간단히 구현
  return false
})

// 멘토 목록 로드
const loadMentors = async () => {
  try {
    loading.value = true
    error.value = ''
    
    const params: any = {}
    if (searchSkill.value.trim()) {
      params.skill = searchSkill.value.trim()
    }
    if (sortBy.value) {
      params.orderBy = sortBy.value
    }

    mentors.value = await MentorService.getMentors(params)
  } catch (err: any) {
    error.value = err.response?.data?.error || '멘토 목록을 불러오는데 실패했습니다.'
  } finally {
    loading.value = false
  }
}

// 검색
const searchMentors = () => {
  loadMentors()
}

// 필터 초기화
const clearFilters = () => {
  searchSkill.value = ''
  sortBy.value = ''
  loadMentors()
}

// 멘토 이미지 URL 생성
const getMentorImageUrl = (mentorId: number) => {
  return UserService.getProfileImageUrl('mentor', mentorId)
}

// 이미지 에러 처리
const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement
  img.src = 'https://placehold.co/500x500.jpg?text=MENTOR'
}

// 매칭 요청 모달 열기
const openMatchRequestModal = (mentor: MentorListItem) => {
  selectedMentor.value = mentor
  matchMessage.value = ''
  matchError.value = ''
  showMatchModal.value = true
}

// 매칭 요청 모달 닫기
const closeMatchModal = () => {
  showMatchModal.value = false
  selectedMentor.value = null
  matchMessage.value = ''
  matchError.value = ''
}

// 매칭 요청 전송
const sendMatchRequest = async () => {
  if (!selectedMentor.value || !authStore.user) return

  try {
    sendingRequest.value = true
    requestingMentorId.value = selectedMentor.value.id
    matchError.value = ''

    await MatchRequestService.createMatchRequest({
      mentorId: selectedMentor.value.id,
      menteeId: authStore.user.id,
      message: matchMessage.value.trim()
    })

    // 성공 시 모달 닫기
    closeMatchModal()
    
    // 성공 알림 (간단히 alert 사용)
    alert(`${selectedMentor.value.profile.name}님에게 매칭 요청을 보냈습니다!`)

  } catch (err: any) {
    matchError.value = err.response?.data?.error || '매칭 요청 전송에 실패했습니다.'
  } finally {
    sendingRequest.value = false
    requestingMentorId.value = null
  }
}

// 컴포넌트 마운트
onMounted(() => {
  loadMentors()
})
</script>

<style scoped>
.mentors-container {
  min-height: calc(100vh - 60px);
  padding: 2rem 0;
}

.mentors-header {
  text-align: center;
  margin-bottom: 2rem;
}

.mentors-header h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  color: var(--color-text);
}

.subtitle {
  color: var(--color-text-soft);
  font-size: 1.125rem;
}

/* 검색 섹션 */
.search-section {
  margin-bottom: 2rem;
}

.search-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.search-controls {
  display: grid;
  grid-template-columns: 1fr auto auto;
  gap: 1rem;
  align-items: end;
}

.search-group {
  display: flex;
  flex-direction: column;
}

.search-label {
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: var(--color-text);
}

.search-input-group {
  display: flex;
  gap: 0.5rem;
}

.search-input {
  flex: 1;
  padding: 0.75rem;
  border: 2px solid var(--color-border);
  border-radius: 8px;
  font-size: 1rem;
}

.search-input:focus {
  outline: none;
  border-color: var(--color-primary);
}

.search-btn,
.clear-btn {
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.search-btn {
  background: var(--color-primary);
  color: white;
}

.search-btn:hover:not(:disabled) {
  background: var(--color-primary-dark);
}

.clear-btn {
  background: transparent;
  color: var(--color-text-soft);
  border: 2px solid var(--color-border);
}

.clear-btn:hover:not(:disabled) {
  border-color: var(--color-text-soft);
  color: var(--color-text);
}

.filter-group {
  display: flex;
  flex-direction: column;
}

.sort-select {
  padding: 0.75rem;
  border: 2px solid var(--color-border);
  border-radius: 8px;
  font-size: 1rem;
  background: white;
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

/* 에러 섹션 */
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

/* 멘토 목록 */
.mentors-content {
  margin-top: 2rem;
}

.mentors-info {
  margin-bottom: 1.5rem;
}

.mentors-count {
  color: var(--color-text-soft);
  font-size: 0.875rem;
}

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
  max-width: 400px;
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

/* 멘토 그리드 */
.mentors-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.mentor-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: all 0.3s;
  border: 1px solid var(--color-border);
}

.mentor-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.mentor-image {
  height: 120px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.mentor-image img {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid white;
}

.mentor-info {
  padding: 1.5rem;
}

.mentor-name {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
  color: var(--color-text);
}

.mentor-email {
  color: var(--color-text-soft);
  font-size: 0.875rem;
  margin-bottom: 1rem;
}

.mentor-bio {
  margin-bottom: 1.5rem;
}

.mentor-bio p {
  color: var(--color-text-soft);
  line-height: 1.5;
  font-size: 0.875rem;
}

.mentor-skills h4 {
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
  color: var(--color-text);
}

.skills-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.skill-tag {
  padding: 0.25rem 0.75rem;
  background: var(--color-primary);
  color: white;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
}

.no-skills {
  color: var(--color-text-soft);
  font-style: italic;
  font-size: 0.875rem;
}

.mentor-actions {
  display: flex;
  justify-content: center;
}

.match-btn {
  width: 100%;
  padding: 0.75rem;
  font-weight: 600;
}

/* 모달 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: white;
  border-radius: 12px;
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid var(--color-border);
}

.modal-header h3 {
  margin: 0;
  color: var(--color-text);
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--color-text-soft);
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-body {
  padding: 1.5rem;
}

.mentor-summary {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: var(--color-background-soft);
  border-radius: 8px;
}

.modal-mentor-image {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  object-fit: cover;
}

.modal-mentor-skills {
  color: var(--color-text-soft);
  font-size: 0.875rem;
  margin: 0;
}

.message-group {
  margin-bottom: 1rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: var(--color-text);
}

.form-textarea {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid var(--color-border);
  border-radius: 8px;
  font-size: 1rem;
  resize: vertical;
  font-family: inherit;
}

.form-textarea:focus {
  outline: none;
  border-color: var(--color-primary);
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid var(--color-border);
}

/* 공통 버튼 스타일 */
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

.btn-secondary {
  background: transparent;
  color: var(--color-text-soft);
  border: 2px solid var(--color-border);
}

.btn-secondary:hover:not(:disabled) {
  border-color: var(--color-text-soft);
  color: var(--color-text);
}

/* 반응형 */
@media (max-width: 768px) {
  .mentors-container {
    padding: 1rem 0;
  }

  .mentors-header h1 {
    font-size: 2rem;
  }

  .search-controls {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .search-input-group {
    flex-direction: column;
  }

  .mentors-grid {
    grid-template-columns: 1fr;
  }

  .modal-overlay {
    padding: 0.5rem;
  }

  .modal-content {
    margin: 0;
  }

  .mentor-summary {
    flex-direction: column;
    text-align: center;
  }

  .modal-footer {
    flex-direction: column;
  }
}
</style>
