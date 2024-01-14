from django.contrib import admin
from gallery.models import Image, Photograph, Camera, Lens
from sorl.thumbnail.admin import AdminImageMixin

class ImageAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('title', 'published', 'taken', 'photograph', 'camera', 'image') # lens, 'tags'
    list_filter = ['published', 'taken', 'photograph', 'camera', 'lens', 'tags']
    search_fields = ['title', 'tags', 'photograph', 'camera', 'lens']
    ordering = ['-taken']
    date_hierarchy = 'taken'


admin.site.register(Image, ImageAdmin)
admin.site.register(Photograph)
admin.site.register(Camera)
admin.site.register(Lens)

