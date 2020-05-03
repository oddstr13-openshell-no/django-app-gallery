#!/usr/bin/env python
import os

from django.core.management.base import BaseCommand, CommandError

from gallery.models import Image

ROW_SEP = unicode(chr(30))
COL_SEP = unicode(chr(31))

"""
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

class Photograph(models.Model): # FIXIT
    name        = models.CharField(max_length=64, blank=True)
    displayname = models.CharField(max_length=32, blank=True)

class Camera(models.Model):
    name        = models.CharField(max_length=64)
    url         = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, default="")

class Lens(models.Model):
    name        = models.CharField(max_length=64)
    url         = models.URLField()
    description = models.TextField()
    camera      = models.ForeignKey("Camera", on_delete=models.SET_NULL, blank=True, null=True, related_name="lenses")

"""

class Command(BaseCommand):
    help = 'Dumps image metadata'

    def add_arguments(self, parser):
        parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        with open('imagedump.table', 'wt') as fh:
            for im in Image.objects.all():
                fn = os.path.basename(im.image.path)
                self.stdout.write(u'{0}\n'.format(fn))
                fh.write(COL_SEP.join([
                    unicode(im.id),
                    fn,
                    im.title,
                    im.description,
                    im.published.isoformat(' ') if im.published else '',
                    im.taken.isoformat(' ') if im.taken else '',
                    ','.join(im.tags.names()),
                    im.photograph.name,
                    im.camera.name if im.camera else ''
                ]).encode('utf-8'))
                fh.write(ROW_SEP)

        #for poll_id in options['poll_id']:
        #    try:
        #        poll = Poll.objects.get(pk=poll_id)
        #    except Poll.DoesNotExist:
        #        raise CommandError('Poll "%s" does not exist' % poll_id)

        #    poll.opened = False
        #    poll.save()

        #    self.stdout.write('Successfully closed poll "%s"' % poll_id)
