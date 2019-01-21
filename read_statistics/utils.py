import datetime
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from .models import ReadNum, ReadDetail
from django.utils import timezone


def read_statistics_once_read(request, obj):
    content_type = ContentType.objects.get_for_model(obj)
    key = f'{content_type.model}_{obj.pk}_isRead'
    if not request.COOKIES.get(key):
        # 总阅读数 +1
        read_num, created = ReadNum.objects.get_or_create(content_type=content_type, object_id=obj.pk)
        read_num.read_num += 1
        read_num.save()

        # 当天日期阅读数 +1
        date = timezone.now().date()
        read_detail, created = ReadDetail.objects.get_or_create(content_type=content_type, object_id=obj.pk, date=date)
        read_detail.read_num += 1
        read_detail.save()
    return key


def get_seven_days_read_data(content_type):
    today = timezone.now().date()
    date_list = []
    read_nums_list = []
    for i in range(7, 0, -1):
        delta = datetime.timedelta(days=i)
        date = today - delta
        date_list.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
        result = read_details.aggregate(read_num_sum=Sum('read_num'))
        read_nums_list.append(result['read_num_sum'] or 0) # 前面如果为False,取默认值0
    return date_list, read_nums_list