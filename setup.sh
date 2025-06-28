#!/bin/bash

echo "멘토-멘티 매칭 앱 실행 스크립트"
echo "================================"

# 백엔드 의존성 설치
echo "백엔드 의존성 설치 중..."
cd back-end
python -m pip install -r requirements.txt

# 프론트엔드 의존성 설치  
echo "프론트엔드 의존성 설치 중..."
cd ../front-end
npm install

echo "설치 완료!"
echo ""
echo "실행 명령어:"
echo "백엔드: cd back-end && python main.py"
echo "프론트엔드: cd front-end && npm run dev"
