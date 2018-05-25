# -*- coding: utf-8 -*-
from ECC import KeyECC
from RSA import KeyRSA
import os
import sys


def generateKey():
    "Tạo khoá cho RSA và ECC sử dụng mã hoá và giải mã"
    # Tạo khoá công khai và bí mật RSA
    pivkey_rsa, pubkey_rsa = KeyRSA.generateRsaKey()

    # Tạo khoá công khai và bí mật ECC
    pivkey_ecc, pubkey_ecc = KeyECC.generateEccKey()

    name = str(raw_input("Nhập vào tên user: "))

    path = str(os.getcwd()) + "/Key/"
    # Kiểm tra xem file chứa khoá đã tồn tại hay chưa
    if os.path.exists(path + "%s_RSA_publickey.txt" % name) or os.path.exists(path +"%s_RSA_privatekey.text" %name):
        sys.exit("Đã tồn tại file khoá!")

    print "Đang tạo khoá RSA..."

    with open(path + "%s_RSA_publickey.txt" % name, "w") as pubrsa:
        pubrsa.write("%s,%s" %(pubkey_rsa[0], pubkey_rsa[1]))

    with open(path + "%s_RSA_privatekey.txt" %name, "w") as pivrsa:
        pivrsa.write("%s,%s" %(pivkey_rsa[0], pivkey_rsa[1]))

    print "Đang tạo khoá ECC..."

    with open(path + "%s_ECC_publickey.txt" %name, "w") as pubecc:
        pubecc.write("%s,%s" %(pubkey_ecc[0], pubkey_ecc[1]))

    with open(path +"%s_ECC_privatekey.txt" %name, "w") as pivecc:
        pivecc.write("%s" %pivkey_ecc)

    # print "\nKhoá công khai RSA: \n", pubkey_rsa
    # print "\nKoá bí mật RSA: \n", pivkey_rsa
    # print "\nKhóa công khai ECC: \n", pubkey_ecc
    # print "\nKhoá bí mật ECC: \n", pivkey_ecc
    print "Khoá đã được tạo và lưu vào thư mục Key!"
