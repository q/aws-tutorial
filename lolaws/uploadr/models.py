from django.db import models
from django.conf import settings

from storages.backends.s3boto import S3BotoStorage

# These settings can should be set per model.
# Can/should fall back to a default AWS_STORAGE_BUCKET_NAME
# Not sure what to do about the url yet...

# Some type of function to do this would be nice so we don't have to put
# a if/else at the top of all of our models that have a File/ImageField.
BUCKETNAME = getattr(settings, "IMAGE_BUCKET_NAME", None)
CLOUDFRONT_URL = getattr(settings, "IMAGE_BUCKET_CLOUDFRONT_URL", None)

if BUCKETNAME is not None and CLOUDFRONT_URL is not None:
    print 's3 storage'
    storage = S3BotoStorage(bucket=BUCKETNAME, custom_domain=CLOUDFRONT_URL)
else:
    # wut do if you don't have these settings? Default to local file storage?
    # Seems like you would only want to do that if DEBUG is on. If it's not
    # should probably raise an exception because writing to local storage in
    # dev or prod is bad. Those files will be lost.
    raise Exception

# Create your models here.
class StoredImage(models.Model):
    image = models.ImageField(upload_to="filez", storage=storage)
    upload_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-upload_date']
