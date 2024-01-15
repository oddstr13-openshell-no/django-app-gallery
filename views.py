from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from gallery.models import Image


def index(request):
    images = Image.objects.filter(published__lte=timezone.now()).order_by("-published")

    return render(request, "gallery/index.html", {"images": images})


def imagemap(request):
    images = Image.objects.filter(published__lte=timezone.now()).order_by("-published")
    return render(
        request, "gallery/imagemap.xml", {"images": images}, content_type="text/xml"
    )


def by_tag(request, tag):
    images = (
        Image.objects.filter(tags__name__in=[tag])
        .filter(published__lte=timezone.now())
        .order_by("-published")
    )

    return render(request, "gallery/by_tag.html", {"images": images})


def image(request, id):
    _image = get_object_or_404(Image, id=id)
    return render(request, "gallery/image.html", {"image": _image, "limage": [_image]})


def image_old_redirect(request, id):
    id = int(id) + 1
    return redirect("gallery.views.image", permanent=True, id=id)
