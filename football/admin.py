from django.contrib import admin  
from football.models import *  
  
admin.site.register(Player)
admin.site.register(Coach)
admin.site.register(Club)
admin.site.register(PlayingRecord)
admin.site.register(CoachingRecord)
admin.site.register(TransferRecord)
