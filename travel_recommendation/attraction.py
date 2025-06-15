import openai
import requests
import pandas as pd

# ✅ OpenAI 키 설정
openai.api_key = ""    # ⚠️ 본인의 OpenAI 키로 교체하세요!

# ✅ GPT로 연관 키워드 확장
def get_related_keywords(keyword):
    try:
        prompt = f"""
        '{keyword}'라는 여행 목적 키워드와 관련된 유사 키워드를 5개 추천해주세요.
        단어만 콤마로 구분해서 출력하세요. 예: 휴식, 자연, 산책, 명상, 힐링
        """
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        raw = response.choices[0].message.content
        return [k.strip() for k in raw.split(",") if k.strip()]
    except Exception as e:
        print(f"❌ GPT 키워드 확장 실패: {e}")
        return [keyword]

# ✅ GPT로 간단한 소개 생성
def generate_overview(title):
    try:
        prompt = f"'{title}'라는 장소에 대해 간단한 관광 소개글을 한글로 2~3문장으로 작성해줘."
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"(GPT 소개 생성 실패: {e})"

# ✅ 관광지 검색 함수 (지역 + 키워드 포함 조건)
def search_places(keywords, region, max_results=10):
    url = "http://apis.data.go.kr/B551011/KorService2/searchKeyword2"
    servicekey = ''    # ⚠️ 본인의 TourAPI 키로 교체하세요!
    
    collected = []
    for keyword in keywords:
        for page in range(1, 6):  # 최대 5페이지 조회
            params = {
                'MobileOS': 'ETC',
                'MobileApp': 'Soso',
                'serviceKey': servicekey,
                '_type': 'json',
                'numOfRows': 10,
                'pageNo': page,
                'keyword': keyword
            }

            try:
                response = requests.get(url, params=params)
                data = response.json()
                items = data['response']['body']['items']
                if isinstance(items, str):  # 빈 문자열
                    break
                results = items.get('item', [])
                for item in results:
                    title = item.get('title', '')
                    addr1 = item.get('addr1', '')
                    if region in addr1:  # 지역명 포함 여부 확인
                        collected.append({'title': title, 'addr1': addr1})
                        if len(collected) >= max_results:
                            return collected
            except Exception as e:
                print(f"❌ 관광지 API 오류: {e}")
                break
    return collected

# ✅ 메인 실행 함수
def main():
    print("🔍 지역 맞춤형 관광지 추천")

    keyword = input("📌 여행 목적 또는 키워드를 입력하세요 (예: 재충전, 문화 체험 등): ").strip()
    region = input("🌍 여행하고 싶은 지역을 입력하세요 (예: 전주, 부산, 강릉 등): ").strip()

    related = get_related_keywords(keyword)
    print("\n🔎 확장된 키워드:", related)

    places = search_places(related, region, max_results=10)

    if not places:
        print(f"❌ '{region}' 지역에 '{keyword}' 관련 관광지를 찾을 수 없습니다.")
        return

    for i, place in enumerate(places, 1):
        overview = generate_overview(place['title'])
        print(f"\n{i}. 📍 {place['title']}")
        print(f"🗺️ 주소: {place['addr1']}")
        print(f"📝 소개: {overview}")

# ✅ 실행
main()
