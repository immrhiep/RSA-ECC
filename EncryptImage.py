# -*- coding: utf-8 -*-

from ECC import Curve
from ECC import EccMath
from RSA.RsaMath import OS2IP, I2OSP
from PIL import Image
from ECC import EncodeECC
import time
import math
import random
import os

n = Curve.getCurve()[1]
G = Curve.getCurve()[-1]

path_image = str(os.getcwd()) + "/Image/"
path_key = str(os.getcwd()) + "/Key/"

def rsa_cipher(key, mess):
    n, eORd = key
    return pow(mess, eORd, n)


def rsaEncrypt(publickey, data):
    "Mã hoá bằng thuật toán RSA với đầu vào là chuỗi bytes đọc từ file ảnh"

    cipher_rsa = []

    # Đọc 127 bytes một để mã hoá
    for i in range(0, len(data), 127):
        value = data[i:i+127]
        m = OS2IP(value)
        c = rsa_cipher(publickey, m)
        cipher_rsa.append(I2OSP(c, 128))

    # Trả về chuỗi bytes sau khi mã hoá
    return b''.join(cipher_rsa)


def rsaDecrypt(privatekey, data):
    "Giải mã bằng thuật toán RSA với đầu vào là chuỗi bytes được giải mã từ ECC"

    plain_rsa = []

    # Đọc 128 bytes một để giải mã
    for i in range(0, len(data), 128):
        value = data[i:i+128]
        c = OS2IP(value)
        m = rsa_cipher(privatekey, c)
        plain_rsa.append(I2OSP(m, 127))

    # Trả về chuỗi bytes sau khi giải mã
    return b''.join(plain_rsa)


def elgamalEn(m, P):
    "Mã hoá Elgamal tính giá trị C2"

    M = EncodeECC.encode(m)
    C2 = EccMath.add_Points(M, P)
    return C2


def elgamalDe(C, C2):
    "Giải mã Elgamal trả về bản rõ m"

    M = EccMath.add_Points(C2, C)
    m = EncodeECC.decode(M)
    return m


def eccEncrypt(rsa_value, publicKey):
    "Mã hoá ECC với đầu vào là chuỗi bytes đã được mã hoá bằng RSA"

    k = random.randint(1, n)
    C1 = EccMath.scalar_Point(k, G)
    P = EccMath.scalar_Point(k, publicKey)
    # start_time = time.time()
    cipher_points = []
    for i in range(0, len(rsa_value), 31):
        plain = rsa_value[i:i+31]
        plain = OS2IP(plain)
        ecc_enc = elgamalEn(plain, P)
        cipher_points.append(ecc_enc)
    # print "%s seconds" %(time.time() - start_time)
    cipher_bytes = []
    for point in cipher_points:
        point_to_bytes = I2OSP(point[0], 32) + I2OSP(point[1], 32)
        cipher_bytes.append(point_to_bytes)

    cipher_bytes = b''.join(cipher_bytes)
    c = I2OSP(C1[0], 32) + I2OSP(C1[1], 32)

    return c + cipher_bytes


def eccDecrypt(data_cipher, privateKey):
    "Giải mã ECC với đầu vào là chuỗi bytes từ hình ảnh đã mã hoá"

    c = data_cipher[:64]
    C1 = (OS2IP(c[:32]), OS2IP(c[-32:]))
    C = EccMath.scalar_Point(privateKey, C1)
    C = EccMath.negatives_Point(C)

    data_cipher = data_cipher[64:]
    points = []
    for i in range(0, len(data_cipher), 64):
        data = data_cipher[i:i+64]
        x = OS2IP(data[:32])
        y = OS2IP(data[-32:])
        points.append((x, y))

    plain_data = []
    for point in points:
        plain_data.append(elgamalDe(C, point))

    plain_bytes = []
    for j in plain_data:
        plain_bytes.append(I2OSP(j, 31))

    plain_data = b''.join(plain_bytes)

    plain_data = remove_padding(plain_data)

    return plain_data


def padding(data, t):
    "Thêm bytes \x00 hoặc \x01 vào đầu chuỗi bytes"

    if data[0] != "\x00":
        while len(data) % t != 0:
            data = "\x00" + data
    else:
        while len(data) % t != 0:
            data = "\x01" + data
    return data


def remove_padding(data):
    if data[0] == "\x00":
        return data.lstrip("\x00")
    else:
        return data.lstrip("\x01")


def imageEncrypt(data, rsa_publickey, ecc_publickey):
    "Mã hoá hình ảnh bằng RSA và ECC"

    data = padding(data, 127)
    # Mã hoá bằng RSA
    # start_time = time.time()
    rsa_encrypted = rsaEncrypt(rsa_publickey, data)
    # print "%s seconds" %(time.time() - start_time)
    rsa_encrypted = padding(rsa_encrypted,31)
    ecc_encrypted = eccEncrypt(rsa_encrypted, ecc_publickey)

    return ecc_encrypted


def imageDecrypt(data, rsa_privatekey, ecc_privatekey):
    "Giải mã hình ảnh đã được mã hoá bằng RSA và ECC"

    ecc_decrypted = eccDecrypt(data, ecc_privatekey)
    ecc_decrypted = remove_padding(ecc_decrypted)
    rsa_decrypted = rsaDecrypt(rsa_privatekey, ecc_decrypted)
    rsa_decrypted = remove_padding(rsa_decrypted)

    return rsa_decrypted


def creatImage(data, name):
    path_enc = path_image + "/ImageEncrypted/"
    num_pixel = (len(data) + 2) / 3
    W = H = int(math.ceil(num_pixel ** 0.5))
    if data[0] == "\x00":
        data = "\x01" * (W * H * 3 - len(data)) + data
    else:
        data = "\x00" * (W * H * 3 - len(data)) + data

    img = Image.frombytes("RGB", (W, H), data)
    img.save(path_enc + "%s.bmp" % name)
    print "Mã hoá thành công!\n"
    img.show()


def read_file_to_Encrypt(file_input, file_rsaKey, file_eccKey):
    "Đọc file hình ảnh, file chứa khoá công khai rsa và ecc"

    with open(file_input, "rb") as infile:
        data = infile.read()
    # im = Image.open(file_input)
    # data = im.tobytes()

    with open(file_rsaKey, "r") as rsaKey:
        rsa_publickey = rsaKey.read()
    n, e = rsa_publickey.split(",")
    rsa_publickey = (int(n), int(e))

    with open(file_eccKey, "r") as eccKey:
        ecc_publickey = eccKey.read()
    x, y = ecc_publickey.split(",")
    ecc_publickey = (int(x), int(y))

    return data, rsa_publickey, ecc_publickey


def recoverImage(data, name):
    path_recover = path_image + "/ImageDecrypted/"

    with open(path_recover + "%s.jpg" %name, "wb") as outfile:
        outfile.write(data)

    im = Image.open(path_recover + "%s.jpg" %name)
    im.show()
    print "Giải mã thành công!\n"


def read_file_to_Decrypt(file_input, file_rsaKey, file_eccKey):
    "Đọc file hình ảnh, file chứa khoá bí mật rsa và ecc"

    im = Image.open(file_input)
    data = im.tobytes()
    data = remove_padding(data)

    with open(file_rsaKey, "r") as rsaKey:
        rsa_privatekey = rsaKey.read()
    n, d = rsa_privatekey.split(",")
    rsa_privatekey = (int(n), (int(d)))

    with open(file_eccKey, "r") as eccKey:
        ecc_privatekey = eccKey.read()
    ecc_privatekey = int(ecc_privatekey)

    return data, rsa_privatekey, ecc_privatekey


def Encryption():

    print "Mã hoá RSA & ECC"
    image = str(raw_input("Nhập tên ảnh cần mã hoá: "))
    image = path_image + image

    user_name = str(raw_input("Nhập tên user: "))
    img_name = str(raw_input("Nhập vào tên ảnh sau khi mã hoá: "))

    rsa_filekey = path_key + "%s_RSA_publickey.txt" % user_name
    ecc_filekey = path_key + "%s_ECC_publickey.txt" % user_name

    data, rsa_publickey, ecc_publickey = read_file_to_Encrypt(image, rsa_filekey, ecc_filekey)
    start_time = time.time()
    encrypted = imageEncrypt(data, rsa_publickey, ecc_publickey)
    print "\nTime: %s seconds" %(time.time() - start_time)

    return creatImage(encrypted, img_name)


def Decryption():
    path_de = path_image + "/ImageEncrypted/"

    print "Gải mã RSA & ECC"
    image = str(raw_input("Nhập tên ảnh cần giải mã: "))
    image = path_de + image

    user_name = str(raw_input("Nhập tên user: "))
    img_name = str(raw_input("Nhập vào tên ảnh sau khi giải mã: "))
    # img_name = path_recover + img_name

    rsa_filekey = path_key + "%s_RSA_privatekey.txt" % user_name
    ecc_filekey = path_key + "%s_ECC_privatekey.txt" % user_name

    data, rsa_privatekey, ecc_privatekey = read_file_to_Decrypt(image, rsa_filekey, ecc_filekey)
    start_time = time.time()
    decrypted = imageDecrypt(data, rsa_privatekey, ecc_privatekey)
    print "\nTime: %s seconds" %(time.time() - start_time)

    return recoverImage(decrypted, img_name)
