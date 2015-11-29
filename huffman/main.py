# -*- coding: koi8_r -*-
from huffman import *
import struct
import networkx as nx
import matplotlib.pyplot as plt
#ctypes.
#a=huffman("УЮОЁКЁМНКЕЙЯЮМДПЯЕПЦЁИНБХВУЮОЁКЁМЯЕПЦЁИ╨БЦЕМНБХВУЮОЁКЁМЮНКЕМЮЮМЮРНКЭ©БМЮ")
#str="УЮОЁКЁМНКЕЙЯЮМДПЯЕПЦЁИНБХВУЮОЁКЁМЯЕПЦЁИ╨БЦЕМНБХВУЮОЁКЁМЮНКЕМЮЮМЮРНКЭ©БМЮ"
file=open("11.txt")
l=file.read()
#print l
#a=huffman("wasfweeeeffasasadfasddfww"
a = 824
bin_data = struct.pack('<H',824)
print 'bin_data length:',len(bin_data)

with open('data.bin','wb') as f:
    f.write(bin_data)




a=huffman(l)
print a.message
a.encode()
g=a.print_tree()
print a.message













#a.encode_to_file("6")
#print a.message
#f=io.open('6.htxt','w')
#f.write(unicode(a.message))
print
#f.close()
#f=io.open('6.htxt')
#a=f.readlines()
#b=huffman(None)
#b.decode_from_file("6.htxt")
#print b.message
#s=struct.Struct('c')
#p=s.pack('4')
#print s.size