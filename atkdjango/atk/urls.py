from django.urls import path
from django.conf.urls.static import static

from . import views

urlpatterns = [
#    path('random/', views.randombabe, name='randombabe'),
#    path('exotics/', views.atksite, {'site': 'exotics'}),
#    path('hairy/', views.atksite, {'site': 'hairy'}),
#    path('galleria/', views.atksite, {'site': 'galleria'}),
#    path('allsites/', views.atksite, {'site': 'allsites'}),
#    path('exotics/<int:per_page>', views.atksite, {'site': 'exotics'}),
#    path('hairy/<int:per_page>', views.atksite, {'site': 'hairy'}),
#    path('galleria/<int:per_page>', views.atksite, {'site': 'galleria'}),
#    path('allsites/<int:per_page>', views.atksite, {'site': 'allsites'}),
##    path('site/<str:site>/', views.search),
##    path('site/<str:site>/<int:per_page>', views.atksite),
##    path('site/<str:site>/all/', views.atksite, {'per_page': 0}),
##    path('site/<str:site>/page/<int:page>', views.search),
##    path('site/<str:site>/num/<int:num>', views.sitenum),
##    path('site/<str:site>/random/', views.siterandom),
##    path('site/<str:site>/search/<str:search>', views.search),
    path('', views.search, {'site': 'allsites'}),
    path('model/<str:model>/', views.model),
#    path('model/<str:model>/page/<int:page>', views.model),
    path('num/<int:num>/', views.sitenum),
    path('search/<str:category>/<str:search>/', views.search, {'site': 'search'}),
    path('search/<str:category>/<str:search>/page/<int:page>/', views.search, {'site': 'search'}),
    path('search/', views.search, {'site': 'search'}),
    #path('tag/<str:search>/page/<int:page>/', views.search, {'site': 'tag'}),
    #path('tag/<str:search>/', views.search, {'site': 'tag'}),
    path('stats/', views.stats),
    path('random/', views.siterandom),
    path('randomnovotes/', views.randomnovotes),
    path('random/<str:site>/', views.siterandom),
    path('randomrandom/', views.randomrandom),
    path('duel/', views.duel, {'site': 'duel'}),
    path('duelduel/', views.duel, {'site': 'duelduel'}),
    path('novotes/', views.duel, {'site': 'novotes'}),
    path('<str:site>/top/page/<int:page>/', views.top),
    path('<str:site>/top/', views.top),
    path('vote/num/<int:num>/<int:vote>/<int:second>/', views.vote, {'site': 'num'}),
    path('vote/<str:site>/<int:vote>/<int:second>/', views.vote),
##    path('monthtop/', views.monthtop),
    path('month/', views.duel, {'site': 'month'}),
##    path('month/<int:vote>/<int:second>/', views.month),
    path('lastvote/', views.search, {'site': 'lastvote'}),
    path('<str:site>/page/<int:page>', views.search),
    path('<str:site>/', views.search),
]