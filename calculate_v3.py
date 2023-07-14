import math

def calculate_v3(m1, m2, m3, m4, E_x, T1):
    T_i = (m2 / (m1 + m2)) * T1
    Q = (m1 + m2) - (m3 + m4)
    numerator = 2 * m4 * (T_i + Q - E_x)
    denominator = m3 * (m3 + m4)
    v3 = math.sqrt(numerator / denominator)
    return v3
