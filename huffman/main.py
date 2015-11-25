# -*- coding: koi8_r -*-
from huffman import *
import struct
import io



#a=huffman("УЮОЁКЁМНКЕЙЯЮМДПЯЕПЦЁИНБХВУЮОЁКЁМЯЕПЦЁИ╨БЦЕМНБХВУЮОЁКЁМЮНКЕМЮЮМЮРНКЭ©БМЮ")
#str="УЮОЁКЁМНКЕЙЯЮМДПЯЕПЦЁИНБХВУЮОЁКЁМЯЕПЦЁИ╨БЦЕМНБХВУЮОЁКЁМЮНКЕМЮЮМЮРНКЭ©БМЮ"
#file=open("war.txt")
#l=file.read()
#print l
#a=huffman("wasfweeeeffasasadfasddfww")
a=huffman("affffssssssssaewrdsadfkalef")
a.encode()
#print a.message
f=io.open('6.htxt','w')
f.write(unicode(a.message))
print
f.close()
f=io.open('6.htxt')
a=f.readlines()
a.decode()
with open("test.bnr", "wb") as f:
    
    f.write(struct.pack('i', int(a.message[::2], 2)))
#a.encode_to_file("6")
#print a.message
print
a.decode_from_file("6.htxt")
#print a.message
#print str
#print a.codes_dict
#f=open("1.txt","w")
#f.write(str)
#f=open("2.txt","wb")
#f.write(bytes(1))
#print bytes(1)
