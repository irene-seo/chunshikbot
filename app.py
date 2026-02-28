import streamlit as st
import os
import base64
import random
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(
    page_title="춘식도락 봇 🐱",
    page_icon="🐱",
    layout="centered"
)

def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

chunsik_b64 = get_base64_image("chunsik.png.png")

st.markdown(f"""
<style>
    html, body, #root, .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stApp"],
    .main {{
        background-color: #FEE500 !important;
        background-image: url("data:image/png;base64,{chunsik_b64}") !important;
        background-repeat: repeat !important;
        background-size: 33.33vw !important;
        background-position: top left !important;
    }}
    .block-container {{
        background-color: white;
        border-radius: 24px;
        padding: 2rem 2rem 3rem 2rem;
        margin: 1.5rem 1rem 2rem 1rem !important;
        max-width: 95% !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }}
    .stButton > button {{
        background-color: #FEE500 !important;
        color: #3C1E1E !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: bold !important;
    }}
    .stButton > button:hover {{
        background-color: #F5DC00 !important;
    }}
    .stButton > button[kind="primary"] {{
        background-color: #3C1E1E !important;
        color: #FEE500 !important;
        font-size: 1.1rem !important;
        padding: 0.7rem !important;
    }}
    h1 {{
        text-align: center;
        color: #3C1E1E !important;
        white-space: nowrap !important;
        font-size: clamp(1.7rem, 6.5vw, 2.5rem) !important;
    }}
    h3 {{
        font-size: clamp(0.9rem, 3.5vw, 1.1rem) !important;
    }}
    h1 a, h2 a, h3 a {{
        display: none !important;
    }}
    hr {{
        border-color: #FEE500 !important;
    }}
    header[data-testid="stHeader"] {{
        display: none !important;
    }}
    [data-testid="stToolbar"] {{
        display: none !important;
    }}
</style>
""", unsafe_allow_html=True)

# 헤더
st.markdown("# 🐱 춘식도락 봇 🐱")
st.markdown("<p style='text-align:center; color:#3C1E1E; font-size:1.1rem;'>오늘 뭐 먹을지 춘식이가 골라줄게요!</p>", unsafe_allow_html=True)

st.divider()

# 기분/컨디션 선택
st.subheader("😊 오늘 컨디션이 어때요?")
mood = st.selectbox(
    "",
    [
        "보통이에요 😐",
        "피곤해요 😴",
        "스트레스 받아요 😤",
        "기분 좋아요 😄",
        "배고파 죽겠어요 🍽️",
        "입맛이 없어요 😞",
        "야근 예정이에요 💻",
        "다이어트 중이에요 🥗",
    ],
    label_visibility="collapsed"
)

# 팀원 랜덤 뽑기
st.subheader("🎲 오늘 메뉴 고를 사람 뽑기!")
st.caption("팀원 이름을 입력하면 춘식이가 랜덤으로 뽑아줄게요!")

members_input = st.text_input(
    "",
    placeholder="예: 아이린, 춘식, 라이언, 어피치",
    label_visibility="collapsed"
)

if st.button("🎲 뽑기!", use_container_width=False):
    if members_input.strip():
        members = [m.strip() for m in members_input.split(",") if m.strip()]
        if members:
            chosen = random.choice(members)
            st.success(f"🐱 오늘 메뉴는 **{chosen}**님이 고르세요냥~! 책임지는 거다냥 😸")
    else:
        st.warning("팀원 이름을 입력해주세요!")

# 기타 요청
other = st.text_input(
    "🗒️ 기타 요청사항 (선택)",
    placeholder="예: 고기 먹고 싶어요, 가볍게 먹고 싶어요..."
)

st.divider()

# 메뉴 입력
st.subheader("🍽️ 오늘의 메뉴 입력")
st.caption("엘리가오더에서 메뉴 정보를 입력해주세요!")

if "menus" not in st.session_state:
    st.session_state.menus = [
        {"name": "", "desc": "", "calories": "", "protein": ""}
    ]

for i, menu in enumerate(st.session_state.menus):
    with st.expander(
        f"메뉴 {i+1}" + (f" · {menu['name']}" if menu['name'] else " · 메뉴 입력"),
        expanded=True
    ):
        st.session_state.menus[i]["name"] = st.text_input(
            "메뉴 이름 *", value=menu["name"], key=f"name_{i}",
            placeholder="예: 된장찌개"
        )

        st.session_state.menus[i]["desc"] = st.text_area(
            "구성", value=menu["desc"], key=f"desc_{i}",
            placeholder="예: 된장찌개, 흰쌀밥, 계란말이, 김치",
            height=80
        )

        # 메뉴 사진 업로드
        uploaded = st.file_uploader(
            "📸 메뉴 사진 (선택)", type=["jpg", "jpeg", "png"],
            key=f"img_{i}"
        )
        if uploaded:
            st.image(uploaded, width=200)

        col1, col2 = st.columns(2)
        with col1:
            st.session_state.menus[i]["calories"] = st.text_input(
                "칼로리 (kcal)", value=menu["calories"], key=f"cal_{i}",
                placeholder="예: 650"
            )
        with col2:
            st.session_state.menus[i]["protein"] = st.text_input(
                "단백질 (g)", value=menu["protein"], key=f"protein_{i}",
                placeholder="예: 25"
            )

col1, col2 = st.columns(2)
with col1:
    if st.button("➕ 메뉴 추가", use_container_width=True):
        st.session_state.menus.append(
            {"name": "", "desc": "", "calories": "", "protein": ""}
        )
        st.rerun()
with col2:
    if len(st.session_state.menus) > 1:
        if st.button("➖ 마지막 메뉴 삭제", use_container_width=True):
            st.session_state.menus.pop()
            st.rerun()

st.divider()

# 추천 버튼
if st.button("🐱 춘식이한테 추천 받기!", type="primary", use_container_width=True):
    valid_menus = [m for m in st.session_state.menus if m["name"]]

    if not valid_menus:
        st.warning("메뉴를 최소 1개 이상 입력해주세요!")
    else:
        menu_text = ""
        for i, m in enumerate(valid_menus, 1):
            menu_text += f"{i}. {m['name']}\n"
            if m['desc']:
                menu_text += f"   구성: {m['desc']}\n"
            if m['calories']:
                menu_text += f"   칼로리: {m['calories']}kcal\n"
            if m['protein']:
                menu_text += f"   단백질: {m['protein']}g\n"

        prompt = f"""당신은 카카오 사내식당 '춘식도락'의 귀엽고 친근한 메뉴 추천 봇 '춘식이'입니다.
아래 정보를 바탕으로 오늘 점심 메뉴를 추천해주세요.

## 오늘의 메뉴:
{menu_text}

## 직원 상태:
- 오늘 컨디션: {mood}
- 기타 요청: {other if other else "없음"}

## 추천 규칙:
- 칼로리는 이미 앱에 나오니 칼로리 언급 최소화
- 단백질, 영양 밸런스 위주로 추천 이유 설명
- 컨디션에 딱 맞는 메뉴 골라주기
- 1순위 추천 + 2순위 추천 형식으로
- 춘식이 말투로 귀엽고 친근하게 (이모지 적절히)
- 마지막에 오늘 하루 응원 한마디!
- 반드시 한국어로만 답변! 영어 절대 사용 금지!
- 영어 단어 하나도 쓰지 말 것"""

        with st.spinner("🐱 춘식이가 고민 중이에요..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            result = response.choices[0].message.content

        st.balloons()
        st.success("🐱 춘식이의 추천!")
        st.markdown(result)
