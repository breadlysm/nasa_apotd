import urllib
from lxml import etree
import os
import datetime

now = datetime.datetime.now()
url = "https://apod.nasa.gov/apod/astropix.html"
response = urllib.urlopen(url)
htmlparser = etree.HTMLParser()
tree = etree.parse(response, htmlparser)
folder = os.path.expanduser('~/Pictures/nasa/')
imageurl = ('https://apod.nasa.gov/apod/'
            + tree.xpath('/html/body/center[1]/p[2]/a/@href')[0]
            )
imagename = (folder
             + now.strftime("%Y_%m_%d_")
             + imageurl.split('/')[-1]
             )
urllib.urlretrieve(imageurl, imagename)

