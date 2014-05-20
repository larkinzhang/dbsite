from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'football.views.index', name='index'),
    url(r'^player/$', 'football.views.player', name='player'),
    url(r'^player/result$', 'football.views.player_result', name='player_result'),
    url(r'^coach/$', 'football.views.coach', name='coach'),
    url(r'^coach/result$', 'football.views.coach_result', name='coach_result'),
    url(r'^club/$', 'football.views.club', name='club'),
    url(r'^club/result$', 'football.views.club_result', name='club_result'),
)
