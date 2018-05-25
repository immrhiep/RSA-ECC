# -*- coding: utf-8 -*-

from RSA.RsaMath import OS2IP, I2OSP
from PIL import Image
import math
import os
import time
path_image = str(os.getcwd()) + "/Image/"

def cipher(key, mess):
    n, eORd = key
    return pow(mess, eORd, n)


def RSAencrypt(publickey, data):
    cipher_rsa = []
    for i in range(0, len(data), 127):
        value = data[i:i+127]
        m = OS2IP(value)
        c = cipher(publickey, m)
        cipher_rsa.append(I2OSP(c, 128))
    return b''.join(cipher_rsa)


def RSAdecrypt(privatekey, data):
    plain_rsa = []
    for i in range(0, len(data), 128):
        value = data[i:i+128]
        c = OS2IP(value)
        m = cipher(privatekey, c)
        plain_rsa.append(I2OSP(m, 127))

    return b''.join(plain_rsa)


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


def creatImage(data, name):
    path_image_encrypt = path_image + "/ImageEncrypted/"

    num_pixel = (len(data) + 2) / 3
    W2 = H2 = int(math.ceil(num_pixel ** 0.5))
    if data[0] == "\x00":
        data = "\x01" * (W2 * H2 * 3 - len(data)) + data
    else:
        data = "\x00" * (W2 * H2 * 3 - len(data)) + data

    img = Image.frombytes("RGB", (W2, H2), data)
    img.save(path_image_encrypt + "%s.bmp" %name)
    img.show()


def recoverImage(data, name):
    path_image_decrypt = path_image + "/ImageDecrypted/"

    with open(path_image_decrypt + "%s.jpg" %name, "wb") as outfile:
        outfile.write(data)
    print "Giải mã thành công!"


def read_file_to_Encrypt(file_input, file_rsaKey):
    "Đọc file hình ảnh, file chứa khoá công khai rsa"

    with open(file_input, "rb") as infile:
        data = infile.read()
    # im = Image.open(file_input)
    # data = im.tobytes()

    with open(file_rsaKey, "r") as rsaKey:
        rsa_publickey = rsaKey.read()
    n, e = rsa_publickey.split(",")
    rsa_publickey = (int(n), int(e))

    return data, rsa_publickey


def read_file_to_Decrypt(file_input, file_rsaKey):
    "Đọc file hình ảnh, file chứa khoá bí mật rsa"
    path_image = str(os.getcwd()) + "/Image/ImageEncrypted/"

    im = Image.open(path_image + file_input)
    data = im.tobytes()
    data = remove_padding(data)

    with open(file_rsaKey, "r") as rsaKey:
        rsa_privatekey = rsaKey.read()
    n, d = rsa_privatekey.split(",")
    rsa_privatekey = (int(n), (int(d)))

    return data, rsa_privatekey


def EncryptionRSA():

    path = str(os.getcwd()) + "/Key/"

    print "Mã hoá RSA"
    image = str(raw_input("Nhập tên ảnh cần mã hoá: "))
    image = path_image + image

    user_name = str(raw_input("Nhập tên user: "))
    img_name = str(raw_input("Nhập tên ảnh sau khi mã hoá: "))

    rsa_filekey = path + "%s_RSA_publickey.txt" % user_name

    data, rsa_publickey = read_file_to_Encrypt(image, rsa_filekey,)
    data = padding(data, 127)
    start_time = time.time()
    encrypted = RSAencrypt(rsa_publickey, data)
    print "\nTime: %s seconds" %(time.time() - start_time)
    print "Mã hoá thành công\n"
    return creatImage(encrypted, img_name)


def DecryptionRSA():

    path = str(os.getcwd()) + "/Key/"

    print "Giải mã RSA"
    image = str(raw_input("Nhập tên ảnh cần giải mã: "))

    user_name = str(raw_input("Nhập tên user: "))
    img_name = str(raw_input("Nhập tên sau khi giải mã: "))

    rsa_filekey = path + "%s_RSA_privatekey.txt" % user_name

    data, rsa_privatekey = read_file_to_Decrypt(image, rsa_filekey)
    data = remove_padding(data)
    start_time = time.time()
    decrypted = RSAdecrypt(rsa_privatekey, data)
    print "\nTime: %s seconds" %(time.time() - start_time)
    decrypted = remove_padding(decrypted)
    print "Giải mã thành công\n"
    return recoverImage(decrypted, img_name)