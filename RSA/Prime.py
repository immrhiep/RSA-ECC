# -*- coding: utf-8 -*-

# from os import urandom
import random
import math
import RsaMath

"Sử dụng kiểm tra Rabin Miller để kiểm tra số nguyên tố"


def rabinMiller(n, k=64):
    "Thuật toán Rabin Miller"

    # s = 0
    # d = n - 1
    s = RsaMath.integerBitSize(n)
    s = RsaMath.gcd(2 ** s, n - 1)
    d = (n - 1) // s
    s = RsaMath.integerBitSize(s) - 1
    while k:
        k = k - 1
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for r in xrange(1, s - 1):
            x = pow(x, 2, n)
            if x == 1:
                return False
            if x == n - 1:
                break
        else:
            return False
    return True


def isPrime(number):
    "Kiểm tra số nguyên tố"

    if number < 2:
        return False
    # Khai báo danh sách các số nguyên tố bé dưới 1000.
    lowPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443,
                 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]

    if number in lowPrimes:
        return True

    for prime in lowPrimes:
        if number % prime == 0:
            return False

    '''Nếu số cần kiểm tra không nằm trong lowPrimes
        thì chuyển qua kiểm tra Rabin Miller'''
    return rabinMiller(number)


def getPrime(nlen):
    p_min = math.floor(2 ** ((nlen - 1) / 2)) + 1
    p_max = math.ceil(2 ** (nlen / 2)) - 1
    while True:
        p = random.randint(p_min, p_max)
        if isPrime(p):
            return p
