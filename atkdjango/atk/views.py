from django.shortcuts import render,redirect
from django.template import loader
from django.http import HttpResponse, HttpRequest
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, F, Sum, Lookup, Field
from django.db.models.query import QuerySet
from .models import Babe, SiteBabe, AllBabe, AllBabe_view, Vote, Novote, AllScore, BestScore, ExternalSite
import os
import random
import datetime
from dateutil.relativedelta import relativedelta

def sitestats(site):
    count=AllBabe.objects.filter(site=site).count()
    likes=AllBabe.objects.filter(site=site).aggregate(Sum('likes'))['likes__sum']
    monthlikes=AllBabe.objects.filter(site=site).aggregate(Sum('monthlikes'))['monthlikes__sum']
    duellikes=AllBabe.objects.filter(site=site).aggregate(Sum('duellikes'))['duellikes__sum']
    return {'count': count, 'likes': likes, 'monthlikes': monthlikes, 'duellikes': duellikes}

def printsite(site):
    stats = sitestats(site)
    return "<tr><td>" + site + ":</td><td>[count:" + str(stats['count']) + "</td><td>likes:" + str(stats['likes']) + "</td><td>duel:" + str(stats['duellikes']) + "</td><td>monthlikes:" + str(stats['monthlikes']) + "</td><td>all:" + str(stats['likes']+stats['duellikes']+stats['monthlikes']) + "</td><td>]" + "</td></tr>"

def stats(request):
    response=""
    response+="<table>"
    response+=printsite('blog')
    response+=printsite('exotics')
    response+=printsite('galleria')
    response+=printsite('hairy')
    response+="</table><br>"
    babes = Babe.objects.count()
    sitebabes = SiteBabe.objects.count()
    response+="sitebabes: " + str(sitebabes) + "<br>"
    response+="total: " + str(babes+sitebabes) + "<br>"
    uniq=AllBabe.objects.values('name').distinct().count()
    response+="unique: " + str(uniq) + "<br>"
    response+="<br>"
    duelvotes = Vote.objects.filter(votemonth__isnull=True,vote__gt=0,second__gt=0).count()
    novotes = AllBabe.objects.filter(likes=0,duellikes=0,monthlikes=0).count()
    response += "Duel votes: " + str(duelvotes) + " (novotes: " + str(novotes) + ") <br>"
    monthvotes = Vote.objects.filter(votemonth__isnull=False).count()
    response += "Month votes: " + str(monthvotes) + "<br>"
    likevotes = Vote.objects.filter(votemonth__isnull=True,second=0).count()
    response += "Like votes: " + str(likevotes) + "<br>"
    unlikevotes = Vote.objects.filter(votemonth__isnull=True,vote=0).count()
    response += "Unlike votes: " + str(unlikevotes) + "<br>"
    response += "Total votes: " + str(duelvotes + monthvotes + likevotes + unlikevotes) + "<br>"
    response+="<br><br>"
    response += "Hall of Fame:<br><br>"
    halloffame = AllBabe.objects.values('name').annotate(ncount=Count('name')).order_by('-ncount')[0:10]
    for babe in halloffame:
        response += str(babe['ncount']) + " <a href='/atk/model/" + str(babe['name']) + "'>" + str(babe['name']) + "</a><br>"

    response += "<br><br><a href='/atk/search/pob/poland/'>Polish</a>:<br><br>"
    polish = AllBabe.objects.values('name').annotate(ncount=Count('name')).filter(pob__icontains='poland').order_by('-ncount')
    for babe in polish:
        response += str(babe['ncount']) + " <a href='/atk/model/" + str(babe['name']) + "'>" + str(babe['name']) + "</a><br>"

    response += "<br>Most liked models:<br>"
    liked = AllBabe.objects.values('name').annotate(ssum=Sum('likes')).order_by('-ssum')[0:100]
    for like in liked:
        response += str(like['ssum']) + " <a href='/atk/model/" + like['name'] + "/'>" + like['name'] + "</a><br>"
    ages = Babe.objects.values('age').annotate(ncount=Count('*')).order_by(F('age').asc(nulls_last=True))
    #return HttpResponse(ages)
    response += "<br>Ages:<br>"
    for age in ages:
        response += "<a href='/atk/search/age/" + str(age['age']) + "'>" + str(age['age']) + "</a>" + " " + str(age['ncount']) + "<br>"
    response += "<br>Votemonth<br>"
    votemonths = Vote.objects.values('votemonth').annotate(ncount=Count('votemonth')).order_by('-votemonth')
    for votemonth in votemonths:
        response += "<a href=/atk/votemonth-" + str(votemonth['votemonth']) + "/top/>" + str(votemonth['votemonth']) + "</a> " + str(votemonth['ncount']) + "<br>"
    return HttpResponse(response)

def randomrandom(request):
    randomnum = random.randrange(AllBabe.objects.filter(likes__gte=0).count())
    babes = AllBabe.objects.filter(likes__gte=0).order_by('-id')[randomnum:randomnum+1]
    response = sitedisplay(request,babes,'randomrandom',1,'atk/randomrandom.html')
    return HttpResponse(response)

def siterandom(request,site='allsites'):
    if site not in ['allsites','exotics','hairy','galleria','blog']:
        err='site not found'
        return error(request,err,site)
    babes = []
    if site == 'allsites':
        randomnum = random.randrange(AllBabe.objects.filter(likes__gte=0).count())
        babes = AllBabe.objects.filter(likes__gte=0).order_by('id')[randomnum:randomnum+1]
    else:
        query = AllBabe.objects.filter(site=site,likes__gte=0)
        maxnum = len(query)
        if maxnum > 0:
            randomnum = random.randrange(maxnum)
            babes = query[randomnum:randomnum+1]
    site='random'
    template='atk/random.html'
    response = sitedisplay(request,babes,site,1,template, page_title='Random')
    return HttpResponse(response)

def randomnovotes(request):
    query = AllBabe.objects.filter(likes=0,duellikes=0,monthlikes=0)
    maxnum = len(query)
    babes=''
    if maxnum > 0:
        randomnum = random.randrange(maxnum)
        babes = query[randomnum:randomnum+1]
    response = sitedisplay(request,babes,'randomnovotes',0,'atk/random.html', page_title='Random NoVotes')
    return HttpResponse(response)

def randomnolikes(request):
    query = AllBabe.objects.filter(likes=0)
    maxnum = len(query)
    babes=''
    if maxnum > 0:
        randomnum = random.randrange(maxnum)
        babes = query[randomnum:randomnum+1]
    response = sitedisplay(request,babes,'randomnolikes',0,'atk/random.html', page_title='Random NoVotes')
    return HttpResponse(response)

def vote(request,site,vote='',second='',num=''):
    #return HttpResponse(request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[0].strip())
    if site=='duel' or site=='duelduel' or site=='month' or site=='novotes' or site=='randomnovotes' or site=='random' or site=='randomrandom' or site=='num':
        if vote == second:
            err='vote cannot be same as second'
            return error(request,err)

        babe = ''
        if vote >= 10000000:
            babe = Babe.objects.get(id=vote)
        elif vote < 10000000 and vote != 0:
            babe = SiteBabe.objects.get(id=vote)
        elif second != 0 and vote==0:
            if second >= 10000000:
                babe = Babe.objects.get(id=second)
            elif second < 10000000 and second != 0:
                babe = SiteBabe.objects.get(id=second)
        else:
            err='sth went wrong|mo8owunidxhw'
            return error(request,err)

        if site=='month':
            votemonth= AllBabe.objects.filter(id=vote).values('date')[0]['date'][0:4]
            monthvotes = Vote.objects.values('vote').filter(votemonth=votemonth).count()
            if monthvotes >= 500:
                err = 'There are ' + str(monthvotes) + ' votes for that month, voting is closed'
                return error(request,err)
            newVote = Vote.objects.create(vote=vote,second=second,votemonth=votemonth,ip=get_ip(request))
        else:
            newVote = Vote.objects.create(vote=vote,second=second,ip=get_ip(request))

        if site=='duel' or site=='duelduel' or site=='novotes':
            babe.duellikes += 1
            babe.save()
        elif site=='month':
            babe.monthlikes += 1
            babe.save()
        elif site=='random' or site=='randomnovotes' or site=='num' or site=='randomrandom':
            if vote>0 and second==0:
                babe.likes+=1
                babe.save()
            elif vote==0 and second>0:
                babe.likes-=1
                babe.save()
            else:
                err='sth went wrong|fe4orim4cwdw'
                return error(request,err)
        else:
            err='sth went wrong|wdf3cr2exw'
            return error(request,err)
        if site=='num':
            site=site + '/' + str(num)
        url='/atk/' + site + '/'
        return redirect(url)
    else:
        return error(request,'site not found')

def duel(request,site):
    if site=='duel' or site=='duelduel' or site=='month' or site=='novotes':
        votemonth = get_votemonth()
        maxnum=-1
        numvotes=''
        page_title=''
        treshold=0
        if site=='month':
            numvotes = Vote.objects.values('vote').filter(votemonth=votemonth).count()
            if numvotes >= 500:
                err = 'There are ' + str(numvotes) + ' votes for that month, voting is closed'
                return error(request,err)
            if numvotes >= 100:
                treshold=0
            if numvotes >= 200:
                treshold=2
            if numvotes >= 300:
                treshold=5
            if numvotes >= 400:
                treshold=10
            maxnum = AllBabe.objects.filter(date__istartswith=votemonth,likes__gte=0,monthlikes__gte=treshold).count()
        elif site=='duel' or site=='duelduel':
            maxnum = AllBabe.objects.filter(likes__gte=0).count()
            numvotes = Vote.objects.values('vote').filter(votemonth__isnull=True,vote__gt=0,second__gt=0).count()
        elif site == 'novotes':
            novotes = list(AllBabe.objects.filter(likes=0,duellikes=0,monthlikes=0))
            maxnum = len(novotes)
            if maxnum<2:
                response = sitedisplay(request,'','novote',1,'atk/duel.html')
                return HttpResponse(response)
        else:
            return error(request,'wrong site|32eddwq3c3')
        randomnum1 = random.randrange(maxnum)
        randomnum2 = -1
        while True:
            randomnum2 = random.randrange(maxnum)
            if randomnum1 != randomnum2:
                break
        if site=='month':
            babes  = list(AllBabe.objects.filter(date__istartswith=votemonth,likes__gte=0,monthlikes__gte=treshold).order_by('id')[randomnum1:randomnum1+1])
            babes += list(AllBabe.objects.filter(date__istartswith=votemonth,likes__gte=0,monthlikes__gte=treshold).order_by('id')[randomnum2:randomnum2+1])
            page_title='Duel Month'
        elif site=='duel' or site=='duelduel':
            babes  = list(AllBabe.objects.filter(likes__gte=0).order_by('id')[randomnum1:randomnum1+1])
            babes += list(AllBabe.objects.filter(likes__gte=0).order_by('id')[randomnum2:randomnum2+1])
            page_title='Duel'
        elif site == 'novotes':
            babes =  list(AllBabe.objects.filter(id=novotes[randomnum1].id))
            babes += list(AllBabe.objects.filter(id=novotes[randomnum2].id))
            page_title='Duel NoVotes'
        else:
            return error(request,'wrong site|f4wgewa4w')
        #a = 3 + b
        template='atk/' + site + '.html'
        if site=='novotes' or site=='month':
            template='atk/duel.html'
        response = sitedisplay(request,babes,site,1,template,babes,0,'',numvotes,2,treshold,page_title=page_title)
        return HttpResponse(response)
    else:
        return error(request,'site not found')

def top(request,site,page=1,votemonth=0):
    related=''
    detail=0
    liked=''
    babes=''
    per_page=''
    template='atk/template_base.html'
    
    if site=='duel' or site=='duelduel' or site=='month' or site=='monthrank' or site=='monthlist' or site == 'likes' or site == 'liked' or site == 'dueltopmodel' or site=='monthmodel' or site=='bestscore' or site == 'monthpic' or site == 'allpic' or site == 'allmodel' or site == 'allscore' or site == 'votemonth' or site == 'age':
        if site=='duel' or site=='duelduel':
            per_page=100
            babes = AllBabe_view.objects.order_by('-duellikes','-likes','-monthlikes')[(page-1)*per_page:page*per_page]
            if site=='duelduel':
                template='atk/duelduel.html'

        if site=='month':
            #TODO: this sorting is dynamic, think about something more static
            per_page=32
            babes = AllBabe_view.objects.filter(date__startswith=get_votemonth()).order_by('-monthlikes','-duellikes','-likes')[(page-1)*per_page:page*per_page]

        if site=='votemonth':
            monthvotes = Vote.objects.values('vote').filter(votemonth=votemonth).count()
            if monthvotes <= 0:
                err="votemonth incorrect or has no votes|54745432"
                return error(request,err)
            per_page=32
            babes = AllBabe_view.objects.filter(date__startswith=votemonth).order_by('-monthlikes','-duellikes','-likes')[(page-1)*per_page:page*per_page]
            site="votemonth-" + str(votemonth)

        if site=='monthrank':
            per_page=48
            months = list(Vote.objects.values('votemonth').filter(votemonth__isnull=False).order_by('-votemonth').distinct())[int((page-1)*per_page/4):int(page*per_page/4)]
            babes = []
            for month in months:
                #TODO: this sorting is dynamic, think about something more static
                monthlist = list(AllBabe_view.objects.filter(date__startswith=month['votemonth']).order_by('-monthlikes','-duellikes','-likes')[0:4])
                for babe in monthlist:
                    babes.append(babe)

        if site=='monthlist':
            babes = list(AllBabe_view.objects.filter(date__istartswith=get_votemonth(),likes__gte=0).order_by('-date'))

        if site=='likes':
            per_page=100
            babes= AllBabe_view.objects.order_by('-likes','-duellikes','-monthlikes')[(page-1)*per_page:page*per_page]

        if site=='allpic':
            per_page=100
            babes= AllBabe_view.objects.all().annotate(alllikes=F('likes') + F('monthlikes') + F('duellikes')).order_by('-alllikes','-likes','-duellikes')[(page-1)*per_page:page*per_page]
        
        if site=='allmodel':
            per_page=100
            liked = AllBabe_view.objects.values('name').annotate(vote=Sum('totallikes')).order_by('-vote')[(page-1)*per_page:page*per_page]
            babes = []
            for like in liked:
                #TODO: this is ugly as fuck
                babee = list(AllBabe_view.objects.filter(name=like['name']).order_by('-totallikes')[0:1])
                for babe in babee:
                    babes.append(babe) 

        if site=='allscore':
            per_page=100
            liked = AllScore.objects.values('name','vote')[(page-1)*per_page:page*per_page]
            babes = []
            for like in liked:
                #TODO: this is ugly as fuck
                babee = list(AllBabe_view.objects.filter(name=like['name']).order_by('-totallikes')[0:1])
                for babe in babee:
                    babes.append(babe)

        if site=='monthpic':
            per_page=100
            babes= AllBabe_view.objects.order_by('-monthlikes','-likes','-duellikes')[(page-1)*per_page:page*per_page]

        if site=='liked':
            per_page=100
            liked = AllBabe_view.objects.values('name').annotate(vote=Sum('likes')).order_by('-vote')[(page-1)*per_page:page*per_page]
            babes = []
            for like in liked:
                #TODO: this is ugly as fuck
                babee = list(AllBabe_view.objects.filter(name=like['name']).order_by('-likes')[0:1])
                for babe in babee:
                    babes.append(babe)

        if site=='dueltopmodel':
            per_page=100
            liked = AllBabe_view.objects.values('name').annotate(vote=Sum('duellikes')).order_by('-vote')[(page-1)*per_page:page*per_page]
            babes = []
            for like in liked:
                #TODO: this is ugly as fuck
                babee = list(AllBabe_view.objects.filter(name=like['name']).order_by('-duellikes')[0:1])
                for babe in babee:
                    babes.append(babe)

        if site=='monthmodel':
            per_page=100
            liked = AllBabe_view.objects.values('name').annotate(vote=Sum('monthlikes')).order_by('-vote')[(page-1)*per_page:page*per_page]
            babes = []
            for like in liked:
                #TODO: this is ugly as fuck
                babee = list(AllBabe_view.objects.filter(name=like['name']).order_by('-monthlikes')[0:1])
                for babe in babee:
                    babes.append(babe)

        if site=='bestscore':
            per_page=100
            liked = BestScore.objects.values('name','vote')[(page-1)*per_page:page*per_page]
            babes = []
            for like in liked:
                #TODO: this is ugly as fuck
                babee = list(AllBabe_view.objects.filter(name=like['name']).order_by('-likes')[0:1])
                for babe in babee:
                    babes.append(babe)

        if site=='age':
            per_page=100
            babes = AllBabe_view.objects.filter(likes__gte=-1,age__regex=r'^[0-9]*$').order_by('-age','-date','-id')[(page-1)*per_page:page*per_page]

        response = sitedisplay(request,babes,site+"/top",page,template,related,detail,liked,'',per_page,page_title="Top " + site.capitalize())
        return HttpResponse(response)
    return error(request,'site not found|8456323434')

def sitenum(request,num,site = 'allsites'):
    if site not in ['allsites','exotics','hairy','galleria','blog']:
        err='site not found'
        return error(request,err,site)
    try:
        babes = [AllBabe.objects.get(id=num)]
    except ObjectDoesNotExist:
        err='babe not found'
        return error(request,err,site)
    babe_name=babes[0].name
    #related = AllBabe.objects.filter(name=babe_name).exclude(id=num).order_by('-date')
    related = list(AllBabe.objects.filter(name=babe_name).order_by('-date','site'))
    index = related.index(babes[0])
    prev_num=''
    next_num=''
    if index > 0:
        prev_num=related[index-1].id
    if index < len(related)-1:
        next_num=related[index+1].id
    site='num/' + str(num)
    page_title = babe_name
    template = loader.get_template('atk/sitenum.html')
    context = {
        'babes': babes,
        'site': site,
        'related' : related,
        'page_title': page_title,
        'num' : num,
        'prev_num' : prev_num,
        'next_num' : next_num,
    }
    response = template.render(context, request)
    return HttpResponse(response)


def search(request,site,search='',category='',page=1,per_page=20,order=''):
    if site not in ['allsites','exotics','hairy','galleria','blog','search','hidden','banned','novote','nolikes','alles','lastvote']:
        err='site not found|syvffserck|' + site
        return error(request,err,site)
    if order!='':
        if order not in ['-date','date','-id','id','-site','site','-age','age','-likes','likes','-monthlikes','monthlikes','-duellikes','duellikes']:
            err='order keyword not recognized|43f3gf3wwg5'
            return error(request,err,site)
    if search=='':
        if request.GET.get('name'):
            category='name'
            if request.GET.get('category'):
                category=request.GET.get('category')
            #message = 'You submitted: %r' % request.GET['name']
            url = '/atk/search/' + category + '/' + request.GET['name']
            return redirect(url)
        else:
            if site not in ['allsites','exotics','hairy','galleria','blog','hidden','banned','novote','nolikes','alles','lastvote']:
                err='empty search string'
                return error(request,err)
    else:
        if category not in ['name','id','tags','pob','age']:
            err='unrecognized search category: ' + category
            return error(request,err,site)
        if len(search) < 3 and category!='age':
            err="search string must have at least 3 characters"
            return error(request,err)
    offset = (page - 1) * per_page
    modeldetail={}
    page_title=''
    show_search_sort=''
    show_sort=''
    try:
        order_by=('-date','site','-id')
        if order!='':
            #TODO: .asc() should help with #24 - copied from def stats()
            #order_by=(str(F('age').asc(nulls_last=True)),*order_by)
            order_by=(order,*order_by)
        if site=='search':
            query_filter = str(category + '__icontains')
            babes = AllBabe_view.objects.filter(**{ query_filter: search },likes__gte=-1).order_by(*order_by)[offset:offset+per_page]
            numResults = AllBabe_view.objects.filter(**{ query_filter: search },likes__gte=-1).count()
            #TODO: put filter into variable and have one query
            if order=='-age' or order=='age':
                #filter_conditions = { **{ query_filter: search }, "likes__gte": -1, "age__regex": r'^[0-9]*$' }            
                babes = AllBabe_view.objects.filter(**{ query_filter: search },likes__gte=-1,age__regex=r'^[0-9]*$').order_by(*order_by)[offset:offset+per_page]
                numResults = AllBabe_view.objects.filter(**{ query_filter: search },likes__gte=-1,age__regex=r'^[0-9]*$').count()
            if not babes:
                modeldetail=get_modeldetails(search,babes.count())
            page_title = category + ":" + search
            show_search_sort='true'
        elif site in ['exotics','hairy','galleria','blog']:
            babes = AllBabe_view.objects.filter(site=site,likes__gte=0).order_by(*order_by)[offset:offset+per_page]
            numResults = AllBabe_view.objects.filter(site=site,likes__gte=0).count()
            page_title = site.capitalize()
            show_sort='true'
        elif site=='allsites':
            babes = AllBabe_view.objects.filter(likes__gte=0).order_by(*order_by)[offset:offset+per_page]
            numResults = AllBabe_view.objects.filter(likes__gte=0).count()
            show_sort='true'
        elif site=='hidden':
            babes = AllBabe_view.objects.filter(likes=-1).order_by(*order_by)[offset:offset+per_page]
            numResults = AllBabe_view.objects.filter(likes=-1).count()
            page_title = site.capitalize()
        elif site=='banned':
            babes = AllBabe_view.objects.filter(likes__lt=-1).order_by(*order_by)[offset:offset+per_page]
            numResults = AllBabe_view.objects.filter(likes__lt=-1).count()
            page_title = site.capitalize()
        elif site=='alles':
            babes = AllBabe_view.objects.order_by(*order_by)[offset:offset+per_page]
            numResults = AllBabe_view.objects.count()
            page_title = site.capitalize()
        elif site=='novote':
            query = AllBabe_view.objects.filter(likes=0,duellikes=0,monthlikes=0).order_by(*order_by)
            babes = query[offset:offset+per_page]
            numResults = len(query)
            page_title = site.capitalize()
        elif site=='nolikes':
            query = AllBabe_view.objects.filter(likes=0).order_by(*order_by)
            babes = query[offset:offset+per_page]
            numResults = len(query)
            page_title = site.capitalize()
        elif site=='lastvote':
            lastVote = Vote.objects.filter(vote__gt=0,second__gt=0).order_by('-id').first()
            babes = list(AllBabe_view.objects.filter(id=lastVote.vote))
            babes += list(AllBabe_view.objects.filter(id=lastVote.second))
            numResults = len(babes)
            page_title = site.capitalize()
        else:
            return error(request,'wrong site|se5hsfwdwz')
    except ObjectDoesNotExist:
        err='babe not found'
        return error(request,err)
    template = loader.get_template('atk/search.html')
    context = {
        'babes': babes,
        'site': site,
        'category': category,
        'page' : page,
        'pages': numResults // per_page + 1,
        'search' : search,
        'numResults': numResults,
        'modeldetail': modeldetail,
        'per_page' : per_page,
        'page_title': page_title,
        'order': order,
        'show_search_sort': show_search_sort,
        'show_sort': show_sort,
    }
    response = template.render(context, request)
    return HttpResponse(response)

def model(request,model,filter='none',sort='none',page=1,per_page=10):
    site='allsites'
    if sort not in ['none', 'likes','duellikes','monthlikes','totallikes']:
        err='order sort: ' + sort + ' not recognized|564ye45tge'
        return error(request,err,site)
    offset = (page - 1) * per_page
    babes=[]
    try:
        order_by=('-date','site','-id')
        if sort!='none':
            order_by=('-'+sort,*order_by)

        if filter=='none':
            babes = AllBabe_view.objects.filter(name=model).order_by(*order_by)
        elif filter=='nolikes':
            babes = AllBabe.objects.filter(name=model,likes=0).order_by('-date','-id')
        elif filter=='blog':
            babes = AllBabe.objects.filter(name=model,site='blog').order_by('-date','-id')
        elif filter=='exotics':
            babes = AllBabe.objects.filter(name=model,site='exotics').order_by('-date','-id')
        elif filter=='galleria':
            babes = AllBabe.objects.filter(name=model,site='galleria').order_by('-date','-id')
        elif filter=='hairy':
            babes = AllBabe.objects.filter(name=model,site='hairy').order_by('-date','-id')
        else:
            err='filter: ' + filter + ' not recognized|frhf5tdgf'
            return error(request,err,site)
    except ObjectDoesNotExist:
        err='babe not found|cve65yhfsfw'
        return error(request,err,site)
    if not babes:
        err='babe not found|2f43fwdewr4'
        return error(request,err,site)
    photo_num=babes.count()
    if filter != 'none':
        photo_num=len(AllBabe.objects.filter(name=model))
    modeldetail=get_modeldetails(model,photo_num)
    template = loader.get_template('atk/template_base.html')
    context = {
        'babes': babes,
        'site': site,
        'page' : page,
        'modeldetail': modeldetail,
        'page_title': model,
        'photo_num': photo_num,
    }
    response = template.render(context, request)
    #response = sitedisplay(request,babes,site,page,'atk/likes.html')
    return HttpResponse(response)

def get_modeldetails(model,babes_count=1):
    modeldetail={}
    modeldetail = AllBabe.objects.filter(name=model).aggregate(Sum('likes'))
    modeldetail['monthlikes__sum']=AllBabe.objects.filter(name=model).aggregate(Sum('monthlikes'))['monthlikes__sum']
    modeldetail['duellikes__sum']=AllBabe.objects.filter(name=model).aggregate(Sum('duellikes'))['duellikes__sum']
    if modeldetail['monthlikes__sum'] is not None and modeldetail['duellikes__sum'] is not None:
        modeldetail['totallikes__sum']=modeldetail['likes__sum']+modeldetail['monthlikes__sum']+modeldetail['duellikes__sum']
    try:
        modeldetail['blogdetails'] = list(AllBabe.objects.filter(name=model,site='blog').order_by('-date')[0:1])[0]
        modeldetail['blogdetails']=generate_tags2([modeldetail['blogdetails']])
    except:
        result="didn't work, LOL"
    try:
        modeldetail['topphoto'] = list(AllBabe.objects.filter(name=model).order_by('-likes')[0:1])[0]
        modeldetail['avg_likes'] = round(modeldetail['likes__sum'] / babes_count,2)
        modeldetail['avg_duellikes'] = round(modeldetail['duellikes__sum'] / babes_count,2)
        modeldetail['avg_monthlikes'] = round(modeldetail['monthlikes__sum'] / babes_count,2)
        modeldetail['avg_totallikes'] = round(modeldetail['totallikes__sum'] / babes_count,2)
    except:
        result="didn't work, LOL"
    modelurls=''
    try:
        modelurls = list(ExternalSite.objects.filter(name=model))[0].urls
    except:
        something='wrong'
    if modelurls!='':
        modeldetail['external_sites'] = generate_urls(modelurls)
    modeldetail['original_name'] = model
    modeldetail['external_name'] = model.replace(' ','-').lower()
    modeldetail['vipergirls_name'] = model.replace(' ','+')
    modeldetail['wikifeet_name'] = model.replace(' ','_')
    return modeldetail

def tag(request,tag,page=1,per_page=10):
    offset = (page - 1) * per_page
    try:
        babes = AllBabe.objects.filter(tags__icontains=tag).order_by('-date','-id')
    except ObjectDoesNotExist:
        err='babe not found'
        return error(request,err,site)
    response = sitedisplay(request,babes,'allsites')
    return HttpResponse(response)

def atksite(request,site,page=1,per_page=10):
    if site not in ['allsites','exotics','hairy','galleria','blog']:
        err='site not found'
        return error(request,err,site)
    offset = (page - 1) * per_page
    if site=='allsites':
        if per_page==0:
            babes = AllBabe.objects.order_by('-date','-id')
        else:
            babes = AllBabe.objects.order_by('-date','-id')[offset:offset+per_page]
    else:
        if per_page==0:
            babes = AllBabe.objects.filter(site=site).order_by('-date','-id')
        else:
            babes = AllBabe.objects.filter(site=site).order_by('-date','-id')[offset:offset+per_page]
    response = sitedisplay(request,babes,site,page)
    return HttpResponse(response)

def sitedisplay(request, babes, site='allsites', page = 1, template = 'atk/template_base.html',related = '', detail = 0, topvotes = '', numvotes = '', per_page = 20, treshold = 0, page_title=''):
    template = loader.get_template(template)
    context = {
        'babes': babes,
        'site': site,
        'page' : page,
        'related' : related,
        'detail' : detail,
        'topvotes' : topvotes,
        'numvotes' : numvotes,
        'per_page' : per_page,
        'treshold' : treshold,
        'page_title' : page_title,
    }
    response = template.render(context, request)
    return HttpResponse(response)

def error(request, message, site='allsites'):
    template = loader.get_template('atk/error.html')
    context = {
        'message': message,
        'site': site,
    }
    response = template.render(context, request)
    return HttpResponse(response)

def generate_tags2(babe):
    if babe[0].tags != "" and babe[0].tags is not None:
        tags=babe[0].tags.split("|")
        taglist=[]
        for tag in tags:
            temp=tag.split("/blog/")
            tagname=temp[1]
            URL="/atk/search/tags/" + tagname + ""
            final_tag=[URL, tagname]
            taglist.append(final_tag)
        babe[0].tags=taglist
    return babe[0]

def generate_urls(modelurls):
    if modelurls != "" and modelurls is not None:
        urls=modelurls.split("|")
        urllist=[]
        for url in urls:
            temp=url.split(";")
            num=temp[1]
            site=temp[0]
            final_url=[site,num]
            urllist.append(final_url)
        urllist.sort(key = lambda x: int(x[1]), reverse=True)
        return urllist
    return ''

def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ipaddress = x_forwarded_for.split(',')[-1].strip()
    else:
        ipaddress = request.META.get('REMOTE_ADDR')
    #return ipaddress
    return request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[-1].strip()

@Field.register_lookup
class NotEqual(Lookup):
    lookup_name = 'ne'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return '%s <> %s' % (lhs, rhs), params

def get_votemonth():
    counter=1
    while True:
        currentDate = datetime.datetime.now() - relativedelta(months=counter)
        #currentDate = datetime.datetime.now() - relativedelta(months=20)
        votemonth = currentDate.strftime("%y%m")
        monthvotes = Vote.objects.values('vote').filter(votemonth=votemonth).count()
        if monthvotes < 500:
            return votemonth
        # don't show older, and prevent infinite loop
        if votemonth == '1301':
            return votemonth
        counter+=1
        #TODO: maybe additional condition to break infinite loop
