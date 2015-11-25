# -*- coding: koi8_r -*-
from huffman import *
import struct
import binascii



#a=huffman("УЮОЁКЁМНКЕЙЯЮМДПЯЕПЦЁИНБХВУЮОЁКЁМЯЕПЦЁИ╨БЦЕМНБХВУЮОЁКЁМЮНКЕМЮЮМЮРНКЭ©БМЮ")
#str="УЮОЁКЁМНКЕЙЯЮМДПЯЕПЦЁИНБХВУЮОЁКЁМЯЕПЦЁИ╨БЦЕМНБХВУЮОЁКЁМЮНКЕМЮЮМЮРНКЭ©БМЮ"
file=open("11.txt")
l=file.read()
#print l
#a=huffman("wasfweeeeffasasadfasddfww")
a=huffman(l)
a.encode_to_file("6")
#print a.message
#f=io.open('6.htxt','w')
#f.write(unicode(a.message))
print
#f.close()
#f=io.open('6.htxt')
#a=f.readlines()
b=huffman(None)
b.decode_from_file("6.htxt")
s=struct.Struct('c')
p=s.pack('4')
print s.size