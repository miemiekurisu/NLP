from numpy import *

frname = 'pku_training.txt'

def iptsplitdata():
    return 0

def ipttrdata(frname):
    fr = open(frname)
    wordlist = fr.read().decode('gbk')
    wll = wordlist.split(' ')
    wll1=[]
    for i in wll:
        wll1.append(i.strip())
    return wll1
    
ws={}

wll1 = ipttrdata(frname)
for i in wll1:
    if len(i)>0:
        if i[0] in ws.keys():
            ws[i[0]].append(i)
        else:
            ws[i[0]]=[i]