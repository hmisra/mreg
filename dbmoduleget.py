from google.appengine.ext import db

class Feed(db.Model):
    feedstoredate=db.DateProperty()
    feedof=db.StringProperty()
    feedtitle=db.StringProperty()
    feedlink=db.StringProperty()
    feeddescription=db.TextProperty()
    feedpubdate=db.StringProperty()
    
def reader(feedname):
    linkdata=""
    #q = db.GqlQuery("SELECT * FROM Feed")
    #db.delete(q)
    feeds=db.GqlQuery("SELECT * from Feed WHERE feedof = :1", feedname)
    feeds=sorted(feeds, key=lambda x: x.feedstoredate)
    for feed in feeds:
        linkdata = linkdata + "\n<h2><a href=\"" + feed.feedlink + "\" >" + feed.feedtitle + "</a> </h2>\n <h4>"+feed.feedpubdate +" </h4>\n"+"<p>"+ feed.feeddescription +"</p> <hr>"
    return linkdata
