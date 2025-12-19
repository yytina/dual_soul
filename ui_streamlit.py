import streamlit as st
import datetime
from korean_lunar_calendar import KoreanLunarCalendar
from utils import calculate_tarot_number
from tarot_data import TAROT_IMAGES

# 1. 페이지 세팅
st.set_page_config(page_title="Dual Soul", layout="centered")

st.title("🌗 당신의 두 가지 영혼")
st.write("양력 생일과 음력 생일에 숨겨진 당신의 자아를 확인하세요.")

# 2. (가상) 계산된 카드 번호 (실제 로직에서는 생일 계산 결과가 들어감)
solar_card_number = 4  # 예: 황제 (Emperor)
lunar_card_number = 9  # 예: 은둔자 (Hermit)

# 사용자 입력 받기

# 1. 최소 날짜 설정 (1950년 1월 1일)
min_date = datetime.date(1950, 1, 1)

# 2. 최대 날짜 설정 (오늘) - 만 1살 이상이 사용
max_date = datetime.date.today()- datetime.timedelta(days=365)

birth_date = st.date_input(
    "당신의 양력 생일을 선택하세요",
    value=None,           # 초기값 (None이면 사용자가 입력하기 전까지 비어있음)
    min_value=min_date,   # 핵심: 달력의 시작 연도를 1950년으로 설정
    max_value=max_date    # 옵션: 오늘 날짜 이후는 선택 못하게 막음
)
if birth_date is not None:
    st.write(f"선택한 생일: {birth_date}")

if birth_date:
    # 1. 양력(Solar) 번호 계산
    solar_card_number = calculate_tarot_number(birth_date.year, birth_date.month, birth_date.day)
    # 2. 음력(Lunar) 변환 및 번호 계산
    calendar = KoreanLunarCalendar()
    calendar.setSolarDate(birth_date.year, birth_date.month, birth_date.day)
    
    # 음력 날짜 가져오기 (문자열 형태: '1995-09-01')
    lunar_iso = calendar.LunarIsoFormat() 
    l_year, l_month, l_day = map(int, lunar_iso.split('-'))
    
    lunar_card_number = calculate_tarot_number(l_year, l_month, l_day)

    # 3. 결과 보여주기
    st.write(f"🌞 당신의 양력 카드는 **{solar_card_number}번** 입니다.")
    st.write(f"🌛 당신의 음력 카드는 **{lunar_card_number}번** 입니다.")

# 테스트용 이미지 URL (위키미디어 퍼블릭 도메인 이미지)
# 실제 프로젝트에선 로컬 파일 경로(예: "./images/4.jpg")를 쓰세요.
# img_url_base = "https://upload.wikimedia.org/wikipedia/commons/"
# card_urls = {
#     4: img_url_base + "c/c3/RWS_Tarot_04_Emperor.jpg",
#     9: img_url_base + "4/4d/RWS_Tarot_09_Hermit.jpg"
# }

# 3. 화면 분할 (컬럼 2개 생성)
col1, col2 = st.columns(2)

# --- 양력(Solar) 섹션 ---
with col1:
    if solar_card_number:
        st.subheader("🌞 Outer Self")
        st.caption(f"양력 생일 카드: {solar_card_number}번")
        
        # 이미지 출력 (use_column_width=True로 하면 컬럼 너비에 딱 맞게 들어갑니다)
        st.image(TAROT_IMAGES[solar_card_number], caption="The Emperor", width='stretch')
        
        st.info("사회적 가면, 리더십, 체계") # 키워드 예시
    else:
        # [초기 상태] 입력 전에는 카드 뒷면 이미지를 보여줍니다.
        # 무료 이미지 사이트나 가지고 계신 카드 뒷면 이미지 경로를 넣으세요.
        st.image("https://upload.wikimedia.org/wikipedia/commons/5/53/RWS_Tarot_16_Tower.jpg", caption="생일을 선택하면 카드가 공개됩니다.", width=300) 
        # (위 링크는 예시입니다. 실제로는 카드 뒷면 이미지를 사용하세요)
        st.info("👈 왼쪽(혹은 위)에서 생년월일을 선택해주세요.")

# --- 음력(Lunar) 섹션 ---
with col2:
    st.subheader("🌛 Inner Self")
    st.caption(f"음력 생일 카드: {lunar_card_number}번")
    
    st.image(TAROT_IMAGES[lunar_card_number], caption="The Hermit", width='stretch')
    
    st.success("내면의 지혜, 고독, 성찰") # 키워드 예시

# 4. 하단 설명
st.divider()
st.markdown("### 🔮 AI의 해석")
st.write("""
겉으로는 **황제**처럼 강한 리더십을 보이며 주변을 통제하려 하지만, 
사실 내면 깊은 곳에는 **은둔자**처럼 혼자만의 동굴에서 쉬고 싶어 하는 욕구가 강하군요.
이 두 자아가 충돌할 때 스트레스를 받을 수 있습니다.
""")