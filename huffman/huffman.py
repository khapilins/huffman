# -*- coding: koi8_r -*-
import operator
import re
import os
import math
import networkx as nx
import matplotlib.pyplot as plt

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
        bytes_l=[]
        try:
            byte=file.read(1)
            while byte:
                bytes_l.append(byte)
                #tmp.append(self._unpack_int([ord(byte)]))
                byte=file.read(1)      
        finally:
            file.close()  
        tmp_int=[ord(b) for b in bytes_l]
        print tmp_int
        print len(tmp_int)
        tmp=self._unpack_int(tmp_int)
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
            print str           
            tmp_int=int(str,2)
            res.append(tmp_int)
            j=i
        ##############################
        try:
            if self.message[j:]:
                str=self.message[j:]
                t=['0' for i in range(8-len(self.message[j:]))]
                str=str.join(t)
                r=str+''.join(t)
                res.append(int(str,2))
        except IndexError:pass
        print self.message
        return res

    def _unpack_int(self,list_int):
        res=[]   
        l=list_int
        for i in range(len(l)):
            b=str(bin(l[i])).split('b')[1]
            tmp=[]
            if i<len(l)-1:
                for j in range(1,9):
                    try:
                        if b[-j]:
                            tmp.append(b[-j])
                    except IndexError:
                        tmp.append('0')
                tmp.reverse()
                res.append(''.join(tmp))
                print ''.join(res)
                print len(''.join(res))
            else:
                tmp.append(b)
                res.append(''.join(tmp))
                print ''.join(res)
                print len(''.join(res))
        return ''.join(res)
        
    def print_tree(self):
        g=self._get_nx_graph()
        g=nx.bfs_tree(g,round(self.root.node_prob_value,3))
        pos=nx.spring_layout(g)
        nx.draw_networkx(g,pos,node_color='w',node_size=2000)                
        nx.draw_networkx_edge_labels(g,pos)
        #nx.draw_networkx(nx.(g,self.root.node_prob_value),nx.spring_layout(g),node_color='w',node_size=2000)        
        plt.show()

    def _get_nx_graph(self,root=None, g=None,pos=None):
        if not g:
            g=nx.Graph()                    
        if root:
            tmp_root=root
        else: tmp_root=self.root
        tmp_r_nx=round(tmp_root.node_prob_value,3)       
        g.add_node(tmp_r_nx,{''})                      
        if tmp_root.right:
            tmp_r_r_nx=round(tmp_root.right.node_prob_value,3)       
            self._get_nx_graph(tmp_root.right, g,pos)
            g.add_edge(tmp_r_nx,tmp_r_r_nx,{'':1})
        if tmp_root.left:
            tmp_r_l_nx=round(tmp_root.left.node_prob_value,3)       
            self._get_nx_graph(tmp_root.left, g,pos)
            g.add_edge(tmp_r_nx,tmp_r_l_nx,{'':0})
        return g

    def print_node(self,node):
        pass


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