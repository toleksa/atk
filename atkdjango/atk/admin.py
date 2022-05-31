from django.contrib import admin

# Register your models here.
from .models import Babe, SiteBabe, AllBabe, Vote, ExternalSite

admin.site.register(Babe)
admin.site.register(SiteBabe)
admin.site.register(AllBabe)
admin.site.register(Vote)
admin.site.register(ExternalSite)

