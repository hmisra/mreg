from google.appengine.ext import db
import datetime
from xml.dom import minidom
from itertools import cycle
import string
import re 
import httplib 
import urllib2
from google.appengine.ext import webapp
import webapp2
import wsgiref.handlers


class Feed(db.Model):
    feedstoredate=db.DateProperty()
    feedof=db.StringProperty()
    feedtitle=db.StringProperty()
    feedlink=db.StringProperty()
    feeddescription=db.TextProperty()
    feedpubdate=db.StringProperty()
    
def listinfo(type): 
    infofile = "feedlist." + type 
    datafile = open(infofile, "r") 
    line = datafile.readline() 

    record = {} 

    while line: 
        data = string.split(line, ';') 
        feedname = data[0] 
        address = data[1] 
        record[feedname] = address 
        line = datafile.readline() 

    return record 

feedinfo = listinfo("dat") 

class ModelFeed: 

    def __init__(self): 
        self.data = [] 

    def feeddata (self, feedname): 
        feedaddress = feedinfo[feedname] 
        return feedaddress 

    def links (self, address, feedname):
        try:
            file_request = urllib2.Request(address) 
            file_opener = urllib2.build_opener() 
            file_feed = file_opener.open(file_request).read() 
            file_xml = minidom.parseString(file_feed)
        except urllib2.URLError as e :
            linkdata=str(e)
            return "URL Error : "+linkdata
        except urllib2.HTTPError as e :
            linkdata=str(e)
            return "HTTP Error : "+linkdata
        except httplib.HTTPException as e :
            linkdata=str(e)
            return "HTTP Error : "+linkdata
        alreadyindblist=[]
        linkdata=""
        database = db.GqlQuery("SELECT * from Feed WHERE feedof = :1", feedname)
        for data in database:
            alreadyindblist.append(data.feedof+data.feedtitle+data.feedpubdate)
       
        item_node = file_xml.getElementsByTagName("item") 


        for item in item_node: 
            titles = item.getElementsByTagName("title")
            for title in titles:
                if title.firstChild!=None:
                    ftitle=title.firstChild.data
                else:
                    ftitle="No Title"
                    

            links=item.getElementsByTagName("link")
            for link in links:
                if link.firstChild!=None:
                    flink=link.firstChild.data
                else:
                    flink="#"

            descriptions=item.getElementsByTagName("description")
            for description in descriptions:
                if description.firstChild!=None:
                    fdescription=description.firstChild.data
                else:
                    fdescription="No Description"


            pubdates=item.getElementsByTagName("pubDate")
            for pubdate in pubdates:
                if pubdate.firstChild!=None:
                    fpubdate=pubdate.firstChild.data
                else:
                    fpubdate="01/01/01"
                
            

            indexcompstring=feedname+ftitle+fpubdate
            if indexcompstring in alreadyindblist:
                linkdata="No new feeds for "+feedname
                continue
            else:
                feed=Feed(feedtitle=ftitle,feedlink=flink,feeddescription=fdescription,feedpubdate=fpubdate)
                feed.feedstoredate=datetime.datetime.now().date()
                feed.feedof=feedname
                feed.put()
                linkdata=feedname+" stored in database."
                                
        return linkdata 

    def image (self, feedname): 
        image_address = imginfo[feedname] 
        return image_address 


def inodeValue(doc, nodename): 
    dom = minidom.parseString(doc) 
    node = dom.getElementsByTagName(nodename) 
    norm = node[0].toxml() 
    node_no_xml = re.sub('(<title>)|(<\/title>)|(<link>)|(<\/link>)|(<url>)|(</url>)', '', norm) 
    value = str(node_no_xml) 
    print value 
    return value 


def dnodeValue(doc, nodename): 
    dom = minidom.parseString(doc) 
    node = dom.getElementsByTagName(nodename) 
    norm = node[0].toxml() 
    node_no_xml = re.sub('(<title>)|(<\/title>)|(<link>)|(<\/link>)|(<description>)|(<\/description>)', '', norm) 
    value = str(node_no_xml) 
    print value 
    return value 

def bodyfn(feedname): 
    feed = ModelFeed() 
    feedurl = feed.feeddata(feedname)
    body= feed.links(feedurl,feedname)	
    return body 

     

def reader(feedname): 
    i = 0 
    body = bodyfn(feedname) 
    output = body 
    return output

class MyHandler(webapp.RequestHandler):
  def get(self):
	  self.response.out.write(reader('Amazon'))
	  self.response.out.write("<br>")
	  self.response.out.write(reader('Foundry'))
	  self.response.out.write("<br>")
	  self.response.out.write(reader('Redhat'))
	  self.response.out.write("<br>")
	  
	  
	  
	  
app = webapp2.WSGIApplication([('/dbupdate', MyHandler)])
    
