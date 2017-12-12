#contextualise.py
#USAGE: python3 contextualise.py [individual] [char file for individual] [numbers of chars used] [weight for context vector]
#EXAMPLE: python3 contextualise.py man_N data/pride/Darcy.chars 20 6
#-------
import sys
import re
import math
import numpy as np
import utils
from collections import Counter

num_dims = 4000	#Num dims in BNC dm file
target = sys.argv[1] #A kind (e.g. toad_N)
chars_file = sys.argv[2]
num_chars = int(sys.argv[3])
context_weight = int(sys.argv[4])


'''Get character name'''
character = ""
m = re.search(".*/(.*).chars",chars_file)
if m:
    character = m.group(1)
else:
    character = chars_file[:-6]
character=character.lower()+"_char_N"


'''Load files'''
background_space = utils.readDM("BNC.w10.4000c.5000r.ppmi.rownorm.dm")
background_cols = utils.readDims("BNC.w10.4000c.5000r.ppmi.rownorm.cols")
chars = utils.readChars(chars_file)


'''Compute contextualisation'''
c=1
reweighted_vectors = []
for context in sorted(chars, key=chars.get, reverse=True):
    ppmi=chars[context]
    
    i = 0
    context_vector = np.zeros(num_dims)
    #print("Reweighting vector with context",context)
    for col in background_cols:
        if context in background_space and col in background_space:     #in case core space does not include context (e.g. bnc.2000 does not include 'rat')
            context_vector[i] = pow(utils.cosine_similarity(background_space[context], background_space[col]), context_weight)
            if math.isnan(context_vector[i]):
                context_vector[i] = 0.0
        i+=1

    context_vector = utils.normalise(context_vector)
    reweighted_vectors.append(background_space[target]*context_vector)
    c+=1

    if c > num_chars:
        break



'''Add character to space'''
#print("Computing vector for",character)
background_space[character] = sum(reweighted_vectors)

new_chars = {}
for i in range(len(background_space[character])):
    new_chars[background_cols[i]] = background_space[character][i]


'''Print top contexts for character'''
c=1
top_contexts=""
for char in sorted(new_chars, key=new_chars.get, reverse=True):
    if c < 50:
        top_contexts+=char+' '
        c+=1
print("\nTop contexts for",character,":",top_contexts[:-1])


'''Print neighbours for original kind and contextualised vector.'''
print("\nOriginal neighbours for kind:")
print(utils.sim_to_matrix(background_space, target, 20))
print("New neighbours:")
top_neighbours = utils.sim_to_matrix(background_space, character, 100)
print(top_neighbours[:20])


'''Print coherence for contextualised vector.'''
print("\nCoherence for",character,utils.coherence(background_space,top_contexts.split()))


'''Print hyponymy scores'''
hypernyms = {}
c = 0
for n in top_neighbours:
    if n[-2:] == "_N":
        h = utils.hyponymy(background_space,character,n)[1]
        hypernyms[n] = h
        c+=1
    if c == 50:
        break

print("\nTop hypernyms:")
d = Counter(hypernyms)
for k,v in d.most_common(10):
    print(k,v)
