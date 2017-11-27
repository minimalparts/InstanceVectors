from math import sqrt
import numpy as np

def readDM(dm_file):
    dm_dict = {}
    with open(dm_file) as f:
        dmlines=f.readlines()
    f.close()

    #Make dictionary with key=row, value=vector
    for l in dmlines:
        items=l.rstrip().split()
        row=items[0]
        vec=[float(i) for i in items[1:]]
        vec=np.array(vec)
        dm_dict[row]=vec
    return dm_dict

def cap_pos(w):
    pos = w[-1].upper()
    return w[:-1]+pos

def readDims(cols_file):
    with open(cols_file) as f:
        cols=f.read().splitlines()
    f.close()
    return cols

def readChars(char_file):
    chars = {}
    c = open(char_file,"r")
    for l in c:
        pair = l.rstrip("\n").split("\t")
        context = cap_pos(pair[1].lower())
        chars[context]=float(pair[0])
    c.close()
    return chars

def normalise(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm

def cosine_similarity(v1, v2):
    if len(v1) != len(v2):
        raise ValueError("Vectors must be of same length")
    num = np.dot(v1, v2)
    den_a = np.dot(v1, v1)
    den_b = np.dot(v2, v2)
    return num / (sqrt(den_a) * sqrt(den_b))

def sim_to_matrix(dm_dict,word,n):
    cosines={}
    c=0
    for k,v in dm_dict.items():
        cos = cosine_similarity(dm_dict[word], v)
        cosines[k]=cos
        c+=1
    c=0
    neighbours = []
    for t in sorted(cosines, key=cosines.get, reverse=True):
        if c<n:
            #print(t,cosines[t])
            neighbours.append(t)
            c+=1
        else:
            break
    return neighbours

def coherence(dm_dict,contexts):
    cosines = []
    for i in range(len(contexts)-2):
        for j in range(i,len(contexts)-1):
            cos = cosine_similarity(dm_dict[contexts[i]],dm_dict[contexts[j]])
            cosines.append(cos)
    return sum(cosines)/len(cosines)


def hyponymy(dm_dict,w1,w2):
    sum_mins=0
    sum_w1=0
    sum_w2=0

    for i in range(len(dm_dict[w1])):
        weight1=dm_dict[w1][i]
        weight2=dm_dict[w2][i]
        sum_mins+=min(float(weight1),float(weight2))
        sum_w1+=float(weight1)
        sum_w2+=float(weight2)

    clarkeDE=sum_mins/sum_w1
    clarkeDEinv=sum_mins/sum_w2

    invCL=sqrt(clarkeDE*(1-clarkeDEinv))

    return clarkeDE,invCL
