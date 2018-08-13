"""  FOR DISCUSSION :
from django.db import models
from django.conf import settings


class Article(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    cost = models.DecimalField(decimal_places=2, max_digits=20)
    location = models.CharField(max_length=150)
    category = models.ForeignKey('Category', related_name='default_category',
                                 null=True, blank=True,
                                 on_delete=models.CASCADE)
    # image = models.ImageField(upload_to='products/', blank=True, null=True)
    # ? mobile/ aka contact


class Category(models.Model):
    title = models.CharField(max_length=120, unique=True)

    # slug = models.SlugField(unique=True)

    def __unicode__(self):
        return self.title

"""