from PIL import Image
from PIL.ExifTags import TAGS
import datetime

def get_exif(img):
    # http://stackoverflow.com/a/765403
    ret = {}
    #img = Image.open(fn)
    info = img._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret

def decode_exif_datetime(s):
    res = None
    
    if res is None: # Curse you if you ever swap month and day of month.
        try:
            res = datetime.datetime.strptime(s, '%Y/%m/%d %H:%M:%S')
        except ValueError: pass
    
    if res is None: # ..... w-what?... *sigh*
        try:
            res = datetime.datetime.strptime(s, '%Y:%m:%d %H:%M:%S')
        except ValueError: pass
    
    if res is None: # I have not yet seen this 'out in the wild', even if it is the only correct one :/
        try:
            res = datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
        except ValueError: pass
    
    return res
