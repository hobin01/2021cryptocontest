from bitstring import BitArray

def Prince_Enc(P, K):
    k0, k0prime, k1 = KeyExpansion(K)
    
    C = P ^ k0
    
    C = C ^ k1 ^ RC[0]

    C = sbox(C, S)
    C = M_Layer(C) ^ RC[1] ^ k1

    C = sbox(C, S)
    C = Mprime_Layer(C)
    C = sbox(C, Sinv)

    C = C ^ RC[2] ^ k1
    C = Minv_Layer(C)
    C = sbox(C, Sinv)

    C = C ^ RC[3] ^ k1
    
    C = C ^ k0prime

    return C

def Prince_Dec(C, K):
    k0, k0prime, k1 = KeyExpansion(K)
    
    P = C ^ k0prime
    
    P = P ^ k1 ^ RC[3]

    P = sbox(P, S)
    P = M_Layer(P) ^ RC[2] ^ k1

    P = sbox(P, S)
    P = Mprime_Layer(P)
    P = sbox(P, Sinv)

    P = P ^ RC[1] ^ k1
    P = Minv_Layer(P)
    P = sbox(P, Sinv)

    P = P ^ RC[0] ^ k1
    
    P = P ^ k0

    return P

def KeyExpansion(K):
    k0 = K[  0: 64]
    k0prime = k0.copy()
    k0prime.ror(1)
    k0prime = k0prime ^ (k0 >> 63)
    k1 = K[ 64:128]
    return k0, k0prime, k1

def sbox(data, box):
    ret = BitArray()
    for nibble in data.cut(4):
        ret.append(box[int(nibble.hex, 16)])
    return ret

def M_Layer(C):
    C = Mprime_Layer(C)
    C = shiftrows(C, False)
    return C

def Minv_Layer(C):    
    C = shiftrows(C, True)
    C = Mprime_Layer(C)
    return C

def Mprime_Layer(data):
    ret = BitArray(length = 64)
    ret[ 0:16] = m0(data[ 0:16])
    ret[16:32] = m1(data[16:32])
    ret[32:48] = m1(data[32:48])
    ret[48:64] = m0(data[48:64])
    return ret

def m0(data):
    ret = BitArray(length = 16)
    ret[ 0] = data[4] ^ data[ 8] ^ data[12]
    ret[ 1] = data[1] ^ data[ 9] ^ data[13]
    ret[ 2] = data[2] ^ data[ 6] ^ data[14]
    ret[ 3] = data[3] ^ data[ 7] ^ data[11]
    ret[ 4] = data[0] ^ data[ 4] ^ data[ 8]
    ret[ 5] = data[5] ^ data[ 9] ^ data[13]
    ret[ 6] = data[2] ^ data[10] ^ data[14]
    ret[ 7] = data[3] ^ data[ 7] ^ data[15]
    ret[ 8] = data[0] ^ data[ 4] ^ data[12]
    ret[ 9] = data[1] ^ data[ 5] ^ data[ 9]
    ret[10] = data[6] ^ data[10] ^ data[14]
    ret[11] = data[3] ^ data[11] ^ data[15]
    ret[12] = data[0] ^ data[ 8] ^ data[12]
    ret[13] = data[1] ^ data[ 5] ^ data[13]
    ret[14] = data[2] ^ data[ 6] ^ data[10]
    ret[15] = data[7] ^ data[11] ^ data[15]
    return ret

def m1(data):
    ret = BitArray(length = 16)
    ret[ 0] = data[0] ^ data[ 4] ^ data[ 8]
    ret[ 1] = data[5] ^ data[ 9] ^ data[13]
    ret[ 2] = data[2] ^ data[10] ^ data[14]
    ret[ 3] = data[3] ^ data[ 7] ^ data[15]
    ret[ 4] = data[0] ^ data[ 4] ^ data[12]
    ret[ 5] = data[1] ^ data[ 5] ^ data[ 9]
    ret[ 6] = data[6] ^ data[10] ^ data[14]
    ret[ 7] = data[3] ^ data[11] ^ data[15]
    ret[ 8] = data[0] ^ data[ 8] ^ data[12]
    ret[ 9] = data[1] ^ data[ 5] ^ data[13]
    ret[10] = data[2] ^ data[ 6] ^ data[10]
    ret[11] = data[7] ^ data[11] ^ data[15]
    ret[12] = data[4] ^ data[ 8] ^ data[12]
    ret[13] = data[1] ^ data[ 9] ^ data[13]
    ret[14] = data[2] ^ data[ 6] ^ data[14]
    ret[15] = data[3] ^ data[ 7] ^ data[11]
    return ret

def shiftrows(data, inverse):
    ret = BitArray(length = 64)
    idx = 0
    for nibble in data.cut(4):
        ret[idx * 4:(idx + 1) * 4] = nibble
        if not inverse:
            idx = (idx + 13) % 16
        else:
            idx = (idx +  5) % 16
    return ret

RC = (BitArray(hex = '0x0000000000000000'),
      BitArray(hex = '0x13198a2e03707344'),
      BitArray(hex = '0xa4093822299f31d0'),
      BitArray(hex = '0x082efa98ec4e6c89'))

S = ('0xb', '0xf', '0x3', '0x2', '0xa', '0xc', '0x9', '0x1',
     '0x6', '0x7', '0x8', '0x0', '0xe', '0x5', '0xd', '0x4')

Sinv = ('0xb', '0x7', '0x3', '0x2', '0xf', '0xd', '0x8', '0x9',
        '0xa', '0x6', '0x4', '0x0', '0x5', '0xe', '0xc', '0x1')

def test():
    testvector1p = BitArray(hex = '0x0000000000000000')
    testvector1k = BitArray(hex = '0x00000000000000000000000000000000')
    testvector1c = BitArray(hex = '0xE35168F91283502C')
    print('Testvector 1의 암호문 :', Prince_Enc(testvector1p, testvector1k))
    print('Testvector 1의 평문   :', Prince_Dec(testvector1c, testvector1k))
    testvector2p = BitArray(hex = '0xFFFFFFFFFFFFFFFF')
    testvector2k = BitArray(hex = '0x00000000000000000000000000000000')
    testvector2c = BitArray(hex = '0x96775187FC6A9943')
    print('Testvector 2의 암호문 :', Prince_Enc(testvector2p, testvector2k))
    print('Testvector 2의 평문   :', Prince_Dec(testvector2c, testvector2k))
    testvector3p = BitArray(hex = '0x0000000000000000')
    testvector3k = BitArray(hex = '0xFFFFFFFFFFFFFFFF0000000000000000')
    testvector3c = BitArray(hex = '0x6988AE78039566BD')
    print('Testvector 3의 암호문 :', Prince_Enc(testvector3p, testvector3k))
    print('Testvector 3의 평문   :', Prince_Dec(testvector3c, testvector3k))
    testvector4p = BitArray(hex = '0x0000000000000000')
    testvector4k = BitArray(hex = '0x0000000000000000FFFFFFFFFFFFFFFF')
    testvector4c = BitArray(hex = '0xC611A0EC10C574E4')
    print('Testvector 4의 암호문 :', Prince_Enc(testvector4p, testvector4k))
    print('Testvector 4의 평문   :', Prince_Dec(testvector4c, testvector4k))
    testvector5p = BitArray(hex = '0x0123456789ABCDEF')
    testvector5k = BitArray(hex = '0x0000000000000000FEDCBA9876543210')
    testvector5c = BitArray(hex = '0x2579F2F660306F5E')
    print('Testvector 5의 암호문 :', Prince_Enc(testvector5p, testvector5k))
    print('Testvector 5의 평문   :', Prince_Dec(testvector5c, testvector5k))
    testvector6p = BitArray(hex = '0x0123456789ABCDEF')
    testvector6k = BitArray(hex = '0xFFFFFFFFFFFFFFFFFEDCBA9876543210')
    testvector6c = BitArray(hex = '0xE31CF8A9AE6A50C7')
    print('Testvector 6의 암호문 :', Prince_Enc(testvector6p, testvector6k))
    print('Testvector 6의 평문   :', Prince_Dec(testvector6c, testvector6k))
    
def READ(pt, ct):
    f = open('pt.dat', 'rb')
    data = BitArray(f.read())
    for i in range(len(data) // 64):
        tmp = BitArray()
        for j in range(8):
            tmp.append(data[64 * i + 64 - 8 * (j + 1):64 * i + 64 - 8 * j])
        pt.append(tmp)
    f.close()

    f = open('ct.dat', 'rb')
    data = BitArray(f.read())
    for i in range(len(data) // 64):
        tmp = BitArray()
        for j in range(8):
            tmp.append(data[64 * i + 64 - 8 * (j + 1):64 * i + 64 - 8 * j])
        ct.append(tmp)
    f.close()

pt, ct = [], []
READ(pt, ct)
