from django.shortcuts import get_object_or_404, render
# 分页器
from django.core.paginator import Paginator
from .models import Blog, BlogType
from django.conf import settings
from django.db.models import Count

# Create your views here.
def blog_list(request):
    blogs = Blog.objects.all()
    context = get_common_data(request, blogs)
    return render(request, 'blog/blog_list.html', context)


def blog_detail(request, blog_pk):  # pk -> 主键
    context = {}
    blog = get_object_or_404(Blog, pk=blog_pk)
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['blog'] = blog
    return render(request, 'blog/blog_detail.html', context)


def blogs_with_type(request, blog_type_pk):
    # get_page 可以进行容错处理
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    # 通过分类获取博客
    blogs = Blog.objects.filter(blog_type=blog_type)
    context = get_common_data(request, blogs)
    context['blog_type'] = blog_type                    # 博客分类
    return render(request, 'blog/blogs_with_type.html', context)


def blogs_with_date(request, year, month, day):

    blogs = Blog.objects.filter(created_time__year=year, created_time__day=day)
    context = get_common_data(request, blogs)
    # get_page 可以进行容错处理
    context['blogs_with_date'] = f'{ year }年{ month }月'
    return render(request, 'blog/blog_with_date.html', context)


def get_common_data(request, blogs):
    paginator = Paginator(blogs, settings.EACH_PAGE_NUM)
    page_num = request.GET.get('page', 1)
    page_of_blogs = paginator.get_page(page_num)
    # 当前页码
    current_page_num = page_of_blogs.number
    page_list = list(range(max(current_page_num - 2, 1), min(current_page_num + 2, paginator.num_pages) + 1))
    # 加上省略号代码
    if page_list[0] - 1 >= 2:
        page_list.insert(0, "...")
    if paginator.num_pages - page_list[-1] >= 2:
        page_list.append("...")
    # 加上首页尾页
    if page_list[0] != 1:
        page_list.insert(0, 1)
    if page_list[-1] != paginator.num_pages:
        page_list.append(paginator.num_pages)

    blog_dates = Blog.objects.dates('created_time', 'day', order='DESC')
    date_count_dict = {}
    for date in blog_dates:
        date_count = Blog.objects.filter(created_time__year=date.year,
                                         created_time__month=date.month,
                                         created_time__day=date.day).count()
        date_count_dict[date] = date_count

    context = {}
    # get_page 可以进行容错处理
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    # BlogType.objects.annotate(blog_count = Count('blog_type')) 为获取到的每一条数据加上一个注解
    # 相当于加上一个字段
    context['blog_types'] = BlogType.objects.annotate(blog_count = Count('blog_type'))
    context['blog_dates'] = date_count_dict # Blog.objects.dates('created_time', 'day', order='DESC')
    context['page_list'] = page_list
    return context