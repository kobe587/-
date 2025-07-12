import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt

def find_intersection(base_exp, base_log, initial_guess):
    """
    지수함수 y = base_exp^x 와 로그함수 y = log_base_log(x) 의 교점을 찾습니다.

    Args:
        base_exp (float): 지수함수의 밑 (a^x 에서 a).
        base_log (float): 로그함수의 밑 (log_b(x) 에서 b).
        initial_guess (float or list of floats): 교점을 찾기 위한 초기 추정값.
                                                 교점이 여러 개일 수 있으므로,
                                                 다양한 초기 추정값을 시도하여
                                                 모든 교점을 찾을 수 있습니다.

    Returns:
        numpy.ndarray: 찾은 교점의 x 좌표 배열.
    """

    # 두 함수의 차이를 정의하는 함수
    # f(x) = base_exp^x
    # g(x) = log_base_log(x)
    # 우리는 f(x) - g(x) = 0 을 만족하는 x를 찾는다.
    def equation_to_solve(x):
        if x <= 0:
            # 로그 함수의 진수 조건: x는 양수여야 함
            # fsolve가 음수나 0을 시도할 경우, 매우 큰 값 또는 np.inf를 반환하여
            # 해당 영역에서 해가 없음을 '알려줌'
            return np.inf
        return base_exp**x - np.log(x) / np.log(base_log)

    # fsolve를 사용하여 방정식의 근을 찾음
    # fsolve는 배열 형태의 초기 추정값을 받을 수 있지만,
    # 각 초기 추정값에 대해 하나의 해를 찾으려고 시도합니다.
    # 여러 개의 교점을 찾으려면 여러 번 호출해야 할 수 있습니다.
    try:
        if isinstance(initial_guess, (int, float)):
            # 단일 초기 추정값인 경우
            roots = fsolve(equation_to_solve, initial_guess)
        elif isinstance(initial_guess, (list, np.ndarray)):
            # 여러 초기 추정값인 경우, 각각에 대해 fsolve를 실행
            roots = []
            for guess in initial_guess:
                root, info, ier, msg = fsolve(equation_to_solve, guess, full_output=True)
                # ier == 1 이면 성공적으로 해를 찾았다는 의미
                if ier == 1 and root[0] > 0: # 진수 조건 만족
                    roots.append(root[0])
            roots = np.array(roots)
            # 중복된 해 제거 (fsolve는 같은 해를 여러 번 찾을 수 있음)
            roots = np.unique(np.round(roots, decimals=6)) # 소수점 6자리까지 반올림 후 중복 제거

    except ValueError as e:
        print(f"Error during calculation: {e}. Check if initial_guess is positive and bases are valid.")
        return np.array([])
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return np.array([])

    return roots

# --- 예시 사용 ---

# 1. 일반적인 경우 (교점 1개 또는 2개)
print("--- 예시 1: y = 2^x, y = log_2(x) ---")
# y=x 대칭인 경우 교점은 y=x 위에 존재할 가능성이 높으므로 x=1 주변에서 찾아봄
intersection_points_1 = find_intersection(base_exp=2, base_log=2, initial_guess=[0.5, 1.0, 2.0])
print(f"교점의 x 좌표: {intersection_points_1}")
# y=2^x와 y=log_2(x)는 y=x 대칭이며, (2,2)와 (4,4)에서 만납니다.
# fsolve는 초기값에 따라 (2,2) 또는 (4,4) 중 하나를 찾을 수 있습니다.
# 위 코드는 여러 초기값으로 시도하여 둘 다 찾도록 했습니다.

print("\n--- 예시 2: y = 1.5^x, y = log_e(x) (자연로그) ---")
# 이 경우는 교점이 하나만 있을 가능성이 높습니다.
intersection_points_2 = find_intersection(base_exp=1.5, base_log=np.e, initial_guess=1.0)
print(f"교점의 x 좌표: {intersection_points_2}")

print("\n--- 예시 3: y = 0.5^x, y = log_0.5(x) (감소 함수) ---")
# 감소 함수는 교점이 하나만 있습니다.
intersection_points_3 = find_intersection(base_exp=0.5, base_log=0.5, initial_guess=1.0)
print(f"교점의 x 좌표: {intersection_points_3}")

# --- 그래프로 교점 확인 (선택 사항) ---
def plot_functions_and_intersections(base_exp, base_log, intersections):
    x_vals = np.linspace(0.1, 5, 400) # x > 0
    y_exp = base_exp**x_vals
    y_log = np.log(x_vals) / np.log(base_log) # log_b(x) = ln(x) / ln(b)

    plt.figure(figsize=(8, 6))
    plt.plot(x_vals, y_exp, label=f'$y = {base_exp}^{{x}}$', color='blue')
    plt.plot(x_vals, y_log, label=f'$y = \log_{{{base_log:.2f}}}(x)$', color='red')
    plt.plot(x_vals, x_vals, label='$y = x$', linestyle='--', color='gray', alpha=0.7) # y=x 대칭 확인용

    for x_intersect in intersections:
        y_intersect_exp = base_exp**x_intersect
        plt.scatter(x_intersect, y_intersect_exp, color='green', zorder=5, s=100,
                    label=f'교점: ({x_intersect:.2f}, {y_intersect_exp:.2f})' if x_intersect == intersections[0] else '')
        plt.text(x_intersect + 0.1, y_intersect_exp,
                 f'({x_intersect:.2f}, {y_intersect_exp:.2f})', fontsize=9, color='green')


    plt.title(f'Intersection of $y = {base_exp}^{{x}}$ and $y = \log_{{{base_log:.2f}}}(x)$')
    plt.xlabel('$x$')
    plt.ylabel('$y$')
    plt.legend()
    plt.grid(True)
    plt.ylim(-2, 6) # 적절한 y축 범위 설정
    plt.axvline(0, color='black', linewidth=0.5)
    plt.axhline(0, color='black', linewidth=0.5)
    plt.show()

# 그래프 예시 실행
print("\n--- 그래프로 교점 확인 ---")
plot_functions_and_intersections(2, 2, intersection_points_1)
plot_functions_and_intersections(1.5, np.e, intersection_points_2)
plot_functions_and_intersections(0.5, 0.5, intersection_points_3)

# 특이 케이스: 교점이 3개인 경우 (매우 드물며, 밑의 범위가 특정 조건에 해당할 때만 발생)
# 예를 들어, y = a^x 와 y = log_a(x) 에서 a가 e^(1/e) 근처일 때
# 참고: e^(1/e) 약 1.4446678
# 아래 예시는 3개의 교점을 찾을 수도 있고, 초기 추정값에 따라 2개만 찾을 수도 있습니다.
print("\n--- 예시 4: 교점 3개 가능성 (a = e^(1/e) 근처) ---")
base_val_for_three_intersections = 1.44
# 여러 초기 추정값을 시도하여 가능한 모든 교점을 찾도록 합니다.
initial_guesses_for_three = [0.1, 0.5, 1.0, 2.0, 3.0, 4.0] # 더 넓은 범위의 추정값
intersection_points_4 = find_intersection(base_exp=base_val_for_three_intersections,
                                          base_log=base_val_for_three_intersections,
                                          initial_guess=initial_guesses_for_three)
print(f"교점의 x 좌표: {intersection_points_4}")
plot_functions_and_intersections(base_val_for_three_intersections,
                                 base_val_for_three_intersections,
                                 intersection_points_4)

# 교점이 없는 경우
print("\n--- 예시 5: 교점이 없는 경우 ---")
intersection_points_5 = find_intersection(base_exp=5, base_log=5, initial_guess=1.0)
print(f"교점의 x 좌표: {intersection_points_5}")
plot_functions_and_intersections(5, 5, intersection_points_5)
