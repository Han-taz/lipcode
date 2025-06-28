# 멘토-멘티 매칭 앱 🎯

전문적인 멘토링 서비스를 위한 현대적인 웹 애플리케이션입니다. 멘토와 멘티를 효과적으로 매칭하여 1:1 멘토링을 지원합니다.

## ✨ 주요 기능

- 👤 **사용자 관리**: 멘토/멘티 역할 기반 회원가입 및 프로필 관리
- 🔍 **멘토 검색**: 기술 스택과 경험 기반 멘토 필터링 및 검색
- 💌 **매칭 요청**: 개인화된 메시지와 함께 멘토링 요청 전송
- 📋 **요청 관리**: 멘토를 위한 요청 승인/거절 시스템
- 🖼️ **이미지 업로드**: 프로필 사진 업로드 및 관리
- 🔐 **JWT 인증**: 안전한 토큰 기반 인증 시스템

## 🏗️ 프로젝트 구조

```
lipcode/
├── back-end/              # Python FastAPI 백엔드
│   ├── app/
│   │   ├── core/          # 설정, 데이터베이스, 의존성
│   │   ├── models/        # SQLAlchemy 데이터 모델
│   │   ├── routers/       # API 엔드포인트 라우터
│   │   ├── schemas/       # Pydantic 스키마 (검증)
│   │   └── utils/         # 인증 및 유틸리티
│   ├── images/            # 업로드된 프로필 이미지
│   ├── main.py            # FastAPI 애플리케이션 진입점
│   ├── requirements.txt   # Python 의존성
│   └── .env              # 환경 변수
├── front-end/             # Vue 3 + TypeScript 프론트엔드
│   ├── src/
│   │   ├── components/    # 재사용 가능한 Vue 컴포넌트
│   │   ├── views/         # 페이지 뷰 컴포넌트
│   │   ├── stores/        # Pinia 상태 관리
│   │   ├── services/      # API 서비스 클래스
│   │   ├── types/         # TypeScript 타입 정의
│   │   ├── composables/   # Vue 3 컴포저블
│   │   └── router/        # Vue Router 설정
│   ├── package.json       # Node.js 의존성
│   └── vite.config.ts     # Vite 빌드 설정
├── requirements/          # 프로젝트 요구사항 문서
├── setup.sh              # 자동 설치 스크립트
├── run.sh                # 애플리케이션 실행 스크립트
└── README.md             # 프로젝트 문서
```

## 🛠️ 기술 스택

### 백엔드
- **Python 3.8+** - 백엔드 언어
- **FastAPI** - 현대적인 고성능 웹 API 프레임워크
- **SQLAlchemy** - Python SQL 툴킷 및 ORM
- **SQLite** - 임베디드 관계형 데이터베이스
- **JWT (PyJWT)** - JSON Web Token 인증
- **Pydantic** - 데이터 검증 및 직렬화
- **Uvicorn** - ASGI 서버

### 프론트엔드
- **Vue 3** - 프로그레시브 JavaScript 프레임워크
- **TypeScript** - 정적 타입 JavaScript
- **Vite** - 차세대 프론트엔드 빌드 도구
- **Vue Router 4** - Vue.js 공식 라우터
- **Pinia** - Vue 상태 관리 라이브러리
- **Axios** - Promise 기반 HTTP 클라이언트

## 🚀 빠른 시작

### 필수 요구사항
- Python 3.8 이상
- Node.js 16 이상
- npm 또는 yarn

### 1. 자동 설치 (권장)
```bash
# 저장소 클론
git clone <repository-url>
cd lipcode

# 자동 설치 실행
chmod +x setup.sh
./setup.sh
```

### 2. 수동 설치

#### 백엔드 설정
```bash
cd back-end

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경변수 설정
cp .env.example .env  # .env 파일 수정 필요
```

#### 프론트엔드 설정
```bash
cd front-end

# 의존성 설치
npm install
```

### 3. 애플리케이션 실행

#### 자동 실행 (권장)
```bash
# 백엔드와 프론트엔드 동시 실행
chmod +x run.sh
./run.sh
```

#### 수동 실행
```bash
# 터미널 1: 백엔드 실행
cd back-end
python main.py

# 터미널 2: 프론트엔드 실행
cd front-end
npm run dev
```

### 4. 접속 확인
- 🎨 **프론트엔드**: http://localhost:3000
- 🔧 **백엔드 API**: http://localhost:8080
- 📚 **API 문서 (Swagger)**: http://localhost:8080/swagger-ui
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

### 4. 접속 확인
- 🎨 **프론트엔드**: http://localhost:3000
- 🔧 **백엔드 API**: http://localhost:8080
- 📚 **API 문서 (Swagger)**: http://localhost:8080/swagger-ui

## 📱 주요 화면

### 1. 홈 페이지
- 비로그인 사용자: 서비스 소개 및 로그인/회원가입 링크
- 로그인 사용자: 개인화된 대시보드

### 2. 회원가입/로그인
- 멘토/멘티 역할 선택
- 이메일/비밀번호 기반 인증
- JWT 토큰 기반 세션 관리

### 3. 프로필 관리
- 개인 정보 수정 (이름, 자기소개)
- 프로필 이미지 업로드
- 멘토: 기술 스택 관리

### 4. 멘토 목록 (멘티 전용)
- 기술 스택별 멘토 필터링
- 경험/평점 기반 정렬
- 매칭 요청 모달

### 5. 매칭 요청 관리
- 멘토: 받은 요청 확인 및 승인/거절
- 멘티: 보낸 요청 상태 확인

## 🔧 개발 가이드

### API 엔드포인트

#### 인증 관련
- `POST /api/signup` - 회원가입
- `POST /api/login` - 로그인

#### 사용자 프로필
- `GET /api/profile` - 현재 사용자 프로필 조회
- `PUT /api/profile` - 프로필 업데이트

#### 멘토 관리
- `GET /api/mentors` - 멘토 목록 조회
- `GET /api/mentors/{id}` - 특정 멘토 조회

#### 매칭 요청
- `POST /api/match-requests` - 매칭 요청 생성
- `GET /api/match-requests` - 매칭 요청 목록
- `PUT /api/match-requests/{id}/respond` - 요청 승인/거절

### 데이터베이스 스키마

#### Users 테이블
```sql
- id: INTEGER (Primary Key)
- email: VARCHAR (Unique)
- password_hash: VARCHAR
- name: VARCHAR
- role: ENUM('mentor', 'mentee')
- bio: TEXT
- skills: JSON (멘토만)
- image_url: VARCHAR
- created_at: TIMESTAMP
```

#### MatchRequests 테이블
```sql
- id: INTEGER (Primary Key)
- mentee_id: INTEGER (Foreign Key)
- mentor_id: INTEGER (Foreign Key)
- message: TEXT
- status: ENUM('pending', 'accepted', 'rejected')
- created_at: TIMESTAMP
- updated_at: TIMESTAMP
```

## 🎯 사용 방법

### 멘티 사용자 흐름
1. **회원가입**: 멘티로 계정 생성
2. **프로필 설정**: 이름, 자기소개, 프로필 사진 등록
3. **멘토 검색**: 원하는 기술 스택을 가진 멘토 찾기
4. **매칭 요청**: 개인화된 메시지와 함께 요청 전송
5. **요청 관리**: 요청 상태 확인 및 관리

### 멘토 사용자 흐름
1. **회원가입**: 멘토로 계정 생성
2. **프로필 설정**: 기술 스택, 경험, 자기소개 등록
3. **요청 확인**: 멘티들의 매칭 요청 검토
4. **요청 응답**: 요청 승인 또는 거절
5. **멘토링 진행**: 매칭된 멘티와 멘토링 시작

## 🔐 보안 특징

- **JWT 인증**: 안전한 토큰 기반 인증
- **비밀번호 해싱**: bcrypt를 사용한 안전한 비밀번호 저장
- **CORS 설정**: 적절한 Cross-Origin 요청 제한
- **입력 검증**: Pydantic을 통한 강력한 데이터 검증
- **이미지 검증**: 파일 형식 및 크기 제한

## 🧪 테스트

### 백엔드 테스트
```bash
cd back-end
pytest tests/
```

### 프론트엔드 테스트
```bash
cd front-end
npm run test
```

## 📦 배포

### Docker를 사용한 배포 (예정)
```bash
# Docker Compose로 전체 스택 실행
docker-compose up -d
```

### 수동 배포
1. **백엔드**: Gunicorn + Nginx
2. **프론트엔드**: 정적 파일 빌드 후 웹 서버 배포
3. **데이터베이스**: PostgreSQL 또는 MySQL로 마이그레이션

## ✅ 완료된 기능

### 백엔드 (100% 완료)
- [x] 데이터베이스 모델 설계 및 생성
- [x] JWT 인증 시스템 구현
- [x] 회원가입/로그인 API
- [x] 프로필 관리 API
- [x] 멘토 목록 조회 API
- [x] 매칭 요청 관리 API
- [x] 이미지 업로드/서빙 API

### 프론트엔드 (100% 완료)
- [x] API 서비스 클래스 구현
- [x] TypeScript 타입 정의
- [x] Pinia 인증 상태 관리
- [x] 라우터 및 인증 가드 설정
- [x] 네비게이션 바 컴포넌트
- [x] 회원가입/로그인 페이지
- [x] 홈페이지 (대시보드)
- [x] 프로필 관리 페이지
- [x] 멘토 목록 페이지
- [x] 매칭 요청 관리 페이지
- [x] UI/UX 개선 및 토스트 알림

## 🤝 기여 방법

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 문의

프로젝트에 대한 문의사항이 있으시면 이슈를 등록해주세요.

---

**💡 주의사항**
- 이 프로젝트는 교육 목적으로 제작되었습니다
- 프로덕션 환경에서 사용하기 전에 추가적인 보안 검토가 필요합니다
- 환경 변수(.env)에 민감한 정보를 포함하지 마세요
