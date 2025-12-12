# 🚊 소소행 (SosoHaeng)
### RAG를 활용한 소도시 여행지 추천 서비스 및 로컬 상생 올인원 플랫폼

<br>

> 🚨 **안내 (Notice)**
> 본 레포지토리는 캡스톤 디자인 **'12팀 - 내가그린'** 의 **기획서, 보고서, 발표 자료**를 관리하는 **문서 저장소(Archive)** 입니다.
> 실제 서비스 구동을 위한 **소스 코드(Source Code)** 는 역할에 따라 아래의 별도 레포지토리에서 관리됩니다.

<br>

## 🔗 소스 코드 저장소 (Source Code Repositories)
평가 및 상세 코드 확인을 위해서는 아래 링크를 참고해 주세요.

| 구분 | 주요 역할 | 저장소 바로가기 |
| :---: | :--- | :---: |
| **Backend** | **FastAPI** 서버, 로컬 마켓 비즈니스 로직, DB 관리 | [👉 Backend (BE) 바로가기](https://github.com/CAPSTONEEEEE/BE) |
| **Frontend** | **React Native** 앱 UI/UX, 외부 API 연동, Auth | [👉 Frontend (FE) 바로가기](https://github.com/CAPSTONEEEEE/FE) |
| **AI / RAG** | **LangChain** 파이프라인, 벡터 DB(FAISS), 추천 알고리즘 | *(BE 레포지토리에 포함됨)* |

<br>

## 📝 과제 개요 (Project Overview)
* **과제명**: RAG를 활용한 소도시 여행지 추천 서비스, ‘소소행’
* **팀명**: 12 - 내가그린 (NaegaGreen)
* **지도교수**: 황의원 교수님
* **과제 트랙**: 산학 트랙

### 💡 기획 의도
본 프로젝트는 파편화된 여행 정보와 관광의 수도권 편중 현상, 소상공인의 디지털 판로 부재 문제를 해결하기 위한 **'AI 기반 소도시 여행 추천 및 로컬 상생 올인원 플랫폼'**입니다.
기존의 단순 검색 방식을 넘어, **RAG(검색 증강 생성)** 기술을 도입하여 AI가 최신 관광 데이터를 근거로 사용자의 취향을 반영한 여행지를 추천하고, 이를 지역 소상공인의 상품 구매로 연결하여 지역 경제 활성화의 **선순환 구조를 구축** 합니다.

### 🔑 핵심 키워드
`RAG (Retrieval-Augmented Generation)` `LLM` `LBS (Location Based Service)` `Vector DB` `FastAPI`

<br>

## 🌟 주요 기능 및 특징 (Key Features)

### 1. RAG 및 LLM 기반 초개인화 AI 추천 시스템
단순한 키워드 매칭이 아닌, 사용자의 의도를 파악하고 LLM의 환각(Hallucination) 현상을 방지하는 RAG 기술을 적용했습니다.
* **Vector DB(FAISS)**: 한국관광공사 TourAPI의 최신 데이터를 임베딩하여 검색(Retrieval) 성능 최적화
* **Prompt Engineering**: 상황에 맞는 프롬프트를 통해 신뢰도 높은 추천 근거 제시

### 2. LBS(위치 기반 서비스)를 활용한 실시간 축제 매칭
GeoLocation과 Haversine 공식을 활용하여 사용자 현 위치 기준 반경 내(예: 10km) 진행 중인 축제와 행사를 실시간으로 필터링하여 제공합니다.
* **거리 계산 최적화**: DB 레벨에서의 연산을 통해 대량의 위치 데이터 처리 성능 확보

### 3. 지역 상생을 위한 로컬 커머스 통합
여행지 추천이 실제 지역 소비로 연결되도록 소상공인 전용 마켓 플레이스를 제공합니다.
* **특산물 마켓**: 상품 등록 및 관리 기능 제공
* **소통 채널**: 댓글 및 게시판 기반의 비동기 소통으로 정보 비대칭 해소

<br>

## 👨‍💻 팀원 및 역할 (Team Members)

| 이름 (학번) | 역할 | 담당 업무 (Role & Responsibility) |
| :---: | :---: | :--- |
| **김희서** | **Leader**<br>Backend | • 백엔드 API 개발 (FastAPI) 및 프롬프트 엔지니어링<br>• 비즈니스 로직 및 DB 스키마 설계<br>• 로컬 마켓 기능 개발 총괄 |
| **강다혜** | **Member**<br>Frontend | • 회원가입/로그인 API 구현 및 프론트엔드 연동<br>• 한국관광공사 TourAPI 데이터 파이프라인 구축<br>• 축제 정보 및 LBS(위치 기반) 기능 구현 |
| **윤가빈** | **Member**<br>AI / RAG | • AI/RAG 파이프라인 구축 (LangChain)<br>• 벡터 DB(FAISS) 최적화 및 여행지 추천 알고리즘 구현<br>• 반응형 챗봇 설계 |

<br>

## 📁 문서 구조 (Documents)
프로젝트 진행 과정에서 산출된 모든 문서는 본 레포지토리에서 관리됩니다.

<pre style="background-color: #1F3737; padding: 10px; border-radius: 5px; color: #ffffff;">
<code>
NaegaGreen
├── 📁 Final_Submission/      # [최종] 캡스톤 최종 산출물 모음
│    ├── Project_Poster.pdf   # 📄 프로젝트 전시용 포스터
│    ├── Final_Report.pdf     # 📕 최종 결과 보고서
│    ├── Presentation.pdf     # 🖥 최종 발표 자료 (PPT)
│    └── Demo_Video.mp4       # 🎬 서비스 시연 영상
│
├── 📁 1차보고서/              # [기획] 프로젝트 제안 및 기획 단계
│    ├── 12-내가그린-1차보고서.md
│    └── SW구성도.png
│
├── 📁 2차보고서/              # [설계] 중간 점검 및 설계 단계
│    ├── 2차 보고서.md
│    └── SW구조도.png
│
├── GroundRule.MD             # 팀 그라운드 룰
└── README.md                 # 프로젝트 문서 안내 (Current)
</code>
</pre>
