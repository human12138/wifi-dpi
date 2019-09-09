from django.shortcuts import render
from django.http import HttpResponse
import pymysql
from wifi_attack.dfidb import *
from wifi_attack.interface_sta import *

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

        ip = str(request.GET['ip'])
        mac = str(request.GET['mac'])
        ap_mac = str(request.GET['ap_mac'])
        start_date = str(request.GET['start_date']).split('-')
        stop_date = str(request.GET['stop_date']).split('-')
        page_id = int(request.GET['page_id'])
        #print(ip+" "+mac+" "+ap_mac+" "+start_date+" "+stop_date)


        ip_list = getstaip(ap_mac,mac,start_date,stop_date)
        ap_list = usedap(ap_mac,mac,start_date,stop_date)
        list = stacount(ap_mac,mac,start_date,stop_date)
        flow_list = staflowinfo(ap_mac,mac,start_date,stop_date,page_id)
        flow = flow_list[0]
        count = flow_list[1]

        Ip_list = list['IP_Bytes']
        port_list = list['port_Bytes']
        proto_list = list['proto_Bytes']

        protocol_label = []
        protocol_data = []
        desdata_x = []
        desdata_y = []
        port_x = []
        port_y = []
        ip_data = []
        ap_data1 = []
        ipinfo = []

        for i in range(len(proto_list)):
            protocol_label.append(proto_list[i]['Protocol'])
            protocol_data.append({'name': proto_list[i]['Protocol'],'value':proto_list[i]['sum_bytes']})
        for i in range(len(Ip_list)):
            desdata_x.append(Ip_list[i]['sum_bytes'])
            desdata_y.append(Ip_list[i]['Dest_IP'])
        for i in range(len(port_list)):
            port_x.append(port_list[i]['sum_bytes'])
            port_y.append(port_list[i]['Dest_Port'])
        for ip in ip_list:
            ip_data.append({'ip_history':ip['Source_IP']})
        for ap in ap_list:
            ap_data1.append({'mac': ap['Dest_Mac'],'date':(str(ap['last_date'])+" "+str(ap['last_time']))})
        print(ip_data)

        for f in flow:
            ipinfo.append({'desmac':f['Dest_Mac'],'desip':f['Dest_IP'],'desport':f['Dest_Port'],'protocol':f['Protocol'],'address':f['Host'],
                          'byte':f['Bytes'],'dangerous':'false','date':(str(f['Date'])+" "+str(f['Time']))})
        data = {"protocol_label":protocol_label,"protocol_data":protocol_data,"ipinfo":ipinfo,"desdata_x":desdata_x,
                "desdata_y":desdata_y,"portdata_x":port_x,"portdata_y":port_y,"ip_data":ip_data,"ap_data1":ap_data1,"count":count}
        print(count)
        return HttpResponse(json.dumps(data))

def getflow(request):
    ip = str(request.GET['ip'])
    mac = str(request.GET['mac'])
    ap_mac = str(request.GET['ap_mac'])
    start_date = str(request.GET['start_date']).split('-')
    stop_date = str(request.GET['stop_date']).split('-')
    page_id = int(request.GET['page_id'])

    flow_list = staflowinfo(ap_mac,mac,start_date,stop_date,page_id)
    if page_id == 0:
        flow = flow_list[0]
    else:
        flow = flow_list
    ipinfo = []
    for f in flow:
        ipinfo.append({'desmac': f['Dest_Mac'], 'desip': f['Dest_IP'], 'desport': f['Dest_Port'],
                       'protocol': f['Protocol'], 'address': f['Host'],'byte': f['Bytes'], 'dangerous': 'false','date':(str(f['Date'])+" "+str(f['Time']))})
    data = {"ipinfo":ipinfo,}
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




