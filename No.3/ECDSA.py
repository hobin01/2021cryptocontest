# -*- coding: utf-8 -*-

# ECC P256r1

# 필요 모듈 import
from lsh import LSHDigest
import random

# recommended parameter (SEC2)
# ECC : y^2 = x^3+ax+b over F(p)

p = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
a = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC
b = 0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B

# random seed
S = 0xC49D360886E704936A6678E1139D26B7819F7E90
random.seed(S)

# generating point
Gx = 0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296
Gy = 0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5

# order
n = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551

# inverse of num (modulo mod) 계산
def inverse(num, mod):
    r1, r2 = num, mod
    t1, t2 = 1, 0
    while (r2 > 0):
        q = r1//r2
        r = (r1 - q * r2) % mod
        r1, r2 = r2, r
        t = (t1 - q * t2) % mod
        t1, t2 = t2, t
    return t1 % mod

# 2*(Qx, Qy) 계산
def doubling(Qx, Qy, Fp, Ea):
    # EC : y^2 = x^3 + ax + b over F(p)
    # parameter Fp = p, Ea = a in above function
    # result is pre-calculated result
    lambda_= ((3 * Qx * Qx + Ea) * inverse(2 * Qy, Fp)) % Fp
    x_res = (lambda_**2 - 2 * Qx) % Fp
    y_res = ((Qx - x_res) * lambda_ - Qy) % Fp
    result = (x_res, y_res)
    return result

# (Px, Py) + (Qx, Qy) 계산
# Fp는 doubling의 Fp와 동일
def add(Px, Py, Qx, Qy, Fp):
    lambda_ = ((Qy - Py) * (inverse(Qx - Px, Fp))) % Fp
    x_res = (lambda_**2 - Px - Qx) % Fp
    y_res = ((Px - x_res) * lambda_ - Py) % Fp
    result = (x_res, y_res)
    return result

# k * (Qx, Qy) 계산, shamir trick 이용
# Fp, Ea는 doubling의 Fp, Ea와 동일
def multiple(Qx, Qy, k, Fp, Ea):
    bin_k = bin(k)[2:]
    result = (Qx, Qy)
    for i in range(1, len(bin_k)):
        if bin_k[i] == '1':
            result = doubling(result[0], result[1], Fp, Ea)
            result = add(result[0], result[1], Qx, Qy, Fp)
        else:
            result = doubling(result[0], result[1], Fp, Ea)
    return result

# 특정인 A의 키 쌍 만들기
# (개인키, 공개키)
def make_key():
    global p, a, b, S, Gx, Gy, n
    PrivateKey = random.randint(1, n-1)
    (Qx, Qy) = multiple(Gx, Gy, PrivateKey, p, a)
    PublicKey = (Qx, Qy)
    result = (PrivateKey, PublicKey)
    return result

# LSH256 해시 함수를 이용해 메시지 해싱
def Hashing(msg):
    Lsh = LSHDigest.getInstance(256, 256)
    if type(msg) is str:
        msg = msg.encode('utf-8')
    Lsh.update(msg)
    Hash = Lsh.final()
    return Hash
    
# 서명 생성
def make_signature(msg, d):
    # msg : message, d : private key
    global p, a, b, S, Gx, Gy, n
    
    # LSH 해쉬 함수를 이용한 msg 해쉬 결과 = Hash (type=bytearray)
    Hash = Hashing(msg)
    
    # 서명 생성
    # 계산의 편의를 위해 Hash를 int로 변경 (e)
    e = ''.join(format(x, '02x') for x in Hash)
    e = int('0x'+e, 16)
    
    Ln = len(bin(n)) - 2 # bin(n) = '0b....'
    
    z = bin(e)[:Ln + 2] # bin(e) = '0b...'
    z = int(z, 2)
    
    r, s = 0, 0
    
    while True:
        # shamir trick 이용해 k * g 계산
        k = random.randint(1,n-1)
        (x, y) = multiple(Gx, Gy, k, p, a)
        
        # r = x (mod n) 계산
        r = x % n
        
        # s = k^(-1) * (z + rd) (mod n) 계산
        inverse_k = inverse(k, n)
        s = (inverse_k * (z + r * d)) % n 
        
        if r != 0 and s != 0:
            break
    
    signature1 = (r, s)
    signature2 = (r, ((-1)*s) % n)
    signature = (signature1, signature2)
    return signature

# 서명 검증
def sig_verification(sig, Q, msg):
    # sig : signature, Q : public key, msg : message
    global p, a, b, S, Gx, Gy, n
    
    # Q : 곡선 위의 점 인증
    Qx, Qy = Q[0], Q[1]
    # Q = O(무한 원점) 인지 확인
    # Q + Q = Q 이면 Q는 O
    if doubling(Qx, Qy, p, a) == Q:
        print("Public key Q is O")
        return False
    
    # Q가 곡선 위의 점인지 확인
    # EC : y^2 = x^3 + ax + b over F(p)
    if (Qy**2) % p != (Qx**3 + a * Qx + b) % p:
        print("Q is not in curve")
        return False
    
    # n * Q = O 인지 확인
    # n * Q + Q = Q 이면 n * Q = O
    nQ = multiple(Qx, Qy, n, p, a)
    if add(nQ[0], nQ[1], Qx, Qy, p) == Q:
        print("n*Q is O")
        return False
    
    # 서명 유효성 인증
    r, s = sig[0], sig[1]
    
    # r, s in [1, n-1] 인지 확인
    if r < 1 or r > n or s < 1 or s > n:
        print("r, s is not in [1, n-1]")
        return False
    
    # LSH 해쉬 함수를 이용한 msg 해쉬 결과 = Hash (type=bytearray)
    Hash = Hashing(msg)
    
    # 계산의 편의를 위해 Hash를 int로 변경 (e)
    e = ''.join(format(x, '02x') for x in Hash)
    e = int('0x'+e, 16)
    
    Ln = len(bin(n)) - 2 # bin(n) = '0b....'
    
    z = bin(e)[:Ln + 2] # bin(e) = '0b...'
    z = int(z, 2)
    
    # u1, v1 = zw, u2, v2 = rw 계산, w = s^(-1) mod n
    w1 = inverse(s, n)
    u1 = (z * w1) % n
    u2 = (r * w1) % n
    
    # (x1, y1) = u1 * G + u2 * Q 계산
    # (x1, y1) = O (무한원점) 이면 무효
    (x1, y1) = (0, 0)
    u1xG = multiple(Gx, Gy, u1, p, a)
    u2xQ = multiple(Qx, Qy, u2, p, a)
    
    (x1, y1) = add(u1xG[0], u1xG[1], u2xQ[0], u2xQ[1], p)
    
    if doubling(x1, y1, p, a) == (x1, y1) : 
        print("(x1, y1) is O")
        return False
    
    # 최종 검증
    if (r % n == x1 % n):
        print("signature is valid")
        return True
    else:
        print("signature is invalid")
        return False
         
    
    
    