from django.db.models import Count, F, Case, When
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Tweets
from .serializers import TweetSerializer, TweetCreateSerializer
from .utils import merge_values


class TweetsListApiView(ListCreateAPIView):
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self):

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

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TweetSerializer
        elif self.request.method == 'POST':
            return TweetCreateSerializer


class TweetDetailApiView(RetrieveAPIView):
    serializer_class = TweetSerializer

    def get_queryset(self):

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
            ).filter(**self.kwargs)

        return merge_values(queryset)[0]

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        return queryset


class TweetLikeApiView(APIView):

    def post(self, request):
        tweet_id = request.data.get('id')
        action = request.data.get('action')

        tweet = Tweets.objects.get(id=tweet_id)

        if action == 'like':
            tweet.users_like.add(request.user.id)
        elif action == 'dislike':
            tweet.users_like.remove(request.user.id)

        return Response()
