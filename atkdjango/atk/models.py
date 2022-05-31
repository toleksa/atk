from django.db import models

# Create your models here.

class Babe(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    gallery = models.CharField(max_length=100, default=None, blank=True, null=True) 
    name = models.CharField(max_length=50, default=None, blank=True, null=True)
    model = models.CharField(max_length=100, default=None, blank=True, null=True)
    link = models.CharField(max_length=200, default=None, blank=True, null=True)
    date = models.CharField(max_length=8, default=None, blank=True, null=True)
    age = models.CharField(max_length=10, default=None, blank=True, null=True)
    pob = models.CharField(max_length=50, default=None, blank=True, null=True)
    occ = models.CharField(max_length=50, default=None, blank=True, null=True)
#    file = models.CharField(max_length=50, default=None, blank=True, null=True)
#    tn = models.CharField(max_length=50, default=None, blank=True, null=True)
    file = models.ImageField(upload_to='pics')
    tn = models.ImageField(upload_to='pics')
    tags = models.CharField(max_length=1000, default=None, blank=True, null=True)
    likes = models.IntegerField(default=0)
    monthlikes = models.IntegerField(default=0)
    duellikes = models.IntegerField(default=0)

class SiteBabe(models.Model):
    date = models.CharField(max_length=8, default=None, blank=True, null=True)
    name = models.CharField(max_length=50, default=None, blank=True, null=True)
    site = models.CharField(max_length=8, default=None, blank=True, null=True)
    tags = models.CharField(max_length=1000, default=None, blank=True, null=True)
    likes = models.IntegerField(default=0)
    monthlikes = models.IntegerField(default=0)
    duellikes = models.IntegerField(default=0)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['date', 'name', 'site'], name='unique_sitebabe')
        ]

class AllBabe(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    date = models.CharField(max_length=8, default=None, blank=True, null=True)
    name = models.CharField(max_length=50, default=None, blank=True, null=True)
    site = models.CharField(max_length=8, default=None, blank=True, null=True)
    gallery = models.CharField(max_length=100, default=None, blank=True, null=True)
    model = models.CharField(max_length=100, default=None, blank=True, null=True)
    file = models.ImageField(upload_to='pics')
    tn = models.ImageField(upload_to='pics')
    age = models.IntegerField(default=None, blank=True, null=True)
    pob = models.CharField(max_length=50, default=None, blank=True, null=True)
    occ = models.CharField(max_length=50, default=None, blank=True, null=True)
    tags = models.CharField(max_length=1000, default=None, blank=True, null=True)
    likes = models.IntegerField(default=0)
    monthlikes = models.IntegerField(default=0)
    duellikes = models.IntegerField(default=0)
    class Meta:
        managed = False
        db_table = "atk_allsites"

class Vote(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    date = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(default=None, blank=True, null=True)
    votemonth = models.IntegerField(default=None, blank=True, null=True)
    vote = models.IntegerField()
    second = models.IntegerField(default=None, blank=True, null=True)

class Novote(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    class Meta:
        managed = False
        db_table = "atk_novote"

class BestScore(models.Model):
    name = models.CharField(max_length=50, default=None, blank=True, null=True)
    c = models.IntegerField()
    s = models.IntegerField()
    vote = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'best_score'

class ExternalSite(models.Model):
    name = models.CharField(max_length=50, primary_key=True, unique=True)
    urls = models.CharField(max_length=1000, default=None, blank=True, null=True)

