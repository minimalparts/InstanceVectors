#contextualise.py
#USAGE: python3 contextualise.py [individual] [space file] [cols file] [char file for individual] [numbers of chars used] [weight for context vector]
#EXAMPLE: python3 contextualise.py man_N bnc.dm bnc.cols data/Darcy.chars 20 6
#-------
import sys
import re
import numpy as np
import utils

num_dims = 4000	#Num dims in BNC dm file
target = sys.argv[1] #A kind (e.g. toad_N)
space_file = sys.argv[2]
cols_file = sys.argv[3]
chars_file = sys.argv[4]
num_chars = int(sys.argv[5])
context_weight = int(sys.argv[6])


'''Get character name'''
character = ""
m = re.search(".*/(.*).chars",chars_file)
if m:
    character = m.group(1)
else:
    character = chars_file[:-6]
character=character.lower()+"_N"


'''Load files'''
space = utils.readDM(space_file)
cols = utils.readDims(cols_file)
chars = utils.readChars(chars_file)




'''Compute contextualisation'''
c=1
reweighted_vectors = []
for context in sorted(chars, key=chars.get, reverse=True):
    ppmi=chars[context]
    
    #print("Reweighting vector with context",context,ppmi)
    i = 0
    context_vector = np.zeros(num_dims)
    for col in cols:
        if context in space and col in space:     #in case core space does not include context (e.g. bnc.2000 does not include 'rat')
            context_vector[i] = pow(utils.cosine_similarity(space[context], space[col]), context_weight)
        i+=1

    context_vector = utils.normalise(context_vector)
    reweighted_vectors.append(space[target]*context_vector)
    c+=1

    if c > num_chars:
        break



#print("Computing vector for",character)
space[character] = sum(reweighted_vectors)



'''Add character to space'''
new_chars = {}
for i in range(len(space[character])):
    new_chars[cols[i]] = space[character][i]


'''Print top contexts for character'''
c=1
top_contexts=""
for char in sorted(new_chars, key=new_chars.get, reverse=True):
    if c < 20:
        top_contexts+=char+' '
        c+=1
print("\nTop contexts for",character,":",top_contexts[:-1])


'''Print neighbours for original kind and contextualised vector.'''
print("\nOriginal neighbours for kind:")
print(utils.sim_to_matrix(space, target, 20))
print("New neighbours:")
print(utils.sim_to_matrix(space, character, 20))


'''Print coherence for contextualised vector.'''
print("\nCoherence for",character,utils.coherence(space,top_contexts.split()))


'''Print hyponymy scores'''
print(utils.hyponymy(space,character,"man_N")[1])
