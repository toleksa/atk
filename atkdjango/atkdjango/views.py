from django.http import HttpResponseRedirect, HttpResponse


def homepage(request):
  return HttpResponseRedirect('/atk/')
  response = "<center><img src='/storage/header.jpg'></center><br><br><a href='/atk/'>atk</a><br><br><a href='/atk/site/blog'>blog</a></br><a href='/atk/site/exotics'>exotics</a></br><a href='/atk/site/hairy'>hairy</a></br><a href='/atk/site/galleria'>galleria</a><br><a href='/atk/site/allsites/'>allsites</a><br><br><a href='/atk/randomrandom/'>randomrandom</a><br><a href='/atk/stats/'>stats</a><br><br>"
  return HttpResponse(response)

