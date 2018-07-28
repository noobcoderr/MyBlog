"""定义　learning_logs的url模式"""

from django.urls import path
from . import views

app_name = 'learning_logs'

urlpatterns = [

    # 主页
    path('', views.index, name='index'),

    # 所有主题页面
    path('topics/', views.topics, name='topics'),

    # 显示特定主题的页面
    path('topics/<int:topic_id>/', views.topic, name='topic'),

    # 用于添加新主题的网页
    path('new_topic/', views.new_topic, name='new_topic'),

    # 用于添加新条目的网页,每个条目与特定的主题相关联
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),

    # 用于编辑条目的页面
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),

    # 用一个单独的页面显示选中的文章
    path('display_entry/<int:entry_id>/', views.display_entry, name='display_entry'),

    # 按年月分类
    path('entry_with_date/<int:year>/<int:month>/', views.entry_with_date, name='entry_with_date'),

]