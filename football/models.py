# coding=utf-8
from django.db import models
import datetime

# Create your models here.

NATIONALITY_CHOICES = (
    ('Engliand', '英格兰'),
    ('Germany', '德国'),
    ('Italy', '意大利'),
    ('Spain', '西班牙'),
)

POSITION_CHOICES = (
    ('fore', '前锋'),

)

class Club(models.Model):
    name = models.CharField(max_length=50)
    league = models.CharField(max_length=50)
    city = models.CharField(max_length=50,null=True,blank=True)
    country = models.CharField(max_length=50,null=True,blank=True,choices=NATIONALITY_CHOICES)

class Coach(models.Model):
    name = models.CharField(max_length=50)
    birthday = models.DateField(null=True,blank=True)
    nationality = models.CharField(max_length=50,null=True,blank=True,choices=NATIONALITY_CHOICES)

class Player(models.Model):
    name = models.CharField(max_length=50)
    birthday = models.DateField(null=True,blank=True)
    nationality = models.CharField(max_length=50,null=True,blank=True,choices=NATIONALITY_CHOICES)
    height = models.IntegerField(null=True,blank=True)
    weight = models.IntegerField(null=True,blank=True)
    position = models.CharField(max_length=50,null=True,blank=True,choices=POSITION_CHOICES)
