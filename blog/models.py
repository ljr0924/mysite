from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class BlogType(models.Model):
    # 分类名字
    type_name = models.CharField(max_length=20)

    def __str__(self):
        return self.type_name


class Blog(models.Model):
    # 标题
    title = models.CharField(max_length=50)
    # 分类
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING, related_name='blog_type')
    # 内容
    content = RichTextUploadingField()
    # 作者
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    # 创建时间
    created_time = models.DateTimeField(auto_now_add=True)
    # 最后修改时间
    last_updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<Blog: {self.title}>"

    class Meta:
        ordering = ['-created_time']

