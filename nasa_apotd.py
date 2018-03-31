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

now = datetime.datetime.now()
base = "https://apod.nasa.gov/apod/"
apotd_page = 'astropix.html'

parser = argparse.ArgumentParser(description='Download images from nasa APOTD')

parser.add_argument(
    '--location',
    '-l',
    help='Choose save location via GUI',
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
