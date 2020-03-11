from django.urls import path
from .views import *

app_nampe = 'accounts'

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_check, name='login'),
]