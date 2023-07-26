import math

def calculate_v3(m1, m2, m3, E_x, T_i):
    m1 = float(m1)
    m2 = float(m2)
    m3 = float(m3)
    E_x = int(E_x)
    T_i = int(T_i)
    print("PODACI: ",m1,m2,m3,E_x, T_i)
    T_i = (m2 / (m1 + m2)) * T_i
    Q = (m1 + m2) - (m3 + m1)
    numerator = 2 * m1 * (T_i + Q - E_x)
    denominator = m3 * (m3 + m1)
    print("+++++++++++++++++++++++++",numerator, denominator)
    v3 = math.sqrt(abs(numerator) / abs(denominator))
    return v3
