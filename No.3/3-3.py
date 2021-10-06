# -*- coding: utf-8 -*-

import ECDSA 
import ExtendedStack as st
import sys

# 남은 횟수 없을 시 종료
def error_check(cnt):
    if cnt <= 0:
        sys.exit()
    else:
        return
    
def hashing(pubkey):
    Qx = pubkey[0]
    Qy = pubkey[1]
    Qx_bytes = Qx.to_bytes(32, 'big')
    Qy_bytes = Qy.to_bytes(32, 'big')
    Hash_Qx = ECDSA.Hashing(Qx_bytes)
    Hash_Qy = ECDSA.Hashing(Qy_bytes)
        
    Hash_Qx = ''.join(format(x, '02x') for x in Hash_Qx)
    Hash_Qy = ''.join(format(x, '02x') for x in Hash_Qy)
    
    return Hash_Qx, Hash_Qy

print("=========================================")
print("메시지를 입력하세요.")
msg = input()
print('\n')
print("키를 생성합니다.\n")
privateKey, publicKey = ECDSA.make_key()
print("서명을 생성합니다.\n")
signature = ECDSA.make_signature(msg, privateKey)
print("생성된 메시지, 키, 서명은 다음과 같습니다.\n")
print("메시지 : ", msg)
print("\n")
print("개인키 : ", hex(privateKey))
print("\n")
print("공개키 : Qx, Qy")
print("Qx : ", hex(publicKey[0]))
print("Qy : ", hex(publicKey[1]))
print("\n")
print("서명 : r, s")
print("r : ", hex(signature[0][0]))
print("s : ", hex(signature[0][1]))
print("\n")
print("공개키의 해시 값 : LSH(Qx), LSH(Qy)")
hx, hy = hashing(publicKey)
print("LSH(Qx) : ", '0x' + hx)
print("LSH(Qy) : ", '0x' + hy)
print("=========================================")

stack, cnt = st.init()

print("모드를 입력하세요.")
print("생성된 서명과 공개키로 서명 검증 확인 (검증 성공) : 1")
print("임의의 공개키에 대한 해시값 생성 (검증 실패) : 2")
print("임의의 공개키를 생성 (검증 실패) : 3")
print("임의의 서명 생성 (검증 실패) : 4")
print("직접 입력 (올바른 입력 시 검증 성공) : 5")
mode = int(input("mode : "))

if mode not in [1, 2, 3, 4, 5]:
    print("다시 입력하세요.")
    mode = int(input("mode : "))

while True:
    # ECDSA 모듈에서 서명 생성 시 (r, s), (r, -s) 2가지 서명 생성
    # (r, s)를 사용하기 위해 signature[0]를 택함.
    scripts, scriptPubKey, scriptSig, cnt = st.make_script(cnt, signature[0], publicKey, msg, mode)
    scripts, cnt, valid = st.scripts_to_queue(scripts, cnt)
    
    if cnt <= 0 or valid == True:
        break

error_check(cnt)
print("=========================================")
print("scriptPubKey : ", end = "")
for scr in scriptPubKey:
    print(scr, end = " ")
print('\n')
print("scriptSig : ", end = "")
for scr in scriptSig:
    print(scr, end=" ")
print('\n')
print("=========================================")
print('\n')

while scripts.empty() == False:
    stack, valid = st.oper(stack, msg, scripts)
    
    if valid == False:
        break

error_check(cnt)
print('\n')
print("=========================================")
print("최종 결과")
if len(stack) == 1 and stack[0] == "True":
    print("서명 검증에 성공하였습니다.")
    print("UnLocking Success")
else:
    print("서명 검증에 실패하였습니다.")
    print("UnLocking Fail")
st.print_stack(stack)

input("엔터를 누르면 종료합니다.")