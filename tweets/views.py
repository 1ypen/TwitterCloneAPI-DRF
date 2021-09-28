from django.db.models import Count, F, Case, When
from rest_framework.generics import ListCreateAPIView

from .models import Tweets, TweetImage
from .serializers import TweetsListSerializer
from .utils import merge_values


class TweetsListApiView(ListCreateAPIView):

    def get_queryset(self):
        user_likes_id = []
        if self.request.user.is_authenticated:
            user_likes_id = self.request.user.tweets_liked.values_list('id', flat=True)

        queryset = Tweets.objects \
            .select_related('user') \
            .prefetch_related('users_like') \
            .prefetch_related('images') \
            .values(
                'id', 'created_date', 'text',
                like_count=Count('users_like'),
                img=F('images__img'),
                is_liked=Case(When(id__in=user_likes_id, then=True), default=False),
                user_name=F('user__name'),
                user_login=F('user__login'),
                user_avatar=F('user__avatar')
            )

        return merge_values(queryset)

    serializer_class = TweetsListSerializer
