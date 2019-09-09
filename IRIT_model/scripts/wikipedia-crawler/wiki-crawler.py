# -*- coding: utf-8 -*-
# Wikipedia Crawler v4
# Inspired by Hardik Vasa's Wikipedia Crawler V3
# @author: Magdeleine Erwan

# argument 1 : nombre de sites a crawler depuis chaque 

#Import Libraries

import time     #For Delay
import urllib2
import re

from bs4 import BeautifulSoup
import sys


corpus_path=sys.argv[1]

#Defining pages

starting_pages = ["https://fr.wikipedia.org/wiki/Intelligence_artificielle","https://fr.wikipedia.org/wiki/Alan_Turing","https://fr.wikipedia.org/wiki/Robot","https://fr.wikipedia.org/wiki/Machine","https://fr.wikipedia.org/wiki/Intelligence","https://fr.wikipedia.org/wiki/Anthropomorphisme","https://fr.wikipedia.org/wiki/Paradoxe","https://fr.wikipedia.org/wiki/Bise_(vent)","https://fr.wikipedia.org/wiki/Chatbot"]

seed_page = "https://fr.wikipedia.org"  #Crawling the French Wikipedia

#Downloading entire Web Document (Raw Page Content)
def download_page(url):
    try:
        req=urllib2.Request(url)
        resp=urllib2.urlopen(req)
        respData=str(resp.read())
        flag=1
        return respData, flag
    except Exception as e:
        print(str(e))
        flag=False
        respData=[]
        return respData,flag

#permet de verifier si une chaine est entierement composee de nombre (utilisee pour corriger les problemes dus au non break spaces qui apparaissent lors du parsing
def is_numerical(text):
    for letter in text:
        if ord(letter)<48 or ord(letter)>57:
            return False
    return True

# Extraire les paragraphes de texte du fichier HTML
def extract_data(raw_html):

    raw_data=""
    soup=BeautifulSoup(raw_html,'html.parser')

    # Suppression des tags HTML non désirés

    for sup_tag in soup.findAll('sup'):
        sup_tag.replace_with('')

    for table_tag in soup.findAll('table'):
        table_tag.replace_with('')

    for sub_tag in soup.findAll('sub'):
        sub_tag.replace_with('')

    for span_tag in soup.findAll('span'):
            span_tag.replace_with('')

    for span_tag in soup.findAll('li'):
        span_tag.replace_with('')

    for link in soup.find_all('p'):
        raw_data=raw_data+link.get_text()

    return raw_data
    
    
#Extract all the links
#Finding 'Next Link' on a given web page
def get_next_link(s):
    start_link = s.find("<a href")
    if start_link == -1:    #If no links are found then give an error!
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_quote = s.find('"', start_link)
        end_quote = s.find('"',start_quote+1)
        link = str(s[start_quote+1:end_quote])
        return link, end_quote
          

#Getting all links with the help of 'get_next_links'
def get_all_links(page):
    links = []
    while True:
        link, end_link = get_next_link(page)
        if link == "no_links":
            break
        else:
            links.append(link)      #Append all the links in the list named 'Links'
            #time.sleep(0.1)
            page = page[end_link:]
    return links 


#Crawl Initiation
#Check for file type in URL so crawler does not crawl images and text files
def extension_scan(url):
    a = ['.png','.jpg','.jpeg','.gif','.tif','.txt','JPG','svg']
    j = 0
    while j < (len(a)):
        if a[j] in url:
            #print("There!")
            flag2 = 1
            break
        else:
            #print("Not There!")
            flag2 = 0
            j = j+1
    #print(flag2)
    return flag2


#URL parsing for incomplete or duplicate URLs
def url_parse(url):
    try:
        from urllib.parse import urlparse
    except ImportError:
        from urlparse import urlparse
    url = url  #.lower()    #Make it lower case
    s = urlparse(url)       #parse the given url
    seed_page_n = seed_page #.lower()       #Make it lower case
    #t = urlparse(seed_page_n)     #parse the seed page (reference page)
    i = 0
    flag = 0
    while i<=9:
        if url == "/":
            url = seed_page_n
            flag = 0  
        elif not s.scheme:
            url = "http://" + url
            flag = 0
        elif "#" in url:
            url = url[:url.find("#")]
            flag = 0
        elif "?" in url:
            url = url[:url.find("?")]
            flag = 0
        elif s.netloc == "":
            url = seed_page + s.path
            flag = 0
        #elif "www" not in url:
        #    url = "www."[:7] + url[7:]
        #    flag = 0
            
        elif url[len(url)-1] == "/":
            url = url[:-1]
            flag = 0
        #elif s.netloc != t.netloc:
        #    url = url
        #    flag = 1
        #    break        
        else:
            url = url
            flag = 0
            break
        
        i = i+1
        s = urlparse(url)   #Parse after every loop to update the values of url parameters
    
    if "fr.wikipedia.org" not in url:
        flag = 1

    return(url, flag)
     
t0 = time.time()
database = {}   #Create a dictionary

#Main Crawl function that calls all the above function and crawls the entire site sequentially
def web_crawl():

    crawled=[]

    for starting_page in starting_pages:

        count = 0
        print "new link"
        if starting_page in crawled:
            pass
        else:
            to_crawl = [starting_page]      #Define list name 'Seed Page'        
                      
        while count <200:

            urll = to_crawl.pop(0)      #If there are elements in to_crawl then pop out the first element
            urll,flag = url_parse(urll)
            flag2 = extension_scan(urll)
            time.sleep(3)

            #If flag = 1, then the URL is outside the seed domain URL
            if  flag==1 or flag2 == 1:
               # print("flag")
                pass        #Do Nothing
                
            else:       
                if urll in crawled:     #Else check if the URL is already crawled
                    pass
                else:       #If the URL is not already crawled, then crawl i and extract all the links from it
                    # Download raw HTML page
                    raw_html,flagg = download_page(urll)
                    #print(flagg)                  
                    
                    if flagg==1:
                    # Extract the full text of the article
                        data=extract_data(raw_html)
                        if len(data)<2000:
                            crawled.append(urll)
                        else:
                            count=count+1
                            print(starting_pages.index(starting_page),len(starting_pages),count)
                            print("Link = "+urll)
                            to_crawl = to_crawl + get_all_links(raw_html)
                            to_crawl = [g for g in to_crawl if '/wiki/' in g and 'Aide:' not in g and 'Catégorie:' not in g and "Discussion:" not in g and "Portail:" not in g and g not in crawled] #permet de recupérer uniquement les liens menant vers des articles wikipedia
                            data=data.replace(u'\xa0',u' ') #remplacement des espaces insecables par des espaces normaux
                            data=data.replace(u'’',u"'") #remplacement des appostrophes particulières en appostrophes simples
                            data=data.replace(u'œ',u'oe')
                            data=data.replace(u'°C',u'degré celcius')
                        
                            # filtrage des caracteres speciaux
                            filtered_data=[]
                            for word in data.split(' '): #Boucle sur les mots récupérés
                                reconstructed_word=''
                                for letter in word: # remplacement des non breakable space en espaces classiques
                                    if ord(letter) in range (0,126) or ord(letter) in range (192,255): #filtrage des caractères spéciaux
                                            reconstructed_word += letter


                                filtered_data.append(reconstructed_word)


                            for ind in xrange(len(filtered_data)-1,-1,-1): #regroupement des nombres contenant plus de 3 caractères 
                            
                                mot=filtered_data[ind]
                                mot_precedent=filtered_data[ind-1]
                                is_num_mot=is_numerical(mot)
                                is_num_prec=is_numerical(mot_precedent)
                                if is_num_mot==True and is_num_prec==True:
                                    filtered_data[ind-1]=mot_precedent+mot
                                    del filtered_data[ind]
                                


                            crawled.append(urll)
                    
                            #Writing the output data into a text file
                            file = open(corpus_path+'raw_database.txt', 'a')        #Open the text file called raw_database.txt
                            #file.write(data.encode('utf8'))
                            file.write((' '.join(filtered_data)).encode('utf8'))      #write the content of the page in th file
                            file.close()                            #Close the file
    
                            #Remove duplicated from to_crawl
                            n = 1
                            j = 0
                           # #k = 0
                            while j < (len(to_crawl)-n):
                                if to_crawl[j] in to_crawl[j+1:(len(to_crawl)-1)]:
                                    to_crawl.pop(j)
                                    n = n+1
                                else:
                                    pass     #Do Nothing
                                j = j+1
                  
                  # i=i+1
                    #print(i)
                    #print(k)
                    #print(to_crawl)
                    #print("Iteration No. = " + str(i))
                    #print("To Crawl = " + str(len(to_crawl)))
                    #print("Crawled = " + str(len(crawled)))
    return ""

print (web_crawl())
t1 = time.time()
total_time = t1-t0
print(total_time)
