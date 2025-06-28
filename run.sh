#!/bin/bash

echo "🚀 멘토-멘티 매칭 앱 실행"
echo "=========================="

# 백엔드 실행
echo "📡 백엔드 서버 시작 중..."

# 가상환경 활성화
echo "🐍 Python 가상환경 활성화 중..."
source .venv/bin/activate

cd back-end

# Python 의존성 설치 확인
if [ ! -f ".deps_installed" ]; then
    echo "📦 Python 의존성 설치 중..."
    /Users/kevin/project/lipcode/.venv/bin/python -m pip install -r requirements.txt
    touch .deps_installed
    echo "✅ 의존성 설치 완료"
fi

echo "🚀 백엔드 서버 실행 중..."
/Users/kevin/project/lipcode/.venv/bin/python main.py &

# 백엔드 PID 저장
BACKEND_PID=$!

# 프론트엔드 실행
echo "🎨 프론트엔드 서버 시작 중..."
cd ../front-end
echo "✅ 프론트엔드 서버가 http://localhost:3000 에서 실행됩니다"
npm run dev &

# 프론트엔드 PID 저장
FRONTEND_PID=$!

echo ""
echo "🎉 앱 실행 완료!"
echo ""
echo "📱 프론트엔드: http://localhost:3000"
echo "🔧 백엔드 API: http://localhost:8080"
echo "📚 Swagger UI: http://localhost:8080/swagger-ui"
echo ""
echo "💡 종료하려면 Ctrl+C를 누르세요"

# 종료 시그널 처리
trap "echo '🛑 서버를 종료합니다...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT

# 대기
wait
