from bitstring import BitArray
import prince

def find_k1xork0prime():
    new_ct = []
    for i in range(0, 80*256):
        new_ct.append(prince.ct[i] ^ prince.RC[3])

    ### k1 ^ k0prime
    k1xork0primelist = [set([i for i in range(16)]) for _ in range(16)]
    k1xork0prime = BitArray()

    for t in range(5):
        for i in range(16):
            checklist = set()
            for j in range(16):
                summ = BitArray('0x0')
                for k in range(16 * t, 16 * (t + 1)):
                    summ = summ ^ prince.S[int((new_ct[k][4 * i:4 * (i + 1)] ^ BitArray(str(hex(j)))).hex, 16)]
                if summ == BitArray('0x0'):
                    checklist.add(j)
            k1xork0primelist[i] = k1xork0primelist[i] & checklist

    ### k1 ^ k0prime = 0xc15a4bc85555484b
    for i in range(16):
        k1xork0prime = k1xork0prime + BitArray(str(hex(list(k1xork0primelist[i])[0])))

    return k1xork0prime
