from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import get_user_model
from .models import *
from .forms import *

from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
import json
from django.contrib import messages
from django.db.models import Count 
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



def post_list(request, tag=None):
    tag_all = Tag.objects.annotate(num_post=Count('post')).order_by('-num_post')
    
    if tag:
        post_list = Post.objects.filter(tag_set__name__iexact=tag)
    else:
        post_list = Post.objects.all()
    
    if request.method == 'POST':
        tag = request.POST.get('tag')
        tag_clean = ''.join(e for e in tag if e.isalnum())
        return redirect('post:post_search', tag_clean)
    
    comment_form = CommentForm()
    
    paginator = Paginator(post_list, 3)
    page_num = request.POST.get('page')
    
    try:
        posts = paginator.page(page_num)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    if request.is_ajax():
        return render(reqeust, 'post/post_list_ajax.html', {
            'posts': posts,
            'comment_form': comment_form,
        })
    
    if request.user.is_authenticated:
        username = request.user
        
        friends = username.friends.all()
        request_friends = username.friend_requests
        
        user = get_object_or_404(get_user_model(), username=username)
        user_profile = user.profile
        
        friend_list = user.friends.all()
        my_friend_user_list = list(map(lambda friend: friend.user, friend_list))
        
        friend_request_list = user.friend_requests.all()
        
        my_friend_request_user_list = list(map(lambda friend_request: friend_request.to_user, friend_request_list))
        
        
        return render(request, 'post/post_list.html', {
            'tag': tag,
            'tag_all': tag_all,
            'user_profile': user_profile,
            'posts': post_list,
            'comment_form': comment_form,
            'friends': friends,
            'request_friends': request_friends,
            'my_friend_user_list': my_friend_user_list,
            'my_friend_request_user_list': my_friend_request_user_list,
        })
    else:
        return render(request, 'post/post_list.html', {
            'tag': tag,
            'tag_all': tag_all,
            'posts': post_list,
            'comment_form': comment_form,
        })



@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            post.tag_save()
            messages.info(request, '새 글이 등록되었습니다')
            return redirect('post:post_list')
    else:
        form = PostForm()
    return render(request, 'post/post_new.html', {
        'form': form,
    })
    

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.warning(request, '잘못된 접근입니다')
        return redirect('post:post_list')
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            post.tag_set.clear()
            post.tag_save()
            messages.success(request, '수정완료')
            return redirect('post:post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'post/post_edit.html', {
        'post': post,
        'form': form,
    })

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user or request.method == 'GET':
        messages.warning(request, '잘못된 접근입니다')
        return redirect('post:post_list')
    
    if request.method == 'POST':
        post.delete()
        return redirect('post:post_list')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
@login_required
def comment_new(request):
    pk = request.POST.get('pk')
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return render(request, 'post/comment_new_ajax.html', {
                'comment': comment,
            })
    return redirect('post:post_list')


@login_required
def comment_delete(request):
    pk = request.POST.get('pk')
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST' and request.user == comment.author:
        comment.delete()
        message = '삭제완료'
        status = 1
    else:
        message = '잘못된 접근입니다'
        status = 0
    
    return HttpResponse(json.dumps({'message': message, 'status': status}), content_type="application/json")


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    