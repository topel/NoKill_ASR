#!/bin/bash

. ./path.sh
. ./cmd.sh

# Definition des repertoires
corpus_path=data/training_corpus
g2p=data/Phonetisaurus_model
locdata=data/local
locdict=$locdata/dict
model=data/model
loclang=data/local/lang
lang=data/lang
lang_test=data/lang_test
acoustic=data/acoustic

dev=../ELEMENTS_SAMOVA_TURING_TEST/TEXTES_SAMOVA_TURING_TEST/TRAITE_TT_all.txt


# wiki_crawl permet de crawler le corpus wikipedia si =1 ou non si il existe deja
# Attention si wiki_crawl = 1 cela supprimera le corpus wikipédia crawlé précédemment

# L'opération de crawling est très longue...
let wiki_crawl=0

# pretraitement permet de fusionner en un seul corpus ainsi que d'appliquer le prétraitement au corpus global 
let pretraitement=0

if [ $wiki_crawl -eq 1 ]
then
	##############################################
	echo " === Crawling du corpus wikipedia ===" #
	##############################################

	if [ -f $corpus_path/raw_database.txt ]; 
	then 
		rm $corpus_path/raw_database.txt #Suppression du corpus précédent
	fi

	touch $corpus_path"raw_database.txt" # Création du nouveau fichier du corpus
	
	# Appel du crawler wikipedia pour générer la database Créé un fichier raw_database.txt contenant le texte brut extrait des pages wikipedia ciblees ( a commenter si non utilisé)
	python scripts/wikipedia-crawler/wiki-crawler.py $corpus_path

	echo "crawling terminé"
fi

if [ $pretraitement -eq 1 ]
then
############################################################################
	echo " === Preparation de l'entrainement du modèle de langage ===" #
############################################################################
	if [ -f $corpus_path/CORPUS.txt ]
	then
		rm $corpus_path/CORPUS.txt
	fi

	if [ -f $corpus_path/CORPUS_TRAITE.txt ]
	then
		rm $corpus_path/CORPUS_TRAITE.txt
	fi

	if [ -f $corpus_path/SORTED_CORPUS_TRAITE.txt ]
	then 
		rm $corpus_path/SORTED_CORPUS_TRAITE.txt
	fi

	if [ -f $corpus_path/CORPUS_TRAIN.txt ]
	then
		rm $corpus_path/CORPUS_TRAIN.txt
	fi

	if [ -f $corpus_path/CORPUS_TEST.txt ]
	then
		rm $corpus_path/CORPUS_TEST.txt
	fi

	if [ -f $corpus_path/UNIQ_CORPUS.txt ]
	then
		rm $corpus_path/UNIQ_CORPUS.txt
		touch $corpus_path/UNIQ_CORPUS.txt
	fi

	# Association des fichiers pour créer le corpus d'entrainement
	echo "--- Fusion des corpus ---"	
	cat $corpus_path/1_Textes_site_nokill.txt $corpus_path/1_ESTERS2_dev.txt $corpus_path/1_ESTERS2.txt $corpus_path/2_ESTERS2.txt $corpus_path/Traite_Commonvoice_ALL.txt $corpus_path/raw_database.txt > $corpus_path/CORPUS.txt

	# Mise en forme du corpus pour effectuer l'apprentissage (genere un fichier database.txt contenant le corpus traité et un fichier corpuswords.txt contenant les mots présents dans ce corpus)
	echo "--- Mise en forme du corpus d'apprentissage ---"
	python scripts/parseESTERSyncV2.py $corpus_path/CORPUS.txt $corpus_path/CORPUS_TRAITE.txt

	# Separation en ensemble de test et ensemble de train
	sort -R $corpus_path/CORPUS_TRAITE.txt > $corpus_path/SORTED_CORPUS_TRAITE.txt

	let nbligne=`wc -l $corpus_path/CORPUS.txt | awk '{print $1}'`
	let nblignetrain=$nbligne*80/100
	let nblignetest=$nbligne-$nblignetrain
	
	echo "--- Separation des corpus en entrainement/test ---"
	head -n $nblignetrain $corpus_path/SORTED_CORPUS_TRAITE.txt > $corpus_path/CORPUS_TRAIN.txt
	tail -n $nblignetest $corpus_path/SORTED_CORPUS_TRAITE.txt > $corpus_path/CORPUS_TEST.txt

	#Verification de la présence de tous les mots dans le corpus d'apprentissage et verification de leur nombre d'occurences
	echo "--- Verification des occurences ---" 
	python scripts/verifs_occurences.py $corpus_path/CORPUS_TRAIN.txt $dev $locdata/
	
	echo "--- Multiplication ---"
	python scripts/multiplier.py $locdata/low_ngrams.txt $corpus_path/CORPUS_TRAIN.txt $corpus_path/augmented_CORPUS_TRAIN.txt
	
fi

##################################################
echo "=== entrainement du modèle de langage ===" #
##################################################
if [ -f $locdata/vocab-full.txt ]; then
	rm $locdata/vocab-full.txt
fi

ngram-count -order 3  -write-vocab $locdata/vocab-full.txt -wbdiscount -text $corpus_path/augmented_CORPUS_TRAIN.txt -lm $locdata/LM.gz

echo "ensemble test"
ngram -lm $locdata/LM.gz -ppl $corpus_path/CORPUS_TEST.txt

echo "ensemble dev"
ngram -lm $locdata/LM.gz -ppl $dev


############################################
echo "=== preparation du dictionnaire ===" #
############################################

if [ -f $locdict/vocab-oov.txt ]; then 
	rm $locdict/vocab-oov.txt
fi

if [ -f $locdict/lexicon-iv.txt ]; then
	rm $locdict/lexicon-iv.txt
fi

if [ -f $locdict/lexicon.txt ]; then
	rm $locdict/lexicon.txt
fi
if [ -f $locdict/lexiconp.txt ]; then
	rm $locdict/lexiconp.txt
fi

echo "--- Recherche des mots hors vocabulaire ---"

# Recherche des mots du corpus qui ne sont pas présents dans le dictionnaire
awk 'NR==FNR{words[$1]; next;} !($1 in words)' \
	$locdict/fr.dict $locdata/vocab-full.txt |\
	egrep -v '<.?s>' | sort -n > $locdict/vocab-oov.txt

echo "--- génération de la phonetisation des mots hors vocabulaires ---"

## Suppression des mots de vocabulaire ajoutés mais non présents
sed -i '/-pau-/d'  $locdict/vocab-oov.txt

echo "--- Suppressions des OOVs sous representes ---"
comm -1 -2 $locdata/vocab-textes.txt $locdict/vocab-oov.txt > $locdict/updated_vocab-oov.txt

## Generation de la phonetisation des mots manquants
phonetisaurus-apply --model $g2p/model.fst --word_list $locdict/updated_vocab-oov.txt > $locdict/lexicon-oov.txt

cat $locdict/lexicon-oov.txt $locdict/fr.dict | sort > $locdict/lexicon.txt

echo "nombre de phonemes lexique :"
phone_lex=$(cat $locdict/lexicon.txt | awk '{$1="";print $0}' | tr -s ' ' '\n' | sort | uniq -c | wc -l)
echo $phone_lex

echo "nombre de phonemes dictionnaire original"
phone_dict=$(cat $locdict/fr.dict | awk '{$1="";print $0}' | tr -s ' ' '\n' | sort | uniq -c | wc -l)
echo $phone_dict

if [ $phone_dict -ne $phone_lex ]
then
	echo "Phone list not ok quitting"
	exit
else
	echo "phones OK"
fi

echo "--- Preparation des phone lists ---"

echo SIL > $locdict/silence_phones.txt
echo SIL > $locdict/optional_silence.txt

grep -v -w SIL $locdict/lexicon.txt | \
	awk '{for(n=2;n<=NF;n++) { p[$n]=2; }} END{for(x in p){print x}}' |\
	sort > $locdict/nonsilence_phones.txt

# Ajout du symbole <unk> dans le lexique
echo -e "<unk>\tSIL" >> $locdict/lexicon.txt

# Suppression des fichiers temporaires issus de la précédente génération de modèle
if [ -f $loclang/align_lexicon.txt ]
then
	rm $loclang/align_lexicon.txt
fi

if [ -f $loclang/lex_ndisambig ]
then
	rm $loclang/lex_ndisambig
fi

if [ -f $loclang/lexiconp.txt ]
then
	rm $loclang/lexiconp.txt
fi

if [ -f $loclang/lexiconp_disambig.txt ]
then
	rm $loclang/lexiconp_disambig.txt
fi

if [ -f $loclang/phone_map.txt ]
then
	rm $loclang/phone_map.txt
fi

# Suppression des fichiers générés lors du précédent run de prepare_lang.sh
if [ -f $lang/L.fst ]
then
	rm $lang/L.fst
fi

if [ -f $lang/L_disambig.fst ]
then
	rm $lang/L_disambig.fst
fi

if [ -f $lang/oov.int ]
then
	rm $lang/oov.int
fi

if [ -f $lang/oov.txt ]
then
	rm $lang/oov.txt
fi

if [ -d $lang/phones ]
then
	rm -Rf $lang/phones
fi

if [ -f $lang/phones.txt ]
then
	rm $lang/phones.txt
fi

if [ -f $lang/topo ]
then
	rm $lang/topo
fi

if [ -f $lang/words.txt ]
then
	rm $lang/words.txt
fi


scripts/prepare_lang.sh --phone_symbol_table /home/pellegri/tools/ASR_DEMO_SAMOVA/Stage_Erwan/ModelGeneration/data/acoustic/phones.txt $locdict \
        '<unk>' $loclang data/lang

#sed -i '1d' data/lang/words.txt
#sed -i '2d' data/lang/words.txt

##############################################
echo "=== Formatage du modele de langue ===" #
##############################################

utils/format_lm.sh $lang $locdata/LM.gz $locdict/lexicon.txt $lang_test

rmdir --ignore-fail-on-non-empty $acoustic/graph/
mkdir $acoustic/graph

utils/mkgraph.sh $lang_test $acoustic $acoustic/graph 
