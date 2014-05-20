from django.forms import ModelForm
from football.models import Player, Coach, Club

class PlayerForm(ModelForm):
    class Meta:
        model = Player

class CoachForm(ModelForm):
    class Meta:
        model = Coach

class ClubForm(ModelForm):
    class Meta:
        model = Club
