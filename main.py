from google.appengine.ext import webapp
import webapp2
import wsgiref.handlers
import string 
import sys 
from google.appengine.ext.webapp \
     import template
import dbmoduleget as dbget




class MyHandler(webapp.RequestHandler):
  def get(self):
	  self.response.out.write('''<html lang="en"><head>
  <meta charset="utf-8" />
  <title>Infosys Rainbow</title>
  <link rel="stylesheet" href="http://code.jquery.com/ui/1.10.0/themes/base/jquery-ui.css" />
  <script src="http://code.jquery.com/jquery-1.8.3.js"></script>
  <script src="http://code.jquery.com/ui/1.10.0/jquery-ui.js"></script>
  <link rel="stylesheet" href="/resources/demos/style.css" />
  <script>
  $(function() {
    $( "#tabs" ).tabs();
  });
  </script>
  <style media="screen" type="text/css">
  #tabs {
	position:absolute;
	top:15%;
	right:2%;
	width:80%;
	height:80%
	}
  #ta{
  position:absolute;
  top:10%;
  right:2%;
  }
  </style>
</head>
<body>
<img src="/images/logo.jpg" width='230px' height='100px'>
<a href="#top" id="ta">TOP</a>
<div id="tabs" style="widht:80%px; overflow:scroll" >
<div id="top"></div>
  <ul>
    <li><a href="#tabs-1">Amazon News</a></li>
    <li><a href="#tabs-2">Cloud Foundry News</a></li>
    <li><a href="#tabs-3">Redhat News</a></li>
  </ul>
  <div id="tabs-1">
    <br><p>''' + dbget.reader('Amazon') +''' </p>
  </div>
  <div id="tabs-2" >
    <br><p>'''+ dbget.reader('Foundry')+'''</p>
  </div>
  <div id="tabs-3">
    <br><p>'''+dbget.reader('Zlinux')+'''</p>
  </div>
  
</div>
 
 
</body>
</html>''' )
     
  
app = webapp2.WSGIApplication([('/', MyHandler)])
    
                               
