from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpandMethod, ReadDetail


class Topic(models.Model):
    """主题,如python,linux,django,mysql等"""

    # 主题的名称
    name = models.CharField(max_length=200, verbose_name="主题名称")
    # 主题的时间戳
    date_add = models.DateTimeField('创建时间', auto_now_add=True)
    # 主题的拥有者
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="作者")
    # 主题简介
    abstract = models.TextField(max_length=200, help_text='简单概括一下这个主题', verbose_name="主题简介")

    def __str__(self):
        """返回模型的字符串表示"""
        return self.name

    class Meta:
        ordering = ['date_add']


class Category(models.Model):
    """某一篇文章的标签分类"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# 标签
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Entry(models.Model, ReadNumExpandMethod):
    """学到的有关某个主题的具体文章"""
    STATUS_CHOICE = (
        ('y', '原创'),
        ('z', '转载'),
    )

    # 文章所属主题
    topic = models.ForeignKey('Topic', on_delete=models.DO_NOTHING, verbose_name='博客分类')

    # 文章的标题
    title = models.CharField('标题', max_length=70)

    # 文章的内容
    text = RichTextUploadingField()

    # 文章的创建时间
    date_added = models.DateTimeField('创建时间', auto_now_add=True)

    # 最后修改时间
    last_update_time = models.DateTimeField(auto_now=True)

    # 浏览数
    # readnum = models.ForeignKey('ReadNum', on_delete=models.CASCADE)

    # 原创，转载
    category = models.CharField('文章分类', max_length=10, choices=STATUS_CHOICE, default='y')

    # 作者
    entry_owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="作者")

    read_details = GenericRelation(ReadDetail)

    # 点赞数
    # likes = models.PositiveIntegerField('views', default=0)

    # 摘要
    excerpt = models.CharField(max_length=54, blank=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        """返回模型的字符串表示"""
        return self.title

    # 重写保存的方法
    def save(self, *args, **kwargs):

        self.excerpt = self.text[:54]

        # 调用父类的保存方法保存到数据库中
        super(Entry, self).save(*args, **kwargs)





















