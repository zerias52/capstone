from django.urls import path
from .views import *

urlpatterns = [
   path("login/", UserLoginView.as_view(), name="login"),
   path("logout/", user_logout, name='logout'),
   path('signup/', SignUpView.as_view(), name='signup'),
]