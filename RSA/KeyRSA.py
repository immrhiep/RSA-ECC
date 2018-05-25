# -*- coding: utf-8 -*-
import Prime
import RsaMath


def generateRsaKey(size=1024, e=65537):
    "Tạo khoá RSA theo PKCS#1 với kích thước mặc định là 1024-bits"
    d = 1
    while True:
        p = Prime.getPrime(size)
        q = Prime.getPrime(size)
        if RsaMath.gcd((p-1), e)==1 and RsaMath.gcd((q-1), e)==1:
            break

    n = p * q
    lam_da = ((p - 1) * (q - 1)) / RsaMath.gcd((p - 1), (q - 1))


    while d < 2 ** (size/2):
        d = RsaMath.mod_inverse(e, lam_da)


    publicKey = (n, e)
    privateKey = (n, d)

    return privateKey, publicKey
