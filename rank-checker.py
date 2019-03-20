import sys
import urllib.request
import traceback
import re
from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.parse import quote
from bs4 import BeautifulSoup

#constants
results_per_page = 50
max_pages = 2

#variables
counter_page=0
rank=0
visited=set()   
mentions=set()            
                    

def record_mentions(content):
    for link in BeautifulSoup(content, features='html.parser').findAll('a', href=True):  
                if "url?q=" in link["href"]:
                    
                    if link.text=='Cached' or len(link.text)<2: continue
                    list_href = [x.replace("/url?q=","") for x in (re.split(":(?=http)",link["href"])) if "webcache" not in x and not x.startswith("//")]
                    
                    if len(list_href)!=1:
                        print ("error parsing: " + link["href"]+ ", candidate urls:" + list_href) 
                    href_without_params = str(list_href[0]).split('&',1)[0]
                    
                    if (href_without_params not in visited):
                        visited.add (href_without_params)
                        parsed_uri = urlparse(list_href[0])
                        rank+=1
                        print("{:3.3}: {:35.30} {:25.20} {:65.60}".format(str(rank) , link.text  , str(parsed_uri.hostname), href_without_params ))
                        if parsed_uri.hostname == hostname:
                            mentions.add((str(rank) , link.text  , str(parsed_uri.hostname), href_without_params ))                


if __name__ == '__main__':

    #searches for <hostname> in the google results for <query>
    hostname="docs.python.org"
    query="abc"

    while counter_page < max_pages:
        try:
            
            url =  "https://www.google.com/search?q="+ quote(query) + "&num=" + str(results_per_page) +"&start=" + str(counter_page * results_per_page)
            req = urllib.request.Request(url,  headers={'User-Agent' : "Magic Browser"})         
            record_mentions(urlopen( req, timeout=5).read())            
            counter_page+=1
                
        except Exception as e:
            print ("error: " +  " " +type(e).__name__+ " -> "+ str(e))
            sys.exit()
    
    print ("-------------------")
    for rank,text,domain,url in mentions:
        print("{:3.3}: {:35.30} {:25.20} {:65.60}".format(str(rank) , text  , domain, url ))
    
