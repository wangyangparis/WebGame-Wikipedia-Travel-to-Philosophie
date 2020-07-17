#!/usr/bin/python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from json import loads
from urllib.request import urlopen
import urllib.parse
from urllib.parse import urlencode
import ssl
from flask import Flask, request

global cache 
cache={}

def getJSON(page):
    params = urlencode({
      'format': 'json',  
      'action': 'parse', 
      'prop': 'text', 
      'redirects':True,
      'page': page})
    API = "https://fr.wikipedia.org/w/api.php"  
    # désactivation de la vérification SSL pour contourner un problème sur le
    # serveur d'évaluation -- ne pas modifier
    gcontext = ssl.SSLContext()
    response = urlopen(API + "?" + params, context=gcontext)
    return response.read().decode('utf-8') #.decode('unicode')


def getRawPage(page):
    # prob de redirection if page!= page: 
    parsed = loads(getJSON(page))
    #print(parsed)
    try:
        #print(persed)
        title = parsed['parse']['title'] 
        content = parsed['parse']['text']['*']  
        #print(content)
        return title, content
    except KeyError:
        # La page demandée n'existe pas
        return None, None


def getPage(page):
    if page in cache.keys():
        return page, cache[page]
        
    try:
        page,content=getRawPage(page)
        soup=BeautifulSoup(content,features="html.parser")
        paragraphes=soup.find('div', {"class": "mw-parser-output"}).find_all('p',recursive=False)
        links=[]
        titles=[]
        count=0
        for p in paragraphes:
            a=p.find_all('a')
            for link in a:
                if link.get('href').startswith("/wiki") and (':' not in link.get('href')): #eliminate Aide:
                    l=urllib.parse.unquote(link.get('href')[6:].replace('_',' '))
                    if l != [] and (l not in links) and "#" not in l and count<=10:
                        links.append(l)
                        titles.append(link.get('title'))
                        count=count+1
        
                else:
                    pass
    
    except:
        return (None,[])
    links=links[:10]
    cache[page]=links
    return page,links
    
if __name__ == '__main__':
    print("Ça fonctionne !")
    