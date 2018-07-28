from django.contrib import admin
from learning_logs.models import Topic, Entry

# 定制后台的显示


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date_add', 'owner',)
    ordering = ('-date_add',)


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('topic', 'id', 'get_read_num', 'title', 'date_added',)
    ordering = ('-date_added',)
    list_filter = ['date_added', 'topic']
    search_fields = ['title']

#
