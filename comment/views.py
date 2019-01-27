from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from .models import Comment
from .forms import CommentForm


def update_comment(request):
    # 重定向回原页面
    referer = request.META.get('HTTP_REFERER', reverse('home'))

    comment_form = CommentForm(request.POST, user=request.user)
    if comment_form.is_valid():  # 判断表单有效性
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']
        comment.save()
        return redirect(referer)
    else:
        return render(request, 'error.html', {'message': comment_form.errors, 'redirect_to': referer})
