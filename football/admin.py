from django.contrib import admin  
from football.models import *  
  
admin.site.register(Player)
admin.site.register(Coach)
admin.site.register(Club)
admin.site.register(PlayerTransferRecord)
admin.site.register(CoachTransferRecord)
admin.site.register(PlayingRecord)
admin.site.register(CoachingRecord)
