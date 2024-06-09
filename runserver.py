#!/usr/bin/env python

import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler, ThreadingHTTPServer

from sqlread import SQLRead

from rssgrabber import RSS_READ_TAB, run_rssgrabber



#http://94.158.81.18:33331/rss_tjournal_refugees.xml
#http://94.158.81.18:33331/rss_poland.xml     
#http://94.158.81.18:33331/rss_ukraine.xml          
#http://94.158.81.18:33331/rss_learnpolish.xml     
#http://94.158.81.18:33331/rss_warsaw.xml         








class S(BaseHTTPRequestHandler):

    
    
    
    file_tab = [    ("index.html"                         , "text/html"                , None ), 
                                                          
                                                                                        
                    ("favicon.ico"                        , "image/x-icon"             , 'static' ),
                                                          
                    
                    #("torrents_news.xml"                  , "application/atom+xml" ,     "torrent" ), 
                                                          
                    
                ]


    def IntegrateRSS(self):
        for rss in RSS_READ_TAB:
            if (rss.is_save_rss):
                item = (  rss.rawfilename ,  rss.mimetypestr, rss.dir)
                self.file_tab.append( item )


    def __init__(self, *args, **kwargs):
        self.IntegrateRSS()
        run_rssgrabber()
        super().__init__(*args, **kwargs)

        


    def is_binary_mime(self,mimetype:str):
        return  (mimetype=="image/png") or (mimetype=="application/octet-stream") or (mimetype=="image/x-icon")


    def execute_request_file_unsafe(self,filename:str,mimetype:str):


        if (not os.path.exists(filename)):
            self.send_error(404)
            return 


        self.send_response(200)
        self.send_header('Content-type', mimetype)
        self.end_headers()
        
        try:
            
            if self.is_binary_mime(mimetype):
                with open(filename, 'rb') as fh:
                    self.wfile.write(fh.read())            
            else:
                file = open(filename,mode='r')
                text = file.read()
                file.close()        
                #print("Read "+str(len(text))+" from '"+filename+"'")
                self.wfile.write( text.encode("utf8") )
            
        except Exception as  e:
            print("Read '"+filename+"' error: "+str(e))





          
  

    def do_GET(self):
        page = self.path.strip('/\\ ')
        print("REQ: "+page)


        for ft in self.file_tab:
            if (page.startswith(ft[0])):    
                filepath = ft[0] if  ft[2]==None else os.path.join(ft[2],ft[0])
                mimetype = ft[1]
                self.execute_request_file_unsafe( filepath, mimetype )
                return
            
        self.send_error(400)
            


    #def do_POST(self):
    #    content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
    #    post_data = self.rfile.read(content_length) # <--- Gets the data itself
    #    self._set_headers()
    #    self.wfile.write("<html><body><h1>POST!</h1><pre>" + post_data + "</pre></body></html>")







def run(server_class=ThreadingHTTPServer, handler_class=S, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()





if __name__ == "__main__":



    
    
    
    
    run(addr="192.168.0.30", port=33331)
