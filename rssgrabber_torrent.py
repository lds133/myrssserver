from __future__ import annotations

import requests
import time
import json
import os
from bs4 import BeautifulSoup
from datetime import datetime

from rssgrabber_base import RSSGet,RSSGrab
from torrentnews_item import RSSItem
from torrentnews_db import  TorrentNewsDB


 
class RSSGetTorrent(RSSGet):

    DIR = 'torrent'


    def PreInit(self):
        super().PreInit()
        self.grabberid = RSSGrabTorrent.TITLE
        self.is_save_headers = False
        self.is_save_html = False
        self.is_save_rss = False
        self.dir = RSSGetTorrent.DIR
        
        
    def __init__(self, site:str, path:str, filename:str, dbname:str,dbname_newitems:str=None ):
        super().__init__( site, path, filename )
        self.dbname = dbname
        self.dbnamenew = dbname_newitems
        
        

class RSSGetTorrentDB(RSSGet):

    DIR = 'torrent'


    def PreInit(self):
        super().PreInit()
        self.grabberid = RSSSaveTorrentNews.TITLE
        self.is_save_headers = False
        self.is_save_html = False
        self.is_save_rss = True
        self.dir = RSSGetTorrentDB.DIR
        
        
        
    def __init__(self, dbname:str, filename:str ):
        super().__init__(None,None,filename)
        self.dbname = dbname



class RSSGrabTorrent(RSSGrab):        


    TITLE = 'torrent'

    def __init__(self):
        print('Collect torrent news')
        
        
        
    def Title(self):
        return self.TITLE
        
    def ReadHTMLFromURL(self,rss:RSSGet)->str:
        html_text = None
        with requests.Session() as s:
            print("Reading: "+rss.url)
            r = s.get(rss.url, headers=rss.req_headers)
            html_text = r.text
            if (rss.is_save_html):
                print("Writing HTML: "+rss.htmlfilename)
                with open(rss.htmlfilename, 'w', encoding='utf-8') as f:
                    f.write(r.text)
            if (rss.is_save_headers):
                with open(self.headfilename, 'w', encoding='utf-8') as f:
                   f.write( json.dumps(dict(r.headers), indent = 4)  )

        return html_text
        
    def ReadHTMLFromFile(self,rss:RSSGet)->str:
        print("Reading HTML: "+rss.htmlfilename)
        html_text = None
        with open(rss.htmlfilename) as fp:
            html_text = fp.read()
        return html_text
    
    
    
    
    def GrabUnsafe(self,rss:RSSGet):
        assert(rss.dbname!=None)
        html_text = self.ReadHTMLFromURL(rss)
        #html_text = self.ReadHTMLFromFile(rss)
        rssitems = TorrentHTMLParser.Parse(rss.url,html_text,rss.filename)
        if (rss.dbnamenew == None):
            db = TorrentNewsDB(rss.DIR,rss.dbname) 
            db.UpdateDB(rssitems,TorrentNewsDB.FILTRYEAR_ALL)
        else:
            db = TorrentNewsDB(rss.DIR,rss.dbname) 
            db.UpdateDB(rssitems,TorrentNewsDB.FILTRYEAR_OLD)
            db = TorrentNewsDB(rss.DIR,rss.dbnamenew) 
            db.UpdateDB(rssitems,TorrentNewsDB.FILTRYEAR_NEW)
        




class RSSSaveTorrentNews(RSSGrab):        


    TITLE = 'torrentdb'

    def __init__(self):
        print('Export torrent news database')
        
        
        
    def Title(self):
        return self.TITLE
        
        
    def GrabUnsafe(self,rss:RSSGet):
        assert(rss.dbname!=None)
        db = TorrentNewsDB(rss.DIR,rss.dbname)
        db.Load()
        db.WriteRSS(rss.xmlfilename,"Torrent News "+rss.dbname)
    
    
    
    
class TorrentHTMLParser():
    
    
    def Parse(url:str,html_text:str,source_title:str)->list[RSSItem]:
    
        if ('kikass' in url ):
            return TorrentHTMLParser.Parse_kikass(url,html_text,source_title)

        if ('1337x' in url ):
            return TorrentHTMLParser.Parse_leetx(url,html_text,source_title)

        
        return None
    
    
    @staticmethod
    def Parse_kikass(url:str,html_text:str,source_title:str)->list[RSSItem]:
        rssitems = []
        print("Parsing: kikass")
        soup =  BeautifulSoup(html_text, 'html.parser')
        index = 0
        for tag in soup.find_all('div', attrs={'class':'torrentname'}):
            i = RSSItem()
            i.src = source_title
            rssitems.append( i )
            ntag = tag.find('a', attrs={'class':'cellMainLink'})
            i.text = ntag.text.strip()
            i.link = url + ntag['href']
            ppp = tag.parent.parent
            n=0
            for td in ppp.find_all('td'):
                if n==1:
                    i.size = td.text.strip()
                if n==2:
                    i.author = td.text.strip()
                if n==4:
                    i.seed = td.text.strip()
                if n==5:
                    i.leech = td.text.strip()         
                n+=1
            i.index = index
            i.SplitText()
            
            if (i.title==None):
                print("Parse error: "+i.text)
            
            index+=1
    
        return rssitems
    
    
    @staticmethod
    def Parse_leetx(url:str,html_text:str,source_title:str)->list[RSSItem]:
        rssitems = []
        print("Parsing: leetx")
        soup =  BeautifulSoup(html_text, 'html.parser')
        index = 0
        for tag in soup.find_all('td', attrs={'class':'name'}):
            i = RSSItem()
            i.src = source_title
            rssitems.append( i )
            ntag = tag.find('a',attrs={'class': None})
            i.text = ntag.text.strip().replace('.',' ')
            i.link = url + ntag['href']
            ppp = tag.parent
            n=0
            for td in ppp.find_all('td'):
                if n==1:
                    i.seed= td.text.strip()
                if n==2:
                    i.leech = td.text.strip()
                if n==4:
                    #i.size = td.text.strip()
                    i.size = td.find(string=True, recursive=False)
                if n==5:
                    i.author = td.text.strip()         
                n+=1
            i.index = index
            i.SplitText()
            
            if (i.title==None):
                print("Parse error: "+i.text)
            
            index+=1
    
        return rssitems
    
    
if __name__ == "__main__":

    #rss =RSSGetTorrent('https://kikass.to','/popular-movies','kikass_movies','movie_old','movie_new')
    #rss =RSSGetTorrent('https://kikass.to','/popular-tv','kikass_tv','tv')
    #rss = RSSGetTorrent('https://www.1337x.to','/popular-movies-week','1337x_movies',,'movie_old','movie_new')
    #rss = RSSGetTorrent('https://www.1337x.to','/popular-tv-week','1337x_tv','tv')

    #rss.is_save_html = True

    #torrent   = RSSGrabTorrent()
    

    #torrent.Grab(rss)


    #exit()


    
    torrentdb = RSSSaveTorrentNews()    
    
    xml1 = RSSGetTorrentDB('movie_new','torrents_newsD')
    xml2 = RSSGetTorrentDB('movie_old','torrents_newsB')
    xml3 = RSSGetTorrentDB('tv',   'torrents_newsC')
    
    
    torrentdb.Grab(xml1)    
    torrentdb.Grab(xml2)    
    torrentdb.Grab(xml3)  
    


    
    

    