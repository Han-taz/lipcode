#!/bin/bash

echo "🚀 백엔드 서버 시작 중..."

# 프로젝트 루트로 이동
cd /Users/kevin/project/lipcode

# 가상환경 활성화
source .venv/bin/activate

# 백엔드 디렉토리로 이동
cd back-end

# 서버 시작
echo "📡 FastAPI 서버를 http://localhost:8080 에서 실행합니다..."
python3 main.py
