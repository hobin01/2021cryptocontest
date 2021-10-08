from bitstring import BitArray

def Hash(M):
    IV = BitArray(hex = '0x88888888888888889999999999999999')
    CV = IV
    m = len(M) // 256
    for i in range(m):
        CV = Compression(CV, M[256 * i:256 * (i + 1)])
    return CV

def Compression(CV, M):
    C = Midori64(CV[  0: 64], M[  0:128] ^ CV) + Midori64(CV[ 64:128], M[128:256] ^ CV)
    C = C ^ M[  0:128] ^ M[128:256]
    CV = MIX(C)
    return CV

def MIX(C):
    tmp = BitArray(length = 128)
    tmp[  0: 32] = C[  0: 32]
    tmp[ 32: 64] = C[ 96:128]
    tmp[ 64: 96] = C[ 64: 96]
    tmp[ 96:128] = C[ 32: 64]
    return tmp

def Midori64(M, K):
    WK, RK = RoundKeyGen(K)
    return MidoriCore(M, WK, RK)

def MidoriCore(X, WK, RK):
    S = X ^ WK    
    for i in range(15):
        S = SubCell(S)
        S = ShuffleCell(S)
        S = MixColumn(S)
        S = S ^ RK[i]
    S = SubCell(S)
    Y = S ^ WK
    return Y

def SubCell(S):
    ret = BitArray()
    for nibble in S.cut(4):
        ret.append(Sb0[int(nibble.hex, 16)])
    return ret

def ShuffleCell(S):
    tmp = BitArray(length = 64)
    tmp[ 0: 4] = S[ 0: 4]
    tmp[ 4: 8] = S[40:44]
    tmp[ 8:12] = S[20:24]
    tmp[12:16] = S[60:64]
    tmp[16:20] = S[56:60]
    tmp[20:24] = S[16:20]
    tmp[24:28] = S[44:48]
    tmp[28:32] = S[ 4: 8]
    tmp[32:36] = S[36:40]
    tmp[36:40] = S[12:16]
    tmp[40:44] = S[48:52]
    tmp[44:48] = S[24:28]
    tmp[48:52] = S[28:32]
    tmp[52:56] = S[52:56]
    tmp[56:60] = S[ 8:12]
    tmp[60:64] = S[32:36]
    return tmp

def MixColumn(S):
    ret = BitArray()
    for nibble in S.cut(16):
        ret.append(Matrix(nibble))
    return ret
        
def Matrix(data):
    ret = BitArray(length = 16)
    ret[ 0: 4] = data[ 4: 8] ^ data[ 8:12] ^ data[12:16]
    ret[ 4: 8] = data[ 0: 4] ^ data[ 8:12] ^ data[12:16]
    ret[ 8:12] = data[ 0: 4] ^ data[ 4: 8] ^ data[12:16]
    ret[12:16] = data[ 0: 4] ^ data[ 4: 8] ^ data[ 8:12]
    return ret
    
def RoundKeyGen(K):
    WK = K[  0: 64] ^ K[ 64:128]
    RK = [BitArray()] * 15
    for i in range(15):
        RK[i] = K[64 * (i % 2): 64 * (i % 2 + 1)] ^ BitArray(hex = alpha[i
                                                                         ])
    return WK, RK

Sb0 = ['0xc', '0xa', '0xd', '0x3', '0xe', '0xb', '0xf', '0x7', '0x8', '0x9', '0x1', '0x5', '0x0', '0x2', '0x4', '0x6']
alpha = ['0x0001010110110011', '0x0111100011000000', '0x1010010000110101', '0x0110001000010011', '0001000001001111'
         , '0x1101000101110000', '0x0000001001100110', '0x0000101111001100', '0x1001010010000001', '0x0100000010111000'
         , '0x0111000110010111', '0x0010001010001110', '0x0101000100110000', '0x1111100011001010', '0x1101111110010000']

def test():
    testvector1 = BitArray(length = 256)
    print('Test Vector 1 해시 값 :', Hash(testvector1))
    testvector2 = BitArray(length = 512)
    print('Test Vector 2 해시 값 :', Hash(testvector2))
    testvector3 = BitArray(hex = '0x000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f')
    print('Test Vector 3 해시 값 :', Hash(testvector3))

def collision():
    c1 = BitArray('0x88888888888888889999999999999999888888888888888899999999999999999998899898999988888998898988889999988998989999888889988989888899')
    c2 = BitArray('0x9998899898999988888998898988889999988998989999888889988989888899')
    print(Hash(c1) == Hash(c2))
