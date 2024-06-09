
import os


class RSSGetFileInfo():


    def __init__(self, ):
        self.mimetypestr = None
        self.rawfilename =  None
        self.dir = None
        self.grabberid = None
        self.is_save_rss = False
        
        
class MDTextStatus():


    def MDTextReset(self,id:str):
        pass
        
    def MDTextAdd(self,id:str,text:str):
        pass
        
        
    def MDTextSave(self):
        pass
                
        
        

class RSSGet(RSSGetFileInfo):

    HEADERS =  {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    DIR = None

    def __init__(self, site:str, path:str, filename:str ):
        super().__init__()
        self.mimetypestr = "application/atom+xml"
        self.PreInit()
        self.site = site
        self.path = path
        self.filename = filename
        self.PostInit()

        
        

    def PreInit(self):
        self.grabberid = None
        self.req_headers = RSSGet.HEADERS
        self.is_save_headers = False
        self.is_save_html = False
        self.is_save_rss = True
        self.dir = None
        self.headers_file_ext =  '.json'
        self.rss_file_ext = '.xml' 
        self.html_file_ext = '.html' 


    def PostInit(self):
        self.rawfilename =  self.filename + self.rss_file_ext
        self.xmlfilename = self.dir +'/'+ self.rawfilename
        self.headfilename = self.dir +'/'+self.filename + self.headers_file_ext    
        self.htmlfilename = self.dir +'/'+self.filename + self.html_file_ext  
        self.url = None if (self.site==None or self.path==None) else  ( str(self.site or '') + str(self.path or '') )
        assert(self.dir!=None)
        assert(self.grabberid!=None)
        
        self.CheckDir()
        
        
    def CheckDir(self):
        assert(self.DIR!=None)
        assert(self.DIR!="")
        if not os.path.exists(self.DIR):
            os.makedirs(self.DIR)
            print("Directory "+self.DIR+" created")
            
        
    def ID(self):
        return self.filename
        
        
class RSSGrab():        

    def __init__(self):
        self.currmdstatus = None
        self.currrss = None
        
        
        
        
        
        
    def Grab(self,rss:RSSGet,mdstatus:MDTextStatus):
        self.currmdstatus = mdstatus
        self.currrss = rss

        self.GrabUnsafe(rss)

        self.currmdstatus = None
        self.currrss = None
        
        
    def GrabUnsafe(self,rss:RSSGet):
        raise NotImplementedError
        
        
        
    def MDReset(self):
        if (self.currmdstatus != None) and (self.currrss!=None):
            self.currmdstatus.MDTextReset(self.currrss.ID())
            
        
    def MDAdd(self,text:str):
        if (self.currmdstatus != None) and (self.currrss!=None):
            self.currmdstatus.MDTextAdd(self.currrss.ID(),text)
        
        
    def MDSave(self):
        if (self.currmdstatus != None) and (self.currrss!=None):
            self.currmdstatus.MDTextSave()
        
        
        