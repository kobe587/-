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
        print("경고: 총 운항 횟수가 0이거나 음수이므로 모든 확률은 0으로 계산됩니다.")
        return probabilities

    probabilities["delay_rate"] = delayed_flights / total_flights
    probabilities["cancellation_rate"] = cancelled_flights / total_flights
    probabilities["accident_rate"] = accident_flights / total_flights

    return probabilities

# --- 예시 데이터 ---
# 실제 데이터는 항공사, 공항, 기간 등에 따라 크게 달라질 수 있습니다.
# 이 값들은 예시를 위한 임의의 숫자입니다.

total_flights_data = 10000  # 예를 들어, 한 해 동안 10,000편의 비행
delayed_flights_data = 1500  # 그 중 1,500편이 지연
cancelled_flights_data = 200   # 200편이 결항
accident_flights_data = 1      # 1건의 사고 발생 (다행히 매우 드물죠!)

# --- 확률 계산 ---
flight_probabilities = calculate_flight_probabilities(
    total_flights_data,
    delayed_flights_data,
    cancelled_flights_data,
    accident_flights_data
)

# --- 결과 출력 ---
print(f"총 운항 횟수: {total_flights_data:,}편\n") # 숫자에 콤마 추가

print(f"**항공기 지연율**: {flight_probabilities['delay_rate']:.4f} "
      f"({flight_probabilities['delay_rate'] * 100:.2f}%)")
print(f"**항공기 결항률**: {flight_probabilities['cancellation_rate']:.4f} "
      f"({flight_probabilities['cancellation_rate'] * 100:.2f}%)")
print(f"**항공기 사고율**: {flight_probabilities['accident_rate']:.7f} "
      f"({flight_probabilities['accident_rate'] * 100:.5f}%)") # 사고율은 매우 작으므로 더 많은 소수점 표시
