from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model


def post_list(request):
    if request.user.is_authenticated:
        username = request.user
        user = get_object_or_404(get_user_model(), username=username)
        user_profile = user.profile
        return render(request, 'post/post_list.html', {
            'user_profile': user_profile
        })
    else:
        return render(request, 'post/post_list.html')