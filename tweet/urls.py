from django.urls import path

from . import views

urlpatterns = [
    path('list/', views.TweetListApiView.as_view(), name='tweet-list'),
    path('bookmarks/', views.Bookmarks.as_view(), name='bookmarks'),
    path('detail/<int:pk>/', views.TweetDetailApiView.as_view(), name='tweet-detail'),
    path('like/', views.TweetLikeApiView.as_view(), name='tweet-like-ajax'),
    path('delete/', views.TweetDeleteApiView.as_view(), name='tweet-delete-ajax'),
]