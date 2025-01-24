from django.urls import path
from . import views

app_name = 'generator'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post-list'),
    path('new/', views.PostCreateView.as_view(), name='post-create'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    path('<int:pk>/clone/', views.PostCloneView.as_view(), name='post-clone'),
]