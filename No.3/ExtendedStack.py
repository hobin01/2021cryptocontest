# -*- coding: utf-8 -*-

import ECDSA
from queue import Queue
import random

# 초기화
def init():
    print("확장된 스택 프로세서 입니다.")
    print("메시지 소유권을 지정하고 확인합니다.\n")
    
    stack = []
    cnt = 5
    
    return stack, cnt

# 남은 카운트 프린트
def print_cnt(cnt):
    if cnt <= 0:
        print("남은 기회가 없습니다.")
    else:
        print("남은 기회 : ", cnt)
    return

# 스택 내용 프린트
def print_stack(stack):
    if len(stack) == 0:
        print("stack is empty")
    
    else:
        print("========== stack ===========")
        if type(stack[-1]) is tuple:
            print("top ----> ", (hex(stack[-1][0])[2:], hex(stack[-1][1])[2:]))
        else:
            print("top ----> ", stack[-1])
        for i in range(len(stack) - 2, -1, -1):
            print("============================")
            if type(stack[i]) is tuple:
                print("          ", (hex(stack[i][0])[2:], hex(stack[i][1])[2:]))
            else:
                print("          ", stack[i])
        print('============================\n')
    return

# script 생성
# parameter - signature, pubkey : 수신자의 서명, 수신자의 공개키
# msg, mode : 암호화 메시지, 테스트 모드
def make_script(cnt, sig, pubkey, msg, mode):
    print_cnt(cnt)
    print("================================================")
    print("명령어는 다음과 같이 입력됩니다.")
    print("<서명(hex)> <공개키(hex)> 복사명령어 해쉬명령어 <공개키 해쉬값(hex)> 동일검증명령어 서명검증명령어")
    print("<r,s> <Qx,Qy> OP_DUP OP_HASH <HashX,HashY> OP_EQUALVERIFY OP_CHECKSIG")
    print("ex) <abcd,0123> <01234,abcde> OP_DUP OP_HASH <0000,ffff> OP_EQUALVERIFY OP_CHECKSIG")
    print("================================================")
    
    if mode == 5:
        scripts = input("명령어를 입력하세요 : ")
    else:
        if mode == 1:
            (Qx, Qy) = pubkey
            
        if mode == 2:
            AttackerKey = random.randint(1, ECDSA.n)
            (Qx, Qy) = ECDSA.multiple(ECDSA.Gx, ECDSA.Gy, AttackerKey, ECDSA.p, ECDSA.a)
            
        if mode == 3:
            AttackerKey = random.randint(1, ECDSA.n)
            (Qx, Qy) = ECDSA.multiple(ECDSA.Gx, ECDSA.Gy, AttackerKey, ECDSA.p, ECDSA.a)
            pubkey = (Qx, Qy)
            
        if mode == 4:
            AttackerKey = random.randint(1, ECDSA.n)
            AttackerSig = ECDSA.make_signature(msg, AttackerKey)
            sig = AttackerSig[0]
            (Qx, Qy) = pubkey
        
        Qx_bytes = Qx.to_bytes(32, 'big')
        Qy_bytes = Qy.to_bytes(32, 'big')
        Hash_Qx = ECDSA.Hashing(Qx_bytes)
        Hash_Qy = ECDSA.Hashing(Qy_bytes)
                
        Hash_Qx = ''.join(format(x, '02x') for x in Hash_Qx)
        Hash_Qy = ''.join(format(x, '02x') for x in Hash_Qy)
            
        scripts = ""
        scripts += "<" + hex(sig[0])[2:] + "," + hex(sig[1])[2:] + "> "
        scripts += "<" + hex(pubkey[0])[2:] + "," + hex(pubkey[1])[2:] + "> "
        scripts += "OP_DUP OP_HASH "
        scripts += "<" + str(Hash_Qx) + "," + str(Hash_Qy) + "> "
        scripts += "OP_EQUALVERIFY OP_CHECKSIG "
    
    scriptPubKey = []
    scriptSig = []
    
    for i in range(len(scripts.split())):
        if i == 0 or i == 1:
            scriptSig.append(scripts.split()[i])
        else:
            scriptPubKey.append(scripts.split()[i])
    
    return scripts, scriptPubKey, scriptSig, cnt

# scripts를 큐로 변환
def scripts_to_queue(scripts, cnt):
    queue = Queue()
    scripts = scripts.split()
    
    OperDict = {'OP_DUP' : 0x76, 'OP_HASH' : 0xAA, 'OP_EQUALVERIFY' : 0x88, 'OP_CHECKSIG' : 0xAC}
    valid_script = True
    
    for oper in scripts:
        if oper[0:3] == "OP_":
            if oper in OperDict.keys():
                queue.put(OperDict[oper])
            else:
                print("잘못된 명령어입니다.\n")
                cnt -= 1
                valid_script = False
                break
        else:
            if oper[0] == '<':
                try:
                    numbers = oper.split(',')
                    num1 = int('0x' + numbers[0][1:], 16)
                    num2 = int('0x' + numbers[1][:-1], 16)
                    num_byte = (len(numbers[0][1:]) // 2) + (len(numbers[1][:-1]) // 2)
                    queue.put(num_byte)
                    queue.put((num1, num2))
                except:
                    print("잘못된 값입니다.\n")
                    cnt -= 1
                    valid_script = False
                    break
            else:
                print("잘못된 입력입니다.\n")
                cnt -= 1
                valid_script = False
                break
            
    return queue, cnt, valid_script

# 연산
# op_code : 해당 operation code
# msg : 메시지
# scripts : 전체 명령, type = Queue
def oper(stack, msg, scripts):
    
    # scripts 큐의 front 값으로 op_code 판단
    op_code = scripts.get()
    # 올바르게 작동 중인지 체크
    valid = True
    # 해시 값 push
    # 올바른 op_code 일 때, 해당 바이트만큼의 값을 push
    # ex. op_code = 0x02, scripts = 0x01 0x02 0x03
    # 0x0203 = 515 를 stack에 push
    if op_code >= 0x01 and op_code <=0x4B:
        print("push 입니다.")
        num = scripts.get()
        stack.append(num)
        print_stack(stack)
        
        return stack, valid
    
    # OP_DUP
    # 스택의 top 값을 복사
    elif op_code == 0x76:
        print("duplicate 입니다.")
        st_top = stack[-1]
        stack.append(st_top)
        
        print_stack(stack)
        
        return stack, valid
    
    # OP_HASH
    # 스택의 top 값에 LSH256 적용
    # LSH 라이브러리에 적용 시 32바이트로 입력
    # ex. 1 = b'\x00\x00\.....\x01'
    elif op_code == 0xAA:
        print("hash 입니다.")
        pubkey = stack.pop()
        Qx = pubkey[0]
        Qy = pubkey[1]
        Qx_bytes = Qx.to_bytes(32, 'big')
        Qy_bytes = Qy.to_bytes(32, 'big')
        Hash_Qx = ECDSA.Hashing(Qx_bytes)
        Hash_Qy = ECDSA.Hashing(Qy_bytes)
        
        Hash_Qx = ''.join(format(x, '02x') for x in Hash_Qx)
        Hash_Qy = ''.join(format(x, '02x') for x in Hash_Qy)
        Hash_Qx = int('0x' + Hash_Qx, 16)
        Hash_Qy = int('0x' + Hash_Qy, 16) 
        
        pubkeyHash = (Hash_Qx, Hash_Qy)
        stack.append(pubkeyHash)
        
        print_stack(stack)
        
        return stack, valid
    
    # OP_EQUALVERIFY
    # 해시 값 검증
    elif op_code == 0x88:
        print("equal and verify 입니다.")
        hash1 = stack.pop()
        hash2 = stack.pop()
        
        if hash1 ==  hash2:
            print("hash 값이 일치합니다.")
        else:
            valid = False
            print("hash 값이 일치하지 않습니다.")
        
        print_stack(stack)
        return stack, valid
    
    # OP_CHECKSIG
    # 서명 검증
    elif op_code == 0xAC:
        print("check signature 입니다.")
        pubkey = stack.pop()
        sig = stack.pop()
        verifying = ECDSA.sig_verification(sig, pubkey, msg)
        
        if verifying == True:
            print("서명 검증에 성공하였습니다.")
            stack.append("True")
        else:
            valid = False
            print("서명 검증에 실패하였습니다.")
            stack.append("False")
        
        print_stack(stack)
        return stack, valid
    
    else:
        print("올바르지 않은 명령어(op_code)입니다.")
        valid = False
        print_stack(stack)
        return stack, valid
        
