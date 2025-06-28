import { apiClient } from './api'
import type { 
  MentorListItem,
  MentorQueryParams,
  MatchRequest,
  MatchRequestCreate,
  MatchRequestOutgoing
} from '@/types/api'

export class MentorService {
  // 멘토 목록 조회
  static async getMentors(params?: MentorQueryParams): Promise<MentorListItem[]> {
    return await apiClient.get<MentorListItem[]>('/mentors', params)
  }
}

export class MatchRequestService {
  // 매칭 요청 생성
  static async createMatchRequest(data: MatchRequestCreate): Promise<MatchRequest> {
    return await apiClient.post<MatchRequest>('/match-requests', data)
  }

  // 받은 매칭 요청 목록 (멘토용)
  static async getIncomingRequests(): Promise<MatchRequest[]> {
    return await apiClient.get<MatchRequest[]>('/match-requests/incoming')
  }

  // 보낸 매칭 요청 목록 (멘티용)
  static async getOutgoingRequests(): Promise<MatchRequestOutgoing[]> {
    return await apiClient.get<MatchRequestOutgoing[]>('/match-requests/outgoing')
  }

  // 매칭 요청 수락 (멘토용)
  static async acceptRequest(requestId: number): Promise<MatchRequest> {
    return await apiClient.put<MatchRequest>(`/match-requests/${requestId}/accept`)
  }

  // 매칭 요청 거절 (멘토용)
  static async rejectRequest(requestId: number): Promise<MatchRequest> {
    return await apiClient.put<MatchRequest>(`/match-requests/${requestId}/reject`)
  }

  // 매칭 요청 취소 (멘티용)
  static async cancelRequest(requestId: number): Promise<MatchRequest> {
    return await apiClient.delete<MatchRequest>(`/match-requests/${requestId}`)
  }
}
