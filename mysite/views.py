from django.shortcuts import render_to_response
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import get_seven_days_read_data
from blog.models import Blog

def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    date_list, read_nums_list = get_seven_days_read_data(blog_content_type)

    print(read_nums_list)
    context = {}
    context['read_nums_list'] = read_nums_list
    context['date_list'] = date_list
    return render_to_response('home.html', context)