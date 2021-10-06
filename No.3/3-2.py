# -*- coding: utf-8 -*-

import ECDSA
import random

print("================================")
print("==== ECDSA 서명 생성 및 검증 ====")
print("================================")
print("메시지를 입력하세요.")
msg = input("Enter : ")

print('\n')
print("================================")
print("키를 생성합니다.\n")
key = ECDSA.make_key()
print("개인키 : ")
print("d : ", hex(key[0]))
print('\n')
print("공개키 : ")
print("Qx : ", hex(key[1][0]))
print("Qy : ", hex(key[1][1]))

print('\n')
print("================================")
print("서명을 생성합니다.\n")
signature = ECDSA.make_signature(msg, key[0])
print("서명 = (r1, s1), (r2, s2)")
print("r1 : ")
print(hex(signature[0][0]))
print("s1 : ")
print(hex(signature[0][1]))
print('\n')
print("r2 : ")
print(hex(signature[1][0]))
print("s2 : ")
print(hex(signature[1][1]))

print('\n')
print("====== (r1, s1) 서명 검증 =======")
print("서명 검증을 합니다.\n")
sig = signature[0]
verifying = ECDSA.sig_verification(sig, key[1], msg)
if verifying == True:
    print("서명 검증에 성공하였습니다.")
else:
    print("서명 검증에 실패하였습니다.")

print('\n')
print("====== (r2, s2) 서명 검증 =======")
print("서명 검증을 합니다.\n")
sig = signature[1]
verifying = ECDSA.sig_verification(sig, key[1], msg)
if verifying == True:
    print("서명 검증에 성공하였습니다.")
else:
    print("서명 검증에 실패하였습니다.")
    
print('\n')
print("================================")
print("=====서명 검증 실패 테스트=======")
print("================================")
print("임의의 서명 값을 생성합니다.")
print("기존 공개키로 임의의 서명을 검증합니다.")
n = ECDSA.n
invalid_private_key = random.randint(1, n-1)
invalid_sig = ECDSA.make_signature(msg, invalid_private_key)

print("r1 : ")
print(hex(invalid_sig[0][0]))
print("s1 : ")
print(hex(invalid_sig[0][1]))
print('\n')
print("r2 : ")
print(hex(invalid_sig[1][0]))
print("s2 : ")
print(hex(invalid_sig[1][1]))

print("\n")
print("====== (r1, s1) 서명 검증 =======")
print("서명 검증을 합니다.\n")
verifying = ECDSA.sig_verification(invalid_sig[0], key[1], msg) 
if verifying == True:
    print("서명 검증에 성공하였습니다.")
else:
    print("서명 검증에 실패하였습니다.")

print("\n")
print("====== (r2, s2) 서명 검증 =======")
print("서명 검증을 합니다.\n")
verifying = ECDSA.sig_verification(invalid_sig[1], key[1], msg) 
if verifying == True:
    print("서명 검증에 성공하였습니다.")
else:
    print("서명 검증에 실패하였습니다.")
    
print('\n')
print("================================")
print("=====서명 검증 실패 테스트=======")
print("================================")
print("임의의 키를 생성합니다.")
print("기존 서명을 임의의 키로 생성된 공개키로 검증합니다.")
invalid_key = ECDSA.make_key()

print("개인키 : ")
print("d : ", hex(invalid_key[0]))
print('\n')
print("공개키 : ")
print("Qx : ", hex(invalid_key[1][0]))
print("Qy : ", hex(invalid_key[1][1]))
print('\n')

print("r1 : ")
print(hex(signature[0][0]))
print("s1 : ")
print(hex(signature[0][1]))
print('\n')
print("r2 : ")
print(hex(signature[1][0]))
print("s2 : ")
print(hex(signature[1][1]))
print("\n")
print("====== (r1, s1) 서명 검증 =======")
print("서명 검증을 합니다.\n")
verifying = ECDSA.sig_verification(signature[0], invalid_key[1], msg) 
if verifying == True:
    print("서명 검증에 성공하였습니다.")
else:
    print("서명 검증에 실패하였습니다.")

print("\n")
print("====== (r2, s2) 서명 검증 =======")
print("서명 검증을 합니다.\n")
verifying = ECDSA.sig_verification(signature[1], invalid_key[1], msg) 
if verifying == True:
    print("서명 검증에 성공하였습니다.")
else:
    print("서명 검증에 실패하였습니다.")
    
input("엔터를 누르면 종료합니다.")