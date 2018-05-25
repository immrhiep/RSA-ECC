# -*- coding: utf-8 -*-
import binascii
import sys


def gcd(a, b):
    "Tìm ước chung nhỏ lớn nhất của hai số bằng thuật toán Euclid"

    while a != 0:
        a, b = b % a, a
    return b


def mod_inverse(a, m):
    "Tìm x sao cho a * x % m = 1 sử dụng thuật toán Euclid mở rộng"

    if gcd(a, m) != 1:
        return None  # a và m không phải là 2 số nguyên tố cùng nhau.

    x1, x2, x3 = 1, 0, a
    y1, y2, y3 = 0, 1, m

    while y3 != 0:
        q = x3 // y3
        y1, y2, y3, x1, x2, x3 = (
            x1 - q * y1), (x2 - q * y2), (x3 - q * y3), y1, y2, y3

    return x1 % m
 

def I2OSP(x, xLen):
    "Chuyển số nguyên x thành chuỗi octet có chiều dàn xLen"

    if x > 256 ** xLen:
        raise ValueError("So nguyen qua lon")
    h = hex(x)[2:]
    if h[-1] == "L":
        h = h[:-1]
    if len(h) & 1 == 1:
        h = "0%s" % h
    x = binascii.unhexlify(h)
    return b'\x00' * int(xLen - len(x)) + x


def OS2IP(x):
    "Chuyển đổi chuỗi octet thành số nguyên"

    h = binascii.hexlify(x)
    return int(h, 16)


def stringXOR(a, b):
    "XOR string"

    if sys.version_info[0] < 3:
        return "".join((chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b)))
    else:
        return bytes(x ^ y for (x, y) in zip(a, b))


def integerByteSize(n):
    "Tính kích thước bits của một số nguyên"

    quanta, mod = divmod(integerBitSize(n), 8)
    if mod or n == 0:
        quanta += 1
    return quanta


def integerBitSize(n):
    "Tính kích thước bytes của một số nguyên"

    if n == 0:
        return 1
    s = 0
    while n:
        s += 1
        n >>= 1
    return s
