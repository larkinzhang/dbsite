# coding=utf-8
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core import serializers
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.views import generic
from django.utils import simplejson
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime
from datetime import timedelta
from football.forms import PlayerForm, CoachForm, ClubForm
from football.models import Player, Coach, Club

@login_required
def index(request):
    return HttpResponseRedirect("/football/player")

@login_required
def player(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = PlayerForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponse(simplejson.dumps({ "error": False }))
            else:
                return HttpResponse(simplejson.dumps({ "error": True, "errorlist": form.errors }))
        else:
            form = PlayerForm();
            return render_to_response('football/player.html', {'form':form}, context_instance=RequestContext(request))
    else:
        return render_to_response('football/player_trade.html', context_instance=RequestContext(request))

@login_required
def coach(request):
    if not request.user.is_superuser:
        return HttpResponse("没有权限！")
    if request.method == 'POST':
        form = CoachForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(simplejson.dumps({ "error": False }))
        else:
            return HttpResponse(simplejson.dumps({ "error": True, "errorlist": form.errors }))
    else:
        form = CoachForm();
        return render_to_response('football/coach.html', {'form':form}, context_instance=RequestContext(request))

@login_required
def club(request):
    if not request.user.is_superuser:
        return HttpResponse("没有权限！")
    if request.method == 'POST':
        form = ClubForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = User.objects.create_user(username, "", password)
            user.save()

            club = Club(name=form.cleaned_data["name"],league=form.cleaned_data["league"],city=form.cleaned_data["city"],country=form.cleaned_data["country"],admin=user)
            club.save()
            
            return HttpResponse(simplejson.dumps({ "error": False }))
        else:
            return HttpResponse(simplejson.dumps({ "error": True, "errorlist": form.errors }))
    else:
        form = ClubForm();
        return render_to_response('football/club.html', {'form':form}, context_instance=RequestContext(request))

@login_required
def player_result(request):
    if not request.user.is_superuser:
        return HttpResponse("没有权限！")
    if request.method == 'POST':
        delnum = request.POST.get('delnum', '')
        player = Player.objects.get(pk=delnum)
        player.delete()

    playerset = Player.objects.all()
    return render_to_response('football/player_result.html', {'playerset':playerset}, context_instance=RequestContext(request))

@login_required
def coach_result(request):
    if not request.user.is_superuser:
        return HttpResponse("没有权限！")
    if request.method == 'POST':
        delnum = request.POST.get('delnum', '')
        coach = Coach.objects.get(pk=delnum)
        coach.delete()

    coachset = Coach.objects.all()
    return render_to_response('football/coach_result.html', {'coachset':coachset}, context_instance=RequestContext(request))

@login_required
def club_result(request):
    if not request.user.is_superuser:
        return HttpResponse("没有权限！")
    if request.method == 'POST':
        delnum = request.POST.get('delnum', '')
        club = Club.objects.get(pk=delnum)
        admin = club.admin
        admin.delete()
        club.delete()

    clubset = Club.objects.all()
    return render_to_response('football/club_result.html', {'clubset':clubset}, context_instance=RequestContext(request))
