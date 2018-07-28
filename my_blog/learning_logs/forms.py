"""第一个表单"""

from django import forms
from .models import Topic, Entry
from ckeditor.widgets import CKEditorWidget


class TopicForms(forms.ModelForm):
    """添加新主题的表单"""
    class Meta:
        model = Topic
        fields = ['name', 'abstract']
        labels = {'name': ''}


class EntryForm(forms.ModelForm):
    """添加新条目的表单"""
    class Meta:
        model = Entry
        fields = ['title', 'category', 'text', 'entry_owner']
        labels = {'text': ''}
        widgets = {
            'text': CKEditorWidget(config_name='comment_ckeditor')
        }

# class EntryForm(forms.Form):
#     title = forms.CharField()
#     category = forms.CharField()
#     text = forms.CharField(widget=CKEditorWidget(config_name='comment_ckeditor'),
#                            error_messages={"required": "评论内容不能为空"})



