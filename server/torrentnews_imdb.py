
from imdb import Cinemagoer




from torrentnews_item import RSSItem
import requests




class TorrentNewsIMBD():


    LINK_PREFIX = 'https://www.imdb.com/title/tt'
    
    IMDB_NOTFOUND = '???'

    def __init__(self):
        self.ia = Cinemagoer()
        
        
        
    def SetCover(self,rss:RSSItem,url:str):
    
        n = url.rfind('@')
        m = url.rfind('.')
        if (n!=-1) and (m!=-1):
            url = url[:n + 1] + url[m:]
        else:
            n = url.rfind('._')
            m = url.rfind('_.')  
            url = url[:n + 1] + url[m+2:]            
     
        rss.cover = url
        response = requests.head(url)  
        rss.cover_length = int(response.headers.get('content-length', None)) 
        rss.cover_type = response.headers.get('Content-Type',None)
        
        
    def Fill(self,rss:RSSItem,imdb):
        rss.imdbid = imdb.movieID
        if ('cover url' in imdb.data):
            self.SetCover(rss,imdb.data['cover url'])
        
        
    def CompareTitlesSoft(self,t1:str,t2:str)->bool:
        return RSSItem.comparestr(t1,t2,False)
        
    def CompareTitlesHard(self,t1:str,t2:str)->bool:
        return RSSItem.comparestr(t1,t2,True) 
        
    def UpdateItem(self, rss:RSSItem,isforceupdate:bool=False):
        if (rss.imdbid!=None) and (not isforceupdate):
            return
        if (rss.title==None):
            print("Update skip, NULL title detected")
            return
        
        print("Update: "+rss.title)
        
        try:
            items = self.ia.search_movie(rss.title)
        except Exception as e:
            print("IMDb error: "+str(e))
            items=None
            return
        
        if (items==None) or ( len(items)==0 ):
            print("Nothing similar found in IMDb '%s'" % rss.title)
            return
        firstfound = None
        for i in items:
            if (firstfound == None):
                firstfound = i
                
                
                #todo: put update in try-catch, get raiting
                
                
            #self.ia.update(i)
                
                
#rating (string)
#User rating on IMDb from 1 to 10, e.g. '7.8'.
#votes (string)
#Number of votes, e.g. '24,101'.
                
            #rrr = i.data['rating']
            if ('year' in i):
                iyear = int( i['year'] )
            else:
                iyear = None
            
            if (rss.season!=None):
                if i["kind"] in ["tv series", "tv mini series"]:
                    print("Found as TV series '%s' - '%s' " % (i['title'],rss.title))
                    self.Fill(rss,i)
                    break
            else:
                if (rss.year!=None) and (iyear!=None):
                     if (rss.year == iyear):
                        print("Found by year '%s' - '%s' " % (i['title'],rss.title))
                        self.Fill(rss,i)
                        break
                        
            if self.CompareTitlesHard(i['title'],rss.title):
                print("Tile compare ok '%s' - '%s' " % (i['title'],rss.title))
                self.Fill(rss,firstfound)
                break
                
            if (rss.year==None) or (iyear==None):
                if self.CompareTitlesSoft(i['title'],rss.title):
                    print("Best guess '%s' - '%s' " % (i['title'],rss.title))
                    self.Fill(rss,firstfound)
                    break

            #print('"'+i['title'] + '" :  id:"'+i.movieID+'"')
        if (rss.imdbid == None):
            print("Not found in IMDb among %i items" % len(items))    
            rss.imdbid = TorrentNewsIMBD.IMDB_NOTFOUND


    def UpdateAll(self, rssitems,isforceupdate:bool=False):
        for i in rssitems:
            self.UpdateItem(i,isforceupdate)



if __name__ == "__main__":


           
    from torrentnews_db import  TorrentNewsDB

    db = TorrentNewsDB('torrent','movie')
    db.Load()
    
    
    imbd = TorrentNewsIMBD()
    
    imbd.UpdateAll(db.data,True)
    
    db.Save()
    
    