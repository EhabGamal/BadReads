from django.db import models
from django.contrib.auth.models import User


# class User(models.Model):
#     name = models.CharField(max_length=255)
#     email = models.EmailField(blank=False)
#     password = models.CharField(max_length=255)
#     img = models.ImageField(upload_to='images/users/')
#
#     def __str__(self):
#         return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    summary = models.TextField(null=True)
    published_at = models.DateField(null=True)
    img = models.ImageField(upload_to='images/books/')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, default=1)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=255)
    born_at = models.DateField(blank=True)
    died_at = models.DateField(blank=True)
    bio = models.TextField(null=True)
    img = models.ImageField(upload_to='images/authors/')

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    authors = models.ManyToManyField('Author')
    categories = models.ManyToManyField('Category')
    books = models.ManyToManyField('Book', through='Rate')

    def __str__(self):
        return self.user.email


class Rate(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    STATES = [('read', 'Read'), ('wish', 'Wish'), ('none', 'None')]
    state = models.CharField(max_length=10, choices=STATES, default='none')
    RATES = [(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")]
    rate = models.CharField(max_length=1, choices=RATES)

    def __str__(self):
        return self.rate
