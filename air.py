import streamlit as st

# --- 확률 계산 함수 (이전에 정의한 함수와 동일) ---
def calculate_flight_probabilities(total_flights, delayed_flights, cancelled_flights, accident_flights):
    """
    항공 운항의 지연율, 결항률, 사고율을 계산합니다.

    Args:
        total_flights (int): 총 운항 횟수.
        delayed_flights (int): 지연된 운항 횟수.
        cancelled_flights (int): 결항된 운항 횟수.
        accident_flights (int): 사고가 발생한 운항 횟수.

    Returns:
        dict: 각 확률(지연율, 결항률, 사고율)을 담은 딕셔너리.
              총 운항 횟수가 0인 경우 모든 확률은 0으로 처리됩니다.
    """
    probabilities = {
        "delay_rate": 0.0,
        "cancellation_rate": 0.0,
        "accident_rate": 0.0
    }

    if total_flights <= 0:
        # Streamlit에서는 print 대신 st.warning을 사용하는 것이 좋습니다.
        st.warning("총 운항 횟수가 0이거나 음수이므로 모든 확률은 0으로 계산됩니다.")
        return probabilities

    probabilities["delay_rate"] = delayed_flights / total_flights
    probabilities["cancellation_rate"] = cancelled_flights / total_flights
    probabilities["accident_rate"] = accident_flights / total_flights

    return probabilities

# --- Streamlit 애플리케이션 시작 ---
st.set_page_config(
    page_title="항공 운항 위험 확률 대시보드",
    layout="centered", # wide 또는 centered 선택 가능
)

st.title("✈️ 항공 운항 위험 확률 분석")
st.markdown("항공편의 **지연율, 결항률, 사고율**을 계산하여 보여줍니다.")

# --- 사용자 입력 섹션 ---
st.header("데이터 입력")
st.markdown("각 항목의 횟수를 입력해주세요.")

col1, col2 = st.columns(2)

with col1:
    total_flights_input = st.number_input(
        "**총 운항 횟수**",
        min_value=0,
        value=10000, # 기본값 설정
        step=1,
        help="특정 기간 동안 운항된 총 비행 횟수입니다."
    )
with col2:
    delayed_flights_input = st.number_input(
        "**지연된 운항 횟수**",
        min_value=0,
        value=1500, # 기본값 설정
        step=1,
        help="총 운항 횟수 중 지연된 비행 횟수입니다."
    )

col3, col4 = st.columns(2)

with col3:
    cancelled_flights_input = st.number_input(
        "**결항된 운항 횟수**",
        min_value=0,
        value=200, # 기본값 설정
        step=1,
        help="총 운항 횟수 중 결항된 비행 횟수입니다."
    )
with col4:
    accident_flights_input = st.number_input(
        "**사고 발생 횟수**",
        min_value=0,
        value=1, # 기본값 설정
        step=1,
        help="총 운항 횟수 중 사고가 발생한 횟수입니다. (매우 드묾)"
    )

# 입력값 유효성 검사 (지연/결항/사고 횟수가 총 운항 횟수를 초과하지 않도록)
if (delayed_flights_input > total_flights_input or
    cancelled_flights_input > total_flights_input or
    accident_flights_input > total_flights_input):
    st.error("지연, 결항 또는 사고 횟수는 총 운항 횟수를 초과할 수 없습니다. 값을 다시 확인해주세요.")
else:
    # --- 확률 계산 및 결과 표시 섹션 ---
    st.header("분석 결과")
    st.markdown("입력된 데이터를 기반으로 계산된 확률입니다.")

    flight_probabilities = calculate_flight_probabilities(
        total_flights_input,
        delayed_flights_input,
        cancelled_flights_input,
        accident_flights_input
    )

    if total_flights_input > 0:
        # 결과 표 형식으로 보여주기
        st.subheader("확률 요약")
        st.table({
            "항목": ["지연율", "결항률", "사고율"],
            "확률 (소수점)": [
                f"{flight_probabilities['delay_rate']:.4f}",
                f"{flight_probabilities['cancellation_rate']:.4f}",
                f"{flight_probabilities['accident_rate']:.7f}" # 사고율은 더 정밀하게
            ],
            "확률 (%)": [
                f"{flight_probabilities['delay_rate'] * 100:.2f}%",
                f"{flight_probabilities['cancellation_rate'] * 100:.2f}%",
                f"{flight_probabilities['accident_rate'] * 100:.5f}%" # 사고율은 더 정밀하게
            ]
        })

        st.markdown(
            """
            ---
            **참고**: 사고율은 매우 낮으므로 소수점 자릿수를 더 많이 표시했습니다.
            실제 항공 데이터는 다양한 변수(날씨, 항공사, 공항, 기간 등)에 따라 크게 달라질 수 있습니다.
            """
        )

# --- 푸터 ---
st.sidebar.markdown("### 정보")
st.sidebar.info("이 대시보드는 Streamlit으로 구축되었습니다.")
st.sidebar.markdown(f"현재 시간: {st.session_state.get('current_time', '정보 없음')}")

# 페이지 로드 시 현재 시간 저장 (선택 사항)
if 'current_time' not in st.session_state:
    import datetime
    st.session_state['current_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S KST")
