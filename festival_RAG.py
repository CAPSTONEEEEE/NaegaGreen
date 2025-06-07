# 🔧 설치 (최초 1회만)
!pip install openai pandas requests --quiet

# ✅ 1. 패키지 임포트
import requests
import sqlite3
import pandas as pd
from pandas import json_normalize
from openai import OpenAI

# ✅ 2. OpenAI 클라이언트 생성 (GPT 호출용)
client = OpenAI(api_key="")  # ⚠️ 본인의 키로 교체하세요!

# ✅ 3. SQLite 연결 및 테이블 생성
conn = sqlite3.connect("festivals.db")
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS festivals (
    contentid TEXT PRIMARY KEY,
    title TEXT,
    addr1 TEXT,
    eventstartdate TEXT,
    eventenddate TEXT,
    mapx REAL,
    mapy REAL
)
''')
conn.commit()

# ✅ 4. TourAPI에서 축제 데이터 수집
def fetch_and_store_festivals():
    servicekey = 'sNi2tlEh0+B9o0hig8eIQmwPR+tcLeZ46hmkrPWWk2vXNhWFvSpDizqGZy1CtB1tRV4Krz53LU3OHgKvtyihHg=='
    url = 'http://apis.data.go.kr/B551011/KorService2/searchFestival2'

    page = 1
    while True:
        print(f"{page} 페이지 수집 중...")
        params = {
            'MobileOS': 'ETC',
            'MobileApp': 'Soso',
            'serviceKey': servicekey,
            '_type': 'json',
            'eventStartDate': '20250601',
            'eventEndDate': '20250831',
            'numOfRows': 100,
            'pageNo': page
        }

        response = requests.get(url, params=params)
        try:
            data = response.json()
        except ValueError:
            print("❌ JSON 파싱 실패:\n", response.text)
            break

        if isinstance(data, str):
            print("❌ 응답이 문자열입니다:\n", data)
            break

        try:
            items = data['response']['body']['items'].get('item', [])
        except Exception as e:
            print("❌ 응답 구조 오류:", e)
            print("전체 응답:\n", data)
            break

        if not items:
            print("✅ 데이터 수집 완료.")
            break

        df = json_normalize(items)

        for _, row in df.iterrows():
            try:
                cursor.execute("""
                    INSERT OR REPLACE INTO festivals 
                    (contentid, title, addr1, eventstartdate, eventenddate, mapx, mapy)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    str(row.get('contentid')),
                    row.get('title'),
                    row.get('addr1'),
                    row.get('eventstartdate'),
                    row.get('eventenddate'),
                    float(row.get('mapx', 0)) if row.get('mapx') else None,
                    float(row.get('mapy', 0)) if row.get('mapy') else None,
                ))
            except Exception as e:
                print(f"❌ 저장 오류: {e}")

        conn.commit()
        page += 1

# ✅ 5. GPT로 관련 키워드 확장 (RAG 방식의 핵심)
def get_related_keywords(keyword):
    prompt = f"""
여행 관련 축제를 검색하려고 해. '{keyword}'과(와) 의미상 관련된 키워드를 5~7개 정도 추천해줘.
한글 단어만, 쉼표(,)로 구분해서 출력해줘. 예를 들어 '음악'을 입력하면 '재즈, 밴드, 콘서트, EDM, 라이브' 등으로 출력해줘.
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "여행 축제 키워드 추천 도우미입니다."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=100
    )
    raw = response.choices[0].message.content
    return [k.strip() for k in raw.split(",")]

# ✅ 6. SQLite에서 키워드 기반으로 축제 검색
def search_festivals_by_keywords(keywords):
    placeholders = " OR ".join(["title LIKE ? OR addr1 LIKE ?" for _ in keywords])
    query = f"SELECT title, addr1, eventstartdate, eventenddate FROM festivals WHERE {placeholders}"
    params = []
    for kw in keywords:
        like_kw = f"%{kw}%"
        params.extend([like_kw, like_kw])
    cursor.execute(query, tuple(params))
    return cursor.fetchall()

# ✅ 7. 메인 실행 (지역 기반 추가)
def main():
    # 축제 데이터 수집 (이미 했으면 생략 가능)
    fetch_and_store_festivals()

    keyword = input("\n📌 여행 목적 키워드를 입력하세요 (예: 음악, 전통, 불꽃): ")
    region = input("📍 여행 지역을 입력하세요 (예: 전주, 강릉, 부산 등): ")

    # GPT로 키워드 확장
    related_keywords = get_related_keywords(keyword)
    print("\n🔍 확장된 키워드:", related_keywords)

    # 지역 키워드도 함께 검색 조건에 추가
    all_keywords = related_keywords + [region]

    results = search_festivals_by_keywords(all_keywords)

    if results:
        print(f"\n✅ '{keyword}' 및 '{region}' 관련 축제 목록:")
        for row in results:
            print(f"\n🎉 {row[0]}")
            print(f"📍 장소: {row[1]}")
            print(f"📅 일정: {row[2]} ~ {row[3]}")
    else:
        print(f"\n❌ '{keyword}' 또는 '{region}' 관련 축제를 찾을 수 없습니다.")

    # 마무리
    cursor.close()
    conn.close()

# 실행
main()
