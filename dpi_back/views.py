from django.shortcuts import render
from django.http import HttpResponse
import json
# Create your views here.

def getprotocol(request):
    print("hello")
    if request.method == "GET":
        print("hello")
        if (request.GET["start_date"] != None):
            start_date = str(request.GET["start_date"])
            start = start_date.split("-")
        else:
            start = 0
        if (request.GET["stop_date"] != None):
            stop_date = str(request.GET["stop_date"])
            stop = stop_date.split("-")
        else:
            stop = 0
        '''   
        prot_data = countProtinfo(start,stop)
        prot_x = []
        prot_y = []
        for i in range(len(prot_data)):
            prot_x[i] = prot_data[i]['Protocol']
            d = {"value":prot_x[i],"name":prot_y[i]}
            prot_y[i] = d
        '''
        prot_x = ['HTTP','DNS','SSL','DHCP','Unknow']
        prot_y = [{"value":335, "name":'HTTP'},{"value":310, "name":'DNS'},{"value":234, "name":'DHCP'},
                  {"value":135, "name":'Unknow'},{"value":1548, "name":'SSL'}]
        data = {"prot_x":prot_x,"prot_y":prot_y}
        return HttpResponse(json.dumps(data))
