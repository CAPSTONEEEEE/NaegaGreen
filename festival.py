import requests
import pandas as pd
from pandas import json_normalize
import mysql.connector

# ✅ MySQL 접속 정보 입력
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='ekgP0423@',   
    database='tour_db'
)
cursor = conn.cursor()

# ✅ TourAPI 설정
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
        'eventStartDate': '20250602',
        'eventEndDate': '20250610',
        'numOfRows': 100,
        'pageNo': page
    }

    response = requests.get(url, params=params)
    
    try:
        data = response.json()
        if isinstance(data, str):  # 응답이 JSON이 아니라 문자열일 경우
            print("응답이 문자열입니다. 종료합니다.")
            break
        items = data['response']['body']['items'].get('item', [])
    except Exception as e:
        print(f"오류 발생: {e}")
        break


    if not items:
        print("✅ 모든 데이터 수집 완료.")
        break

    df = json_normalize(items)

    # ✅ 행별로 MySQL 저장
    for _, row in df.iterrows():
        try:
            cursor.execute("""
                INSERT INTO festivals (contentid, title, addr1, eventstartdate, eventenddate, mapx, mapy)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                    title = VALUES(title),
                    addr1 = VALUES(addr1),
                    eventstartdate = VALUES(eventstartdate),
                    eventenddate = VALUES(eventenddate),
                    mapx = VALUES(mapx),
                    mapy = VALUES(mapy)
            """, (
                row.get('contentid'),
                row.get('title'),
                row.get('addr1'),
                row.get('eventstartdate'),
                row.get('eventenddate'),
                float(row.get('mapx', 0)),
                float(row.get('mapy', 0)),
            ))
        except Exception as insert_error:
            print(f"❌ 삽입 오류: {insert_error}")

    conn.commit()
    page += 1

# 마무리
cursor.close()
conn.close()
print(" MySQL 저장 완료")
#여기까지 데이터 받아오기

from geopy.distance import geodesic
import mysql.connector

def fetch_festivals_from_mysql():
    # ✅ MySQL 연결 정보
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='ekgP0423@', 
        database='tour_db'
    )
    cursor = conn.cursor(dictionary=True)  # 딕셔너리 모드로 가져오기

    cursor.execute("SELECT title, addr1, eventstartdate, eventenddate, mapy AS lat, mapx AS lng FROM festivals")
    festivals = cursor.fetchall()

    cursor.close()
    conn.close()
    return festivals

def main():
    print("🎯 내 위치 기반 축제 검색기 (MySQL)")
    lat = float(input("📍 현재 위도 입력: "))
    lng = float(input("📍 현재 경도 입력: "))

    festivals = fetch_festivals_from_mysql()

    nearby = []
    for f in festivals:
        if f["lat"] is None or f["lng"] is None:
            continue  # 좌표 없는 데이터는 제외
        dist = geodesic((lat, lng), (f["lat"], f["lng"])).km
        if dist <= 10:
            f["distance_km"] = round(dist, 2)
            nearby.append(f)

    if not nearby:
        print("❌ 10km 이내에 축제가 없습니다.")
        return

    print(f"\n✅ 내 위치 기준 10km 이내 축제 {len(nearby)}건:")
    for f in sorted(nearby, key=lambda x: x["distance_km"]):
        print(f"\n🎉 {f['title']}")
        print(f"   📍 장소: {f['addr1']}")
        print(f"   📅 기간: {f['eventstartdate']} ~ {f['eventenddate']}")
        print(f"   🧭 거리: {f['distance_km']}km")

if __name__ == "__main__":
    main()
