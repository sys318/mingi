import streamlit as st
import random

# 페이지 기본 설정
st.set_page_config(page_title="오늘 저녁 뭐 먹지?", page_icon="🍽️", layout="centered")

# CSS 스타일링 (귀여운 디자인 적용)
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #ff6b6b;
        color: white;
        font-size: 1.2rem;
        font-weight: bold;
        border-radius: 12px;
        padding: 0.6rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #ff5252;
        color: white;
    }
    .result-box {
        background-color: #fff8f0;
        border-radius: 16px;
        padding: 25px;
        text-align: center;
        margin-top: 20px;
        border: 2px solid #ffeae8;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🍽️ 오늘 저녁 뭐 먹지?")
st.write("원하는 조건(음식 종류, 칼로리)을 선택하고 추천 버튼을 눌러보세요!")

# 메뉴 데이터베이스
foods = [
    # 한식 - 칼로리 높음
    {"name": "삼겹살", "category": "한식", "calorie": "칼로리 높음 🔥", "emoji": "🥓"},
    {"name": "김치찌개", "category": "한식", "calorie": "칼로리 높음 🔥", "emoji": "🥘"},
    {"name": "치킨", "category": "한식", "calorie": "칼로리 높음 🔥", "emoji": "🍗"},
    {"name": "떡볶이", "category": "한식", "calorie": "칼로리 높음 🔥", "emoji": "🍢"},
    # 한식 - 칼로리 낮음
    {"name": "비빔밥", "category": "한식", "calorie": "칼로리 낮음 🥗", "emoji": "🥗"},
    {"name": "콩나물국밥", "category": "한식", "calorie": "칼로리 낮음 🥗", "emoji": "🍲"},
    {"name": "두부김치", "category": "한식", "calorie": "칼로리 낮음 🥗", "emoji": "🧈"},

    # 중식 - 칼로리 높음
    {"name": "짜장면", "category": "중식", "calorie": "칼로리 높음 🔥", "emoji": "🍜"},
    {"name": "탕수육", "category": "중식", "calorie": "칼로리 높음 🔥", "emoji": "🥩"},
    {"name": "마라탕", "category": "중식", "calorie": "칼로리 높음 🔥", "emoji": "🍲"},
    # 중식 - 칼로리 낮음
    {"name": "양상추 쇠고기 볶음", "category": "중식", "calorie": "칼로리 낮음 🥗", "emoji": "🥬"},
    {"name": "토마토 달걀볶음", "category": "중식", "calorie": "칼로리 낮음 🥗", "emoji": "🍅"},

    # 일식 - 칼로리 높음
    {"name": "돈카츠", "category": "일식", "calorie": "칼로리 높음 🔥", "emoji": "🥩"},
    {"name": "라멘", "category": "일식", "calorie": "칼로리 높음 🔥", "emoji": "🍜"},
    {"name": "야키소바", "category": "일식", "calorie": "칼로리 높음 🔥", "emoji": "🍝"},
    # 일식 - 칼로리 낮음
    {"name": "초밥", "category": "일식", "calorie": "칼로리 낮음 🥗", "emoji": "🍣"},
    {"name": "회덮밥", "category": "일식", "calorie": "낮음 🥗", "emoji": "🥣"},
    {"name": "메밀소바", "category": "일식", "calorie": "칼로리 낮음 🥗", "emoji": "🥢"}
]

# 카테고리 선택 UI (라디오 버튼 / 세렉트박스)
col1, col2 = st.columns(2)

with col1:
    selected_category = st.radio("음식 종류", ["전체", "한식", "중식", "일식"])

with col2:
    selected_calorie = st.radio("칼로리", ["전체", "칼로리 높음 🔥", "칼로리 낮음 🥗"])

# 추천 버튼
if st.button("🎲 메뉴 추천받기!"):
    # 필터링 로직
    filtered = [
        f for f in foods
        if (selected_category == "전체" or f["category"] == selected_category) and
           (selected_calorie == "전체" or f["calorie"] == selected_calorie)
    ]

    if not filtered:
        st.warning("😅 선택하신 조건에 맞는 메뉴가 없어요! 다른 조건을 선택해보세요.")
    else:
        picked = random.choice(filtered)
        
        # 결과 출력 카드
        st.markdown(f"""
            <div class="result-box">
                <div style="font-size: 5rem;">{picked['emoji']}</div>
                <h2 style="margin: 10px 0;">{picked['name']}</h2>
                <p style="color: #666; font-size: 0.9rem;">#{picked['category']} #{picked['calorie']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.balloons() # 성공 축하 애니메이션 효과!
