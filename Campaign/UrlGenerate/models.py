from django.db import models
from datetime import datetime

# Create your models here.


def game_directory_path(instance, filename):
    return 'games/{0}.{1}'.format(instance.game_name,filename.split(".")[1])




class MobileCodes(models.Model):
    mnc = models.IntegerField()
    mcc = models.IntegerField()
    city = models.CharField(max_length=50)
    zone = models.CharField(max_length=50)
    network = models.CharField(max_length=50)

    def __str__(self):
        return self.city


class Campaign(models.Model):
    #camp_id = models.IntegerField()
    camp_url = models.CharField(max_length=200)
    zone =  models.CharField(max_length=50)
    priority = models.IntegerField(default=0)
    advertiser = models.CharField(max_length=200)
    camp_name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.camp_name)


class User_Camp(models.Model):
    uuid = models.IntegerField(unique=True)
    mnc = models.IntegerField()
    mcc = models.IntegerField()
    android_version = models.CharField(max_length=50)
    phone_make = models.CharField(max_length=100)
    phone_model = models.CharField(max_length=100)

    def __str__(self):
        return str(self.uuid)



class Game(models.Model):
    name=models.CharField(max_length=20)
    # pic=models.ImageField(upload_to=game_directory_path,blank=True,null=True)
    url=models.URLField()
    pic=models.URLField()

    def __str__(self):
        return self.name


class Hit(models.Model):
    user_id = models.ForeignKey(User_Camp,on_delete=models.CASCADE)
    camp_id = models.IntegerField(default=0)
    sms = models.CharField(max_length=2000,default="XXX")
    my_date = models.DateTimeField(auto_now_add=True,editable=True)

    def __str__(self):
        return str(self.my_date)






