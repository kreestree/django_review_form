from django.contrib import admin
from .models import *


# Register your models here.
class ImageAdmin(admin.ModelAdmin):
    list_display = ('problem', 'thumbnail_preview')
    readonly_fields = ['thumbnail_preview']


admin.site.register(Image, ImageAdmin)


class ImageInline(admin.StackedInline):
    readonly_fields = ['thumbnail_preview']
    model = Image
    extra = 0


class ProblemAdmin(admin.ModelAdmin):
    list_display = ('time_create', 'factory_number', 'factory_area', 'problem', 'employee_full_name', 'show_photos')
    list_display_links = ('time_create', 'problem')
    search_fields = ('factory_number__factory_number', 'factory_area__factory_area', 'employee_full_name')
    list_filter = ('time_create', 'factory_number__factory_number', 'factory_area__factory_area')
    inlines = [ImageInline]

    def show_photos(self, problem):
        images = Image.objects.filter(problem=problem)
        if images:
            return mark_safe('<br><br>\n'.join(list(map(lambda image: image.thumbnail_preview, images))))

    show_photos.short_description = 'Фото'
    show_photos.allow_tags = True


admin.site.register(Problems, ProblemAdmin)

admin.site.register(FactoryArea)
admin.site.register(FactoryNumber)
