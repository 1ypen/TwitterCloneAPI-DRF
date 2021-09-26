from django.db.models import Count, F
from rest_framework.generics import ListAPIView

from .models import Tweets
from .serializers import TweetsListSerializer


class TweetsListApiView(ListAPIView):
    queryset = Tweets.objects.all()\
        .select_related('user')\
        .prefetch_related('users_like').\
        values(
            'id', 'created_date', 'text',
            like_count=Count('users_like'),
            user_name=F('user__name'),
            user_login=F('user__login'),
            user_avatar=F('user__avatar')
    )
    serializer_class = TweetsListSerializer

# class TweetsListApiView(ListAPIView):
#     queryset = Tweets.objects.all()
#     serializer_class = TweetsListSerializer
