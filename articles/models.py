from django.db import models
from django.conf import settings


class Articles(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    cost = models.DecimalField(decimal_places=2, max_digits=20)
    category = models.ForeignKey('Category', related_name='default_category',
                                 null=True, blank=True,
                                 on_delete=models.CASCADE)
    location = models.CharField(max_length=200)
    likes = models.ForeignKey('User_likes', on_delete=models.CASCADE)
    # image = models.ImageField(upload_to='smth/', blank=True, null=True)

    class Meta:
        db_table = 'articles'


class Category(models.Model):
    title = models.CharField(max_length=120, unique=True)

    class Meta:
        db_table = 'category'


class User_likes(models.Model):
    user = models.CharField(max_length=200, default='')
    id_article = models.IntegerField(default=0)
    like = models.BooleanField(default=True)

    class Meta:
        db_table = 'user_likes'