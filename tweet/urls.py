from django.urls import path

from . import views

urlpatterns = [
    path('list/', views.TweetListApiView.as_view(), name='tweet-list'),
    path('detail/<int:pk>/', views.TweetDetailApiView.as_view(), name='tweet-detail'),
    path('like/', views.TweetLikeApiView.as_view(), name='tweet-like-ajax')
]