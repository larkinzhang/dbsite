# coding=utf-8

from django import forms
from django.forms import ModelForm
from football.models import Player, Coach, Club

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

class PlayerForm(ModelForm):
    class Meta:
        model = Player

class CoachForm(ModelForm):
    class Meta:
        model = Coach

class ClubForm(forms.Form):
    name = forms.CharField(max_length=50)
    league = forms.CharField(max_length=50)
    city = forms.CharField(max_length=50,required=False)
    country = forms.ChoiceField(required=False,choices=NATIONALITY_CHOICES)
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())
