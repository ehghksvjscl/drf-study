from django.shortcuts import render
from app.models import Post

def echo_page(request):
    return render(request, 'app/echo_page.html')

def liveblog_index(request):
    return render(request, 'app/liveblog_index.html', {
        "post_list": Post.objects.all()
    })

def post_partial(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'app/partial/post.html', {
        "post": post
    })