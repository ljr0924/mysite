from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from .models import Comment
from .forms import CommentForm


def update_comment(request):
    # 重定向回原页面
    # referer = request.META.get('HTTP_REFERER', reverse('home'))
    data = {}
    comment_form = CommentForm(request.POST, user=request.user)
    if comment_form.is_valid():  # 判断表单有效性
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']

        parent = comment_form.cleaned_data['parent']
        if not parent is None:
            comment.root = parent.root if not parent.root is None else parent
            comment.parent = parent
            comment.reply_to = parent.user

        comment.save()
        # return redirect(referer)
        data['status'] = "success"
        data['username'] = comment.user.username
        data['comment_time'] = comment.comment_time.strftime('%Y-%m-%d %H:%M:%S')
        data['text'] = comment.text
        if not parent is None:
            data['reply_to'] = comment.reply_to.username
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if not comment.root is None else ''
    else:
        # return render(request, 'error.html', {'message': comment_form.errors, 'redirect_to': referer})
        data['status'] = "error"
        data['message'] = list(comment_form.errors.values())[0][0]
    return JsonResponse(data)