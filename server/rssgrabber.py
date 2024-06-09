
from rssgrabber_reddit  import  RSSGetReddit,RSSGrabReddit
from rssgrabber_torrent import  RSSGetTorrent,RSSGrabTorrent,RSSSaveTorrentNews,RSSGetTorrentDB
from rssgrabber_status  import  MDGrabberStatus
from threading import Thread
import time
import traceback

FULL_CYCLE_MINUTES = 120

RSS_THREAD = None

GRABBER_STATUS_FILE = MDGrabberStatus()


RSS_READ_TAB = [  

                     #RSSGetTorrentDB('movie_new','torrents_newsD'),
                     #RSSGetTorrentDB('movie_old','torrents_newsB'),
                     
                     
                     #RSSGetReddit( 'tjournal_refugees' ), 
                     
                     #RSSGetTorrentDB('tv',   'torrents_newsC'),

                     RSSGetReddit( 'poland'            ),
                     
                     #RSSGetTorrent('https://kikass.to','/popular-movies','kikass_movies','movie_old','movie_new'),
                     
                     #RSSGetReddit( 'ukraine'           ),
                    
                     #RSSGetTorrent('https://kikass.to','/popular-tv','kikass_tv','tv'),
                    
                     #RSSGetReddit( 'learnpolish'       ),
                     
                     #RSSGetTorrent('https://www.1337x.to','/popular-movies-week','1337x_movies','movie_old','movie_new'),
                     
                     #RSSGetReddit( 'warsaw'            ),
                     
                     #RSSGetTorrent('https://www.1337x.to','/popular-tv-week','1337x_tv','tv'),
                     
                     
                     GRABBER_STATUS_FILE,
    
]

def run_rssgrabber():
    RSS_THREAD = Thread(target = rss_threaded_function )
    RSS_THREAD.start()



def rss_threaded_function():
    statusmd = GRABBER_STATUS_FILE
    readtab = RSS_READ_TAB
    read_delay_sec = int( FULL_CYCLE_MINUTES*60 / len(readtab) )

    reddit    = RSSGrabReddit()
    torrent   = RSSGrabTorrent()
    torrentdb = RSSSaveTorrentNews()
    GRABBERS = { reddit.Title()   : reddit,
                 torrent.Title()  : torrent,
                 torrentdb.Title(): torrentdb
                }


    while(True):
        for rss in readtab:
            try:
                statusmd.MDTextReset(rss.ID())
                GRABBERS[rss.grabberid].Grab(rss,statusmd)
            except Exception as e:
                statusmd.MDTextAdd(rss.ID(),"### Grab error: %s" % str(e))
                statusmd.MDTextAdd(traceback.format_exc())
            finally:
                statusmd.MDTextSave()
        
            time.sleep(read_delay_sec)


    
    
    



if __name__ == "__main__":


    rss_threaded_function()



