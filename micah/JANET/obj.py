b = 1
b = 2
d = 3
a = 4
a = 5
c=6
d = 7
b = 8
d = 9
c = 10
a = 11
b = 12
d = 13
c = 14
b = 15
d=16
d=17
c = 18
c = 19
a = 20
a= 21
a =  22
d = 23
d = 24
c =25
b =26
c = 27
b = 28
c = 29
b = 30


#section two
#question one
from django.db import models
from django.contrib.auth.models import Book

class Book(models.Model):
    title = models.CharField(max_length=200,null=False)
    author = models.CharField(max_length=100,null = False)
    publication_year = models.PositiveIntegerField(null = True)


#question two
from rest_framework import serializers
from . import models

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        models = models.Book
        fields = ('title', 'author', 'publication_year',)
        read_only_fields = ('id')


#question three
#loop tells us that if a given condition is true a repeated action should go on.this happens lest a range is inserted for it

#question four

#conditional statements are used when two or more conditions are taken into consideration



