from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Author(models.Model):
    name = models.CharField(max_length=255)
    born_at = models.DateField(blank=True)
    died_at = models.DateField(blank=True)
    bio = models.TextField(null=True)
    img = models.ImageField(upload_to='images/authors/')
    users = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    desc = models.CharField(max_length=255, default='')
    users = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    summary = models.TextField(null=True)
    published_at = models.DateField(null=True)
    img = models.ImageField(upload_to='images/books/')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    users = models.ManyToManyField(User, through='UserBooks')

    def __str__(self):
        return self.title

    @property
    def rate(self):
        try:
            return int(self.userbooks_set.filter(rate__gt=0).aggregate(Avg('rate'))['rate__avg'])
        except:
            return 0

    @property
    def rate_count(self):
        try:
            return self.userbooks_set.filter(rate__gt=0).count()
        except:
            return 0


class UserBooks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rate = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    wish = models.BooleanField(default=False)
    read = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'book')
