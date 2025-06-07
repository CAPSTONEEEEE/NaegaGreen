!pip install ipywidgets --quiet

import openai
import ipywidgets as widgets
from IPython.display import display
from datetime import datetime

# ✅ OpenAI API 설정
client = openai.OpenAI(api_key="")  # <-- OpenAI API 키를 입력 !!!

# ✅ 날짜 → 계절 변환 함수
def date_to_season(date_obj):
    month = date_obj.month
    if month in [3, 4, 5]:
        return "봄"
    elif month in [6, 7, 8]:
        return "여름"
    elif month in [9, 10, 11]:
        return "가을"
    else:
        return "겨울"

# ✅ GPT 프롬프트 생성 함수
def build_prompt(info):
    prompt = f"""
당신은 사용자에게 딱 맞는 여행지를 추천해주는 똑똑한 여행 플래너입니다.
아래 사용자의 정보를 참고하여 지역 기반 여행지와 활동을 추천해주세요.

📅 여행 시기: {info['date']} ({info['season']})
📍 출발지: {info['start_location']} (선호 거리: {info['distance']}km 이내)
🚗 이동 수단: {info['transport']}
🎯 여행 목적: {info['purpose']}
👥 동반자: {info['companion']}
✈️ 여행 스타일: {info['style_type']} - {info['style_detail']}

위 조건을 반영하여 대한민국 소도시 중에서 2~3곳을 추천해주시고, 각 도시에서 할 수 있는 대표적인 활동, 맛집, 사진 스팟 등을 함께 제안해주세요.
"""
    return prompt.strip()

# ✅ GPT 호출 함수
def chat_with_gpt(prompt, model="gpt-4"):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful and friendly Korean travel assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1000
    )
    return response.choices[0].message.content.strip()

# ✅ 위젯 생성
date_picker = widgets.DatePicker(description="📅 여행 날짜")
start_location = widgets.Text(description="출발 지역")

# ✅ IntSlider로 거리 조절 (10~500, 10단위)
distance = widgets.IntSlider(
    description="이동 거리(km)",
    value=100,
    min=10,
    max=500,
    step=10,
    style={'description_width': 'initial'},
    continuous_update=False
)

transport = widgets.RadioButtons(
    options=["자가용", "고속버스", "기차", "미정"],
    description="🚗 이동 수단",
)

purpose = widgets.RadioButtons(
    options=[
        "마음 정리, 재충전",
        "특별한 사람과 추억",
        "가족과 즐거운 시간",
        "친구들과 액티비티",
        "SNS용 사진",
        "지역 먹거리 체험",
        "문화/역사 경험"
    ],
    description="🎯 목적",
    layout={'width': 'max-content'}
)

companion = widgets.RadioButtons(
    options=["혼자", "연인", "가족", "친구"],
    description="👥 동반자"
)

style = widgets.Dropdown(
    options=["힐링 여행", "액티비티 여행", "관광 명소 여행"],
    description="✈️ 스타일"
)

# 세부 스타일 매핑
style_detail_map = {
    "힐링 여행": ["자연 속", "도심 속"],
    "액티비티 여행": ["수상 레저", "산악 등산", "자전거/ATV", "이색 체험", "실내 체험"],
    "관광 명소 여행": ["역사 유적지", "문화예술 공간", "도시 탐방", "자연 명소"]
}
style_detail = widgets.Dropdown(description="세부 유형")

# 스타일 변경 시 세부 스타일 업데이트
def update_style_detail(*args):
    style_detail.options = style_detail_map.get(style.value, [])

style.observe(update_style_detail, 'value')
update_style_detail()

# ✅ 실행 버튼 정의
submit_button = widgets.Button(description="🚀 여행지 추천받기", button_style='success')
output = widgets.Output()

def on_submit(b):
    with output:
        output.clear_output()
        if not date_picker.value:
            print("❗ 날짜를 선택해주세요.")
            return

        season = date_to_season(date_picker.value)
        user_info = {
            "date": str(date_picker.value),
            "season": season,
            "start_location": start_location.value,
            "distance": distance.value,
            "transport": transport.value,
            "purpose": purpose.value,
            "companion": companion.value,
            "style_type": style.value,
            "style_detail": style_detail.value
        }

        prompt = build_prompt(user_info)
        print(f"📅 여행 시기: {user_info['date']} ({season})")
        print(f"📍 출발지: {user_info['start_location']} (선호 거리: {user_info['distance']}km 이내)")
        print(f"🚗 이동 수단: {user_info['transport']}")
        print(f"🎯 여행 목적: {user_info['purpose']}")
        print(f"👥 동반자: {user_info['companion']}")
        print(f"✈️ 여행 스타일: {user_info['style_type']} - {user_info['style_detail']}")
        print("\n💬 추천 결과:\n")
        print(chat_with_gpt(prompt))

submit_button.on_click(on_submit)

# ✅ 위젯 출력
display(
    date_picker, start_location, distance, transport,
    purpose, companion, style, style_detail,
    submit_button, output
)
