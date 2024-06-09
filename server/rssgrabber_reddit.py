from __future__ import annotations
from rssgrabber_base import RSSGet,RSSGrab,MDTextStatus



import requests
import time
import json




class RSSGetReddit(RSSGet):


    URL = 'https://www.reddit.com'
    DIR = 'reddit'

    def PreInit(self):
        super().PreInit()
        self.grabberid = RSSGrabReddit.TITLE
        self.req_headers = RSSGet.HEADERS
        self.is_save_headers = False
        self.is_save_html = False
        self.is_save_rss = True
        self.dir = RSSGetReddit.DIR

        
        
    def __init__(self, subredditname:str ):
        self.subredditname = subredditname
        super().__init__( RSSGetReddit.URL, '/r/'+subredditname+'/.rss', 'rss_'+subredditname )







class RSSGrabReddit(RSSGrab):        


    TITLE = 'reddit'

    def __init__(self):
        #print('Making cache for my reddit rss strips.')
        pass
        
        
    def Title(self):
        return self.TITLE
        
        
    def GrabUnsafe(self,rss:RSSGet):
        with requests.Session() as s:            
            self.MDAdd("Reading ["+rss.subredditname+"]("+rss.URL+rss.path+")" )
            r = s.get(rss.url, headers=rss.req_headers)
        
        if (rss.is_save_rss):
            self.MDAdd("Writing ["+rss.filename+"]("+rss.rawfilename+")")
            with open(rss.xmlfilename, 'w', encoding='utf-8') as f:
                f.write(r.text)
        if (rss.is_save_headers):
            with open(rss.headfilename, 'w', encoding='utf-8') as f:
                f.write( json.dumps(dict(r.headers), indent = 4)  )





