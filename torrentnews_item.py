from __future__ import annotations
import re
import datetime
import os
import json 
import string
import uuid



class RSSItem:
    
    # todo: compile regex    re.compile("
    
    LONG_TITLE_CHARS = 20
    
    @staticmethod
    def limitlen(s:str,n:int):
        if (len(s)>=n):
            s = s[0: n]
        return s

        
    @staticmethod
    def comparestr(s1:str, s2:str, isstrict:bool=True):
        if (s1==None) or (s2==None):
            return s1==s2
        remove = string.punctuation + string.whitespace
        mapping = {ord(c): None for c in remove}
        s1 = s1.translate(mapping).lower().strip()
        s2 = s2.translate(mapping).lower().strip()
        s1 = RSSItem.limitlen(s1,RSSItem.LONG_TITLE_CHARS)
        s2 = RSSItem.limitlen(s2,RSSItem.LONG_TITLE_CHARS)
        if (len(s1)==len(s2)):
            return s1==s2
        if (isstrict):
            return False
        if (len(s1)<len(s2)):   
            return s2.startswith(s1)
        return s1.startswith(s2) 
            
    

    def ToDict(self)->dict:
        result = {}
        result['t'] = self.title
        if (self.season!=None):
            result['s']=self.season   
        if (self.episode!=None):    
            result['e']=self.episode  
        if (self.year!=None):
            result['y']=self.year   
        if (self.quality!=None):
            result['q']=self.quality 
        result['ts']=self.TimestampStr()   
        result['g']=self.guid  
        if (self.imdbid!=None):
            result['i']=self.imdbid
        if (self.cover!=None):
            result['cu']=self.cover
        if (self.cover_length!=None):
            result['cl']=self.cover_length     
        if (self.cover_type!=None):
            result['ct']=self.cover_type  
        if (self.size!=None):
            result['len']=self.size  
        if (self.src!=None):
            result['src']=self.src
        if (self.text!=None):
            result['txt']=self.text           
        return result
        
    def FromDict(self,d:dict):
        self.title          = d['t']
        self.guid           = d['g']
        self.season         = d['s']      if 's'    in d else None 
        self.episode        = d['e']      if 'e'    in d else None 
        self.year           = d['y']      if 'y'    in d else None 
        self.quality        = d['q']      if 'q'    in d else None 
        self.imdbid         = d['i']      if 'i'    in d else None 
        self.cover          = d['cu']     if 'cu'    in d else None 
        self.cover_length   = d['cl']     if 'cl'   in d else None 
        self.cover_type     = d['ct']     if 'ct'   in d else None 
        self.size           = d['len']    if 'len' in d else None 
        self.src            = d['src']    if 'src' in d else None 
        self.text           = d['txt']    if 'txt' in d else None 
        self.time           = None if d['ts']=='' else datetime.datetime.fromisoformat( d['ts'] )     
    
    def CreateTimestamp(self):
        self.time    =  datetime.datetime.now()
        
    def CheckTimestamp(self,not_older_than_days):
        if (self.time==None):
            return False
        t = datetime.datetime.now() - datetime.timedelta(days=not_older_than_days)
        return self.time>=t
        
        
        
    def IsNew(self,year:int):
        if (self.year == None):
            return False
        return self.year>=year


    
    def Compare(self,i:RSSItem )->bool:
        if RSSItem.comparestr(i.title,self.title,True):
            return True
        if RSSItem.comparestr(i.title,self.title,False):    
            if (i.season!=None) and (i.season==self.season):
                if (i.episode==None) and (self.episode==None):
                    return True 
                return i.episode==self.episode
            if (i.year!=None) and (i.year==self.year):
                return True
        return False
        
    def Merge(self,i:RSSItem):
        if (i.year!=None) and (self.year==None):
            self.year = i.year
    
        
        
    
    def __init__(self):
        self.index         = None
        self.text          = None
        self.link          = None
        self.size          = None
        self.author        = None
        self.seed          = None
        self.leech         = None
                           
        self.title         = None
        self.season        = None
        self.episode       = None
        self.year          = None
        self.quality       = None
                           
        self.time          = None 
                           
        self.guid          = str(uuid.uuid4())
                           
        self.imdbid        = None
        self.cover         = None
        self.cover_length  = None
        self.cover_type    = None
        
        self.src           = None 
        
        
    def TVInfo(self):
        if (self.season!=None):
            if (self.episode!=None):
                return ' S%02iE%02i' % (self.season,self.episode)
            else:
                return ' S%02i' % (self.season)
          
        return ''
        
    def Description(self):
        
        return  '"' +str( self.title   or '?') + '" ' + \
                self.TVInfo() + \
                str( self.year    or '') + ' ' + \
                str( self.quality or '') + \
                ('' if self.size==None else (', Size %s' % self.size) ) + \
                ('' if self.src ==None else (', Found at %s' % self.src) ) 
            
            
    def TimestampStr(self):
        return '' if self.time==None else self.time.isoformat()
    
    
    def Text(self):
        tvinfo = self.TVInfo()
        return  str(self.title or 'Unknown Movie Title') + \
                ('' if self.year==None else (' (%i)' % self.year) ) + \
                ('' if len(tvinfo)==0 else (' ' + tvinfo) ) 
 
    @staticmethod
    def MIN(n1,n2):
        if (n2==None) and (n1!=None):
            return n1
        if (n2!=None) and (n1==None):
            return n2 
        if (n2==None) and (n1==None):
            return None
        return n1 if n1<n2 else n2
            
 
    def SplitText(self):
        
        rxstr_year20xx = r'[\s\(](20[0123][\d])[\s\)]'
        rxstr_year19xx = r'[\s\(](19[456789][\d])[\s\)]'
        rxstr_tv1 = r'[\s\(]S([\d]{1,3})E([\d]{1,3})[\s\)]'
        rxstr_tv2 = r'[\s\(]S([\d]{1,3})[\s\)]'
        rxstr_q1 = r'[\s\(]([\d]{2,4}p)[\s\)]'
        rxstr_q2 = r'[\s\(](WEB[\S]*|HDTV)[\s\)]'
        sepchars = ['(','-']
        stripchars = "\r\n\t -,."
        
        n = None
        m = re.search(rxstr_year20xx, self.text,re.IGNORECASE)
        if (m==None):
            m = re.search(rxstr_year19xx, self.text,re.IGNORECASE)
        if (m!=None):
            n = RSSItem.MIN( n, m.start(0) )
            self.year  = int(m.group(1))
            
        m = re.search(rxstr_tv1, self.text,re.IGNORECASE)
        if (m!=None):
            n = RSSItem.MIN( n, m.start(0) )
            self.season  = int(m.group(1))
            self.episode = int(m.group(2))
            
        m = re.search(rxstr_q1, self.text,re.IGNORECASE)
        if (m!=None):
            n = RSSItem.MIN( n, m.start(0) )
            self.quality  = m.group(1)
            
        m = re.search(rxstr_q2, self.text,re.IGNORECASE)
        if (m!=None):
            n = RSSItem.MIN( n, m.start(0) )
            self.quality  = m.group(1) if self.quality==None else (self.quality+', '+m.group(1))
            
        m = re.search(rxstr_tv2, self.text,re.IGNORECASE)
        if (m!=None):
            n = RSSItem.MIN( n, m.start(0) )
            self.season  = int(m.group(1))
            
        if (n!=None):
            self.title = self.text[0:n]

        if (self.title==None):
            n=-1
            for c in sepchars:
                n = self.text.find(c)
                if (n!=-1):
                    self.title = self.text[0:n]
                    break
         
            
        if (self.title!=None):
            self.title = self.title.replace(".", " ")
            self.title = self.title.strip(stripchars)
            
        




