# coding=utf-8

from django import forms
from django.forms import ModelForm
from football.models import Player, Coach, Club, NATIONALITY_CHOICES, POSITION_CHOICES

SEQUENCE_RELATION_CHOICES = (
    ('NA','无'),
    ('=', '等于'),
    ('<','小于'),
    ('>','大于'),
    ('<=','小于等于'),
    ('>=','大于等于'),
    ('!=','不等于'),
)

NATIONALITY_CHOICES_NA = (
    ('NA','未知'),
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

POSITION_CHOICES_NA = (
    ('NA','未知'),
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

class PlayerQueryForm(forms.Form):
    name = forms.CharField(required = False)
    age_type1 = forms.ChoiceField(choices = SEQUENCE_RELATION_CHOICES)
    age1 = forms.IntegerField(required = False)
    age_type2 = forms.ChoiceField(choices = SEQUENCE_RELATION_CHOICES)
    age2 = forms.IntegerField(required = False)
    nationality = forms.ChoiceField(choices = NATIONALITY_CHOICES_NA)
    height_type1 = forms.ChoiceField(choices = SEQUENCE_RELATION_CHOICES)
    height1 = forms.IntegerField(required = False)
    height_type2 = forms.ChoiceField(choices = SEQUENCE_RELATION_CHOICES)
    height2 = forms.IntegerField(required = False)
    weight_type1 = forms.ChoiceField(choices = SEQUENCE_RELATION_CHOICES)
    weight1 = forms.IntegerField(required = False)
    weight_type2 = forms.ChoiceField(choices = SEQUENCE_RELATION_CHOICES)
    weight2 = forms.IntegerField(required = False)
    position1 = forms.ChoiceField(choices = POSITION_CHOICES_NA)
    position2 = forms.ChoiceField(choices = POSITION_CHOICES_NA)
    position3 = forms.ChoiceField(choices = POSITION_CHOICES_NA)
