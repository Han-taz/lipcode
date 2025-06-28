import { useToast } from '@/composables/useToast'

interface ApiError {
  response?: {
    data?: {
      error?: string
      detail?: string
    }
    status?: number
  }
  message?: string
}

export const useErrorHandler = () => {
  const { error } = useToast()

  const handleError = (err: unknown, defaultMessage: string = '오류가 발생했습니다') => {
    const apiError = err as ApiError
    
    let errorMessage = defaultMessage
    
    if (apiError.response?.data?.error) {
      errorMessage = apiError.response.data.error
    } else if (apiError.response?.data?.detail) {
      errorMessage = apiError.response.data.detail
    } else if (apiError.message) {
      errorMessage = apiError.message
    }

    // HTTP 상태 코드별 특별 처리
    if (apiError.response?.status === 401) {
      errorMessage = '인증이 필요합니다. 다시 로그인해주세요.'
    } else if (apiError.response?.status === 403) {
      errorMessage = '접근 권한이 없습니다.'
    } else if (apiError.response?.status === 404) {
      errorMessage = '요청한 리소스를 찾을 수 없습니다.'
    } else if (apiError.response?.status === 500) {
      errorMessage = '서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.'
    }

    error('오류', errorMessage)
    
    return errorMessage
  }

  return {
    handleError
  }
}
