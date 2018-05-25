# -*- coding: utf-8 -*-
from binascii import hexlify
from os import urandom
import Curve, EccMath

def get_privateKey(n):
    "Tạo khoá bí mật cho hệ mật "

    order_bits = 0
    order = n

    while order > 0:
        order >>= 1
        order_bits += 1

    order_bytes = (order_bits + 7) // 8
    extra_bits = order_bytes * 8 - order_bits

    k = int(hexlify(urandom(order_bytes)), 16)
    k >>= extra_bits

    while k >= n:
        k = int(hexlify(urandom(order_bytes)), 16)
        k >>= extra_bits

    return k


def get_publicKey(k, G):
    "Tạo khoá công khai bằng cách lấy khoá bí mật nhân với điểm cơ sở "

    return EccMath.scalar_Point(k, G)


def generateEccKey():
    "Tạo khoá cho hệ mật Elgamal"

    n = Curve.getCurve()[1]
    G = Curve.getCurve()[4]
    k = get_privateKey(n)
    pk = get_publicKey(k, G)

    return k, pk

