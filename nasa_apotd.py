try:
    # Python 3
    from urllib.request import urlretrieve
    from urllib.request import urlopen
    from tkinter import filedialog as tkFileDialog
except ImportError:
    # Python 2
    from urllib import urlretrieve
    from urllib import urlopen
    import tkFileDialog
from lxml import etree
import os
import datetime
import errno
import argparse

base = "https://apod.nasa.gov/apod/"
apotd_page = 'astropix.html'

parser = argparse.ArgumentParser(description='Download images from nasa APOTD')

parser.add_argument(
    '--days',
    '-d',
    type=int,
    help='Number of days to download from apotd archives',
    action='store')

parser.add_argument(
    '--location',
    '-l',
    help='add flag to select save location via GUI',
    action='store_true')
args = parser.parse_args()

def get_folder(imgname):
    if args.location:
        folder = tkFileDialog.askdirectory(
            title="Choose folder to save image")
    else:
        folder = os.path.join(
            os.path.expanduser('~'),
            'Pictures',
            'Nasa')
        try:
            os.makedirs(folder)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    imgpath = os.path.join(folder, imgname)
    return imgpath


def gettree(url):
    response = urlopen(url)
    htmlparser = etree.HTMLParser()
    tree = etree.parse(response, htmlparser)
    return tree


def get_date(tree):
    date = tree.xpath('/html/body/center[1]/p[2]/text()')
    date = date[0].translate({ord(c): None for c in '\n'})
    try:
        date = datetime.datetime.strptime(
            date, '%Y %B %d')
        date = date.strftime("%Y_%m_%d")
    except Exception as e:
        date = datetime.datetime.strptime(
            date, '%Y %B %d ')
        date = date.strftime("%Y_%m_%d")
    return date


def download_image(tree,url):

    try:
        imageurl = (base 
                    + tree.xpath('/html/body/center[1]/p[2]/a/@href')[0]
                    )
        imagename = get_folder(get_date(tree)
                            + ' '
                            + imageurl.split('/')[-1]
                            )
        
        urlretrieve(imageurl, imagename)
    except Exception as e:
        print("error, did not download. Possibly a video on %s" % (url,))
        pass

def get_last_page(tree):
    lastpageurl = (base + tree.xpath('/html/body/center[3]/a[1]/@href')[0]
                   )
    return lastpageurl


if args.days is not None:
    url = base + apotd_page
    for i in range(args.days):
        tree = gettree(url)
        download_image(tree,url)
        print("Downloaded image %s of %s" % ((i+1),args.days),)
        url = (base + tree.xpath('/html/body/center[3]/a[contains(text(),"<")]/@href')[0])
else:
    download_image(gettree(base + apotd_page),url)
