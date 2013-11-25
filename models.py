from django.db import models

from taggit.managers import TaggableManager
from PIL import Image as PILImage
import datetime

from gallery.lib import get_exif, decode_exif_datetime

from sorl.thumbnail import ImageField
'''
class Paste(models.Model):
    urlid   = models.CharField(max_length=16, unique=True)
    ip      = models.GenericIPAddressField()
    text    = models.TextField()
    lang    = models.ForeignKey("Lang", on_delete=models.PROTECT)
    private = models.BooleanField(default=False)  # Hide paste from public listing
    time    = models.DateTimeField(auto_now_add=True)
    replyto = models.ForeignKey("self", on_delete=models.SET_NULL, blank=True, null=True, related_name="replies") #, related_query_name="reply") # related_query_name requires 1.6

    def __unicode__(self):
        return self.urlid
        
    def save(self):
        if not self.id:
            self.created = datetime.date.today()
        self.updated = datetime.datetime.today()
        super(TodoList, self).save()
'''


class Image(models.Model):
    image       = ImageField(upload_to="gallery/%Y/%m/%d")
    title       = models.CharField(max_length=128)
    description = models.TextField(blank=True, default='')
    published   = models.DateTimeField(blank=True, null=True) # Check this before showing
    taken       = models.DateTimeField(blank=True, null=True)
    tags        = TaggableManager(blank=True)
    photograph  = models.ForeignKey("Photograph", on_delete=models.SET_NULL, blank=True, null=True, related_name="images")
    camera      = models.ForeignKey("Camera", on_delete=models.SET_NULL, blank=True, null=True, related_name="images")
    lens        = models.ForeignKey("Lens", on_delete=models.SET_NULL, blank=True, null=True, related_name="images")
    
    def save(self):
        if not self.id:
            pass # Not created yet
        import sys
        sys.stderr.write(str(dir(self.image))+'\n')
        im = PILImage.open(self.image)
        exif = get_exif(im)
        if "Model" in exif:
            cam_model = exif["Model"].strip('\0').strip()
            camera, created = Camera.objects.get_or_create(name=cam_model)
            if created:
                camera.save()
            self.camera = camera
        
        taken = None
        if "DateTimeOriginal" in exif: # Yea, i want the original timestamp
            taken = decode_exif_datetime(exif["DateTimeOriginal"])
        elif "DateTime" in exif: # No "Original"? i guess this'll do
            taken = decode_exif_datetime(exif["DateTime"])
        elif "DateTimeDigitized" in exif: # *sigh* Fine, i'll take what i get
            taken = decode_exif_datetime(exif["DateTimeDigitized"])
        if taken is not None:
            self.taken = taken
        
        if self.published is None:
            self.published = datetime.datetime.now()

        
        super(Image, self).save()
    
    def __unicode__(self):
        return self.title
    

class Photograph(models.Model): # FIXIT
    name        = models.CharField(max_length=64, blank=True)
    displayname = models.CharField(max_length=32, blank=True)
    
    def __unicode__(self):
        return self.displayname or self.name


class Camera(models.Model):
    name        = models.CharField(max_length=64)
    url         = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, default="")
    
    def __unicode__(self):
        return self.name


class Lens(models.Model):
    name        = models.CharField(max_length=64)
    url         = models.URLField()
    description = models.TextField()
    camera      = models.ForeignKey("Camera", on_delete=models.SET_NULL, blank=True, null=True, related_name="lenses")
    
    def __unicode__(self):
        return self.name
