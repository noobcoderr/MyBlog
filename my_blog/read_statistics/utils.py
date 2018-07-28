import datetime
from django.db.models import Sum
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from .models import ReadNum, ReadDetail


def read_statistics_once_read(request, obj):
    # 阅读统计，可优化封装
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model, obj.id)

    if not request.COOKIES.get(key):
        # 总阅读数 + 1
        readnum,  created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.id)
        readnum.read_num += 1
        readnum.save()

        # 当天阅读数 + 1
        date = timezone.now().date()
        read_detail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.id, date=date)
        read_detail.read_num += 1
        read_detail.save()

    return key


def get_seven_days_read_data(content_type):
    today = timezone.now().date()
    read_nums = []
    dates = []
    for i in range(7, 0, -1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
        result = read_details.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)

    return dates, read_nums


def get_today_hot_date(content_type):
    today = timezone.now().date()
    read_detailes = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')
    return read_detailes[:7]


def get_yesterday_hot_date(content_type):
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    read_detailes = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num')
    return read_detailes[:7]
