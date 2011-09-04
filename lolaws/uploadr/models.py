from django.db import models

# Create your models here.
class StoredImage(models.Model):
    image = models.ImageField(upload_to="filez")
    upload_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-upload_date']
