#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from xml.etree import ElementTree as ET
import sys
from num2words import num2words
from unidecode import unidecode
import re
import os.path
import unicodedata

chiffres_romains={"Ier":"premier ","IIe":"deuxième ","IIIe":"troisième ","IVe":"quatrième ","Ve":"cinquième ","VIe":"sixième ","VIIe":"septième ","VIIIe":"huitième ","IXe":"neuvième ","Xe":"dixième ","XIe":"onzième ","XIIe":"douzième ","XIIIe":"treizième ","XIVe":"quatorzième ","XVe":"quinzième ","XVIe":"seizième ","XVIIe":"dix-septième ","XVIIIe":"dix-huitième ","XIXe":"dix-neuvième ","XXe":"vingtième ","XXIe":"vingt-et-unième ","XXIIe":"vingt-deuxième ","XXIIIe":"vingt-troisième "}

chiffres_romains={"I":"premier ","II":"deuxième ","III":"troisième ","IV":"quatrième ","V":"cinquième ","VI":"sixième ","VII":"septième ","VIII":"huitième ","IX":"neuvième ","X":"dixième ","XI":"onzième ","XII":"douzième ","XIII":"treizième ","XIV":"quatorzième ","XV":"quinzième ","XVI":"seizième ","XVII":"dix-septième ","XVIII":"dix-huitième ","XIX":"dix-neuvième ","XX":"vingtième ","XXI":"vingt-et-unième ","XXII":"vingt-deuxième ","XXIII":"vingt-troisième "}

autre={"1er":"premier","1ère":"première","2ème":"deuxième","3ème":"troisième","4ème":"quatrième","5ème":"cinquième","6ème":"sixième","7ème":"septième ","8ème":"huitième ","9ème":"neuvième ","10ème":"dixième ","11ème":"onzième ","12ème":"douzième ","13ème":"treizième ","14ème":"quatorzième ","15ème":"quinzième ","16ème":"seizième ","17ème":"dix-septième ","18ème":"dix-huitième ","19ème":"dix-neuvième ","20ème":"vingtième ","21ème":"vingt-et-unième ","22ème":"vingt-deuxième ","23ème":"vingt-troisième ","24":"vingt-quatrième ","25ème":"vingt-cinquième",'26ème':"vingt-sixième","27ème":"vingt-septième","28ème":"vingt-huitième","29ème":"vingt-neuvième","30ème":"trentième","31ème":"trente et unième","32ème":"trente-deuxième","33ème":"trente-troisième","34ème":"trente-quatrième","35ème":"trente-cinquième","36e":"trente-sixième","37ème":"trente-septième","38e":"trente-huitième","39ème":"trente-neuvième","40ème":"quarantième","41ème":"quarante-et-unième","42ème":"quarante-deuxième","43ème":"quarante-troisième","44ème":"quarante-quatrième","45ème":"quarante-cinquième","46e":"quarante-sixième","47ème":"quarante-septième","48e":"quarante-huitième","49ème":"quarante-neuvième","50ème":"cinquantième","51ème":"cinquante-et-unième","52ème":"cinquante-deuxième","53ème":"cinquante-troisième","54ème":"cinquante-quatrième","55ème":"cinquante-cinquième","56e":"cinquante-sixième","57ème":"cinquante-septième","58e":"cinquante-huitième","59ème":"cinquante-neuvième","60ème":"soixantième","61ème":"soixante-et-unième","62ème":"soixante-deuxième","63ème":"soixante-troisième","64ème":"soixante-quatrième","65ème":"soixante-cinquième","66e":"soixante-sixième","67ème":"soixante-septième","68e":"soixante-huitième","69ème":"soixante-neuvième"}


autre_bis={"1er":"premier","1ère":"première","2e":"deuxième","3e":"troisième","4e":"quatrième","5e":"cinquième","6e":"sixième","7e":"septième ","8e":"huitième ","9e":"neuvième ","10e":"dixième ","11e":"onzième ","12e":"douzième ","13e":"treizième ","14e":"quatorzième ","15e":"quinzième ","16e":"seizième ","17e":"dix-septième ","18e":"dix-huitième ","19e":"dix-neuvième ","20e":"vingtième ","21e":"vingt-et-unième ","22e":"vingt-deuxième ","23":"vingt-troisième ","24":"vingt-quatrième ","25":"vingt-cinquième",'26e':"vingt-sixième","27e":"vingt-septième","28e":"vingt-huitième","29e":"vingt-neuvième","30e":"trentième","31e":"trente et unième","32e":"trente-deuxième","33e":"trente-troisième"}

def is_numerical(text):
    for letter in text:
        if ord(letter)<48 or ord(letter)>57:
            return False
    return True


def transformation_text(text):
    # ESTER Problem "Mohamed v" ===> "Mohammed cinq"
    #text=text.lower()
    text=text.replace("'","' ")
    text=text.replace(".","")
    text=text.replace(" vi "," six ")
    text=text.replace(" v "," cinq ")
    text=text.replace("+"," plus")
    # map all "mohamed" to "mohammed"
    text=text.replace("mohammed","mohamed")
    # character normalization:
    text=text.replace("&","et")
    # ESTER 2 Problem "19ème" ====> "dix-neuvième"
    text=text.replace("19ème","dix-neuvième")
    text=text.replace("canal +","canal plus")
    text=text.replace("\n"," ")
    text=text.replace("—"," ")
    text=text.replace("»"," ")
    text=text.replace("«"," ")
    text=text.replace("-"," ")
    text=text.replace("–"," ")
    text=text.replace("\xc2\xa0","")
    text=text.replace("À","à")
    #if "###" in text or len(re.findall(r"\[.+\]", text)) > 0 or \
    #    len(re.findall(r"\p{L}+-[^\p{L}]|\p{L}+-$",text)) > 0 \
    #    or len(re.findall("[^\p{L}]-\p{L}+|^-\p{L}+", text)) > 0:
    #    bool=False
    #else:
    # ^^ remove
    text=re.sub(r"\^+","",text)
    text=re.sub(r"\_+","",text)
    # 4x4
    # Remove noise sound (BIP) over Name of places and person
    #text = re.sub(r"¤[^ ]+|[^ ]+¤|¤", "", text.strip())
    if len(re.findall(r"\dx\d",text))>0:
        text=re.sub(r"x","  ",text)
    if len(re.findall("\d+h\d+",text))>0:
        heures=re.findall("\d+h\d+",text)
        for h in heures:
            split_h=h.split('h')
            text_rep=split_h[0]+' heure '+split_h[1]
            text=text.replace(h, text_rep)
    text=text.replace('“',' ')
    text=text.replace('”',' ')
# remove silence character : OK
    #text=re.sub(r"(/.+/","remplacer par la 1er",text)
# Liaison non standard remarquable
    text=text.replace(r'=',' égal ')
    text=text.replace('÷','')
# Comment Transcriber
    text=re.sub(r'\{.+\}','',text)
    text=re.sub(r'\(.+\}','',text)
    text=re.sub(r"\".+\"",'',text)
    text=re.sub('"',' ',text)
    text=text.replace('*','')
    text=text.replace(" ' ",' ')
    text=text.replace("í","i")
    text=text.replace('þ','')
    text=text.replace('æ','ae')
    text=text.replace('-',' ')
    #print "detecter (///|/|<|>)"
# Remove undecidable variant heared like on (n') en:
    #text=text.replace("(","")
    #text=text.replace(")","")
    text=re.sub(r"r'\[[^\]]*\]'","",text)
    text=re.sub(r"\(.*?\)|\(\)","",text)
    text=text.replace("(","")
    text=text.replace(")","")
    #text = re.sub(r"(\+|[*]+|///|/|<|>)", "", text.strip())
    #text=re.sub(r"-|_|\."," ",text.strip())
    text=re.sub(r'(O.K.)','ok',text)
    text = re.sub(r'(O.K)', 'ok', text)
    # Replace . with '':
#text=re.sub(r"{[^{]+}"," ",text.strip())
    # Remove ? ! < > : OK
    #<[^\p{L}]|[^\p{L}]>|#+|<\p{L}+[ ]|<\p{L}+$
    text=re.sub(r":|\?|/|\!|#+|²"," ",text)
    text=re.sub(r"%","pour cent",text)
    text=text.replace(" $","dollar") 
    text=text.replace("$"," dollars")
    text=text.replace(" €",' euro')
    text=text.replace("€",' euros')
    text=text.replace(" £"," livre-sterling")
    text=text.replace("£"," livres-sterling")
    text=text.replace("‎","")
    #text=text.replace("/"," ")
# replace silence character with <sil> : OK
    #text=re.sub(r"(\+)", "<sil>", text)
    #text=re.sub(r"(\+)", "!SIL", text)
    #text=re.sub(r"(///)", "!SIL", text)
    #text=re.sub(r"(///)", "<long-sil>", text)
    #if len(re.findall(r"/.+/", text)) > 0:
        #print "AVANT***********"+text
    #    for unchoosen_text in re.findall(r"/.+/", text):
            # choose first undecideble word
    #        unchoosen_word=unchoosen_text.split(',')
    #        for choosen_word in unchoosen_word:
                # isn't incomprehensible word
    #            if len(re.findall(r"\*+|\d+", choosen_word))==0:
    #                choosen_word = choosen_word.replace('/', '')
    #                text = text.replace(unchoosen_text, choosen_word)
        #print "Apres************"+text
# Remove noise sound (BIP) over Name of places and person
    #text=re.sub(r"(¤.+¤)",'<NOISE>',text)
# replace unkown syllable
    #text=re.sub(r"\*+"," ",text)
    text=text.replace("Č","c")
    text=text.replace("č","c")
    text=text.replace(" β "," beta ")
    text=text.replace(" λ "," lambda ")
# cut of recording : OK
    #text=re.sub(r"\$+","",text)
# remove " character: OK
    text = text.replace(r"+", " plus ")
    # t 'avais
    text = re.sub("\[.*?\]","",text)
    text = re.sub(r"[ ]\'", "\'", text)
    text = re.sub(r"\'", "\' ", text)

    words=[]
    for word in re.split(" ",text):
        if word in chiffres_romains:
            word = chiffres_romains[word]
        elif word in autre:
            word=autre[word]
        words.append(word)
    text=" ".join(words)

    text=text.replace(" ' "," ")
    text=text.replace("[","")
    text=text.replace("]","")
    text=text.replace("{","")
    text=text.replace("}","")
    text=text.replace('Ô','ô')
    text=text.replace('Å','a')
    text=text.replace('>>',"très supérieur à")
    text=text.replace('<<',"très inférieur à")
    text=text.replace('>',"supérieur à")
    text=text.replace('<',"inférieur à")
    text=text.replace('ß','')
    text=text.replace('×',' fois ')
    text=text.replace('@',' ')
    text=text.replace('Ø',' ')
#    text=text.replace(" km h "," kilomètres par heure ")
    text=text.replace('º','')

# Split des nombres exemple :  3D  ....
    num_list = re.findall("[a-zA-Zàéè]+\'*[a-zA-Zàéè]*[-]?\d+""", text)
    for s in range(0,len(num_list)):
        nex=[]
        split_between_char_int=num_list[s]
        for letter in range(0,len(split_between_char_int)):
            nex.append(split_between_char_int[letter])
            if is_numerical(split_between_char_int[letter])==False and is_numerical(split_between_char_int[letter+1])==True:
                    nex.append(' ')
        text = re.sub(str(split_between_char_int), str(''.join(nex)) ,text)

#Split des nombres exemple V2 -> V 2 
    num_list = re.findall("\d+[a-zA-Zàéè]+\'*[a-zA-Zàéè]*", text)

    for s in range(0,len(num_list)):
        nex=[]
        split_between_char_int=num_list[s]
        for letter in range(0,len(split_between_char_int)):
            nex.append(split_between_char_int[letter])
            if is_numerical(split_between_char_int[letter])==True and is_numerical(split_between_char_int[letter+1])==False:
                nex.append(' ')
        text = re.sub(str(split_between_char_int), str(''.join(nex)) ,text)

    num_list=re.findall("\d+\S+\d+",text)
    
    if len(num_list)>0:
        for num in num_list:
            if ',' in num:
                corr=re.sub(',',' virgule ',num)
                text=re.sub(num,corr,text)

    text=re.sub(r',|¸|;',' ',text)

    num_list = re.findall("\d+['\"]",text)
    if len(num_list)>0:
        for num in num_list:
            corr=re.sub("'","",text)
            corr=corr.replace("\"","")
            text=re.sub(num,corr,text)

#    text=text.replace(' min ',' minutes ')
#    text=text.replace(' s ',' secondes ')
#    reglist=re.findall('[0-9] h',text)
#    if len(reglist)>0:
#        for i in reglist:
#            i_rep=i.replace('h','heures')
#            text=re.sub(i,i_rep,text)

# Application de la transformation num2words
    num_list = re.findall("\d+", text)
    if len(num_list) > 0:
        #print "********************************* NUM2WORD"
        for num in num_list:
            num_in_word = num2words(int(num), lang='fr')
            num_in_word=unicodedata.normalize('NFKD', num_in_word).encode('ascii', 'ignore')
            text = re.sub(r"(^|[ ])"+str(num)+"([ ]|$)"," " + str(num_in_word) + " ",text)

    text=text.replace("’","' ")
    text=text.replace(" ' ","")
    text=text.replace("…","")
    text=text.replace('0₂','O deux')
    text=text.replace('½','demi')
    text=text.replace('É','é')
    text=text.replace('Á','a')

    text=re.sub(r" $","",text)
    text=re.sub("^ ", '', text)
   
   # Suppression des ' situés après des mots
    
    reglist=re.findall('\S\S\'',text)
    if len(reglist)>0:
        for i in reglist:
            if "rd" in i or "qu" in i:
                pass
            else:
                i_rep=i.replace('\'','')
                text=re.sub(i,i_rep,text)


#    reglist=re.findall('[0-9] h',text)
#    if len(reglist)>0:
#        for i in reglist:
#            i_rep=i.replace('h','heures')
#            text=re.sub(i,i_rep,text)

# change bounding | to < and > : OK
    #balise=set(re.findall(r"\|\w+_?\w+\|",text))
    #if len(balise)>0:
        #print(balise)
    #    for b in balise:
    #        new_balise='<'+b[1:len(b)-1]+'>'
    #        text=text.replace(b,new_balise)
    #print(text)
    # c'est l'essaim ....
    text=text.replace('|',' ')
    text=re.sub("[ ]-|-$","",text)
    words=[]

    for word in re.split(" ",text):     
        if word in chiffres_romains:
            word = chiffres_romains[word]
        elif word in autre:
            word=autre[word]
        elif word in autre_bis:
            word=autre_bis[word]
        words.append(word)

    text=" ".join(words)
    text=text.lower()

    text=text.replace(" km h "," kilomètres par heure ")
    text=text.replace(" km", " kilomètres ")
    text=text.replace(" kwh"," kilowatt par heure ")
    text=text.replace(" kw"," kilowatt ")
    # replace n succesive spaces with one space. : OK
    text=re.sub(r"\s{2,}"," ",text)

    return text

if len(sys.argv) !=3:
    print ("ERROR Parser : Mauvais usage")
    print ("bon usage :")
    print ("python scripts/parseESTERSyncV2.py <IN_CORPUS> <OUT_CORPUS>")
else:
    corpus_name = sys.argv[2]
    file_name = sys.argv[1]


F2=open(corpus_name,"w")

# Application de la transformation ligne par ligne
with open(file_name,"r") as f:
    lines=f.readlines()
    for line in lines:
        line = re.sub("\[.*?\]","",line) # suppression des crochets avant le découpage en phrase
        line=re.sub(r'\{.+\}','',line)
        line=re.sub(r'\(.+\)','',line)
        line=re.sub(r'\<.+\>','',line)

        
        for phrase in  re.split('\.|\!|\?',line):
            if ("Sur les autres projets Wikimedia" in phrase or phrase=='\n' or len(phrase) <50):
                pass
            else:
                #if any(len(i)>25 for i in phrase.split(' ')): #Verification que les mots ne depassent pas la taille du plus grand mot français
                #    pass
                #else:
                    # Application de la transformation
                corrected = transformation_text(phrase)
                
                F2.write(corrected + "\n")
        
F2.close()

