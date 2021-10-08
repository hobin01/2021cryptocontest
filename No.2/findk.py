from bitstring import BitArray
import prince
import findk1xork0prime

def find_k0(k0prime):
    k0 = k0prime << 1
    if k0prime[0]:
        k0 = k0 ^ BitArray('0x0000000000000001')
    if k0[0]:
        k0 = k0 ^ BitArray('0x0000000000000002')
    return k0

### k0 = 0x687a717a7a6c7073
### k1 = 0x7567737568637072
### k = 0x687a717a7a6c70737567737568637072
def find_k():
    ### k1 ^ k0prime = 0xc15a4bc85555484b
    k1xork0prime = findk1xork0prime.find_k1xork0prime()

    a = [BitArray('0x61'), BitArray('0x62'), BitArray('0x63'), BitArray('0x64'), BitArray('0x65'), BitArray('0x66'), BitArray('0x67'), BitArray('0x68'),
         BitArray('0x69'), BitArray('0x6a'), BitArray('0x6b'), BitArray('0x6c'), BitArray('0x6d'), BitArray('0x6e'), BitArray('0x6f')]
    b = [BitArray('0x70'), BitArray('0x71'), BitArray('0x72'), BitArray('0x73'), BitArray('0x74'), BitArray('0x75'),
         BitArray('0x76'), BitArray('0x77'), BitArray('0x78'), BitArray('0x79'), BitArray('0x7a')]

    for i1 in b:
        for i2 in a:
            for i3 in b:
                for i4 in b:
                    for i5 in a:
                        for i6 in a:
                            for i7 in b:
                                for i8 in b:
                                    k1 = i1 + i2 + i3 + i4 + i5 + i6 + i7 + i8
                                    k0prime = k1 ^ k1xork0prime
                                    k0 = find_k0(k0prime)
                                    if prince.Prince_Enc(prince.pt[0], k0 + k1) == prince.ct[0]:
                                        return k0 + k1

def check():
    flag = True
    ### k = 0x687a717a7a6c70737567737568637072
    k = find_k()

    for i in range(len(pt)):
        if prince.Prince_Enc(prince.pt[i], k) != prince.ct[i]:
            flag = False

    return flag
