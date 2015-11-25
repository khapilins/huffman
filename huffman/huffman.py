# -*- coding: koi8_r -*-
import operator
import re
import os

class huffman:
    message=""

    probability_table={}

    root=0

    codes_dict=[]

    leaves=[]

    def encode(self):
        self.get_list_of_codes()
        self.codes_dict={i.items()[0][0]:i.items()[0][1] for i in self.codes_dict if i.items()[0][0]}
        for item in self.codes_dict.items():
            rep=re.compile(item[0])
            self.message=rep.sub(item[1],self.message)
        return self.message

    def decode(self):
        msg=self.message
        tmp_root=self.root
        res=[]        
        for c in msg:
            if tmp_root.symbol:
                res.append(tmp_root.symbol)
                tmp_root=self.root
            if c=="1":
                tmp_root=tmp_root.right
            else:
                tmp_root=tmp_root.left
        if tmp_root.symbol:
                res.append(tmp_root.symbol)
                tmp_root=self.root
        self.message=''.join(res)
        return res


    def __init__(self,input_message):
        if input_message:
            self.message=input_message
            self.probability_table=dict.fromkeys([c for c in self.message],0.)
            for c in self.message:
                self.probability_table[c]+=1./len(self.message)
            self.probability_table=sorted(self.probability_table.items(), key=operator.itemgetter(1))
            #self.probability_table={item[0]:item[1] for item in probability_table}

    def _get_probs_from_file(self,filename,mode="rb"):
        file=open(filename,mode)        
        lines=[]
        line=file.readline()
        lines=line.split(str(unichr(126)))        
        dict={l.split(str(unichr(127)))[0]:float(l.split(str(unichr(127)))[1]) for l in lines if l!=os.linesep}
        self.probability_table=sorted(dict.items(), key=operator.itemgetter(1))
        file.close()
        self.build_tree()
        return dict

    def _write_probs_to_file(self,filename,mode="wb"):
        file=open(filename,mode)
        for item in self.probability_table:
            file.write(item[0])
            file.write(unicode(unichr(127)))
            file.write(unicode(str(item[1]),errors='replace'))
            file.write(unicode(str(unichr(126))))

    def encode_to_file(self,filename,message=None):
        if message:
            self.message=message        
        self.encode()
        self._write_probs_to_file(filename+".htxt")        
        file=open(filename+".htxt","ab")
        file.write(os.linesep)
        for i in self._pack_to_int():
            file.write(str(chr(i)))            
        file.close()

    def decode_from_file(self,filename):
        self._get_probs_from_file(filename)
        file=open(filename,"rb")
        file.readline()        
        tmp=[]
        try:
            byte=file.read(1)
            while byte:
                tmp.append(self._unpack_int([ord(byte)]))
                byte=file.read(1)      
        finally:
            file.close()  
        self.message=''.join(tmp)
        self.decode()

    def build_tree(self):
        self.leaves=[tree_node(item[1],item[0]) for item in self.probability_table]
        tmp=[]
        list=self.leaves[:]
        while True:
            for i in range(0,len(list),2):
                if i<len(list)-1:
                    tmp.append(tree_node(list[i].node_prob_value+list[i+1].node_prob_value,left=list[i],right=list[i+1]))
                else: tmp.append(list[-1])
            list=tmp
            if len(tmp)==1:break
            tmp=[]
        self.root=tmp[0]
        return self.root

    def get_list_of_codes(self,node=None,codes_list=None):
        if not node:
            self.root=self.build_tree()                           
            tmp_root=self.root
        else: tmp_root=node
        if not codes_list:
            res=[]        
        else: res=codes_list
        if not tmp_root.symbol:
            if tmp_root.right:
                tmp_root.right.node_code=tmp_root.node_code+"1"
                self.get_list_of_codes(tmp_root.right,res)
            if tmp_root.right:
                tmp_root.left.node_code=tmp_root.node_code+"0"
                self.get_list_of_codes(tmp_root.left,res)       
        res.append(tmp_root)
        self.codes_dict.append({tmp_root.symbol:tmp_root.node_code}) 
        return self.codes_dict

    def _pack_to_int(self):
        j=0
        res=[]
        for i in xrange(8,len(self.message)+1,8):
            str=self.message[j:i]
            j=i
            tmp_int=0
            for k in range(8):
                tmp_int+=(2**(7-k))*int(str[k])
            res.append(tmp_int)
        return res

    def _unpack_int(self,list_int):
        res=[]
        for i in list_int:
            b=str(bin(i)).split('b')[1]
            tmp=[]
            for j in range(1,9):
                try:
                    if b[-j]:
                        tmp.append(b[-j])
                except IndexError:
                    tmp.append('0')
            tmp.reverse()
            res.append(''.join(tmp))
        return ''.join(res)

class tree_node:
    left=0
    right=0
    symbol=None
    node_code=""
    node_prob_value=0

    def __init__(self, node_prob=1,symbol=None, node_code="",left=0,right=0):
        self.symbol=symbol
        self.left=left
        self.right=right
        self.node_prob_value=node_prob
        self.node_code=node_code
    
        
