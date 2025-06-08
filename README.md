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
│   └── 📁travel_recommendation/ 
|   |    └── travel_gpt.py  # 프롬프트 가공 후 OpenAI API 호출 → GPT에게 추천 정보 받아와 출력
│   |    └── attraction.py  # 사용자의 여행 목적과 지역을 입력받아 해당 지역 내의 키워드 관련 관광지 정보 제공
│   └── 📁festival_recommendation/ 
|   |    └── festival_tourAPI.py  # 위도/경도 입력 기반으로 반경 15km 내 축제 정보 제공 (TourAPI 활용)
│   |    └── festival_RAG.py  # GPT + RAG 기반으로 입력 키워드를 의미 확장 후 관련 축제 정보 출력
│   └── 📁local_market/ 
|   |    └── local_market_DEMO.py  # 당근마켓 형태로 지역 특산물 판매자와 구매자 연결 (로컬 마켓 기능 구현)
└── FE
    └── xxx
└── AI
    └── xxx
</code>
</pre>

<br>

## 🔗 관련 링크

[그라운드룰](https://github.com/CAPSTONEEEEE/NaegaGreen/blob/main/GroundRule.MD) <br>
[스타트 데모 영상](...)
