from django.shortcuts import render,reverse,redirect
from django.contrib.auth.decorators import login_required
from .models import Comment
from .forms import CommentForm


@login_required
def update_comment(request):
    referer = request.META.get('HTTP_REFERER', 'learning_logs/index.html')
    comment_form = CommentForm(request.POST, user=request.user)
    if comment_form.is_valid():
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']
        parent = comment_form.cleaned_data["parent"]
        if not parent is None:
            comment.root = parent.root if not parent.root is None else parent
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()

        # 返回数据
        data = {
            'status': 'SUCCESS',
            'username': comment.user.username,
            'comment_time': comment.comment_time.strftime('%Y-%m-%d %H:%M-%S'),
            'text': comment.text,
        }
        if not parent is None:
            data["reply_to"] = comment.reply_to.username
        else:
            data["reply_to"] = ''
        data["pk"] = comment.pk
        return redirect(referer)
    else:
        return render(request, 'learning_logs/error.html', {'message': comment_form.errors, 'redirect_to': referer})

