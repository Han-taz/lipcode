// 사용자 역할
export type UserRole = 'mentor' | 'mentee'

// 매칭 요청 상태
export type MatchRequestStatus = 'pending' | 'accepted' | 'rejected' | 'cancelled'

// 로그인 요청
export interface LoginRequest {
  email: string
  password: string
}

// 로그인 응답
export interface LoginResponse {
  token: string
}

// 회원가입 요청
export interface SignupRequest {
  email: string
  password: string
  name: string
  role: UserRole
}

// 프로필 세부정보 - 멘토
export interface MentorProfileDetails {
  name: string
  bio: string
  imageUrl: string
  skills: string[]
}

// 프로필 세부정보 - 멘티
export interface MenteeProfileDetails {
  name: string
  bio: string
  imageUrl: string
}

// 멘토 프로필
export interface MentorProfile {
  id: number
  email: string
  role: 'mentor'
  profile: MentorProfileDetails
}

// 멘티 프로필
export interface MenteeProfile {
  id: number
  email: string
  role: 'mentee'
  profile: MenteeProfileDetails
}

// 사용자 프로필 (Union 타입)
export type UserProfile = MentorProfile | MenteeProfile

// 멘토 프로필 업데이트 요청
export interface UpdateMentorProfileRequest {
  id: number
  name: string
  role: 'mentor'
  bio: string
  image: string // Base64 encoded
  skills: string[]
}

// 멘티 프로필 업데이트 요청
export interface UpdateMenteeProfileRequest {
  id: number
  name: string
  role: 'mentee'
  bio: string
  image: string // Base64 encoded
}

// 멘토 목록 아이템
export interface MentorListItem {
  id: number
  email: string
  role: 'mentor'
  profile: MentorProfileDetails
}

// 매칭 요청 생성
export interface MatchRequestCreate {
  mentorId: number
  menteeId: number
  message: string
}

// 매칭 요청
export interface MatchRequest {
  id: number
  mentorId: number
  menteeId: number
  message: string
  status: MatchRequestStatus
}

// 매칭 요청 (outgoing)
export interface MatchRequestOutgoing {
  id: number
  mentorId: number
  menteeId: number
  status: MatchRequestStatus
}

// 에러 응답
export interface ErrorResponse {
  error: string
  details?: string
}

// 멘토 목록 쿼리 파라미터
export interface MentorQueryParams {
  skill?: string
  orderBy?: 'skill' | 'name'
}
