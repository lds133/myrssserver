
import os

from rssgrabber_base import RSSGetFileInfo,MDTextStatus





class MDGrabberStatus(RSSGetFileInfo,MDTextStatus):

    GLOBALID = "$$$"
    LF="\r\n"

    def __init__(self):
        super().__init__()
        self.mimetypestr = "text/plain"
        self.rawfilename =  "tmp_grabberstatus.md"
        self.dir = None
        self.texts = {}
        self.is_save_rss = True
        
        
    def MDTextReset(self,id:str):
        self.texts[id] = "" 
        
    def MDTextAdd(self,id:str,text:str):
        self.texts[id] += text + self.LF
        
        
    def MDTextSave(self):
        mdtext = "# MDGrabberStatus"+self.LF
        mdtext+=self.texts[self.GLOBALID]+self.LF
        mdtext+=self.LF+self.LF
        
        for id in self.texts.keys():
            if id!=self.GLOBALID:
                mdtext+="## "+id+self.LF
                mdtext+=self.texts[id]+self.LF
                mdtext+=self.LF+self.LF
            
        filepath =  self.rawfilename if  self.dir==None else os.path.join(self.dir,self.rawfilename)
        
        with open(filepath, "w") as text_file:
            text_file.write(mdtext)        