# -*- coding: utf-8 -*-
from __future__ import print_function
import re
import os
import sys

try:
    xrange          # Python 2
except NameError:
    xrange = range  # Python 3

class SEG(object):
    def __init__(self):
        _localDir=os.path.dirname(__file__)
        _curpath=os.path.normpath(os.path.join(os.getcwd(),_localDir))
        curpath=_curpath
        self.d = {}
        print("loading dict...", file=sys.stderr)
        with open(os.path.join(curpath, "main.dic")) as in_file:
            self.set([x.rstrip() for x in in_file])
        with open(os.path.join(curpath,"suffix.dic")) as in_file:
            self.specialwords= set([x.rstrip().decode('utf-8') for x in in_file])
        print('dict ok.', file=sys.stderr)
    #set dictionary(a list)
    def set(self,keywords):
        p = self.d
        q = {}
        k = ''
        for word in keywords:
            word = (chr(11)+word).decode('utf-8')
            if len(word)>5:
                continue
            p = self.d
            ln = len(word)
            for i in xrange(ln-1,-1,-1):
                char = word[i].lower()
                if p=='':
                    q[k] = {}
                    p = q[k]
                if not (char in p):
                    p[char] = ''
                    q = p
                    k = char
                p = p[char]
    
    def _binary_seg(self,s):
        ln = len(s)
        if ln==1:
            return [s]
        R = []
        for i in xrange(ln,1,-1):
            tmp = s[i-2:i]
            R.append(tmp)
        return R
    
    def _pro_unreg(self,piece):
        #print(piece)
        R = []
        tmp = re.sub(u"。|，|,|！|…|!|《|》|<|>|\"|'|:|：|？|\?|、|\||“|”|‘|’|；|—|（|）|·|\(|\)|　"," ",piece).split()
        ln1 = len(tmp)
        for i in xrange(len(tmp)-1,-1,-1):
            mc = re.split(r"([0-9A-Za-z\-\+#@_\.]+)",tmp[i])
            for j in xrange(len(mc)-1,-1,-1):
                r = mc[j]
                if re.search(r"([0-9A-Za-z\-\+#@_\.]+)",r)!=None:
                    R.append(r)
                else:
                    R.extend(self._binary_seg(r))
        return R
        
        
    def cut(self,text):
        """
        """
        text = text.decode('utf-8','ignore')
        p = self.d
        ln = len(text)
        i = ln 
        j = 0
        z = ln
        q = 0
        recognised = []
        mem = None
        mem2 = None
        while i-j>0:
            t = text[i-j-1].lower()
            #print(i,j,t,mem)
            if not (t in p):
                if (mem!=None) or (mem2!=None):
                    if mem!=None:
                        i,j,z = mem
                        mem = None
                    elif mem2!=None:
                        delta = mem2[0]-i
                        if delta>=1:
                            if (delta<5) and (re.search(u"[\w\u2E80-\u9FFF]",t)!=None):
                                pre = text[i-j]
                                #print(pre)
                                if not (pre in self.specialwords):
                                    i,j,z,q = mem2
                                    del recognised[q:]
                            mem2 = None
                            
                    p = self.d
                    if((i<ln) and (i<z)):
                        unreg_tmp = self._pro_unreg(text[i:z])
                        recognised.extend(unreg_tmp)
                    recognised.append(text[i-j:i])
                    #print(text[i-j:i],mem2)
                    i = i-j
                    z = i
                    j = 0
                    continue
                j = 0
                i -= 1
                p = self.d
                continue
            p = p[t]
            j+=1
            if chr(11) in p:
                if j<=2:
                    mem = i,j,z
                    #print(text[i-1])
                    if (z-i<2) and (text[i-1] in self.specialwords) and ((mem2==None) or ((mem2!=None and mem2[0]-i>1))):
                        #print(text[i-1])
                        mem = None
                        mem2 = i,j,z,len(recognised)
                        p = self.d
                        i -= 1
                        j = 0
                    continue
                    #print(mem)
                p = self.d
                #print(i,j,z,text[i:z])
                if((i<ln) and (i<z)):
                    unreg_tmp = self._pro_unreg(text[i:z])
                    recognised.extend(unreg_tmp)
                recognised.append(text[i-j:i])
                i = i-j
                z = i
                j = 0
                mem = None
                mem2 = None
        #print(mem)
        if mem!=None:
            i,j,z = mem
            recognised.extend(self._pro_unreg(text[i:z]))
            recognised.append(text[i-j:i])        
        else:
            recognised.extend(self._pro_unreg(text[i-j:z]))
        return recognised
