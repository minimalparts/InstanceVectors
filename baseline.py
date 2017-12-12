#baseline.py
#USAGE: python3 baseline.py [individual] [space file] [cols file] 
#EXAMPLE: python3 baseline.py Darcy_N data/pride.dm data/pride.cols
#-------
import sys
import re
import numpy as np
import utils
from collections import Counter

character = sys.argv[1] #A name (e.g. Darcy_N)
space_file = sys.argv[2]
cols_file = sys.argv[3]

'''Load files'''
space = utils.readDM(space_file)
cols = utils.readDims(cols_file)

background_space = utils.readDM("BNC.w10.4000c.5000r.ppmi.rownorm.dm")
background_cols = utils.readDims("BNC.w10.4000c.5000r.ppmi.rownorm.cols")


'''Record weights for character'''
character_vector = space[character]
chars = {}
for i in range(len(character_vector)):
    chars[cols[i]] = character_vector[i]


'''Print top contexts for character'''
c=1
top_contexts=""
for char in sorted(chars, key=chars.get, reverse=True):
    if c <= 50:
        top_contexts+=char+' '
        c+=1
print("\nTop contexts for",character,":",top_contexts[:-1])


'''Print neighbours for vector.'''
print("\nNeighbours for character:")
top_neighbours = utils.sim_to_matrix(space, character, 100)
print(top_neighbours[:20])


'''Print coherence for vector.'''
print("\nCoherence for",character,utils.coherence(background_space,top_contexts.split()))


'''Print hyponymy scores'''
hypernyms = {}
c = 0
for n in top_neighbours:
    if n[-2:] == "_N":
        h = utils.hyponymy(space,character,n)[1]
        hypernyms[n] = h
        c+=1
    if c == 50:
        break

print("\nTop hypernyms:")
d = Counter(hypernyms)
for k,v in d.most_common(10):
    print(k,v)
