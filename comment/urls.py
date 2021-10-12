from django.urls import path

from . import views

urlpatterns = [
    path('tweet/<int:pk>/', views.CommentListApiView.as_view(), name='comment-list')
]