# Developer Guide - 멘토-멘티 매칭 앱

## 개발 환경 설정

### 백엔드 개발
```bash
cd back-end
source venv/bin/activate  # 가상환경 활성화
uvicorn main:app --reload --port 8080  # 개발 서버 실행
```

### 프론트엔드 개발
```bash
cd front-end
npm run dev  # 개발 서버 실행
```

## 프로젝트 구조 상세

### 백엔드 (`back-end/`)
```
app/
├── core/
│   ├── config.py          # 앱 설정
│   ├── database.py        # 데이터베이스 설정
│   └── dependencies.py    # FastAPI 의존성
├── models/
│   └── user.py           # SQLAlchemy 모델
├── routers/
│   ├── auth.py           # 인증 관련 API
│   ├── users.py          # 사용자 프로필 API
│   ├── mentors.py        # 멘토 관련 API
│   └── match_requests.py # 매칭 요청 API
├── schemas/
│   └── user.py           # Pydantic 스키마
└── utils/
    └── auth.py           # JWT 인증 유틸리티
```

### 프론트엔드 (`front-end/`)
```
src/
├── components/
│   ├── AppNavbar.vue     # 네비게이션 바
│   ├── ErrorPage.vue     # 에러 페이지 컴포넌트
│   ├── LoadingSpinner.vue # 로딩 스피너
│   └── ToastNotification.vue # 토스트 알림
├── views/
│   ├── HomeView.vue      # 홈/대시보드
│   ├── LoginView.vue     # 로그인
│   ├── SignupView.vue    # 회원가입
│   ├── ProfileView.vue   # 프로필 관리
│   ├── MentorsView.vue   # 멘토 목록
│   ├── MatchRequestsView.vue # 매칭 요청 관리
│   └── NotFoundView.vue  # 404 페이지
├── stores/
│   └── auth.ts           # 인증 상태 관리
├── services/
│   ├── api.ts            # 기본 API 설정
│   ├── auth.ts           # 인증 API
│   ├── user.ts           # 사용자 API
│   └── mentor.ts         # 멘토 API
├── types/
│   └── api.ts            # TypeScript 타입 정의
├── composables/
│   ├── useToast.ts       # 토스트 알림 관리
│   └── useErrorHandler.ts # 에러 처리
└── router/
    └── index.ts          # 라우터 설정
```

## API 엔드포인트 상세

### 인증 (`/api`)
- `POST /signup` - 회원가입
- `POST /login` - 로그인

### 사용자 프로필 (`/api`)
- `GET /profile` - 현재 사용자 프로필 조회
- `PUT /profile` - 프로필 업데이트

### 멘토 관리 (`/api`)
- `GET /mentors` - 멘토 목록 (필터링 지원)
- `GET /mentors/{id}` - 특정 멘토 상세 정보

### 매칭 요청 (`/api`)
- `POST /match-requests` - 새 매칭 요청 생성
- `GET /match-requests` - 요청 목록 (역할별)
- `PUT /match-requests/{id}/respond` - 요청 응답 (승인/거절)
- `DELETE /match-requests/{id}` - 요청 취소

### 이미지 서빙
- `GET /images/{filename}` - 업로드된 이미지 조회

## 주요 기능 구현

### JWT 인증
- 토큰 기반 인증 시스템
- 자동 토큰 갱신
- 로그아웃 시 토큰 제거

### 파일 업로드
- 프로필 이미지 업로드 지원
- 이미지 검증 (형식, 크기)
- Base64 인코딩 처리

### 상태 관리
- Pinia를 사용한 전역 상태 관리
- 인증 상태 관리
- 사용자 프로필 관리

### 라우터 가드
- 인증 필요 페이지 보호
- 역할 기반 접근 제어
- 비인증 사용자 페이지 제한

## 개발 팁

### 백엔드 디버깅
```bash
# 데이터베이스 초기화
rm -f database.db
python main.py

# 로그 확인
uvicorn main:app --reload --log-level debug
```

### 프론트엔드 디버깅
```bash
# 타입 체크
npm run type-check

# 린트 체크
npm run lint

# 빌드 테스트
npm run build
```

### API 테스트
- Swagger UI: http://localhost:8080/swagger-ui
- 직접 curl 요청으로 API 테스트

### 일반적인 문제 해결

1. **CORS 오류**: 백엔드 main.py의 CORS 설정 확인
2. **토큰 만료**: 프론트엔드에서 자동 리다이렉트 구현됨
3. **이미지 업로드 실패**: 파일 크기 및 형식 확인
4. **데이터베이스 오류**: SQLite 파일 권한 확인

## 성능 최적화

### 백엔드
- SQLAlchemy 쿼리 최적화
- 이미지 캐싱 설정
- API 응답 압축

### 프론트엔드
- 컴포넌트 lazy loading
- 이미지 최적화
- 번들 크기 최적화

## 보안 고려사항

1. **비밀번호 해싱**: bcrypt 사용
2. **JWT 보안**: 적절한 만료 시간 설정
3. **입력 검증**: Pydantic으로 강력한 검증
4. **XSS 방지**: Vue.js 기본 보안 기능 활용
5. **CSRF 방지**: SameSite 쿠키 설정

## 배포 전 체크리스트

- [ ] 환경 변수 설정 확인
- [ ] 프로덕션 데이터베이스 설정
- [ ] HTTPS 설정
- [ ] 로그 레벨 조정
- [ ] 에러 모니터링 설정
- [ ] 백업 전략 수립
