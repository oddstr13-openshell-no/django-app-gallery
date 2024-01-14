from django.db import models
from django.utils import timezone

from taggit.managers import TaggableManager
from PIL import Image as PILImage

from gallery.lib import get_exif, decode_exif_datetime

from sorl.thumbnail import ImageField


class Image(models.Model):
    image       = ImageField(upload_to="gallery/%Y/%m/%d")
    title       = models.CharField(max_length=128, blank=True)
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
        if not self.title:
            self.title = self.image.name
        import sys
        sys.stderr.write(str(dir(self.image))+'\n')
        im = PILImage.open(self.image)
        try:
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
        except: pass # No EXIF :/
        
        if self.published is None:
            self.published = timezone.now()

        
        super(Image, self).save()
    
    def __str__(self):
        return self.title

    def listwrapped(self):
        return [self]
    

class Photograph(models.Model): # FIXIT
    name        = models.CharField(max_length=64, blank=True)
    displayname = models.CharField(max_length=32, blank=True)
    
    def __str__(self):
        return self.displayname or self.name


class Camera(models.Model):
    name        = models.CharField(max_length=64)
    url         = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, default="")
    
    def __str__(self):
        return self.name


class Lens(models.Model):
    name        = models.CharField(max_length=64)
    url         = models.URLField()
    description = models.TextField()
    camera      = models.ForeignKey("Camera", on_delete=models.SET_NULL, blank=True, null=True, related_name="lenses")
    
    def __str__(self):
        return self.name

