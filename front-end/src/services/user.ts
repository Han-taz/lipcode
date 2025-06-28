import { apiClient } from './api'
import type { 
  UserProfile,
  UpdateMentorProfileRequest,
  UpdateMenteeProfileRequest
} from '@/types/api'

export class UserService {
  // 프로필 업데이트
  static async updateProfile(
    data: UpdateMentorProfileRequest | UpdateMenteeProfileRequest
  ): Promise<UserProfile> {
    return await apiClient.put<UserProfile>('/profile', data)
  }

  // 프로필 이미지 URL 생성
  static getProfileImageUrl(role: 'mentor' | 'mentee', userId: number): string {
    return `http://localhost:8080/images/${role}/${userId}`
  }

  // 이미지 파일을 Base64로 변환
  static async convertImageToBase64(file: File): Promise<string> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader()
      reader.onload = () => {
        const result = reader.result as string
        // "data:image/jpeg;base64," 부분을 제거하고 순수 Base64만 반환
        const base64 = result.split(',')[1]
        resolve(base64)
      }
      reader.onerror = reject
      reader.readAsDataURL(file)
    })
  }

  // 이미지 파일 검증
  static validateImageFile(file: File): { valid: boolean; error?: string } {
    // 파일 형식 검증
    const allowedTypes = ['image/jpeg', 'image/png']
    if (!allowedTypes.includes(file.type)) {
      return { valid: false, error: 'JPEG 또는 PNG 파일만 업로드 가능합니다.' }
    }

    // 파일 크기 검증 (1MB)
    const maxSize = 1024 * 1024 // 1MB
    if (file.size > maxSize) {
      return { valid: false, error: '파일 크기는 1MB 이하여야 합니다.' }
    }

    return { valid: true }
  }
}
