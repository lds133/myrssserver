#!/usr/bin/env python

import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler, ThreadingHTTPServer

from rssgrabber import RSS_READ_TAB, run_rssgrabber
import copy





class S(BaseHTTPRequestHandler):

    
    
    
    file_tab_init = [    ("index.html"                         , "text/html"                , None ), 
                         ("site.css"                           , "text/css"                 , 'static' ),
                         ("favicon.ico"                        , "image/x-icon"             , 'static' ),
                         ("serverapi.js"                       , "text/javascript"          , 'static' ),
                    ]


    def IntegrateRSS(self):
        for rss in RSS_READ_TAB:
            if (rss.is_save_rss):
                item = (  rss.rawfilename ,  rss.mimetypestr, rss.dir)
                self.file_tab.append( item )


    def __init__(self, *args, **kwargs):
        self.file_tab = copy.copy(self.file_tab_init)
        self.IntegrateRSS()
        super().__init__(*args, **kwargs)

        


    def is_binary_mime(self,mimetype:str):
        return  (mimetype=="image/png") or (mimetype=="application/octet-stream") or (mimetype=="image/x-icon")


    def execute_request_file_unsafe(self,filename:str,mimetype:str):


        if (not os.path.exists(filename)):
            print("File not found: "+filename)
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

    run_rssgrabber()

    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print("Starting httpd server on %s:%i" % (addr,port) )
    httpd.serve_forever()





if __name__ == "__main__":



    
    
    
    
    #run(addr="192.168.30.9", port=33331)
    run(addr="localhost", port=33331)
