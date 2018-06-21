from django.shortcuts import render,HttpResponse

from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
import requests
from django.views.decorators.csrf import csrf_exempt

from urllib.parse import urlparse

from rest_framework.views import APIView,Response

from .models import MobileCodes, Campaign, User_Camp, Hit, Game
import json
import time
from datetime import datetime,timedelta
from django.views import View



# Create your views here.


class API(APIView):

    def get(self,request):
        return HttpResponse('hello')
    def post(self,request,q):
        if q=="curl":

            #data = request.body
            received_json_data = json.loads(request.body.decode("utf-8"))


            mcc = received_json_data['mcc']
            mnc = received_json_data['mnc']
            uuid = received_json_data['uuid']
            android_version = received_json_data['android_version']
            phone_make = received_json_data['phone_make']
            phone_model =received_json_data['phone_model']

            print(mcc, mnc, uuid, android_version, phone_make, phone_model)

            info = MobileCodes.objects.get(mnc=mnc, mcc=mcc)
            print(info.city, info.network, info.zone)

            zone_name = info.zone
            zone_name = zone_name.lower()

            if User_Camp.objects.filter(uuid=uuid).exists():
                userobj = User_Camp.objects.get(uuid=uuid)
                userobj.mnc = mnc
                userobj.mcc = mcc
                userobj.save()
                obj =User_Camp.objects.get(uuid=uuid)
                #print(obj.uuid)
                hit_user = Hit.objects.filter(user_id=obj).order_by('my_date')
                print(hit_user)

                print("i am in hit user",hit_user[0].my_date.utcnow())
                if (datetime.now() - hit_user[0].my_date.utcnow()) >= timedelta(1):

                    fil_li = Hit.objects.filter(user_id=obj,sms="null")
                    print(len(fil_li))
                    for i in fil_li:
                        if i.user_id == obj:
                            Hit.objects.get(pk=i.id).delete()

                    list_of_url = list(Campaign.objects.filter(zone="all india").order_by('-priority')) + \
                                  list(Campaign.objects.filter(zone=zone_name).order_by('-priority'))

                    after_d = Hit.objects.filter(user_id=obj)
                    for i in after_d:
                        for l in list_of_url:
                            if l.id == i.camp_id:
                                list_of_url.remove(l)


                    print(len(fil_li))
                    print(len(list_of_url))
                    print(list_of_url)
                    count = 0
                    listi =[]
                    for li in list_of_url:
                        di={}
                        di["camp_url"] = li.camp_url
                        di["camp_id"] = li.id
                        hitobj = Hit.objects.create(user_id=obj,camp_id=li.id)
                        hitobj.save()

                        count =count+1
                        listi.append(di)

                        if count == 4:
                            break

                    print(listi)

                    return HttpResponse(json.dumps(listi))
                else:
                    d ={"error":"Please try after 24 hour"}

                    return HttpResponse(json.dumps(d))

            else:  # if hit user is not exist
                list_of_url = list(Campaign.objects.filter(zone="all india").order_by('-priority')) + \
                                list(Campaign.objects.filter(zone=zone_name).order_by('-priority'))

                count=0
                #di = {}
                listi=[]
                obj = User_Camp.objects.create(uuid = uuid,mnc=mnc,mcc=mcc,android_version=android_version,phone_make=phone_make,phone_model=phone_model)
                obj.save()
                obj = User_Camp.objects.get(uuid=uuid)
                for li in list_of_url:
                    newobj = Hit.objects.create(user_id=obj, camp_id=li.id)
                    di={}
                    di["camp_url"] = li.camp_url
                    di["camp_id"] = li.id
                    newobj.save()
                    listi.append(di)
                    count = count + 1
                    if count == 4:
                        break

                return HttpResponse(json.dumps(listi),content_type="application/json")


        if q=="sms":
            load_json_data = json.loads(request.body.decode("utf-8"))
            uuid = load_json_data['uuid']
            camp_id = load_json_data['camp_id']
            sms = load_json_data['sms']

            obj = User_Camp.objects.get(uuid=uuid)
            hitobj = Hit.objects.get(user_id =obj,camp_id=camp_id)
            #if sms:
            hitobj.sms = sms
            hitobj.save()
            d={'status':'success'}
            return HttpResponse(json.dumps(d))
            #else:
                #d = {'status': 'failure'}
                #return HttpResponse(json.dumps(d))




def Index(request):
    h = Hit.objects.all()
    for i in h:
        print(i.my_date)
    li = list(Campaign.objects.filter(zone="all india").order_by('-priority'))+list(Campaign.objects.filter(zone="north"))
    print(li[1].zone)
    for l in li:
        print(l.zone)
    return HttpResponse("hello")


class GameApi(View):
    def get(self,request):
        all_games=Game.objects.all()
        data=[]
        for object in all_games:
            data.append({"game_name":object.name,"game_pic":object.pic,"game_url":object.url})
        return HttpResponse(json.dumps(data), content_type="application/json")


    # def post(self,request):
    #     all_games=Game.objects.all()
    #     game=all_games.first()
    #     print(request.data)
    #     success_result={"result":"success"}
    #     failed_Result= {"result":"failed"}
    #
    #     if "game_name" in request.data and "game_pic" in request.data and "game_url" in request.data:
    #         Game.objects.get_or_create(name=request.data["game_name"],pic=request.data["game_pic"],url=request.data["game_url"])
    #         return HttpResponse(json.dumps(success_result), content_type="application/json")
    #
    #     else:
    #         return HttpResponse(json.dumps(failed_Result), content_type="application/json")


#{"uuid":9876,"camp_id":2,"sms":"hello"}
