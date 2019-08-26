from django.shortcuts import render
from django.http import HttpResponse
import pymysql
from wifi_attack.dfidb import *

import json
import datetime
import time
import os

def hello(request):
    db = pymysql.connect("localhost", "root", "root123", "wifi_attack")
    cursor = db.cursor()
    cursor.execute("select * from black_mac")
    results = cursor.fetchall()
    mac=[]
    for d in results:
        mac.append(d[0])
    data = json.dumps(mac)
    return render(request, 'B.html',locals())

def get_mac(request):
    if request.method == "GET":
        
        data = str(request.GET)
        data = data.split("[")[1]
        data = data.split("]")[0]
        data = data.split(",")
        
        result = "修改成功"

        db = pymysql.connect("localhost", "root", "root123", "wifi_attack")
        cursor = db.cursor()
        for d in data:
            if " " in d:
                d = d[2:-1]
            else: 
                d = d[1:-1]
            sql = "INSERT INTO black_mac(mac) " \
                  "VALUES ('%s')" \
                  % (d)
            cursor.execute(sql)
            db.commit()
        
        return HttpResponse(result)
def search(request):
    if request.method == "GET":
        start_date = str(request.GET["start_date"])
        stop_date = str(request.GET["stop_date"])

        print(start_date)
        print(stop_date)
        start_date= start_date + " 00:00:00"
        stop_date = stop_date+" 23:59:59"

        db = pymysql.connect("localhost", "root", "root123", "wifi_attack")
        cursor = db.cursor()
        sql = "select * from attack where attack_date between '%s' and '%s' order by attack_date asc"%(start_date,stop_date)
        cursor.execute(sql)
        list = cursor.fetchall()
        result = {}
        print(list)
        if len(list) == 0:
            result.update({"flag":0})
            data ="wps:未发生\n" \
                "krack:未发生\n" \
                "fake_ap:未发生\n" \
                "broadpwn:未发生\n" \
                "eap_start:未发生\n" \
                "eap_logoff:1\n" \
                "deauth_flood:1\n" \
                "association_flood:未发生\n" \
                "deassociation_flood:未发生\n" \
                "没有攻击发生!恭喜"
            result.update({"data":data})
            result = json.dumps(result)
            return HttpResponse(result)
        else:
            data=""
            flag={'fake_ap':0,'krack':0, 'wps':0, 'association_flood':0, 'black_mac':0, 'deassociation_flood':0,
                  'eap_start':0, 'deauth_flood':0, 'eap_logoff':0,'broadpwn':0}
            attack_type0 = "hello"
            date0 = ""
            for i in range(len(list)):
                if i==0:
                    date0 = str(list[i][4])
                    attack_type0 = list[i][0]
                    flag[attack_type0] = flag[attack_type0]+1
                elif i==len(list)-1:
                    a = "攻击类型:" + attack_type0 + " "
                    date1 = str(list[i][4])
                    flag[attack_type1] = flag[attack_type1] + 1
                    attacked_mac = list[i][1]
                    a = a + "被攻击设备" + attacked_mac + " "
                    if list[i][2] is None:
                        pass
                    else:
                        a = a + "攻击设备" + list[i][2] + " "
                    if list[i][3] is None:
                        pass
                    else:
                        a = a + "受影响设备" + list[i][3] + " "
                    a = a + "开始时间:" + date0 + " 结束时间:" + date1 + "\n"
                    date0 = str(list[i][4])
                    data = data + a
                else:
                    attack_type1 = list[i+1][0]
                    if attack_type1 == attack_type0:
                        pass
                    else:
                        a = "攻击类型:"+attack_type0+" "
                        date1 = str(list[i][4])
                        flag[attack_type1] = flag[attack_type1] + 1
                        attacked_mac = list[i][1]
                        a = a + "被攻击设备"+ attacked_mac+" "
                        if list[i][2] is None:
                            pass
                        else:
                            a = a +"攻击设备"+list[i][2]+" "
                        if list[i][3] is None:
                            pass
                        else:
                            a = a + "受影响设备"+list[i][3]+" "
                        a = a + "开始时间:" +date0 + " 结束时间:" + date1+"\n"
                        date0 = str(list[i+1][4])
                        data = data + a
                        attack_type0 = attack_type1
            text = "wps:%s\n" \
                    "krack:%s\n" \
                    "fake_ap:%s\n" \
                    "broadpwn:%s\n" \
                    "eap_start:%s\n" \
                    "eap_logoff:%s\n" \
                    "deauth_flood:%s\n" \
                    "association_flood:%s\n" \
                    "deassociation_flood:%s\n"\
                    "-------------------------\n"\
                    %(flag["wps"],flag["krack"],flag["fake_ap"],flag["broadpwn"],flag["eap_start"],flag["eap_logoff"],flag["deauth_flood"],flag["association_flood"],flag["deassociation_flood"])
            data = text + data
            result.update({"flag":1})
            result.update({"data":data})
            result = json.dumps(result)
            return HttpResponse(result)




def getfile(request):
    if request.method == "POST":
        #start_time = time.time()
        upload_file = request.FILES['file']
        old_file_name = upload_file.name
        if upload_file:
            file_path = os.path.join('/tmp/test_file/', old_file_name)
            f = open(file_path, 'wb')
            for chunk in upload_file.chunks():
                f.write(chunk)
            f.close()
            return 'success'
        else:
            return 'failed'

def gethistory(request):
    if request.method == "GET":
        start_date=str(request.GET['start_date'])
        stop_date = str(request.GET['stop_date'])
        '''
        start = start_date.split('-')
        stop = start_date.split('-')
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

        srcdata_x = [10, 52, 200, 334, 390, 330, 220]
        srcdata_y = ['192.168.199.126', '192.168.199.124', '192.168.1.3', '192.168.1.2',
                     '192.168.3.6','192.168.199.103', '192.168.3.1']
        desdata_x = [10, 52, 200, 334, 390, 330, 220]
        desdata_y = ['192.168.199.126', '192.168.199.124', '192.168.1.3', '192.168.1.2',
                     '192.168.3.6','192.168.199.103', '192.168.3.1']

        ip = [{'ip': '192.168.1.126','date':  stop_date+' 18:58:00'},{'ip': '192.168.1.103','date': stop_date+' 14:23:03'},
            {'ip': '192.168.3.2','date': stop_date+ ' 10:41:56'},{'ip': '192.168.3.3','date': start_date+' 22:57:31'},
            {'ip':'192.168.1.3','date': start_date+' 19:32:34'}, {'ip':'192.168.1.2','date':start_date+' 15:45:38'},
            {'ip': '192.168.3.6','date': start_date+' 12:32:43'}, {'ip': '192.168.199.124','date': start_date+' 08:32:18'}]


        data = {"prot_x":prot_x,"prot_y":prot_y,"srcdata_x": srcdata_x, "srcdata_y": srcdata_y,
                "desdata_x":desdata_x,"desdata_y":desdata_y,"ip":ip}
        return HttpResponse(json.dumps(data))

def getindex(request):
    if request.method == "GET":
        prot_x = ['HTTP','DNS','SSL','DHCP','Unknow']
        prot_y = [{"value":335, "name":'HTTP'},{"value":310, "name":'DNS'},{"value":234, "name":'DHCP'},
                  {"value":135, "name":'Unknow'},{"value":1548, "name":'SSL'}]
        srcdata_x = [10, 52, 200, 334, 390, 330, 220]
        srcdata_y = ['192.168.199.126', '192.168.199.124', '192.168.1.3', '192.168.1.2',
                     '192.168.3.6','192.168.199.103', '192.168.3.1']
        desdata_x = [10, 52, 200, 334, 390, 330, 220]
        desdata_y = ['192.168.199.126', '192.168.199.124', '192.168.1.3', '192.168.1.2',
                     '192.168.3.6','192.168.199.103', '192.168.3.1']
        ip = [{'ip': '192.168.199.162','mac':'34:23:87:A9:26:9B'},
        {'ip': '192.168.3.103','mac':'D4:EE:07:32:01:5A'},
        {'ip': '192.168.3.2','mac':'D4:EE:07:32:01:5A'},
        {'ip': '192.168.3.3','mac':'D4:EE:07:32:01:5A'},]
        ap_info=[]
        mac = str(request.GET['mac'])
        if mac == 'D4:EE:07:32:01:5A':
            ap_info.append({'info_name': 'AP名称(SSID):','info_data': 'xd-stu'}),
            ap_info.append({'info_name': 'MAC地址:','info_data': 'D4:EE:07:32:01:5A'}),
            ap_info.append({'info_name': '局域网IP:','info_data': '192.168.126.1'}),
            ap_info.append({'info_name': '信道:','info_data': 11}),
            ap_info.append({'info_name': '信号强度:','info_data': '强'})
        elif mac == '34:23:87:A9:26:9B':
            ap_info = [{'info_name': 'AP名称(SSID):','info_data': 'test'},
                       {'info_name': 'MAC地址:','info_data': '34:23:87:A9:26:9B'},
                       {'info_name': '局域网IP:','info_data': '192.168.3.1'},
                       {'info_name': '信道:','info_data': 11},
                       {'info_name': '信号强度:','info_data': '强'}
                      ],
        else:
            ap_info = [{'info_name': 'AP名称(SSID):', 'info_data': 'xd-stu'},
                       {'info_name': 'MAC地址:', 'info_data': 'D4:EE:07:32:01:5A'},
                       {'info_name': '局域网IP:', 'info_data': '192.168.3.1'},
                       {'info_name': '信道:', 'info_data': 11},
                       {'info_name': '信号强度:', 'info_data': '强'}
                      ],
        print(ap_info)
        data = {"srcdata_x": srcdata_x, "srcdata_y": srcdata_y,"desdata_x":desdata_x,"desdata_y":desdata_y,"ip":ip,"prot_x":prot_x,"prot_y":prot_y,"ap_info":ap_info}
        return HttpResponse(json.dumps(data))

def getinfo(request):
    if request.method == "GET":
        #print(request.GET['ip'])
        ip = str(request.GET['ip'])
        mac = str(request.GET['mac'])
        print(ip)
        print(mac)
        list=countIPinfo(mac, ip)
        proto_list = list['Proto_Info']
        host_list = list['Host_Info']
        flow_list = list['Flow_Info']
        host_black = list['Black_Host']
        protocol_label = []
        protocol_data = []
        website_label = []
        website_data = []
        ipinfo = []
        print(proto_list)
        for i in range(len(proto_list)):
            protocol_label.append(proto_list[i]['Protocol'])
            protocol_data.append({'name': proto_list[i]['Protocol'],'value':proto_list[i]['s_byte']})

        #print(protocol_label)
        #print(protocol_data)
        for i in range(len(host_list)):
            website_label.append(host_list[i]['Host'])
            website_data.append({'name': host_list[i]['Host'],'value':host_list[i]['s_byte']})
        for flow in flow_list:
            if host_black[flow['Host']] == False:
                ipinfo.append({'desmac':flow['Dest_Mac'],'desip':flow['Dest_IP'],'srcport':flow['Source_Port'],
                          'desport':flow['Dest_Port'],'protocol':flow['Protocol'],'address':flow['Host'],
                          'byte':flow['Bytes'],'dangerous':'false'})
            else:
                ipinfo.append({'desmac': flow['Dest_Mac'], 'desip': flow['Dest_IP'], 'srcport': flow['Source_Port'],
                          'desport': flow['Dest_Port'], 'protocol': flow['Protocol'], 'address': flow['Host'],
                          'byte': flow['Bytes'], 'dangerous': 'true'})
        ap_data={'name': 'xd_stu','value': 'D4:EE:07:32:01:5A',
                  'children': [{'name': 'D4:EE:07:32:01:5A','value': '192.168.3.1'},
                               {'name': 'D4:EE:07:32:01:5A','label': {'color': 'green'}},
                               {'name': 'D4:EE:07:32:01:5A'},
                               {'name': 'D4:EE:07:32:01:5A'},
                               {'name': 'D4:EE:07:32:01:5A'},
                               {'name': 'D4:EE:07:32:01:5A'},
                               {'name': 'D4:EE:07:32:01:5A'},
                               ]
                  },

        '''
        website_label = ['baidu', 'bilibili', 'neteasy', 'iqiyi', 'qq']
        website_data = [{"value": 335, "name": 'baidu'},{"value": 310, "name": 'neteasy'},{"value": 234, "name": 'iqiyi'},
                        {"value": 135, "name": 'qq'},{"value": 1548, "name": 'bilibili'}]
        protocol_label = ['HTTP', 'DNS', 'SSL', 'DHCP', 'Unknow']
        protocol_data = [{"value": 335, "name": 'HTTP'},{"value": 310, "name": 'DNS'},{"value": 234, "name": 'DHCP'},
                         {"value": 135, "name": 'Unknow'},{"value": 1548, "name": 'SSL'}]
        ipinfo = [
            {'srcmac': "34:23:87:A9:26:9B",'desmac': "D4:EE:07:32:01:5A",'srcip': "192.168.199.162",'desip': "119.3.227.169",
             'srcport': "17600",'desport': "47873",'address': "www.bilibili.com",'date': "2019-06-19 23:13:52",'protocol': "DNS",'byte': "6956",
            'dangerous': 'false'},
            {'srcmac': "34:23:87:A9:26:9B",'desmac': "D4:EE:07:32:01:5B",'srcip': "192.168.199.162",'desip': "119.3.227.168",
             'srcport': "17600",'desport': "47875",'address': "http://www.baidu.com",'date': "2019-06-19 23:13:43",'protocol': "HTTP",'byte': "6956",
             'dangerous': 'false'},
            {'srcmac': "34:23:87:A9:26:9B",'desmac': "D4:EE:07:32:01:50",'srcip': "192.168.199.162",'desip': "119.3.227.166",
             'srcport': "17600",'desport': "47870",'address': "http://zkhhxq.cool168.com/",'date': "2019-06-19 23:13:52",'protocol': "HTTP",'byte': "6956",
             'dangerous': 'true'},
            {'srcmac': "34:23:87:A9:26:9B",'desmac': "D4:EE:07:32:01:5B",'srcip': "192.168.199.162",'desip': "119.3.227.120",
             'srcport': "17600",'desport': "47875",'address': "http://yl163.net/",'date': "2019-06-19 23:13:53",'protocol': "HTTP",'byte': "6956",
             'dangerous': 'true'},
        ]
        
        imgurl = [{"url1":"/static/img/1.jpg","url2":"/static/img/2.jpg","url3":"/static/img/3.jpg",
                   "url4":"/static/img/4.jpg","url5":"/static/img/5.jpg"},
                  {"url1": "/static/img/6.png", "url2": "/static/img/5.jpg", "url3": "/static/img/1.jpg",
                   "url4": "/static/img/3.jpg", "url5": "/static/img/6.png"}
                  ]
        
        data = {"website_label":website_label,"website_data":website_data,"protocol_label":protocol_label,
                "protocol_data":protocol_data,"ipinfo":ipinfo,"imgurl":imgurl}
        '''
        print(ap_data)
        data = {"website_label":website_label,"website_data":website_data,"protocol_label":protocol_label,
                "protocol_data":protocol_data,"ipinfo":ipinfo,"ap_data":ap_data}
        return HttpResponse(json.dumps(data))


def getapinfo(mac):
    if mac == 'D4:EE:07:32:01:5A':
        ap_info=[{'info_name': 'AP名称(SSID):','info_data': 'xd-stu'},
                {'info_name': 'MAC地址:','info_data': 'D4:EE:07:32:01:5A'},
                {'info_name': '局域网IP:','info_data': '192.168.126.1'},
                {'info_name': '信道:','info_data': 11},
                {'info_name': '信号强度:','info_data': '强'}
                ],
    elif mac == '34:23:87:A9:26:9B':
        ap_info = [{'info_name': 'AP名称(SSID):','info_data': 'test'},
                    {'info_name': 'MAC地址:','info_data': '34:23:87:A9:26:9B'},
                    {'info_name': '局域网IP:','info_data': '192.168.3.1'},
                    {'info_name': '信道:','info_data': 11},
                    {'info_name': '信号强度:','info_data': '强'}
                    ],
    else:
        ap_info = [{'info_name': 'AP名称(SSID):', 'info_data': 'xd-stu'},
                    {'info_name': 'MAC地址:', 'info_data': 'D4:EE:07:32:01:5A'},
                    {'info_name': '局域网IP:', 'info_data': '192.168.3.1'},
                    {'info_name': '信道:', 'info_data': 11},
                    {'info_name': '信号强度:', 'info_data': '强'}
                    ],
    print(ap_info)

    return ap_info




