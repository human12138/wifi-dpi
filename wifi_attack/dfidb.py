from DdModel.models import DFI_Info, DPI_Picture
from django.db.models import Sum, Max, Q
from datetime import date
from wifi_attack.hostblacklist import funcList
import time


def insertFlowInfo(flowInfo):
    Flow_Info = DFI_Info(
        Source_Mac = flowInfo['Source_Mac'], 
        Dest_Mac = flowInfo['Dest_Mac'], 
        Source_IP = flowInfo['Source_IP'], 
        Dest_IP = flowInfo['Dest_IP'], 
        Source_Port = flowInfo['Source_Port'], 
        Dest_Port = flowInfo['Dest_Port'], 
        Protocol = flowInfo['Protocol'],
        Bytes = flowInfo['Bytes'], 
        Host = flowInfo['Host']
    )
    Flow_Info.save()


def deleteFlowByDate(dateInfo):
    DFI_Info.objects.filter(Date=dateInfo).delete()


def countProtinfo(startTime=0, endTime=0):    #struct startTime&endTime [year, month, day]
    localtime = time.localtime(time.time() - 3600)
    if startTime == endTime == 0:
        result = DFI_Info.objects.filter(DateTime__gte=time.strftime("%Y-%m-%d %H:%M:%S", localtime)).values('Protocol').annotate(Sum('Bytes')).order_by('-Bytes')
    elif startTime == 0 and endTime != 0:
        result = DFI_Info.objects.filter(Date__lte=date(int(endTime[0]), int(endTime[1]), int(endTime[2]))).values('Protocol').annotate(Sum('Bytes')).order_by('-Bytes')
    elif startTime != 0 and endTime == 0:
        result = DFI_Info.objects.filter(Date__gte=date(int(startTime[0]), int(startTime[1]), int(startTime[2]))).values('Protocol').annotate(Sum('Bytes')).order_by('-Bytes')
    else:
        result = DFI_Info.objects.filter(Date__gte=date(int(startTime[0]), int(startTime[1]), int(startTime[2])), Date__lte=date(int(endTime[0]), int(endTime[1]), int(endTime[2]))).values('Protocol').annotate(Sum('Bytes')).order_by('-Bytes')
    if len(result) >= 10:
        return result[0:10]
    else:
        return result


def countIPinfo(MacInfo, IpInfo):
    IP_Info = {}
    print(MacInfo)
    print(IpInfo)
    proto_info = DFI_Info.objects.filter(Source_Mac=MacInfo, Source_IP=IpInfo).values('Protocol').annotate(s_byte=Sum('Bytes')).order_by('-s_byte')
    #test = DFI_Info.objects.filter(Source_Mac=MacInfo, Source_IP='192.168.199.162')
    #print(len(test))
    if len(proto_info) >= 10:
        IP_Info['Proto_Info'] = proto_info[0:10]
    else:
        IP_Info['Proto_Info'] = proto_info
    #print(IP_Info['Proto_Info'][0])
    host_info = DFI_Info.objects.filter(Host__isnull=False, Source_Mac=MacInfo, Source_IP=IpInfo).values('Host').annotate(s_byte=Sum('Bytes')).order_by('-s_byte')
    if len(host_info) >= 10:
        IP_Info['Host_Info'] = host_info[0:10]
    else:
        IP_Info['Host_Info'] = host_info
    flow_info = DFI_Info.objects.filter(Source_Mac=MacInfo, Source_IP=IpInfo).values('Dest_Mac', 'Dest_IP', 'Source_Port', 'Dest_Port', 'Protocol', 'Bytes', 'Host')
    #print(len(flow_info))
    IP_Info['Flow_Info'] = flow_info
    #pic_path = DPI_Picture.objects.filter(Source_IP=IpInfo).values('Dest_IP', 'Pic_Path', 'DateTime')
    #if len(pic_path) >= 10:
    #    IP_Info['Pic_Path'] = pic_path[0:10]
    #else:
     #   IP_Info['Pic_Path'] = pic_path
    IP_Info['Black_Host'] = blackHost(MacInfo, IpInfo)
    return IP_Info


def insertPictureInfo(fileName):
    dpi_pic = fileName.split('_')
    DPI_pic = DPI_Picture(
        Source_IP = dpi_pic[0],
        Dest_IP = dpi_pic[1],
        DateTime = dpi_pic[2],
        Pic_Path = dpi_pic[3]
    )
    DPI_pic.save()


def detectIP_bytime(startTime=0, endTime=0):
    IP_Count = {}
    localtime = time.localtime(time.time() - 3600)
    if startTime == endTime == 0:
        Client_bytes = DFI_Info.objects.filter(~Q(Source_IP__endswith='.1'), DateTime__gte=time.strftime("%Y-%m-%d %H:%M:%S", localtime)).values('Source_Mac', 'Source_IP').annotate(Sum('Bytes')).order_by('-Bytes')
        Host_bytes = DFI_Info.objects.filter(DateTime__gte=time.strftime("%Y-%m-%d %H:%M:%S", localtime), Host__isnull=False).values('Host', 'Dest_IP').annotate(Sum('Bytes')).order_by('-Bytes')
        IP_Count['Client_Bytes'] = Client_bytes
        IP_Count['Host_Bytes'] = Host_bytes
    elif startTime == 0 and endTime != 0:
        Client_bytes = DFI_Info.objects.filter(~Q(Dest_IP__endswith='.1'), Date__lte=date(int(endTime[0]), int(endTime[1]), int(endTime[2]))).values('Source_Mac', 'Source_IP').annotate(Sum('Bytes')).order_by('-Bytes')
        Host_bytes = DFI_Info.objects.filter(Date__lte=date(int(endTime[0]), int(endTime[1]), int(endTime[2]))).values('Host', 'Dest_IP').annotate(Sum('Bytes')).order_by('-Bytes')
        IP_Count['Client_Bytes'] = Client_bytes
        IP_Count['Host_Bytes'] = Host_bytes
        ip_activetime = DFI_Info.objects.filter(Date__lte=date(int(endTime[0]), int(endTime[1]), int(endTime[2]))).values('Source_Mac', 'Source_IP').annotate(Max('Date'), Max('Time'))
        IP_Count['IP_activetime'] = ip_activetime
    elif startTime != 0 and endTime == 0:
        Client_bytes = DFI_Info.objects.filter(~Q(Dest_IP__endswith='.1'), Date__gte=date(int(startTime[0]), int(startTime[1]), int(startTime[2]))).values('Source_Mac', 'Source_IP').annotate(Sum('Bytes')).order_by('-Bytes')
        Host_bytes = DFI_Info.objects.filter(Date__gte=date(int(startTime[0]), int(startTime[1]), int(startTime[2]))).values('Host', 'Dest_IP').annotate(Sum('Bytes')).order_by('-Bytes')
        IP_Count['Client_Bytes'] = Client_bytes
        IP_Count['Host_Bytes'] = Host_bytes
        ip_activetime = DFI_Info.objects.filter(Date__gte=date(int(startTime[0]), int(startTime[1]), int(startTime[2]))).values('Source_Mac', 'Source_IP').annotate(Max('Date'), Max('Time'))
        IP_Count['IP_activetime'] = ip_activetime
    else:
        Client_bytes = DFI_Info.objects.filter(~Q(Dest_IP__endswith='.1'), Date__gte=date(int(startTime[0]), int(startTime[1]), int(startTime[2])), Date__lte=date(int(endTime[0]), int(endTime[1]), int(endTime[2]))).values('Source_Mac', 'Source_IP').annotate(Sum('Bytes')).order_by('-Bytes')
        Host_bytes = DFI_Info.objects.filter(Date__gte=date(int(startTime[0]), int(startTime[1]), int(startTime[2])), Date__lte=date(int(endTime[0]), int(endTime[1]), int(endTime[2]))).values('Host', 'Dest_IP').annotate(Sum('Bytes')).order_by('-Bytes')
        IP_Count['Client_Bytes'] = Client_bytes
        IP_Count['Host_Bytes'] = Host_bytes
        ip_activetime = DFI_Info.objects.filter(Date__gte=date(int(startTime[0]), int(startTime[1]), int(startTime[2])), Date__lte=date(int(endTime[0]), int(endTime[1]), int(endTime[2]))).values('Source_Mac', 'Source_IP').annotate(Max('Date'), Max('Time'))
        IP_Count['IP_activetime'] = ip_activetime
    return IP_Count


def blackHost(MacInfo, IpInfo):
    hosts = DFI_Info.objects.filter(Source_Mac=MacInfo, Source_IP=IpInfo, Host__isnull=False).values('Host')
    hostList = []
    hostAttr = {}
    #print(hosts)
    if hosts[0]['Host']:
        for i in range(len(hosts)):
            hostList.append(hosts[i]['Host'])
        result = funcList(hostList)
        for i in range(len(hosts)):
            hostAttr[hostList[i]] = result[i]
    return hostAttr


def MacToIP(Macaddr):
    ip = DFI_Info.objects.filter(Source_Mac=Macaddr).values('Source_IP')
    mtoi = {Macaddr: []}
    for i in range(ip):
        mtoi[Macaddr].append(ip[i]['Source_IP'])
    return mtoi
