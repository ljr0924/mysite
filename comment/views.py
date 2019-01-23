from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from .models import Comment


def update_comment(request):
    text = request.POST.get('text', '')
    # 重定向回原页面
    referer = request.META.get('HTTP_REFERER', reverse('home'))

    # 判断用户是否登录
    if not request.user.is_authenticated:
        return render(request, 'error.html', {'message': '用户没有登录', 'redirect_to': referer})

    # 判断评论是否为空
    if text == '':
        return render(request, 'error.html', {'message': '评论内容为空', 'redirect_to': referer})
    try:
        content_type = request.POST.get('content_type', '')
        object_id = int(request.POST.get('object_id', ''))
        # model_class()获得具体的模型对象
        model_class = ContentType.objects.get(model=content_type).model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except Exception as e:
        return render(request, 'error.html', {'message': '评论对象不存在', 'redirect_to': referer})

    # 记录评论内容，保存到数据库
    comment = Comment()
    comment.user = request.user
    comment.text = text
    comment.content_object = model_obj
    comment.save()
    return redirect(referer)
