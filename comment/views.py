from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from .models import Comment


def update_comment(request):
    user = request.user
    text = request.POST.get('text', '')
    content_type = request.POST.get('content_type', '')
    object_id = int(request.POST.get('object_id', ''))
    # model_class()获得具体的模型对象
    model_class = ContentType.objects.get(model=content_type).model_class()
    model_obj = model_class.objects.get(pk=object_id)
    # 记录评论内容，保存到数据库
    comment = Comment()
    comment.user = user
    comment.text = text
    comment.content_object = model_obj
    print(comment)
    comment.save()
    # 重定向回原页面
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    return redirect(referer)

