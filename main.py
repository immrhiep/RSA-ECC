# -*- coding: utf-8 -*-
from EncryptImage import Encryption, Decryption
from ImageRSA import EncryptionRSA, DecryptionRSA
from ImageECC import EncryptionECC, DecrypteionECC
import KeyGenerate
import sys


if __name__ == '__main__':

    def choise(number):
        if number == "1":
            return KeyGenerate.generateKey()
        if number == "2":
            return encryptMenu()
        if number == "3":
            return decryptMenu()
        if number == "4":
            sys.exit()
        else:
            print "Bạn nhập sai! Nhập lại."

    def Menu():
        print '''Mời bạn chọn chức năng!
            1: Tạo khoá
            2: Mã hoá
            3: Giải mã
            4: Thoát'''
        x = str(raw_input("Bạn chọn: "))
        choise(x)

    def choise_encrypt(number):
        if number == "1":
            return EncryptionRSA()
        if number == "2":
            return EncryptionECC()
        if number == "3":
            return Encryption()
        if number == "4":
            sys.exit()

    def encryptMenu():
        print '''Mời bạn chọn: 
            1. Mã hoá RSA
            2. Mã hoá ECC
            3. Mã hoá RSA & ECC
            4. Thoát'''

        x = str(raw_input("Bạn chọn: "))
        choise_encrypt(x)

    def choise_decrypt(number):
        if number == "1":
            return DecryptionRSA()
        if number == "2":
            return DecrypteionECC()
        if number == "3":
            return Decryption()
        if number == "4":
            sys.exit()

    def decryptMenu():
        print '''Mời bạn chọn:
            1. Giải mã RSA
            2. Giải mã ECC
            3. Giải mã RSA & ECC
            4. Thoát'''

        x = str(raw_input("Bạn chọn: "))
        choise_decrypt(x)

    print "Mã hoá hình ảnh bằng RSA & ECC"
    while True:
        Menu()