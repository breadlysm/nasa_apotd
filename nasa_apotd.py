try:
    from urllib.request import urlretrieve
    from urllib.request import urlopen  # Python 3
except ImportError:
    from urllib import urlretrieve
    from urllib import urlopen  # Python 2
from lxml import etree
import os
import datetime
import errno

now = datetime.datetime.now()
base = "https://apod.nasa.gov/apod/"
apotd_page = 'astropix.html'


def get_folder(imgname):
    user = os.path.expanduser('~')
    pictures = os.path.join(user,'Pictures')
    nasa = os.path.join(pictures, 'Nasa')
    try:
        os.makedirs(nasa)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    imgpath = os.path.join(pictures,'Nasa',imgname)
    return imgpath



def gettree(url):
    response = urlopen(url)
    htmlparser = etree.HTMLParser()
    tree = etree.parse(response, htmlparser)
    return tree

# def download_past():

def download_image(tree):
    imageurl = (base
                + tree.xpath('/html/body/center[1]/p[2]/a/@href')[0]
                )
    imagename = get_folder(now.strftime("%Y_%m_%d_") 
                        + imageurl.split('/')[-1]
                        )
    urlretrieve(imageurl, imagename)

download_image(gettree(base + apotd_page))


