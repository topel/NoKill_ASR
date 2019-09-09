#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

NBRE_1GRAM=5
NBRE_2GRAM=5
NBRE_3GRAM=100

word_list=[]

if len(sys.argv) != 4:
    print "ERROR : Verifs.py mauvais usage :"
    print "Bon usage :"
    print "python verifs_occurences.py <corpus_name> <text_name> <out_dir>"
    sys.exit()
else:
    corpus_name=sys.argv[1]
    text_name=sys.argv[2]
    out_dir=sys.argv[3]


###################################################################
# Récupération des mots des différents fichiers sous forme de set #
###################################################################

# Récupération du corpus
f=open(corpus_name,'r')
corpus=f.read()
corpus=corpus.decode('utf8')
f.close()

# Creation d'un set contenant les mots du corpus
corpus_words=set(corpus.split(' '))
corpus_words=set([w.rstrip() for w in corpus_words])

# Recuperation des textes de verification
f=open(text_name,'r')
TT=f.read()
TT=TT.decode('utf8')
f.close()
TT=TT.replace('\n',' ')

texts_words=set(TT.split(' '))
texts_words=set([w.rstrip() for w in texts_words])

#################################################################################
# Verification que tous les mots de text_name soient dans le corpus corpus_name #
#################################################################################

missings = [i for i in texts_words if i not in corpus_words]


################################################################################
# Comptage de la fréquence d'apparition des mots de text_name dans corpus_name #
################################################################################

txt_wrd=list(texts_words)
counts_1gram=[]

for word in range(0,len(txt_wrd)):
    counts_1gram.append((corpus.count(txt_wrd[word]),txt_wrd[word]))

# On créé un set afin de ne recuperer qu'une seule fois l'element dans la table si ce dernier apparait plus d'une fois
counts_1gram=set(counts_1gram)

low_counts_1gram=[i for i in counts_1gram if i[0]<NBRE_1GRAM]

print len(low_counts_1gram),"mots apparaissent moins de", NBRE_1GRAM, "fois"


for i in low_counts_1gram:
    if i[0] > 0:
        word_list.append(i[1])
    

###########################################################################################
# Comptage de la fréquence d'apparition des couples de mots de text_name dans corpus_name #
###########################################################################################

counts_2gram=[]

TT_split=TT.split(' ')

for word in range(0,len(TT_split)-1):
    bigram=' '.join([TT_split[word],TT_split[word+1]])
    counts_2gram.append( (corpus.count(bigram),bigram) )

counts_2gram=set(counts_2gram)

low_counts_2gram=[i for i in counts_2gram if i[0] < NBRE_2GRAM]

print len(low_counts_2gram), "couples de mots apparaissent moins de",NBRE_2GRAM,"fois"

for i in low_counts_2gram:
    if i[0] > 0:
        word_list.append(i[1])


########################################################################################################
# Comptage de la fréquence d'apparition des triplets de mots des textes dans le corpus d'apprentissage #
########################################################################################################

counts_3gram=[]

for word in range(0,len(TT_split)-2):
    trigram=' '.join([TT_split[word],TT_split[word+1],TT_split[word+2]])
    counts_3gram.append( (corpus.count(trigram),trigram) )

counts_3gram=set(counts_3gram)

low_counts_3gram=[i for i in counts_3gram if i[0] < 100]

print len(low_counts_3gram),"triplets de mots apparaissent moins de", NBRE_3GRAM, "fois"

for i in low_counts_3gram:
    if i[0] > 0:
        word_list.append(i[1])


#########################################################
# Ecriture des n-grams sous representes dans un fichier #
#########################################################

f=open(out_dir+"low_ngrams.txt",'w')

for i in word_list:
    f.write(i.encode('utf-8')+'\n')

