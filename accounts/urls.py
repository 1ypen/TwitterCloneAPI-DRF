from django.urls import path

from . import views

urlpatterns = [
    path('follow/', views.FollowOrUnfollow.as_view(), name='user-follow')
]