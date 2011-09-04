from django.contrib import admin

from lolaws.uploadr.models import StoredImage

class StoredImageAdmin(admin.ModelAdmin):
    list_display = ('image','upload_date')

admin.site.register(StoredImage, StoredImageAdmin)
