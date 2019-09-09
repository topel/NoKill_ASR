#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

NBR_COPY=45

if len(sys.argv) != 4:
    print "ERROR : multiplier.py mauvais usage"
    print "bon usage :"
    print "python multiplier.py <low_ngram.txt> <corpus_name> <aug_corpus_name>"
else:
    file_name=sys.argv[1]
    corpus_name=sys.argv[2]
    aug_corpus_name=sys.argv[3]


###########################################
# Récupération des ngams sous representes #
###########################################

f=open(file_name,'r')

ng = f.readlines()

ngrams=[]
for ngr in ng:
    ngrams.append(ngr.rstrip())

f.close()
###########################################################################
#  			Recuperation du corpus				  #
#  Multiplication des phrases qui contiennent des ngrams sous-représentés #
###########################################################################

g=open(corpus_name,'r')
corpus=g.read()

f=open(aug_corpus_name,'w')

a=0
for lines in corpus.split('\n'):
	if any(i in lines for i in ngrams):
		for count in range(0,NBR_COPY):
			f.write(lines+'\n')
	else:
		f.write(lines+'\n')


f.close()	
g.close()



