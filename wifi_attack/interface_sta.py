from DdModel.models import DFI_Info, DPI_Picture
from django.db.models import Sum, Max, Q
from datetime import date
from wifi_attack.hostblacklist import funcList
import time


def getstaip(APmac, STAmac, startTime, endTime):  #struct startTime&endTime [year, month, day]
    ipList = DFI_Info.objects.filter(Dest_Mac=APmac, Source_Mac=STAmac, Date__gte=date(int(startTime[0]), int(startTime[1]), int(startTime[2])), Date__lte=date(int(endTime[0]), int(endTime[1]), int(endTime[2]))).values('Source_IP')
    return ipList


def usedap(APmac, STAmac, startTime, endTime):
    usedAPlist = DFI_Info.objects.filter(Source_Mac=STAmac, Date__gte=date(int(startTime[0]), int(startTime[1]), int(startTime[2])), Date__lte=date(int(endTime[0]), int(endTime[1]), int(endTime[2]))).values('Dest_Mac').annotate(last_date=Max('Date'), last_time=Max('Time'))
    return usedAPlist


def stacount(APmac, STAmac, startTime, endTime):
    staCount = {}
    try:
        serverCount = DFI_Info.objects.filter(Dest_Mac=APmac, Source_Mac=STAmac, Date__gte=date(int(startTime[0]), int(startTime[1]), int(startTime[2])), Date__lte=date(int(endTime[0]), int(endTime[1]), int(endTime[2]))).values('Dest_IP').annotate(sum_bytes=Sum('Bytes')).order_by('-sum_bytes')[0:10]
    except IndexError:
        serverCount = DFI_Info.objects.filter(Dest_Mac=APmac, Source_Mac=STAmac, Date__gte=date(int(startTime[0]), int(startTime[1]), int(startTime[2])), Date__lte=date(int(endTime[0]), int(endTime[1]), int(endTime[2]))).values('Dest_IP').annotate(sum_bytes=Sum('Bytes')).order_by('-sum_bytes')
    try:
        portCount = DFI_Info.objects.filter(Dest_Mac=APmac, Source_Mac=STAmac, Date__gte=date(int(startTime[0]), int(startTime[1]), int(startTime[2])), Date__lte=date(int(endTime[0]), int(endTime[1]), int(endTime[2]))).values('Dest_Port').annotate(sum_bytes=Sum('Bytes')).order_by('-sum_bytes')[0:10]
    except IndexError:
        portCount = DFI_Info.objects.filter(Dest_Mac=APmac, Source_Mac=STAmac, Date__gte=date(int(startTime[0]), int(startTime[1]), int(startTime[2])), Date__lte=date(int(endTime[0]), int(endTime[1]), int(endTime[2]))).values('Dest_Port').annotate(sum_bytes=Sum('Bytes')).order_by('-sum_bytes')
    try:
        protoCount = DFI_Info.objects.filter(Dest_Mac=APmac, Source_Mac=STAmac, Date__gte=date(int(startTime[0]), int(startTime[1]), int(startTime[2])), Date__lte=date(int(endTime[0]), int(endTime[1]), int(endTime[2]))).values('Protocol').annotate(sum_bytes=Sum('Bytes')).order_by('-sum_bytes')[0:10]
    except IndexError:
        protoCount = DFI_Info.objects.filter(Dest_Mac=APmac, Source_Mac=STAmac, Date__gte=date(int(startTime[0]), int(startTime[1]), int(startTime[2])), Date__lte=date(int(endTime[0]), int(endTime[1]), int(endTime[2]))).values('Protocol').annotate(sum_bytes=Sum('Bytes')).order_by('-sum_bytes')
    staCount['IP_Bytes'] = serverCount
    staCount['port_Bytes'] = portCount
    staCount['proto_Bytes'] = protoCount
    return staCount


def staflowinfo(APmac, STAmac, startTime, endTime, ID):
    counts = DFI_Info.objects.filter(Dest_Mac=APmac, Source_Mac=STAmac, Date__gte=date(int(startTime[0]), int(startTime[1]), int(startTime[2])), Date__lte=date(int(endTime[0]), int(endTime[1]), int(endTime[2]))).count()
    try:
        flow_info = DFI_Info.objects.filter(Dest_Mac=APmac, Source_Mac=STAmac, Date__gte=date(int(startTime[0]), int(startTime[1]), int(startTime[2])), Date__lte=date(int(endTime[0]), int(endTime[1]), int(endTime[2]))).values('Dest_Mac', 'Dest_IP', 'Dest_Port', 'Protocol', 'Host','Bytes', 'Date', 'Time')[ID * 10:ID * 10 + 10]
    except IndexError:
        flow_info = DFI_Info.objects.filter(Dest_Mac=APmac, Source_Mac=STAmac, Date__gte=date(int(startTime[0]), int(startTime[1]), int(startTime[2])), Date__lte=date(int(endTime[0]), int(endTime[1]), int(endTime[2]))).values('Dest_Mac', 'Dest_IP', 'Dest_Port', 'Protocol', 'Host','Bytes', 'Date', 'Time')[ID * 10:ID * 10 + counts%10]
    if ID == 0:
        return (flow_info, counts)
    else:
        return flow_info


def datacontext(APmac, STAmac, ProtocolName, startTime=0, endTime=0):
    return


def blackHost(APmac, STAmac, startTime, endTime):
    hosts = DFI_Info.objects.filter(Source_Mac=STAmac, Dest_Mac=APmac, Host__isnull=False, Date__gte=date(int(startTime[0]), int(startTime[1]), int(startTime[2])), Date__lte=date(int(endTime[0]), int(endTime[1]), int(endTime[2]))).values('Host')
    hostList = []
    hostAttr = {}
    if hosts[0]['Host']:
        for i in range(len(hosts)):
            hostList.append(hosts[i]['Host'])
        result = funcList(hostList)
        for i in range(len(hosts)):
            hostAttr[hostList[i]] = result[i]
    return hostAttr