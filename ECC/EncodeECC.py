# -*- coding: utf-8 -*-

from Curve import getCurve
from EccMath import is_on_Curve
import math

p, n, a, b = getCurve()[:4]

def legendre_symbol(a, p):
    "Kí hiệu La răng"

    ls = pow(a, (p - 1) / 2, p)
    return -1 if ls == p - 1 else ls


def modular_sqrt(a, p):
    "Tìm abs(x) sao cho x^2 = a mod p sử dụng thuật toán Tonelli Shank"

    if legendre_symbol(a, p) != 1:
        return 0
    elif a == 0:
        return 0
    elif p == 2:
        return p
    elif p % 4 == 3:
        return pow(a, (p + 1) / 4, p)

    s = p - 1
    e = 0
    while s % 2 == 0:
        s /= 2
        e += 1

    n = 2
    while legendre_symbol(n, p) != -1:
        n += 1

    x = pow(a, (s + 1) / 2, p)
    b = pow(a, s, p)
    g = pow(n, s, p)
    r = e

    while True:
        t = b
        m = 0
        for m in xrange(r):
            if t == 1:
                break
            t = pow(t, 2, p)
        if m == 0:
            return x
        gs = pow(g, 2 ** (r - m - 1), p)
        g = (gs * gs) % p
        x = (x * gs) % p
        b = (b * g) % p
        r = m

# Giá trị lớn nhất có thể nhúng
n_max = int(2**248 -1)

# Giá trị hệ số nhúng
l = int(math.floor(p / (n_max + 1)))


def find_x(n):
    "Nhúng giá trị n vào toạ độ x trên đường cong"

    if n > n_max:
        raise ValueError("Giá trị chuyển đổi quá lớn!")
    else:
        n2 = l*n
        fx2 = (n2 ** 3 + a * n2 + b) % p
        legen = legendre_symbol(int(fx2), p)
        while legen != 1:
            if n2 == l * n + l - 1:
                raise ValueError("Không tồn tại x!")
            else:
                n2 += 1
            fx2 = (n2 ** 3 + a * n2 + b) % p
            legen = legendre_symbol(int(fx2), p)
        return n2


def recover_x(x):
    " Tìm lại giá trị ban đầu trước khi nhúng"

    return int(x / l)


def encode(x):
    "Thực hiện nhúng"

    x = int(find_x(x))
    # print x
    y2 = int((x ** 3 + a * x + b) % p)
    y = modular_sqrt(y2, p)
    # print y
    assert is_on_Curve((x, y))

    return (int(x), y)


def decode(point):
    "Tìm lại giá trị trước khi nhúng"

    x = point[0]
    return recover_x(x)
