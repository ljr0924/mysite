from django.contrib.contenttypes.models import ContentType
from .models import ReadNum


def read_statistics_once_read(request, obj):
    content_type = ContentType.objects.get_for_model(obj)
    key = f'{content_type.model}_{obj.pk}_isRead'
    if not request.COOKIES.get(key):
        if ReadNum.objects.filter(content_type=content_type, object_id=obj.pk).count():
            # 存在记录，加1
            read_num = ReadNum.objects.get(content_type=content_type, object_id=obj.pk)
        else:
            # 不存在记录，初始化记录
            read_num = ReadNum(content_type=content_type, object_id=obj.pk)
        read_num.read_num += 1
        read_num.save()
    return key