from DdModel.models import DFI_Info, DPI_Picture
from django.db.models import Sum, Max, Q
from datetime import date
import time


def showstainfo(APmac, startTime, endTime):   #struct startTime&endTime [year, month, day]
    staInfo = DFI_Info.objects.filter(Date__gte=date(int(startTime[0]), int(startTime[1]), int(startTime[2])), Date__lte=date(int(endTime[0]), int(endTime[1]), int(endTime[2])), Dest_Mac=APmac).values('Source_Mac', 'Source_IP').annotate(last_date=Max('Date'), last_time=Max('Time'))
    return staInfo


def apcount(APmac, startTime, endTime):
    APcount = {}
    STA_Bytes = DFI_Info.objects.filter(Date__gte=date(int(startTime[0]), int(startTime[1]), int(startTime[2])), Date__lte=date(int(endTime[0]), int(endTime[1]), int(endTime[2])), Dest_Mac=APmac).values('Source_Mac').annotate(sum_bytes=Sum('Bytes')).order_by('-smu_bytes')
    Server_Bytes = DFI_Info.objects.filter(Date__gte=date(int(startTime[0]), int(startTime[1]), int(startTime[2])), Date__lte=date(int(endTime[0]), int(endTime[1]), int(endTime[2])), Dest_Mac=APmac).values('Dest_IP').annotate(sum_bytes=Sum('Bytes')).order_by('-smu_bytes')
    try:
        Porto_Bytes = DFI_Info.objects.filter(Date__gte=date(int(startTime[0]), int(startTime[1]), int(startTime[2])), Date__lte=date(int(endTime[0]), int(endTime[1]), int(endTime[2])), Dest_Mac=APmac).values('Protocol').annotate(sum_bytes=Sum('Bytes')).order_by('-smu_bytes')[0:10]
    except IndexError:
        Porto_Bytes = DFI_Info.objects.filter(Date__gte=date(int(startTime[0]), int(startTime[1]), int(startTime[2])), Date__lte=date(int(endTime[0]), int(endTime[1]), int(endTime[2])), Dest_Mac=APmac).values('Protocol').annotate(sum_bytes=Sum('Bytes')).order_by('-smu_bytes')
    APcount['STA_Bytes'] = STA_Bytes
    APcount['Server_Bytes'] = Server_Bytes
    APcount['Proto_Bytes'] = Porto_Bytes
    return APcount
