<template>
  <div class="profile-container">
    <div class="container">
      <div class="profile-header">
        <h1>프로필 관리</h1>
        <p class="subtitle">프로필 정보를 수정하고 이미지를 업데이트하세요</p>
      </div>

      <div v-if="loading" class="loading">
        <p>로딩 중...</p>
      </div>

      <div v-else-if="userProfile" class="profile-content">
        <div class="profile-card">
          <!-- 프로필 이미지 섹션 -->
          <div class="image-section">
            <div class="image-container">
              <img 
                :src="profileImageUrl" 
                :alt="`${userProfile.profile.name}의 프로필`"
                class="profile-image"
                @error="handleImageError"
              />
              <div class="image-overlay">
                <label for="imageInput" class="image-upload-btn">
                  📷 이미지 변경
                </label>
                <input 
                  id="imageInput"
                  type="file"
                  accept="image/jpeg,image/png"
                  @change="handleImageUpload"
                  style="display: none"
                />
              </div>
            </div>
            <div class="image-info">
              <small class="text-muted">
                JPEG 또는 PNG 파일, 500x500~1000x1000px, 최대 1MB
              </small>
            </div>
          </div>

          <!-- 프로필 정보 폼 -->
          <form @submit.prevent="updateProfile" class="profile-form">
            <div class="form-group">
              <label class="form-label">이름</label>
              <input 
                v-model="form.name"
                type="text"
                class="form-input"
                required
                :disabled="updating"
              />
            </div>

            <div class="form-group">
              <label class="form-label">이메일</label>
              <input 
                :value="userProfile.email"
                type="email"
                class="form-input"
                disabled
              />
              <small class="text-muted">이메일은 변경할 수 없습니다</small>
            </div>

            <div class="form-group">
              <label class="form-label">역할</label>
              <div class="role-badge">
                <span :class="['badge', userProfile.role]">
                  {{ userProfile.role === 'mentor' ? '멘토' : '멘티' }}
                </span>
              </div>
              <small class="text-muted">역할은 변경할 수 없습니다</small>
            </div>

            <div class="form-group">
              <label class="form-label">소개</label>
              <textarea 
                v-model="form.bio"
                class="form-textarea"
                rows="4"
                placeholder="자신을 간단히 소개해주세요"
                :disabled="updating"
              ></textarea>
            </div>

            <!-- 멘토인 경우 스킬 입력 -->
            <div v-if="userProfile.role === 'mentor'" class="form-group">
              <label class="form-label">기술 스택</label>
              <div class="skills-input">
                <input 
                  v-model="newSkill"
                  type="text"
                  class="form-input"
                  placeholder="기술을 입력하고 Enter를 누르세요"
                  @keydown.enter.prevent="addSkill"
                  :disabled="updating"
                />
                <button 
                  type="button"
                  @click="addSkill"
                  class="btn btn-secondary"
                  :disabled="!newSkill.trim() || updating"
                >
                  추가
                </button>
              </div>
              <div class="skills-list">
                <span 
                  v-for="(skill, index) in form.skills"
                  :key="index"
                  class="skill-tag"
                >
                  {{ skill }}
                  <button 
                    type="button"
                    @click="removeSkill(index)"
                    class="skill-remove"
                    :disabled="updating"
                  >
                    ×
                  </button>
                </span>
              </div>
              <small class="text-muted">
                보유한 기술이나 전문 분야를 추가해주세요
              </small>
            </div>

            <!-- 에러/성공 메시지 -->
            <div v-if="error" class="error-message">
              {{ error }}
            </div>

            <div v-if="successMessage" class="success-message">
              {{ successMessage }}
            </div>

            <!-- 제출 버튼 -->
            <div class="form-actions">
              <button 
                type="submit"
                class="btn btn-primary"
                :disabled="updating || !hasChanges"
              >
                {{ updating ? '업데이트 중...' : '프로필 업데이트' }}
              </button>
              
              <button 
                type="button"
                @click="resetForm"
                class="btn btn-secondary"
                :disabled="updating"
              >
                취소
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/composables/useToast'
import { UserService } from '@/services/user'
import type { UserProfile, UpdateMentorProfileRequest, UpdateMenteeProfileRequest } from '@/types/api'

const authStore = useAuthStore()
const { success, error: showError } = useToast()
const loading = ref(true)
const updating = ref(false)
const error = ref('')
const successMessage = ref('')
const newSkill = ref('')
const selectedImage = ref<string | null>(null)

const userProfile = ref<UserProfile | null>(null)

const form = reactive({
  name: '',
  bio: '',
  skills: [] as string[]
})

const originalForm = reactive({
  name: '',
  bio: '',
  skills: [] as string[]
})

// 프로필 이미지 URL
const profileImageUrl = computed(() => {
  if (!userProfile.value) return ''
  return UserService.getProfileImageUrl(userProfile.value.role, userProfile.value.id)
})

// 변경사항 확인
const hasChanges = computed(() => {
  return form.name !== originalForm.name ||
         form.bio !== originalForm.bio ||
         JSON.stringify(form.skills) !== JSON.stringify(originalForm.skills) ||
         selectedImage.value !== null
})

// 프로필 정보 로드
const loadProfile = async () => {
  try {
    loading.value = true
    await authStore.fetchCurrentUser()
    userProfile.value = authStore.user
    
    if (userProfile.value) {
      form.name = userProfile.value.profile.name
      form.bio = userProfile.value.profile.bio
      form.skills = userProfile.value.role === 'mentor' 
        ? [...(userProfile.value.profile as any).skills] 
        : []
      
      // 원본 데이터 저장
      originalForm.name = form.name
      originalForm.bio = form.bio
      originalForm.skills = [...form.skills]
    }
  } catch (err) {
    error.value = '프로필을 로드하는데 실패했습니다.'
  } finally {
    loading.value = false
  }
}

// 이미지 업로드 처리
const handleImageUpload = async (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (!file) return

  // 이미지 검증
  const validation = UserService.validateImageFile(file)
  if (!validation.valid) {
    showError('이미지 오류', validation.error || '올바르지 않은 이미지 파일입니다.')
    return
  }

  try {
    selectedImage.value = await UserService.convertImageToBase64(file)
    error.value = ''
    success('이미지 선택', '이미지가 선택되었습니다. 프로필 업데이트를 눌러 저장하세요.')
  } catch (err) {
    showError('이미지 처리 오류', '이미지 처리에 실패했습니다.')
  }
}

// 이미지 에러 처리
const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement
  if (userProfile.value?.role === 'mentor') {
    img.src = 'https://placehold.co/500x500.jpg?text=MENTOR'
  } else {
    img.src = 'https://placehold.co/500x500.jpg?text=MENTEE'
  }
}

// 스킬 추가
const addSkill = () => {
  const skill = newSkill.value.trim()
  if (skill && !form.skills.includes(skill)) {
    form.skills.push(skill)
    newSkill.value = ''
  }
}

// 스킬 제거
const removeSkill = (index: number) => {
  form.skills.splice(index, 1)
}

// 폼 리셋
const resetForm = () => {
  form.name = originalForm.name
  form.bio = originalForm.bio
  form.skills = [...originalForm.skills]
  selectedImage.value = null
  error.value = ''
  successMessage.value = ''
}

// 프로필 업데이트
const updateProfile = async () => {
  if (!userProfile.value) return

  try {
    updating.value = true
    error.value = ''
    successMessage.value = ''

    const updateData = {
      id: userProfile.value.id,
      name: form.name,
      role: userProfile.value.role,
      bio: form.bio,
      image: selectedImage.value || ''
    }

    let updatedProfile: UserProfile

    if (userProfile.value.role === 'mentor') {
      const mentorData: UpdateMentorProfileRequest = {
        ...updateData,
        role: 'mentor',
        skills: form.skills
      }
      updatedProfile = await UserService.updateProfile(mentorData)
    } else {
      const menteeData: UpdateMenteeProfileRequest = {
        ...updateData,
        role: 'mentee'
      }
      updatedProfile = await UserService.updateProfile(menteeData)
    }

    // 상태 업데이트
    authStore.updateUserProfile(updatedProfile)
    userProfile.value = updatedProfile
    
    // 원본 데이터 업데이트
    originalForm.name = form.name
    originalForm.bio = form.bio
    originalForm.skills = [...form.skills]
    selectedImage.value = null

    success('프로필 업데이트', '프로필이 성공적으로 업데이트되었습니다!')

  } catch (err: any) {
    showError('업데이트 실패', err.response?.data?.error || '프로필 업데이트에 실패했습니다.')
  } finally {
    updating.value = false
  }
}

// 컴포넌트 마운트 시 프로필 로드
onMounted(() => {
  loadProfile()
})

// 에러 메시지 자동 제거
watch(error, (newError) => {
  if (newError) {
    setTimeout(() => {
      error.value = ''
    }, 5000)
  }
})
</script>

<style scoped>
.profile-container {
  min-height: calc(100vh - 60px);
  padding: 2rem 0;
}

.profile-header {
  text-align: center;
  margin-bottom: 3rem;
}

.profile-header h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  color: var(--color-text);
}

.subtitle {
  color: var(--color-text-soft);
  font-size: 1.125rem;
}

.loading {
  text-align: center;
  padding: 4rem 0;
  color: var(--color-text-soft);
}

.profile-content {
  max-width: 800px;
  margin: 0 auto;
}

.profile-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

/* 이미지 섹션 */
.image-section {
  padding: 2rem;
  text-align: center;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  border-bottom: 1px solid var(--color-border);
}

.image-container {
  position: relative;
  display: inline-block;
  margin-bottom: 1rem;
}

.profile-image {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.image-overlay {
  position: absolute;
  bottom: 0;
  right: 0;
}

.image-upload-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: var(--color-primary);
  color: white;
  border-radius: 50%;
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.image-upload-btn:hover {
  background: var(--color-primary-dark);
  transform: scale(1.1);
}

.image-info {
  color: var(--color-text-soft);
  font-size: 0.75rem;
}

/* 폼 섹션 */
.profile-form {
  padding: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: var(--color-text);
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid var(--color-border);
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(62, 175, 124, 0.1);
}

.form-input:disabled,
.form-textarea:disabled {
  background-color: #f8fafc;
  color: var(--color-text-soft);
  cursor: not-allowed;
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.role-badge {
  margin-bottom: 0.5rem;
}

.badge {
  display: inline-block;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
}

.badge.mentor {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.badge.mentee {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

/* 스킬 섹션 */
.skills-input {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.skills-input .form-input {
  flex: 1;
}

.skills-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.skill-tag {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  background: var(--color-primary);
  color: white;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 500;
}

.skill-remove {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  font-size: 1.25rem;
  line-height: 1;
  padding: 0;
  margin-left: 0.25rem;
}

.skill-remove:hover {
  opacity: 0.7;
}

/* 메시지 */
.error-message,
.success-message {
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  font-weight: 500;
}

.error-message {
  background: #fef2f2;
  color: var(--color-danger);
  border: 1px solid #fecaca;
}

.success-message {
  background: #f0fdf4;
  color: var(--color-success);
  border: 1px solid #86efac;
}

/* 액션 버튼 */
.form-actions {
  display: flex;
  gap: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--color-border);
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
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
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(62, 175, 124, 0.3);
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
  .profile-container {
    padding: 1rem 0;
  }

  .profile-header h1 {
    font-size: 2rem;
  }

  .image-section,
  .profile-form {
    padding: 1.5rem;
  }

  .skills-input {
    flex-direction: column;
  }

  .form-actions {
    flex-direction: column;
  }
}
</style>
