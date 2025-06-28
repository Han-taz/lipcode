# 멘토-멘티 매칭 앱

이 프로젝트는 멘토와 멘티를 매칭하는 웹 애플리케이션입니다.

## 프로젝트 구조

```
lipcode/
├── back-end/          # Python FastAPI 백엔드
│   ├── app/
│   │   ├── core/      # 설정, 데이터베이스
│   │   ├── models/    # SQLAlchemy 모델
│   │   ├── routers/   # API 라우터
│   │   ├── schemas/   # Pydantic 스키마
│   │   ├── services/  # 비즈니스 로직
│   │   └── utils/     # 유틸리티
│   ├── main.py        # FastAPI 앱 진입점
│   └── requirements.txt
├── front-end/         # Vue 3 프론트엔드
│   ├── src/
│   │   ├── components/ # Vue 컴포넌트
│   │   ├── views/     # 페이지 뷰
│   │   ├── stores/    # Pinia 상태관리
│   │   ├── services/  # API 서비스
│   │   └── types/     # TypeScript 타입
│   └── package.json
└── requirements/      # 프로젝트 요구사항
```

## 기술 스택

### 백엔드
- **Python 3.8+**
- **FastAPI** - 현대적인 웹 API 프레임워크
- **SQLAlchemy** - ORM
- **SQLite** - 로컬 데이터베이스
- **JWT** - 인증
- **Pydantic** - 데이터 검증

### 프론트엔드
- **Vue 3** - 프로그레시브 프레임워크
- **TypeScript** - 타입 안정성
- **Vite** - 빌드 도구
- **Vue Router** - 라우팅
- **Pinia** - 상태 관리
- **Axios** - HTTP 클라이언트

## 설치 및 실행

### 1. 의존성 설치
```bash
chmod +x setup.sh
./setup.sh
```

### 2. 백엔드 실행
```bash
cd back-end
python main.py
```
- 실행 주소: http://localhost:8080
- Swagger UI: http://localhost:8080/swagger-ui
- OpenAPI JSON: http://localhost:8080/openapi.json

### 3. 프론트엔드 실행
```bash
cd front-end
npm run dev
```
- 실행 주소: http://localhost:3000

## 주요 기능

1. **회원가입 및 로그인** - JWT 토큰 기반 인증
2. **프로필 관리** - 멘토/멘티 프로필 등록 및 수정
3. **멘토 목록 조회** - 기술 스택 필터링 및 정렬
4. **매칭 요청** - 멘티가 멘토에게 요청 전송
5. **요청 관리** - 멘토의 요청 수락/거절, 멘티의 요청 취소

## TODO

현재 프로젝트 구조만 생성되었으며, 다음 순서로 개발을 진행해야 합니다:

### Phase 1: 백엔드 개발
- [ ] 데이터베이스 모델 설계 및 생성
- [ ] JWT 인증 시스템 구현
- [ ] 회원가입/로그인 API
- [ ] 프로필 관리 API
- [ ] 멘토 목록 조회 API
- [ ] 매칭 요청 관리 API
- [ ] 이미지 업로드/서빙 API

### Phase 2: 프론트엔드 개발
- [ ] 인증 상태 관리 (Pinia)
- [ ] 회원가입/로그인 폼
- [ ] 프로필 관리 페이지
- [ ] 멘토 목록 페이지
- [ ] 매칭 요청 관리 페이지
- [ ] UI/UX 개선

### Phase 3: 통합 및 테스트
- [ ] API 연동 테스트
- [ ] 보안 검증
- [ ] 최종 배포 준비
# lipcode
