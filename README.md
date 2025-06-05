# 🚊소소행;
### AI를 활용하여 소도시 여행 추천과 지역 축제 정보를 제공하고, 소상공인들의 온/오프라인 판매를 돕는 통합 모바일 플랫폼

<br>

## ❗️전체 시스템 아키텍처 개요
본 프로젝트는 모바일 웹 기반 통합 플랫폼으로, 사용자 인터페이스부터 백엔드 서버, 데이터베이스, 추천 시스템, 외부 API까지 모듈화된 구조를 가지고 있으며, 다음과 같은 기술 스택을 기반으로 동작합니다.

프론트엔드: React

백엔드: Python 기반 FastAPI

데이터베이스: MySQL

AI 추천 시스템: PyTorch + pandas (콘텐츠기반필터링)

위치 기반 서비스: GeoLocation API

외부 정보 요약: ChatGPT API (OpenAI)

외부 관광 데이터: 한국관광공사 TourAPI 4.0

<br>

## 📁 폴더 구조

<pre style="background-color: #1F3737; padding: 10px; border-radius: 5px; color: #ffffff;">
<code>
Start
├── BE
│   └── festival.py  # 지역 기반 행사 정보 제공 코드입니다.
│   └── local_market.py  # 로컬 특산물 등록 및 구매/판매 코드입니다.
└── FE
    └── xxx
└── AI
    └── chatbot.py  # 사용자 입력 받기용 챗봇 코드입니다.
</code>
</pre>

<br>

## 🔗 관련 링크

[그라운드룰](https://github.com/CAPSTONEEEEE/NaegaGreen/blob/main/GroundRule.MD) <br>
[스타트 데모 영상](...)
