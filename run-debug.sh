#!/bin/bash

echo "🔧 멘토-멘티 매칭 앱 진단 및 실행"
echo "=================================="

# 현재 디렉토리 확인
echo "📂 현재 위치: $(pwd)"

# Node.js 및 Python 확인
echo ""
echo "🔍 환경 확인:"
echo "Node.js 버전: $(node --version 2>/dev/null || echo '❌ Node.js가 설치되지 않음')"
echo "npm 버전: $(npm --version 2>/dev/null || echo '❌ npm이 설치되지 않음')"
echo "Python 버전: $(python3 --version 2>/dev/null || echo '❌ Python3가 설치되지 않음')"

# 프로젝트 구조 확인
echo ""
echo "📁 프로젝트 구조 확인:"
if [ -d "back-end" ]; then
    echo "✅ back-end 디렉토리 존재"
else
    echo "❌ back-end 디렉토리 없음"
fi

if [ -d "front-end" ]; then
    echo "✅ front-end 디렉토리 존재"
else
    echo "❌ front-end 디렉토리 없음"
fi

if [ -f "front-end/package.json" ]; then
    echo "✅ package.json 존재"
else
    echo "❌ package.json 없음"
fi

if [ -d "front-end/node_modules" ]; then
    echo "✅ node_modules 존재"
else
    echo "❌ node_modules 없음 - npm install 필요"
fi

# 포트 사용 확인
echo ""
echo "🔌 포트 상태 확인:"
if lsof -ti:3000 >/dev/null 2>&1; then
    echo "⚠️ 포트 3000이 사용 중입니다"
    echo "사용 중인 프로세스: $(lsof -ti:3000)"
else
    echo "✅ 포트 3000 사용 가능"
fi

if lsof -ti:8080 >/dev/null 2>&1; then
    echo "⚠️ 포트 8080이 사용 중입니다"
    echo "사용 중인 프로세스: $(lsof -ti:8080)"
else
    echo "✅ 포트 8080 사용 가능"
fi

echo ""
echo "🚀 서버 실행 중..."

# 사용 중인 포트 정리 (선택사항)
read -p "기존 프로세스를 종료하고 새로 시작하시겠습니까? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🛑 기존 프로세스 종료 중..."
    pkill -f "uvicorn\|vite\|node.*3000\|python.*main.py" 2>/dev/null || true
    sleep 2
fi

# 백엔드 실행
echo ""
echo "📡 백엔드 서버 시작..."
cd back-end

# Python 의존성 설치 확인
if [ ! -f ".dependencies_installed" ]; then
    echo "📦 Python 의존성 설치 중..."
    python3 -m pip install -r requirements.txt
    touch .dependencies_installed
fi

# 백엔드 실행
echo "🟢 백엔드 서버 실행 중... (포트 8080)"
python3 main.py &
BACKEND_PID=$!
echo "백엔드 PID: $BACKEND_PID"

# 백엔드가 시작될 때까지 대기
echo "⏳ 백엔드 서버 시작 대기..."
sleep 3

# 백엔드 상태 확인
if curl -s http://localhost:8080 >/dev/null 2>&1; then
    echo "✅ 백엔드 서버가 성공적으로 시작되었습니다!"
else
    echo "⚠️ 백엔드 서버 상태를 확인할 수 없습니다."
fi

# 프론트엔드 실행
echo ""
echo "🎨 프론트엔드 서버 시작..."
cd ../front-end

# Node.js 의존성 설치 확인
if [ ! -f ".dependencies_installed" ]; then
    echo "📦 Node.js 의존성 설치 중..."
    npm install
    touch .dependencies_installed
fi

echo "🟢 프론트엔드 서버 실행 중... (포트 3000)"
npm run dev &
FRONTEND_PID=$!
echo "프론트엔드 PID: $FRONTEND_PID"

# 프론트엔드가 시작될 때까지 대기
echo "⏳ 프론트엔드 서버 시작 대기..."
sleep 5

# 상태 확인
echo ""
echo "🎉 실행 완료!"
echo "=================================="
echo "📱 프론트엔드: http://localhost:3000"
echo "🔧 백엔드 API: http://localhost:8080"
echo "📚 Swagger UI: http://localhost:8080/swagger-ui"
echo "🔍 디버그 페이지: file://$(pwd)/../debug.html"
echo ""

# 브라우저에서 열기 시도
if command -v open >/dev/null 2>&1; then
    echo "🌐 브라우저에서 앱을 여는 중..."
    sleep 2
    open http://localhost:3000
elif command -v xdg-open >/dev/null 2>&1; then
    echo "🌐 브라우저에서 앱을 여는 중..."
    sleep 2
    xdg-open http://localhost:3000
fi

echo "💡 종료하려면 Ctrl+C를 누르세요"
echo ""

# 로그 모니터링
echo "📊 실시간 상태 모니터링:"
echo "=================================="

# 종료 시그널 처리
cleanup() {
    echo ""
    echo "🛑 서버를 종료합니다..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    pkill -f "uvicorn\|vite\|node.*3000\|python.*main.py" 2>/dev/null || true
    echo "✅ 모든 서버가 종료되었습니다."
    exit 0
}

trap cleanup INT TERM

# 상태 모니터링 루프
while true; do
    sleep 10
    
    # 포트 상태 확인
    if lsof -ti:3000 >/dev/null 2>&1; then
        FRONTEND_STATUS="🟢"
    else
        FRONTEND_STATUS="🔴"
    fi
    
    if lsof -ti:8080 >/dev/null 2>&1; then
        BACKEND_STATUS="🟢"
    else
        BACKEND_STATUS="🔴"
    fi
    
    echo "[$(date '+%H:%M:%S')] Frontend: $FRONTEND_STATUS | Backend: $BACKEND_STATUS"
done
