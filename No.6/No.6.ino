#pragma GCC optimize ("-O3")

typedef unsigned char u8;
typedef unsigned short u16;
//typedef unsigned int u32;

// round: #128
#define NUM_ROUND 128

// key_gen constant
#define CONST_VAL 0xab00cd00

// rotation left
#define ROL(X) ((X<<1) | (X>>31))

// s_box: 4-bit x #16
u32 s_box[16] = {0x3, 0x9, 0x6, 0xf, 0xe, 0x5, 0xd, 0x4, 0xc, 0x7, 0xa, 0x2, 0xb, 0x1, 0x8, 0x0};

// key generation
void new_bs_keygen(u32* r_key, u32 m_key){
  
  u32 m_key_table[4] = {m_key, m_key+32, m_key+64, m_key+96};
  
  r_key[0] = m_key_table[0] ^ 0xAB00CD00;
  r_key[32] = m_key_table[1] ^ 0xAB00CD00;
  r_key[64] = m_key_table[2] ^ 0xAB00CD00;
  r_key[96] = m_key_table[3] ^ 0xAB00CD00;
  
  r_key[1] = ++m_key_table[0] ^ 0x56019A01;
  r_key[33] = ++m_key_table[1] ^ 0x56019A01;
  r_key[65] = ++m_key_table[2] ^ 0x56019A01;
  r_key[97] = ++m_key_table[3] ^ 0x56019A01;
  
  r_key[2] = ++m_key_table[0] ^ 0xAC033402;
  r_key[34] = ++m_key_table[1] ^ 0xAC033402;
  r_key[66] = ++m_key_table[2] ^ 0xAC033402;
  r_key[98] = ++m_key_table[3] ^ 0xAC033402;
  
  r_key[3] = ++m_key_table[0] ^ 0x58066805;
  r_key[35] = ++m_key_table[1] ^ 0x58066805;
  r_key[67] = ++m_key_table[2] ^ 0x58066805;
  r_key[99] = ++m_key_table[3] ^ 0x58066805;
  
  r_key[4] = ++m_key_table[0] ^ 0xB00CD00A;
  r_key[36] = ++m_key_table[1] ^ 0xB00CD00A;
  r_key[68] = ++m_key_table[2] ^ 0xB00CD00A;
  r_key[100] = ++m_key_table[3] ^ 0xB00CD00A;
  
  r_key[5] = ++m_key_table[0] ^ 0x6019A015;
  r_key[37] = ++m_key_table[1] ^ 0x6019A015;
  r_key[69] = ++m_key_table[2] ^ 0x6019A015;
  r_key[101] = ++m_key_table[3] ^ 0x6019A015;
  
  r_key[6] = ++m_key_table[0] ^ 0xC033402A;
  r_key[38] = ++m_key_table[1] ^ 0xC033402A;
  r_key[70] = ++m_key_table[2] ^ 0xC033402A;
  r_key[102] = ++m_key_table[3] ^ 0xC033402A;
  
  r_key[7] = ++m_key_table[0] ^ 0x80668055;
  r_key[39] = ++m_key_table[1] ^ 0x80668055;
  r_key[71] = ++m_key_table[2] ^ 0x80668055;
  r_key[103] = ++m_key_table[3] ^ 0x80668055;
  
  r_key[8] = ++m_key_table[0] ^ 0xCD00AB;
  r_key[40] = ++m_key_table[1] ^ 0xCD00AB;
  r_key[72] = ++m_key_table[2] ^ 0xCD00AB;
  r_key[104] = ++m_key_table[3] ^ 0xCD00AB;
  
  r_key[9] = ++m_key_table[0] ^ 0x19A0156;
  r_key[41] = ++m_key_table[1] ^ 0x19A0156;
  r_key[73] = ++m_key_table[2] ^ 0x19A0156;
  r_key[105] = ++m_key_table[3] ^ 0x19A0156;
  
  r_key[10] = ++m_key_table[0] ^ 0x33402AC;
  r_key[42] = ++m_key_table[1] ^ 0x33402AC;
  r_key[74] = ++m_key_table[2] ^ 0x33402AC;
  r_key[106] = ++m_key_table[3] ^ 0x33402AC;
  
  r_key[11] = ++m_key_table[0] ^ 0x6680558;
  r_key[43] = ++m_key_table[1] ^ 0x6680558;
  r_key[75] = ++m_key_table[2] ^ 0x6680558;
  r_key[107] = ++m_key_table[3] ^ 0x6680558;
  
  r_key[12] = ++m_key_table[0] ^ 0xCD00AB0;
  r_key[44] = ++m_key_table[1] ^ 0xCD00AB0;
  r_key[76] = ++m_key_table[2] ^ 0xCD00AB0;
  r_key[108] = ++m_key_table[3] ^ 0xCD00AB0;
  
  r_key[13] = ++m_key_table[0] ^ 0x19A01560;
  r_key[45] = ++m_key_table[1] ^ 0x19A01560;
  r_key[77] = ++m_key_table[2] ^ 0x19A01560;
  r_key[109] = ++m_key_table[3] ^ 0x19A01560;
  
  r_key[14] = ++m_key_table[0] ^ 0x33402AC0;
  r_key[46] = ++m_key_table[1] ^ 0x33402AC0;
  r_key[78] = ++m_key_table[2] ^ 0x33402AC0;
  r_key[110] = ++m_key_table[3] ^ 0x33402AC0;
  
  r_key[15] = ++m_key_table[0] ^ 0x66805580;
  r_key[47] = ++m_key_table[1] ^ 0x66805580;
  r_key[79] = ++m_key_table[2] ^ 0x66805580;
  r_key[111] = ++m_key_table[3] ^ 0x66805580;
  
  r_key[16] = ++m_key_table[0] ^ 0xCD00AB00;
  r_key[48] = ++m_key_table[1] ^ 0xCD00AB00;
  r_key[80] = ++m_key_table[2] ^ 0xCD00AB00;
  r_key[112] = ++m_key_table[3] ^ 0xCD00AB00;
  
  r_key[17] = ++m_key_table[0] ^ 0x9A015601;
  r_key[49] = ++m_key_table[1] ^ 0x9A015601;
  r_key[81] = ++m_key_table[2] ^ 0x9A015601;
  r_key[113] = ++m_key_table[3] ^ 0x9A015601;
  
  r_key[18] = ++m_key_table[0] ^ 0x3402AC03;
  r_key[50] = ++m_key_table[1] ^ 0x3402AC03;
  r_key[82] = ++m_key_table[2] ^ 0x3402AC03;
  r_key[114] = ++m_key_table[3] ^ 0x3402AC03;
  
  r_key[19] = ++m_key_table[0] ^ 0x68055806;
  r_key[51] = ++m_key_table[1] ^ 0x68055806;
  r_key[83] = ++m_key_table[2] ^ 0x68055806;
  r_key[115] = ++m_key_table[3] ^ 0x68055806;
  
  r_key[20] = ++m_key_table[0] ^ 0xD00AB00C;
  r_key[52] = ++m_key_table[1] ^ 0xD00AB00C;
  r_key[84] = ++m_key_table[2] ^ 0xD00AB00C;
  r_key[116] = ++m_key_table[3] ^ 0xD00AB00C;
  
  r_key[21] = ++m_key_table[0] ^ 0xA0156019;
  r_key[53] = ++m_key_table[1] ^ 0xA0156019;
  r_key[85] = ++m_key_table[2] ^ 0xA0156019;
  r_key[117] = ++m_key_table[3] ^ 0xA0156019;
  
  r_key[22] = ++m_key_table[0] ^ 0x402AC033;
  r_key[54] = ++m_key_table[1] ^ 0x402AC033;
  r_key[86] = ++m_key_table[2] ^ 0x402AC033;
  r_key[118] = ++m_key_table[3] ^ 0x402AC033;
  
  r_key[23] = ++m_key_table[0] ^ 0x80558066;
  r_key[55] = ++m_key_table[1] ^ 0x80558066;
  r_key[87] = ++m_key_table[2] ^ 0x80558066;
  r_key[119] = ++m_key_table[3] ^ 0x80558066;
  
  r_key[24] = ++m_key_table[0] ^ 0xAB00CD;
  r_key[56] = ++m_key_table[1] ^ 0xAB00CD;
  r_key[88] = ++m_key_table[2] ^ 0xAB00CD;
  r_key[120] = ++m_key_table[3] ^ 0xAB00CD;
  
  r_key[25] = ++m_key_table[0] ^ 0x156019A;
  r_key[57] = ++m_key_table[1] ^ 0x156019A;
  r_key[89] = ++m_key_table[2] ^ 0x156019A;
  r_key[121] = ++m_key_table[3] ^ 0x156019A;
  
  r_key[26] = ++m_key_table[0] ^ 0x2AC0334;
  r_key[58] = ++m_key_table[1] ^ 0x2AC0334;
  r_key[90] = ++m_key_table[2] ^ 0x2AC0334;
  r_key[122] = ++m_key_table[3] ^ 0x2AC0334;
  
  r_key[27] = ++m_key_table[0] ^ 0x5580668;
  r_key[59] = ++m_key_table[1] ^ 0x5580668;
  r_key[91] = ++m_key_table[2] ^ 0x5580668;
  r_key[123] = ++m_key_table[3] ^ 0x5580668;
  
  r_key[28] = ++m_key_table[0] ^ 0xAB00CD0;
  r_key[60] = ++m_key_table[1] ^ 0xAB00CD0;
  r_key[92] = ++m_key_table[2] ^ 0xAB00CD0;
  r_key[124] = ++m_key_table[3] ^ 0xAB00CD0;
  
  r_key[29] = ++m_key_table[0] ^ 0x156019A0;
  r_key[61] = ++m_key_table[1] ^ 0x156019A0;
  r_key[93] = ++m_key_table[2] ^ 0x156019A0;
  r_key[125] = ++m_key_table[3] ^ 0x156019A0;
  
  r_key[30] = ++m_key_table[0] ^ 0x2AC03340;
  r_key[62] = ++m_key_table[1] ^ 0x2AC03340;
  r_key[94] = ++m_key_table[2] ^ 0x2AC03340;
  r_key[126] = ++m_key_table[3] ^ 0x2AC03340;
  
  r_key[31] = ++m_key_table[0] ^ 0x55806680;
  r_key[63] = ++m_key_table[1] ^ 0x55806680;
  r_key[95] = ++m_key_table[2] ^ 0x55806680;
  r_key[127] = ++m_key_table[3] ^ 0x55806680;
}

/*
u32 s_box_gen(u32 text){
  u32 output = 0;
  u32 temp = 0;
  int i = 0;
   
  for(i=0;i<8;i++){
    temp = ( ( text >> (4*i) ) & 0x0000000F );
    temp = s_box[temp];
    output = (output | ( temp << (4*i) ) );
 }
 return output;
}

u32 p_box1_gen(u32 text){
  u32 p_idx[32] = {0, 8, 16, 24, 1, 9, 17, 25, 2, 10, 18, 26, 3, 11, 19, 27, 4, 12, 20, 28, 5, 13, 21, 29, 6, 14, 22, 30, 7, 15, 23, 31};
  u32 output = 0;
  u32 temp = 0;
  int i = 0;
 
  for(i=0;i<32;i++){
    temp = ((text>>i) & 0x00000001);
    temp = (temp << p_idx[i]);
    output = (output | temp);
 }
 return output;
}

u32 p_box2_gen(u32 text){
  u32 p_idx[32] = {27, 1, 23, 30, 7, 22, 29, 16, 0, 4, 13, 18, 25, 17, 28, 31, 10, 14, 3, 5, 6, 2, 12, 11, 9, 8, 19, 26, 24, 20, 15, 21};
  u32 output = 0;
  u32 temp = 0;
  int i = 0;
  for(i=0;i<32;i++){
    temp = ((text>>i) & 0x00000001);
    temp = (temp << p_idx[i]);
    output = (output | temp);
 }
 return output;
}
*/

void new_bs_enc(u32* r_key, u32* text){

  int i;

  u8 text1 = (u8)((*text) >> 24);
  u8 text2 = (u8)((*text) >> 16);
  u8 text3 = (u8)((*text) >> 8 );
  u8 text4 = (u8)(*text);

  u8 num1; u8 num2; u8 num3; u8 num4;

  for(i = 0; i < NUM_ROUND; i+=4){
    // sbox_gen with bit slicing
    num1 = ((text1 & 0x80)        | ((text1 & 0x08) << 3) | ((text2 & 0x80) >> 2) | ((text2 & 0x08) << 1) | ((text3 & 0x80) >> 4) | ((text3 & 0x08) >> 1) | ((text4 & 0x80) >> 6) | ((text4 & 0x08) >> 3));
    num2 = (((text1 & 0x40) << 1) | ((text1 & 0x04) << 4) | ((text2 & 0x40) >> 1) | ((text2 & 0x04) << 2) | ((text3 & 0x40) >> 3) | (text3 & 0x04)        | ((text4 & 0x40) >> 5) | ((text4 & 0x04) >> 2));
    num3 = (((text1 & 0x20) << 2) | ((text1 & 0x02) << 5) | (text2 & 0x20)        | ((text2 & 0x02) << 3) | ((text3 & 0x20) >> 2) | ((text3 & 0x02) << 1) | ((text4 & 0x20) >> 4) | ((text4 & 0x02) >> 1));
    num4 = (((text1 & 0x10) << 3) | ((text1 & 0x01) << 6) | ((text2 & 0x10) << 1) | ((text2 & 0x01) << 4) | ((text3 & 0x10) >> 1) | ((text3 & 0x01) << 2) | ((text4 & 0x10) >> 3) | (text4 & 0x01)       );
    
    // f, g, h, k
    text1 = ((~(num1 | num2) & num4) | ((num1 | num2) & ~num4));
    text2 = ((num1 & ~(num2 | num3)) | (~num1 & (num2 | num3)));
    text3 = (((~num1 | num2) & ~(num3 | num4)) | (~num2 & ((num1 & num4) | num3)));
    text4 = ((num2 & ((~num1 & num3 & ~num4) | (num1 & ~num3))) | (~num3 & num4) | (~(num1 | num2) & (~num3 | num4)));
    
    // add rkey_in
    text1 ^= (u8)(r_key[i] >> 24);
    text2 ^= (u8)(r_key[i] >> 16);
    text3 ^= (u8)(r_key[i] >> 8);
    text4 ^= (u8)(r_key[i]);
    
    // pbox2_gen
    num1 = ((text3 & 0x80)        | ((text4 & 0x08) << 3) | ((text4 & 0x40) >> 1) | ((text3 & 0x40) >> 2) | ((text4 & 0x01) << 3) | ((text1 & 0x08) >> 1) | ((text3 & 0x10) >> 3) | ((text1 & 0x10) >> 4));
    num2 = (((text4 & 0x04) << 5) | ((text4 & 0x20) << 1) | ((text1 & 0x80) >> 2) | ((text1 & 0x20) >> 1) | ((text1 & 0x04) << 1) | ((text3 & 0x08) >> 1) | ((text3 & 0x20) >> 4) | ((text4 & 0x80) >> 7));
    num3 = (((text1 & 0x40) << 1) | ((text2 & 0x02) << 5) | ((text3 & 0x04) << 3) | ((text2 & 0x40) >> 2) | ((text2 & 0x80) >> 4) | ((text2 & 0x01) << 2) | ((text1 & 0x01) << 1) | ((text1 & 0x02) >> 1));
    num4 = (((text4 & 0x10) << 3) | ((text2 & 0x10) << 2) | ((text2 & 0x08) << 2) | ((text3 & 0x02) << 3) | ((text2 & 0x04) << 1) | ((text2 & 0x20) >> 3) | (text4 & 0x02) | (text3 & 0x01));
    
    text1 = num1;
    text2 = num2;
    text3 = num3;
    text4 = num4;
    
    //=======================================================
    // sbox_gen
    num1 = ((text1 & 0x80)        | ((text1 & 0x08) << 3) | ((text2 & 0x80) >> 2) | ((text2 & 0x08) << 1) | ((text3 & 0x80) >> 4) | ((text3 & 0x08) >> 1) | ((text4 & 0x80) >> 6) | ((text4 & 0x08) >> 3));
    num2 = (((text1 & 0x40) << 1) | ((text1 & 0x04) << 4) | ((text2 & 0x40) >> 1) | ((text2 & 0x04) << 2) | ((text3 & 0x40) >> 3) | (text3 & 0x04)        | ((text4 & 0x40) >> 5) | ((text4 & 0x04) >> 2));
    num3 = (((text1 & 0x20) << 2) | ((text1 & 0x02) << 5) | (text2 & 0x20)        | ((text2 & 0x02) << 3) | ((text3 & 0x20) >> 2) | ((text3 & 0x02) << 1) | ((text4 & 0x20) >> 4) | ((text4 & 0x02) >> 1));
    num4 = (((text1 & 0x10) << 3) | ((text1 & 0x01) << 6) | ((text2 & 0x10) << 1) | ((text2 & 0x01) << 4) | ((text3 & 0x10) >> 1) | ((text3 & 0x01) << 2) | ((text4 & 0x10) >> 3) | (text4 & 0x01)       );
    
    // f, g, h, k
    text1 = ((~(num1 | num2) & num4) | ((num1 | num2) & ~num4));
    text2 = ((num1 & ~(num2 | num3)) | (~num1 & (num2 | num3)));
    text3 = (((~num1 | num2) & ~(num3 | num4)) | (~num2 & ((num1 & num4) | num3)));
    text4 = ((num2 & ((~num1 & num3 & ~num4) | (num1 & ~num3))) | (~num3 & num4) | (~(num1 | num2) & (~num3 | num4)));
    
    // add rkey_in
    text1 ^= (u8)(r_key[1 + i] >> 24);
    text2 ^= (u8)(r_key[1 + i] >> 16);
    text3 ^= (u8)(r_key[1 + i] >> 8);
    text4 ^= (u8)(r_key[1 + i]);
    
    // pbox2_gen
    num1 = ((text3 & 0x80)        | ((text4 & 0x08) << 3) | ((text4 & 0x40) >> 1) | ((text3 & 0x40) >> 2) | ((text4 & 0x01) << 3) | ((text1 & 0x08) >> 1) | ((text3 & 0x10) >> 3) | ((text1 & 0x10) >> 4));
    num2 = (((text4 & 0x04) << 5) | ((text4 & 0x20) << 1) | ((text1 & 0x80) >> 2) | ((text1 & 0x20) >> 1) | ((text1 & 0x04) << 1) | ((text3 & 0x08) >> 1) | ((text3 & 0x20) >> 4) | ((text4 & 0x80) >> 7));
    num3 = (((text1 & 0x40) << 1) | ((text2 & 0x02) << 5) | ((text3 & 0x04) << 3) | ((text2 & 0x40) >> 2) | ((text2 & 0x80) >> 4) | ((text2 & 0x01) << 2) | ((text1 & 0x01) << 1) | ((text1 & 0x02) >> 1));
    num4 = (((text4 & 0x10) << 3) | ((text2 & 0x10) << 2) | ((text2 & 0x08) << 2) | ((text3 & 0x02) << 3) | ((text2 & 0x04) << 1) | ((text2 & 0x20) >> 3) | (text4 & 0x02) | (text3 & 0x01));
    
    text1 = num1;
    text2 = num2;
    text3 = num3;
    text4 = num4;
    
    //=======================================================
    // sbox_gen
    num1 = ((text1 & 0x80)        | ((text1 & 0x08) << 3) | ((text2 & 0x80) >> 2) | ((text2 & 0x08) << 1) | ((text3 & 0x80) >> 4) | ((text3 & 0x08) >> 1) | ((text4 & 0x80) >> 6) | ((text4 & 0x08) >> 3));
    num2 = (((text1 & 0x40) << 1) | ((text1 & 0x04) << 4) | ((text2 & 0x40) >> 1) | ((text2 & 0x04) << 2) | ((text3 & 0x40) >> 3) | (text3 & 0x04)        | ((text4 & 0x40) >> 5) | ((text4 & 0x04) >> 2));
    num3 = (((text1 & 0x20) << 2) | ((text1 & 0x02) << 5) | (text2 & 0x20)        | ((text2 & 0x02) << 3) | ((text3 & 0x20) >> 2) | ((text3 & 0x02) << 1) | ((text4 & 0x20) >> 4) | ((text4 & 0x02) >> 1));
    num4 = (((text1 & 0x10) << 3) | ((text1 & 0x01) << 6) | ((text2 & 0x10) << 1) | ((text2 & 0x01) << 4) | ((text3 & 0x10) >> 1) | ((text3 & 0x01) << 2) | ((text4 & 0x10) >> 3) | (text4 & 0x01)       );
    
    // f, g, h, k
    text1 = ((~(num1 | num2) & num4) | ((num1 | num2) & ~num4));
    text2 = ((num1 & ~(num2 | num3)) | (~num1 & (num2 | num3)));
    text3 = (((~num1 | num2) & ~(num3 | num4)) | (~num2 & ((num1 & num4) | num3)));
    text4 = ((num2 & ((~num1 & num3 & ~num4) | (num1 & ~num3))) | (~num3 & num4) | (~(num1 | num2) & (~num3 | num4)));
    
    // add rkey_in
    text1 ^= (u8)(r_key[2 + i] >> 24);
    text2 ^= (u8)(r_key[2 + i] >> 16);
    text3 ^= (u8)(r_key[2 + i] >> 8);
    text4 ^= (u8)(r_key[2 + i]);
    
    // pbox2_gen
    num1 = ((text3 & 0x80)        | ((text4 & 0x08) << 3) | ((text4 & 0x40) >> 1) | ((text3 & 0x40) >> 2) | ((text4 & 0x01) << 3) | ((text1 & 0x08) >> 1) | ((text3 & 0x10) >> 3) | ((text1 & 0x10) >> 4));
    num2 = (((text4 & 0x04) << 5) | ((text4 & 0x20) << 1) | ((text1 & 0x80) >> 2) | ((text1 & 0x20) >> 1) | ((text1 & 0x04) << 1) | ((text3 & 0x08) >> 1) | ((text3 & 0x20) >> 4) | ((text4 & 0x80) >> 7));
    num3 = (((text1 & 0x40) << 1) | ((text2 & 0x02) << 5) | ((text3 & 0x04) << 3) | ((text2 & 0x40) >> 2) | ((text2 & 0x80) >> 4) | ((text2 & 0x01) << 2) | ((text1 & 0x01) << 1) | ((text1 & 0x02) >> 1));
    num4 = (((text4 & 0x10) << 3) | ((text2 & 0x10) << 2) | ((text2 & 0x08) << 2) | ((text3 & 0x02) << 3) | ((text2 & 0x04) << 1) | ((text2 & 0x20) >> 3) | (text4 & 0x02) | (text3 & 0x01));
    
    text1 = num1;
    text2 = num2;
    text3 = num3;
    text4 = num4;
    
    //=======================================================
    // sbox_gen
    num1 = ((text1 & 0x80)        | ((text1 & 0x08) << 3) | ((text2 & 0x80) >> 2) | ((text2 & 0x08) << 1) | ((text3 & 0x80) >> 4) | ((text3 & 0x08) >> 1) | ((text4 & 0x80) >> 6) | ((text4 & 0x08) >> 3));
    num2 = (((text1 & 0x40) << 1) | ((text1 & 0x04) << 4) | ((text2 & 0x40) >> 1) | ((text2 & 0x04) << 2) | ((text3 & 0x40) >> 3) | (text3 & 0x04)        | ((text4 & 0x40) >> 5) | ((text4 & 0x04) >> 2));
    num3 = (((text1 & 0x20) << 2) | ((text1 & 0x02) << 5) | (text2 & 0x20)        | ((text2 & 0x02) << 3) | ((text3 & 0x20) >> 2) | ((text3 & 0x02) << 1) | ((text4 & 0x20) >> 4) | ((text4 & 0x02) >> 1));
    num4 = (((text1 & 0x10) << 3) | ((text1 & 0x01) << 6) | ((text2 & 0x10) << 1) | ((text2 & 0x01) << 4) | ((text3 & 0x10) >> 1) | ((text3 & 0x01) << 2) | ((text4 & 0x10) >> 3) | (text4 & 0x01)       );
    
    // f, g, h, k
    text1 = ((~(num1 | num2) & num4) | ((num1 | num2) & ~num4));
    text2 = ((num1 & ~(num2 | num3)) | (~num1 & (num2 | num3)));
    text3 = (((~num1 | num2) & ~(num3 | num4)) | (~num2 & ((num1 & num4) | num3)));
    text4 = ((num2 & ((~num1 & num3 & ~num4) | (num1 & ~num3))) | (~num3 & num4) | (~(num1 | num2) & (~num3 | num4)));
    
    // add rkey_in
    text1 ^= (u8)(r_key[3 + i] >> 24);
    text2 ^= (u8)(r_key[3 + i] >> 16);
    text3 ^= (u8)(r_key[3 + i] >> 8);
    text4 ^= (u8)(r_key[3 + i]);
    
    // pbox2_gen
    num1 = ((text3 & 0x80)        | ((text4 & 0x08) << 3) | ((text4 & 0x40) >> 1) | ((text3 & 0x40) >> 2) | ((text4 & 0x01) << 3) | ((text1 & 0x08) >> 1) | ((text3 & 0x10) >> 3) | ((text1 & 0x10) >> 4));
    num2 = (((text4 & 0x04) << 5) | ((text4 & 0x20) << 1) | ((text1 & 0x80) >> 2) | ((text1 & 0x20) >> 1) | ((text1 & 0x04) << 1) | ((text3 & 0x08) >> 1) | ((text3 & 0x20) >> 4) | ((text4 & 0x80) >> 7));
    num3 = (((text1 & 0x40) << 1) | ((text2 & 0x02) << 5) | ((text3 & 0x04) << 3) | ((text2 & 0x40) >> 2) | ((text2 & 0x80) >> 4) | ((text2 & 0x01) << 2) | ((text1 & 0x01) << 1) | ((text1 & 0x02) >> 1));
    num4 = (((text4 & 0x10) << 3) | ((text2 & 0x10) << 2) | ((text2 & 0x08) << 2) | ((text3 & 0x02) << 3) | ((text2 & 0x04) << 1) | ((text2 & 0x20) >> 3) | (text4 & 0x02) | (text3 & 0x01));
  
    text1 = num1;
    text2 = num2;
    text3 = num3;
    text4 = num4;
  }

  *text = (((u32)text1 << 24) | ((u32)text2 << 16) | ((u32)text3 << 8) | (u32)text4);
}

u8 TEST_VECTOR(u32 in, u32 answer) {
 return (in == answer);
}

void setup() {
 Serial.begin(115200);
 pinMode(LED_BUILTIN, OUTPUT);
 // r_key : 32-bit x #128
 u32 r_key[128] = {0, };
 
 // m_key : 32-bit
 u32 m_key[3] = {0x12345678,0x01020304,0x55667788};
 // text: 32-bit
 u32 text[3] = {0x90ABCDEF,0x0A0B0C0D,0xFFEEDDCC};
 u32 out_text[3]= {0xE4DE2FF8,0xE7F54BDC,0x53485E4F};
 Serial.println("-----------------");
 Serial.println(" TEST VECTOR ");
 Serial.println("-----------------");
 
 for(int i=0; i<3; i++) {
   new_bs_keygen(r_key, m_key[i]);
   new_bs_enc(r_key, &text[i]);
 
   if(TEST_VECTOR(text[i], out_text[i])){
     Serial.println(">> CORRECT");
   }else{
     Serial.println(">> WRONG");
   }
 }
 
 Serial.println("-----------------");
 Serial.println(" BENCHMARK ");
 Serial.println("-----------------");
 
 // m_key : 32-bit
 u32 m_key_bench = 0x12345678;
 // text: 32-bit
 u32 text_bench = 0x90ABCDEF;
 
 u32 time1;
 u32 time2;
 time1 = millis();
 for(int i=0; i<64; i++) {
  new_bs_keygen(r_key, m_key_bench);
  new_bs_enc(r_key, &text_bench);
 }
 
 time2 = millis();
 Serial.print(">> ");
 Serial.println((time2-time1));
 Serial.println("-----------------");
}

void loop() {
}
