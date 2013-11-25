from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

import datetime

from gallery.models import Image


def index(request):
    images = Image.objects.filter(published__lte=datetime.datetime.now()).order_by('-published')
    
    return render(request, 'gallery/index.html', {'images':images})

def by_tag(request, tag):
    images = Image.objects.filter(tags__name__in=[tag]).filter(published__lte=datetime.datetime.now()).order_by('-published')
    
    return render(request, 'gallery/by_tag.html', {'images':images})

def image(request, id):
    _image = get_object_or_404(Image, id=id)
    return render(request, 'gallery/image.html', {'image':_image, 'limage':[_image]})
