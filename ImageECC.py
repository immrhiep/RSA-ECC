# -*- coding: utf-8 -*-
import random
from ECC import EccMath
from ECC import Curve
from RSA.RsaMath import OS2IP, I2OSP
from ECC import EncodeECC
from PIL import Image
from EncryptImage import padding, remove_padding, recoverImage, creatImage
import os
import time

path_image = str(os.getcwd()) + "/Image/"
path_key = str(os.getcwd()) + "/Key/"
n = Curve.getCurve()[1]
G = Curve.getCurve()[-1]

def elgamalEncrypt(m, P):
    M = EncodeECC.encode(m)
    C2 = EccMath.add_Points(M, P)
    return C2


def elgamalDecrypt(C, C2):
    M = EccMath.add_Points(C2, C)
    m = EncodeECC.decode(M)

    return m


def eccEncrypt(data, publicKey):
    k = random.randint(1, n)
    C1 = EccMath.scalar_Point(k, G)
    P = EccMath.scalar_Point(k, publicKey)
    cipher_points = []
    for i in range(0, len(data), 31):
        plain = data[i:i+31]
        plain = OS2IP(plain)
        ecc_enc = elgamalEncrypt(plain, P)
        cipher_points.append(ecc_enc)

    cipher_bytes = []
    for point in cipher_points:
        point_to_bytes = I2OSP(point[0], 32) + I2OSP(point[1], 32)
        cipher_bytes.append(point_to_bytes)

    cipher_bytes = b''.join(cipher_bytes)
    c = I2OSP(C1[0], 32) + I2OSP(C1[1], 32)

    return c + cipher_bytes


def eccDecrypt(data_cipher, privateKey):
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
        plain_data.append(elgamalDecrypt(C, point))

    plain_bytes = []
    for j in plain_data:
        plain_bytes.append(I2OSP(j, 31))

    plain_data = b''.join(plain_bytes)

    return plain_data

def read_file_to_Encrypt(file_input, file_eccKey):
    "Đọc file hình ảnh, file chứa khoá công khai ecc"

    with open(file_input, "rb") as infile:
        data = infile.read()
    # im = Image.open(file_input)
    # data = im.tobytes()

    with open(file_eccKey, "r") as eccKey:
        ecc_publickey = eccKey.read()
    x, y = ecc_publickey.split(",")
    ecc_publickey = (int(x), int(y))

    return data, ecc_publickey


def read_file_to_Decrypt(file_input, file_eccKey):
    "Đọc file hình ảnh, file chứa khoá bí mật ecc"

    im = Image.open(file_input)
    data = im.tobytes()
    data = remove_padding(data)

    with open(file_eccKey, "r") as eccKey:
        ecc_privatekey = eccKey.read()
    ecc_privatekey = int(ecc_privatekey)

    return data, ecc_privatekey

def EncryptionECC():
    print "Mã hoá ECC"
    image = str(raw_input("Nhập tên ảnh cần mã hoá: "))
    image = path_image + image

    user_name = str(raw_input("Nhập tên user: "))
    img_name = str(raw_input("Nhập vào tên ảnh sau khi mã hoá: "))

    ecc_filekey = path_key + "%s_ECC_publickey.txt" % user_name

    data, ecc_publickey = read_file_to_Encrypt(image, ecc_filekey)
    data = padding(data, 31)
    start_time = time.time()
    encrypted = eccEncrypt(data, ecc_publickey)
    print "\nTime: %s seconds" %(time.time() - start_time)
    return creatImage(encrypted, img_name)


def DecrypteionECC():
    path_de = path_image + "/ImageEncrypted/"

    print "Gải mã ECC"
    image = str(raw_input("Nhập tên ảnh cần giải mã: "))
    image = path_de + image

    user_name = str(raw_input("Nhập tên user: "))
    img_name = str(raw_input("Nhập vào tên ảnh sau khi giải mã: "))
    # img_name = path_recover + img_name

    ecc_filekey = path_key + "%s_ECC_privatekey.txt" % user_name

    data, ecc_privatekey = read_file_to_Decrypt(image, ecc_filekey)
    start_time = time.time()
    decrypted = eccDecrypt(data, ecc_privatekey)
    print "\nTime: %s seconds" %(time.time() - start_time)
    decrypted = remove_padding(decrypted)

    return recoverImage(decrypted, img_name)