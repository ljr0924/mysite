from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import LikeCount, LikeRecord

register = template.Library()


@register.simple_tag
def get_like_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    like_count, created = LikeCount.objects.get_or_create(content_type=content_type,
                                                          object_id=obj.id)
    print('like num: ', like_count.liked_num)
    return like_count.liked_num


@register.simple_tag(takes_context=True)
def get_like_status(context, obj):
    content_type = ContentType.objects.get_for_model(obj)
    user = context['user']
    # 如果没有登录，直接返回空字符串
    if not user.is_authenticated:
        return ''
    if LikeRecord.objects.filter(content_type=content_type,
                                 object_id=obj.pk,
                                 user=user
                                 ).exists():
        # 如果已点赞，返回active
        print(LikeRecord.objects.get(content_type=content_type,
                                 object_id=obj.pk,
                                 user=user
                                 ))
        return 'active'
    else:
        return ''


@register.simple_tag
def get_content_type(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return content_type.model