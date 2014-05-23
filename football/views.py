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
from django.db.models import Q
from datetime import datetime, date
from datetime import timedelta
from football.forms import PlayerForm, CoachForm, ClubForm, PlayerQueryForm
from football.models import Player, Coach, Club, PlayerTransferRecord, CoachTransferRecord

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
        club = Club.objects.get(admin=request.user)
        playerrecord = PlayerTransferRecord.objects.all().filter(club_from=club).filter(pending=1)
        return render_to_response('football/player_trade.html', {"pending":len(playerrecord)}, context_instance=RequestContext(request))

@login_required
def coach(request):
    if request.user.is_superuser:
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
    else:
        if request.method == 'POST':
            club = Club.objects.get(admin=request.user)
            coachpk = request.POST.get('coachpk', '')
            typeid = int(request.POST.get('type', ''))
            if typeid == 1:
                coach = Coach.objects.get(pk=coachpk)
                ctr = CoachTransferRecord(coach=coach, club_from=club, club_to=None, season=date.today().year, fee=0, pending=0)
                ctr.save()
                coach.club = None
                coach.save()
            else:
                coach = Coach.objects.get(pk=coachpk)
                ctr = CoachTransferRecord(coach=coach, club_from=None, club_to=club, season=date.today().year, fee=0, pending=0)
                ctr.save()
                coach.club = club
                coach.save()

            return render_to_response('football/coach_trade.html', {"current":None}, context_instance=RequestContext(request))
        else:
            club = Club.objects.get(admin=request.user)
            coach = club.coach_set.all()
            if coach:
                coach = coach[0]
            return render_to_response('football/coach_trade.html', {"current":coach}, context_instance=RequestContext(request))

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
    playerset = Player.objects.all()
    data_type = None
    if not request.user.is_superuser:
        club = Club.objects.get(admin=request.user)
        if request.method == 'POST':
            data_type = int(request.POST.get('data_type'))
            if data_type == 1:
                print "OK!"
                playerset = playerset.filter(club=club)
            else:
                playerset = playerset.filter(~Q(club=club))
        else:
            return HttpResponse("Error!")

    if request.method == 'POST':
        typeid = int(request.POST.get('type', ''))
        if typeid == 1:
            if not request.user.is_superuser:
                return HttpResponse("没有权限！")
            delnum = request.POST.get('delnum', '')
            player = Player.objects.get(pk=delnum)
            player.delete()
        elif typeid == 2:
            name = request.POST.get('name')
            age_type1 = request.POST.get('age_type1')
            age1 = request.POST.get('age1')
            age_type2 = request.POST.get('age_type2')
            age2 = request.POST.get('age2')
            nationality = request.POST.get('nationality')
            height_type1 = request.POST.get('height_type1')
            height1 = request.POST.get('height1')
            height_type2 = request.POST.get('height_type2')
            height2 = request.POST.get('height2')
            weight_type1 = request.POST.get('weight_type1')
            weight1 = request.POST.get('weight1')
            weight_type2 = request.POST.get('weight_type2')
            weight2 = request.POST.get('weight2')
            position1 = request.POST.get('position1')
            position2 = request.POST.get('position2')
            position3 = request.POST.get('position3')

            if name:
                playerset = playerset.filter(name__icontains = name)

            if not nationality == 'NA':
                playerset = playerset.filter(nationality__exact = nationality)

            if height_type1:
                if height_type1 == '=':
                    playerset = playerset.filter(height__exact = height1)
                if height_type1 == '<':
                    playerset = playerset.filter(height__lt = height1)
                if height_type1 == '>':
                    playerset = playerset.filter(height__gt = height1)
                if height_type1 == '<=':
                    playerset = playerset.filter(height__lte = height1)
                if height_type1 == '>=':
                    playerset = playerset.filter(height__gte = height1)
                if height_type1 == '!=':
                    playerset = playerset.filter(~Q(height = height1))

            if height_type2:
                if height_type2 == '=':
                    playerset = playerset.filter(height__exact=height2)
                if height_type2 == '<':
                    playerset = playerset.filter(height__lt = height2)
                if height_type2 == '>':
                    playerset = playerset.filter(height__gt = height2)
                if height_type2 == '<=':
                    playerset = playerset.filter(height__lte = height2)
                if height_type2 == '>=':
                    playerset = playerset.filter(height__gte = height2)
                if height_type2 == '!=':
                    playerset = playerset.filter(~Q(height = height2))
    
            if weight_type1:
                if weight_type1 == '=':
                    playerset = playerset.filter(weight__exact=weight1)
                if weight_type1 == '<':
                    playerset = playerset.filter(weight__lt = weight1)
                if weight_type1 == '>':
                    playerset = playerset.filter(weight__gt = weight1)
                if weight_type1 == '<=':
                    playerset = playerset.filter(weight__lte = weight1)
                if weight_type1 == '>=':
                    playerset = playerset.filter(weight__gte = weight1)
                if weight_type1 == '!=':
                    playerset = playerset.filter(~Q(weight = weight1))

            if weight_type2:
                if weight_type2 == '=':
                    playerset = playerset.filter(weight__exact=weight2)
                if weight_type2 == '<':
                    playerset = playerset.filter(weight__lt = weight2)
                if weight_type2 == '>':
                    playerset = playerset.filter(weight__gt = weight2)
                if weight_type2 == '<=':
                    playerset = playerset.filter(weight__lte = weight2)
                if weight_type2 == '>=':
                    playerset = playerset.filter(weight__gte = weight2)
                if weight_type2 == '!=':
                    playerset = playerset.filter(~Q(weight = weight2))

            if not position1 == 'NA':
                playerset = playerset.filter(position__contains = position1)
            if not position2 == 'NA':
                playerset = playerset.filter(position__contains = position2)
            if not position3 == 'NA':
                playerset = playerset.filter(position__contains = position3)
        
        elif typeid == 3:
            requestnum = request.POST.get('requestnum', '')
            player = Player.objects.get(pk=requestnum)
            copy_from = player.club
            copy_to = Club.objects.get(admin=request.user)
            
            if copy_to == copy_from:
                return HttpResponse(simplejson.dumps({ "error": True }))

            money = request.POST.get('money', '')

            record = PlayerTransferRecord(player=player, club_from=copy_from, club_to=copy_to, season=date.today().year, fee=money, pending=1)
            record.save()

            return HttpResponse(simplejson.dumps({ "error": False }))
        else:
            pass            
   
    return render_to_response('football/player_result.html', {'playerset':playerset,'form':PlayerQueryForm(),'datatype':data_type}, context_instance=RequestContext(request))

@login_required
def player_detail(request):
    if request.method == 'POST':
        detailnum = request.POST.get('detailnum', '')
        detailtype = int(request.POST.get('detailtype', ''))
        if detailtype == 1:
            player = Player.objects.get(pk=detailnum)
            playerrecord = player.playertransferrecord_set.all().filter(pending=0)
            return render_to_response('football/player_detail.html', {'player':player, 'playerrecord':playerrecord}, context_instance=RequestContext(request))
        else:
            player = Player.objects.get(pk=detailnum)
            playerrecord = player.playingrecord_set.all()
            return render_to_response('football/player_detail2.html', {'player':player, 'playerrecord':playerrecord}, context_instance=RequestContext(request))
    else:
        return HttpResponse("error!")

@login_required
def player_trade(request):
    club = Club.objects.get(admin=request.user)
    playerrecord = PlayerTransferRecord.objects.all().filter(club_from=club).filter(pending=1)

    if request.method == 'POST':
        typeid = int(request.POST.get('type', ''))
        approvenum = request.POST.get('approvenum', '')

        if typeid == 1:
            try:
                record = playerrecord.get(pk=approvenum)
            except (KeyError, PlayerTransferRecord.DoesNotExist):
                return HttpResponse("<strong>Error!</strong>")
            else:
                player = record.player
                player.club = record.club_to
                player.save()

                record.pending = 0;
                record.save()

                playerrecord = PlayerTransferRecord.objects.all().filter(club_from=club).filter(pending=1)
        else:
            try:
                record = playerrecord.get(pk=approvenum)
            except (KeyError, PlayerTransferRecord.DoesNotExist):
                return HttpResponse("<strong>Error!</strong>")
            else:
                record.delete()

                playerrecord = PlayerTransferRecord.objects.all().filter(club_from=club).filter(pending=1)
            
    return render_to_response('football/player_notification_list.html', {'playerrecord':playerrecord}, context_instance=RequestContext(request))

@login_required
def coach_result(request):
    if request.method == 'POST':
        delnum = request.POST.get('delnum', '')
        coach = Coach.objects.get(pk=delnum)
        coach.delete()

    coachset = Coach.objects.all()

    if not request.user.is_superuser:
        club = Club.objects.get(admin=request.user)
        coachset = coachset.filter(club=None)

    return render_to_response('football/coach_result.html', {'coachset':coachset}, context_instance=RequestContext(request))

@login_required
def coach_detail(request):
    if request.method == 'POST':
        detailnum = request.POST.get('detailnum', '')
        detailtype = int(request.POST.get('detailtype', ''))
        if detailtype == 1:
            coach = Coach.objects.get(pk=detailnum)
            coachrecord = coach.coachtransferrecord_set.all().filter(pending=0)
            return render_to_response('football/coach_detail.html', {'coach':coach, 'coachrecord':coachrecord}, context_instance=RequestContext(request))
        else:
            coach = Coach.objects.get(pk=detailnum)
            coachrecord = coach.coachingrecord_set.all()
            return render_to_response('football/coach_detail2.html', {'coach':coach, 'coachrecord':coachrecord}, context_instance=RequestContext(request))
    else:
        return HttpResponse("error!")

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
