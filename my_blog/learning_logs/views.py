from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from django.db.models.aggregates import Count
from read_statistics.utils import read_statistics_once_read
from read_statistics.utils import get_seven_days_read_data, get_today_hot_date, get_yesterday_hot_date
from django.utils import timezone
import datetime
from django.db.models import Sum
from django.core.cache import cache

from .models import Topic, Entry
from .forms import TopicForms, EntryForm
from comment.models import Comment

from comment.forms import CommentForm


def get_seven_days_hot_data():
    """获取最近7天内的热门点击文章"""
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    entries = Entry.objects\
                   .filter(read_details__date__lt=today, read_details__date__gte=date)\
                   .values('id', 'title')\
                   .annotate(read_num_sum=Sum('read_details__read_num'))\
                   .order_by('-read_num_sum')
    return entries[:7]


def index(request):
    """学习笔记的主页"""
    entry_content_type = ContentType.objects.get_for_model(Entry)
    dates, read_nums = get_seven_days_read_data(content_type=entry_content_type)

    # 获取7天热门文章的缓存数据
    seven_days_hot_data = cache.get('seven_days_hot_data')
    if seven_days_hot_data is None:
        seven_days_hot_data = get_seven_days_hot_data()
        cache.set('seven_days_hot_data', seven_days_hot_data, 3600)

    context = {
        'read_nums': read_nums,
        'dates': dates,
        'today_hot_data': get_today_hot_date(entry_content_type),
        'yesterday_hot_data': get_yesterday_hot_date(entry_content_type),
        'seven_days_hot_data': seven_days_hot_data
    }

    return render(request, 'learning_logs/index.html', context)


def topics(request):
    """显示所有的主题"""
    topic_time = Topic.objects.dates('date_add', 'month', order='DESC')
    topics_all_list = Topic.objects.all()      # 取出所有主题
    paginator = Paginator(topics_all_list, 6)    # 每６个主题分为一页
    page_num = request.GET.get('page', 1)  # 获取url页码参数,GET请求
    page_of_topics = paginator.get_page(page_num)       # 如果取到非法字符，自动返回第一页，不用再取判断能否转化为整数

    context = {'all_topic': topics_all_list, 'topics': page_of_topics, 'topic_time': topic_time}

    return render(request, 'learning_logs/topics.html', context)


def topic(request, topic_id):
    """显示单个主题内的所有的文章,６篇一页"""
    topic = Topic.objects.get(id=topic_id)
    entry_time = topic.entry_set.dates('date_added', 'month', order='DESC')
    entry_num_dict = {}
    for entry_date in entry_time:
        entry_num = Entry.objects.filter(date_added__year=entry_date.year, date_added__month=entry_date.month).count()
        entry_num_dict[entry_date] = entry_num

    # if topic.owner != request.user:
    #     raise Http404

    entries = topic.entry_set.order_by('-date_added')
    paginator = Paginator(entries, 6)
    page_num = request.GET.get('page', 1)
    page_of_entries = paginator.get_page(page_num)

    context = {
        'entries': page_of_entries,
        'topic': topic,
        'entry_time': entry_num_dict
    }

    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    """添加新主题"""
    if request.method != 'POST':
        # 未提交数据，创建一个新表单
        form = TopicForms
    else:
        # POST提交的数据，对数据进行处理
        form = TopicForms(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """在特定的主题中添加新条目"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # 未提交数据，创建一个新表单
        form = EntryForm()
    else:
        # POST提交的数据，对数据进行处理
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))

    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """编辑既有笔记"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # 初次请求，使用当前笔记填充表单
        form = EntryForm(instance=entry)
    else:
        # POST提交的数据，对数据进行处理
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)


def display_entry(request, entry_id):
    """显示选中的笔记"""
    entry = get_object_or_404(Entry, id=entry_id)
    read_cookie_key = read_statistics_once_read(request, entry)
    entry_content_type = ContentType.objects.get_for_model(entry)
    comments = Comment.objects.filter(content_type=entry_content_type, object_id=entry.id, parent=None)

    topic_type = entry.topic
    pentry_of_topic = Entry.objects.filter(topic=topic_type, date_added__gt=entry.date_added).last()  # 前一篇
    nentry_of_topic = Entry.objects.filter(topic=topic_type, date_added__lt=entry.date_added).first()  # 下一篇博客

    context = {
        'entry': entry,
        'p': pentry_of_topic,
        'n': nentry_of_topic,
        'user': request.user,
        'comments': comments,
        'comment_form': CommentForm(initial={'content_type': entry_content_type.model,
                                             'object_id': entry_id, 'reply_comment_id': 0})
    }

    response = render(request, 'learning_logs/display_entry.html', context)   # 响应
    response.set_cookie(read_cookie_key, 'true', max_age=60)  # 阅读cookie标记

    return response


@login_required
def entry_with_date(request, year, month):
    """按时间年月分类统计"""
    entry_all_list = Entry.objects.filter(date_added__year=year, date_added__month=month)   # 按年月取出对应的文章
    paginator = Paginator(entry_all_list, 6)
    page_num = request.GET.get('page', 1)
    page_of_entries = paginator.get_page(page_num)

    context = {
        'entries': page_of_entries,
        'entry_all_list': entry_all_list,
        'entry_time': '%s年%s月' % (year, month)
    }

    return render(request, 'learning_logs/entry_with_date.html', context)












