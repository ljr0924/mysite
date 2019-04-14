import datetime
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum
from django.core.cache import cache
from django.contrib.contenttypes.models import ContentType

from blog.models import Blog
from read_statistics.utils import get_seven_days_read_data, get_today_and_yesterday_hot_blog


def get_7_day_hot_blog():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    read_details = Blog.objects.filter(read_details__date__lt=today,
                                       read_details__date__gte=date) \
        .values('id', 'title') \
        .annotate(read_num_sum=Sum('read_details__read_num')) \
        .order_by('-read_num_sum')
    return read_details[:7]


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    # 获取近七天日期列表，近七天的日总阅读数量
    date_list, read_nums_list = get_seven_days_read_data(blog_content_type)
    # 获取今天和昨天的热门博客及其阅读量
    today, yesterday = get_today_and_yesterday_hot_blog(blog_content_type)
    # 缓存的方式获取近七天的热门博客及其近七天总阅读量
    weekly_hot_blog = cache.get('weekly_hot_blog')
    if weekly_hot_blog is None:
        weekly_hot_blog = get_7_day_hot_blog()
        cache.set('weekly_hot_blog', weekly_hot_blog, 3600)

    # 页面渲染数据
    context = {}
    context['date_list'] = date_list
    context['read_nums_list'] = read_nums_list
    context['today_hot_blog'] = today
    context['yesterday_hot_blog'] = yesterday
    context['weekly_hot_blog'] = weekly_hot_blog
    return render(request, 'home.html', context)


