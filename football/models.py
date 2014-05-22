# coding=utf-8
from django.db import models
import datetime

# Create your models here.

NATIONALITY_CHOICES = (
    ('Argentina','阿根廷'),
    ('Brazil','巴西'),
    ('China','中国'),
    ('England', '英格兰'),
    ('France','法国'),
    ('Germany', '德国'),
    ('Italy', '意大利'),
    ('Netherland','荷兰'),
    ('Portugal','葡萄牙'),
    ('Spain', '西班牙'),
)

POSITION_CHOICES = (
    ('ST', '前锋'),
    ('AMC','进攻型中场（中）'),
    ('AML','进攻型中场（左）'),
    ('AMR','进攻型中场（右）'),
    ('MC','中场（中）'),
    ('ML','中场（左）'),
    ('MR','中场（右）'),
    ('DM','防守型中场'),
    ('DC','后卫（中）'),
    ('DL','后卫（左）'),
    ('DR','后卫（右）'),
    ('WL','进攻型边后卫（左）'),
    ('WR','进攻型边后卫（右）'),
    ('GK','门将'),
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
    position = models.CharField(max_length=1000,null=True,blank=True,choices=POSITION_CHOICES)

class PlayingRecord(models.Model):
    player_name = models.ForeignKey(Player)
    club_name = models.ForeignKey(Club)
    start_season = models.IntegerField(null = True, blank = True)
    end_season = models.IntegerField(null = True, blank = True)
    games = models.IntegerField(null = True, blank = True)
    goals = models.IntegerField(null = True, blank = True)

class CoachingRecord(models.Model):
    coach_name = models.ForeignKey(Coach)
    club_name = models.ForeignKey(Club)
    start_season = models.IntegerField(null = True, blank = True)
    end_season = models.IntegerField(null = True, blank = True)
    games = models.IntegerField(null = True, blank = True)
    wins = models.IntegerField(null = True, blank = True)

class TransferRecord(models.Model):
    player_name = models.ForeignKey(Player)
    club_from = models.ForeignKey(Club, related_name="club_from")
    club_to = models.ForeignKey(Club, related_name="club_to")
    season = models.IntegerField(null = True, blank = True)
    fee = models.FloatField(null = True, blank = True)


