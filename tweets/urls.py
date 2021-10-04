from django.urls import path

from . import views

urlpatterns = [
    path('list/', views.TweetListApiView.as_view()),
    path('detail/<int:pk>/', views.TweetDetailApiView.as_view()),
    path('like/', views.TweetLikeApiView.as_view())
]