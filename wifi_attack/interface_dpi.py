from DdModel.models import DFI_Info, DPI_Picture
from django.db.models import Sum
from datetime import date
import time


def apmactoapip(APmac):
    APip = DFI_Info.objects.filter(Source_Mac=APmac).values('Source_IP')
    return (APip, len(APip))


def stamactostaip(STAmac, APmac):
    STAip = DFI_Info.objects.filter(Source_Mac=STAmac, Dest_Mac=APmac).values('Source_IP', 'Date', 'Time')
    return (STAip, len(STAip))


def dpicount(APmac, STAlist):
    dpiCount = {}
    localtime = time.localtime(time.time() - 300)
    date_time = time.strftime("%Y-%m-%d %H:%M:%S", localtime)
    Date_now = date_time[0:10]
    Time_now = date_time[11:]
    try :
        StaBytesCount = DFI_Info.objects.filter(Date__gte=Date_now, Time__gte=Time_now, Dest_Mac=APmac).values('Source_Mac').annotate(sum_bytes=Sum('Bytes')).order_by('-sum_bytes')[0:10]
    except IndexError:
        StaBytesCount = DFI_Info.objects.filter(Date__gte=Date_now, Time__gte=Time_now, Dest_Mac=APmac).values('Source_Mac').annotate(sum_bytes=Sum('Bytes')).order_by('-sum_bytes')
    dpiCount['STA_Bytes'] = StaBytesCount
    try:
        ServerBytesCount = DFI_Info.objects.filter(Date__gte=Date_now, Time__gte=Time_now, Dest_Mac=APmac).values('Dest_IP', 'Host').annotate(sum_bytes=Sum('Bytes')).order_by('-sum_bytes')[0:10]
    except IndexError:
        ServerBytesCount = DFI_Info.objects.filter(Date__gte=Date_now, Time__gte=Time_now, Dest_Mac=APmac).values('Dest_IP', 'Host').annotate(sum_bytes=Sum('Bytes')).order_by('-sum_bytes')
    dpiCount['Server_Bytes'] = ServerBytesCount
    try:
        ProtoBytesCount = DFI_Info.objects.filter(Date__gte=Date_now, Time__gte=Time_now, Dest_Mac=APmac).values('Protocol').annotate(sum_bytes=Sum('Bytes')).order_by('-sum_bytes')[0:10]
    except IndexError:
        ProtoBytesCount = DFI_Info.objects.filter(Date__gte=Date_now, Time__gte=Time_now, Dest_Mac=APmac).values('Protocol').annotate(sum_bytes=Sum('Bytes')).order_by('-sum_bytes')
    dpiCount['Proto_Bytes'] = ProtoBytesCount
    return dpiCount
