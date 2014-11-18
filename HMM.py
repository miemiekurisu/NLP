from numpy import *
import copy
pi = array([ 0.63,  0.17,  0.2 ])
weather = array([[ 0.5  ,  0.375,  0.125],
                 [ 0.25 ,  0.125,  0.625],
                 [ 0.25 ,  0.375,  0.375]])
#                  Sunny   Cloudy  Rainy
stat = ['Sunny','Cloudy','Rainy']
obstat = array([[ 0.6 ,  0.2 ,  0.15,  0.05],
                [ 0.25,  0.25,  0.25,  0.25],
                [ 0.05,  0.1 ,  0.35,  0.5 ]])
#                 Dry	Dryish	 Damp   Soggy
ob = ['Dry','Dryish','Damp','Soggy']
seq = ['Dry','Damp','Soggy']
stm= mat(weather)
cm= mat(obstat)

a=mat(ones([3,3]))*0.333
b=mat([[0.5, 0.5],[0.75,0.25],[0.25,0.75]])
P=ones([1,3])*0.333
stat2=[1,2,3]
ob2 = [1,2]
seq2=[1, 1, 1 ,1 ,2 ,1 ,2 ,2, 2, 2]

def calcalphaT(sequence, statmarix,cmatrix,pivictor,observer):
    alpha=[]
    for i in sequence:
        obindex = observer.index(i)
        if len(alpha)==0:
            curr=[]
#             obindex = ob.index(i)
#             for a in range(len(pi)):
#                 curr.append(dot(pi[a],cm[a,obindex]))
            alpha.append([pivictor*array(cmatrix[:,obindex].T)])
        else:
            curr=[]
            col = shape(statmarix)[1]
            for a in range(col):
                curr.append(sum(alpha[-1]*statmarix[:,a]))
            alpha.append(curr*array(cmatrix[:,obindex].T))
    return alpha,sum(alpha[-1])

#this function have a bug, just find one path
def viterbiT(sequence, statmarix,cmatrix,pivictor,observer,statment):
    alpha=[]
    beta = []
    for i in sequence:
        obindex = observer.index(i)
        if len(alpha)==0:
            curr=[]
            alpha.append([pivictor*array(cmatrix[:,obindex].T)])
            beta.append(statment[argmax(alpha[-1])])
        else:
            curr = []
            col = shape(statmarix)[1]
            for a in range(col):
                curr.append(sum(alpha[-1]*statmarix[:,a]))
            alpha.append(curr*array(cmatrix[:,obindex].T))
            beta.append(statment[argmax(alpha[-1])])
    return alpha,sum(alpha[-1]),beta


def test1():
    a,b = calcalphaT(seq,stm,cm,pi,ob)
    print a
    print 'alpha=',b
    

def testV():
    t1,t2,t3 = viterbiT(seq,stm,cm,pi,ob,stat)
    t4,t5,t6 = viterbiT(seq2,a,b,P,ob2,stat2)
    print t3
    print 'and'
    print t6
