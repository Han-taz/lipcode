# 🚀 멘토-멘티 매칭 앱 실행 가이드

## 문제 해결 단계

### 1단계: 현재 상태 확인
브라우저에서 다음 링크를 열어보세요:
- http://localhost:3000 (프론트엔드)
- http://localhost:8080 (백엔드)

### 2단계: 디버그 페이지 확인
프로젝트 폴더의 `debug.html` 파일을 브라우저에서 직접 열어서 상태를 확인하세요.

### 3단계: 수동 실행

#### 터미널 1 - 백엔드 실행
```bash
cd back-end
python3 -m pip install -r requirements.txt
python3 main.py
```

#### 터미널 2 - 프론트엔드 실행
```bash
cd front-end
npm install
npm run dev
```

### 4단계: 자동 실행 스크립트
```bash
chmod +x run-debug.sh
./run-debug.sh
```

## 일반적인 문제와 해결책

### 문제 1: "포트가 이미 사용 중"
```bash
# 사용 중인 프로세스 확인
lsof -ti:3000
lsof -ti:8080

# 프로세스 종료
kill -9 $(lsof -ti:3000)
kill -9 $(lsof -ti:8080)
```

### 문제 2: "Node.js 또는 Python이 없음"
- Node.js 설치: https://nodejs.org/
- Python 3 설치: https://www.python.org/

### 문제 3: "의존성 설치 오류"
```bash
# 캐시 정리 후 재설치
cd front-end
rm -rf node_modules package-lock.json
npm install

cd ../back-end
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

### 문제 4: "빈 화면 또는 오류"
1. 브라우저 개발자 도구 (F12) 열기
2. 콘솔 탭에서 오류 메시지 확인
3. 네트워크 탭에서 API 호출 상태 확인

## 성공적인 실행 확인

### 백엔드 확인 사항:
- ✅ http://localhost:8080 → Swagger UI 페이지
- ✅ http://localhost:8080/swagger-ui → API 문서
- ✅ 터미널에서 "Uvicorn running on..." 메시지

### 프론트엔드 확인 사항:
- ✅ http://localhost:3000 → 멘토-멘티 매칭 앱 홈페이지
- ✅ 터미널에서 "Local: http://localhost:3000" 메시지
- ✅ 로그인/회원가입 버튼 보임

## 연락처
문제가 지속되면 개발자에게 다음 정보와 함께 문의하세요:
- 운영체제 (macOS, Windows, Linux)
- Node.js 버전 (`node --version`)
- Python 버전 (`python3 --version`)
- 오류 메시지 스크린샷
