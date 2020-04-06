from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('post/', include('post.urls', namespace='post')),
    path('', lambda r: redirect('post:post_list'), name='root')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)