from __future__ import annotations
import datetime
import os
import json 
from torrentnews_item import RSSItem
from torrentnews_imdb import TorrentNewsIMBD






class TorrentNewsDB():


    FILTRYEAR_ALL = 0
    FILTRYEAR_NEW = 1
    FILTRYEAR_OLD = 2

    TOO_OLD_DAYS = 31

    def __init__(self,dir:str,dbname:str):
        self.data = []
        self.filename = os.path.join(dir,"torrentnews_"+dbname+".json")
        self.imbd = TorrentNewsIMBD()
        self.dbname = dbname
       
        
        
    def Load(self):
        self.data = []    
        if not os.path.isfile(self.filename):
            return
        print("Loading torrents db: "+self.filename)    
        f = open(self.filename)
        dbdata = json.load(f)
        for e in dbdata:
            i = RSSItem()
            i.FromDict(e)
            self.data.append(i)
        f.close()
        
        
    def Save(self):
        self.imbd.UpdateAll(self.data)
        print("Saving torrents db: "+self.filename) 
        dbdata = []
        delcounter = 0
        for i in self.data:
            if i.CheckTimestamp(self.TOO_OLD_DAYS):
                dbdata.append( i.ToDict() )
            else:
                delcounter +=1
        print("%i old records deleted at %s" % (delcounter,self.dbname))
        with open(self.filename, 'w') as f: 
            f.write(json.dumps(dbdata, indent = 4)) 
        
        
        
    def FindFirst(self,i0:RSSItem)->RSSItem:
        result = []
        for i in self.data:
            if i.Compare(i0):
                return i
        return None
    
    
    
        
    def Add(self,i0:RSSItem)->bool:
        i = self.FindFirst(i0)
        if (i!=None):
            i.Merge(i0)
            print("- %-85s -> %s" % (i0.text, i.Text()) )
            return False
        i0.CreateTimestamp()
        self.data.insert(0,i0)
        print("+ %-85s -> %s" % (i0.text, i0.Text()) )
        return True
    
        
        
    def Get(self,tooold_days)->list[RSSItem]:
        result = []
        for i in self.data:
            if i.CheckTimestamp(tooold_days):
                result.append(i)
        return result
        
        
        
    
    def UpdateDB(self,rssitems:list[RSSItem],yearfilter:int):
        self.Load()
        yeartocheck = datetime.datetime.now().year-1
        counter = 0
        for i in rssitems:
            if (yearfilter==TorrentNewsDB.FILTRYEAR_NEW) and (not i.IsNew(yeartocheck)):
                    print("- TOO OLD -> %s" %  i.Text() )
                    continue
            if (yearfilter==TorrentNewsDB.FILTRYEAR_OLD) and i.IsNew(yeartocheck):
                    print("- TOO NEW -> %s" %  i.Text() )
                    continue
            counter += 1 if self.Add(i) else 0
        print("%i torrents updated at %s" % (counter,self.dbname))    
        if (counter>0):
            self.Save()

        
    def escape(self, str_xml: str ):
        str_xml = str_xml.replace("&", "&amp;")
        str_xml = str_xml.replace("<", "&lt;")
        str_xml = str_xml.replace(">", "&gt;")
        str_xml = str_xml.replace("\"", "&quot;")
        str_xml = str_xml.replace("'", "&apos;")
        return str_xml
        
    def WriteRSS(self,xmlfilename,title,site=None):
        print("Writing XML: "+xmlfilename)
        with open(xmlfilename, 'w', encoding='utf-8') as f:
            f.write('<rss version="2.0">\n')
            f.write('<channel>\n')
            f.write('<title>'+self.escape(title)+'</title>\n')
            if (site!=None):
                f.write('<link>'+site+'</link>\n')
            f.write('<language>en</language>\n')
            f.write('<pubDate>'+str(datetime.datetime.now())+'</pubDate>\n')

            for i in self.Get(self.TOO_OLD_DAYS):
                f.write('<item>\n')
                f.write('<title>'+self.escape(i.Text())+'</title>\n')
                f.write('<description>\n')
                if ((i.imdbid==None) or (i.imdbid==TorrentNewsIMBD.IMDB_NOTFOUND)):
                    imdblink_href = ''
                    imdblink_html = ''
                else:
                    imdblink_href = TorrentNewsIMBD.LINK_PREFIX + i.imdbid 
                    imdblink_html = '&nbsp;<p><a href="'+imdblink_href+'">IMDb</a></p>'
                text_html = '' if i.text==None else ('&nbsp;<p>'+i.text+'</p>')
                f.write('<![CDATA[ <p>'+self.escape(i.Description())+'</p>'+text_html+imdblink_html+' ]]>\n')
                f.write('</description>\n')
                f.write('<pubDate>'+i.TimestampStr()+'</pubDate>\n')
                f.write('<guid>'+i.guid+'</guid>\n')
                if (i.cover!=None):
                    cl = '' if i.cover_length==None else ('length="'+str(i.cover_length)+'"')
                    ct = '' if i.cover_type==None else ('type="'+str(i.cover_type)+'"')
                    f.write('<enclosure  url="'+i.cover+'"  '+cl+' '+ct+' />\n')   
                if (i.imdbid!=None):            
                    f.write('<link>'+imdblink_href+'</link>\n')           
                f.write('</item>\n')
                
            f.write('</channel>\n')
            f.write('</rss>\n')

        
        
        

