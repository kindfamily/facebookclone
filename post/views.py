from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model
from .models import *

from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required



def post_list(request):
    post_list = Post.objects.all()
    
    if request.user.is_authenticated:
        username = request.user
        user = get_object_or_404(get_user_model(), username=username)
        user_profile = user.profile
        return render(request, 'post/post_list.html', {
            'user_profile': user_profile,
            'posts': post_list,
        })
    else:
        return render(request, 'post/post_list.html', {
            'posts': post_list,
        })
    

@login_required
@require_POST
def post_like(request):
    pk = request.POST.get('pk', None)
    post = get_object_or_404(Post, pk=pk)
    post_like, post_like_created = post.like_set.get_or_create(user=request.user)
    
    if not post_like_created:
        post_like.delete()
        message = "좋아요 취소"
    else:
        message = "좋아요"
    
    context = {'like_count': post.like_count,
              'message': message}
    
    return HttpResponse(json.dumps(context), content_type="application/json")
    
@login_required
@require_POST
def post_bookmark(request):
    pk = request.POST.get('pk', None)
    post = get_object_or_404(Post, pk=pk)
    post_bookmark, post_bookmark_created = post.bookmark_set.get_or_create(user=request.user)
    
    if not post_bookmark_created:
        post_bookmark.delete()
        message = "북마크 취소"
        is_bookmarked = 'N'
    else:
        message = "북마크"
        is_bookmarked = 'Y'
    
    context = {'is_bookmarked': is_bookmarked,
              'message': message}
    
    return HttpResponse(json.dumps(context), content_type="application/json")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    