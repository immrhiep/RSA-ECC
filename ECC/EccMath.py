# -*- coding: utf-8 -*-

from Curve import getCurve
from RSA import RsaMath

p, n, a, b, G = getCurve()


def is_on_Curve(point):
    "Kiểm tra điểm point có thuộc đường cong hay không"

    if point is None:
        return True

    x, y = point
    return (y ** 2 - x ** 3 - a * x - b) % p == 0


def negatives_Point(point):
    "Tìm điểm nghịch đảo của point"

    assert is_on_Curve(point)
    if point is None:
        # -0 = 0
        return None
    x, y = point

    return (x, -y % p)


def add_Points(point1, point2):
    "Cộng hai điểm point1 và point2"

    assert is_on_Curve(point1)
    assert is_on_Curve(point2)

    if point1 is None:
        # 0 + point2 = point2
        return point2

    if point2 is None:
        # point1 + 0 = point1
        return point1

    x1, y1 = point1
    x2, y2 = point2

    if x1 == x2 and y1 != y2:
        # point1 + (-point1) = 0
        return None
    if x1 == x2:
        # point1 == point2
        m = (3 * x1 * x1 + a) * RsaMath.mod_inverse(2 * y1, p)
    else:
        m = (y2 - y1) * RsaMath.mod_inverse((x2 - x1) % p, p)

    x3 = (m ** 2 - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p

    return (x3, y3)


def scalar_Point(k, point):
    "Nhân k với điểm point k*point"

    assert is_on_Curve(point)

    if k % n == 0 or point is None:
        return None
    elif k < 0:
        return scalar_Point(-k, negatives_Point(point))

    result = None
    addend = point

    while k:
        if k & 1:
            result = add_Points(result, addend)

        addend = add_Points(addend, addend)
        k >>= 1  # k = k / 2

    return result
