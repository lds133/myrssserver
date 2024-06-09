
import os

from rssgrabber_base import RSSGetFileInfo,MDTextStatus





class MDGrabberStatus(RSSGetFileInfo,MDTextStatus):



    def __init__(self):
        super().__init__()
        self.mimetypestr = "text/plain"
        self.rawfilename =  "tmp_grabberstatus.md"
        self.dir = None
        self.texts = {}
        
        
    def MDTextReset(self,id:str):
        self.texts[id] = "" 
        
    def MDTextAdd(self,id:str,text:str):
        self.texts[id] += "\r\n"+text 
        
        
    def MDTextSave(self):
        mdtext = "# MDGrabberStatus"
        for id in self.texts.keys():
            mdtext+="## "+id+"\r\n"
            mdtext+=self.texts[id]+"\r\n"
            mdtext+="&nbsp;\r\n"
            
        filepath =  self.rawfilename if  self.dir==None else os.path.join(self.dir,self.rawfilename)
        
        with open(filepath, "w") as text_file:
            text_file.write(mdtext)        