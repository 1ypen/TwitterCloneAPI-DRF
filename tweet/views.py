from django.db.models import Count, F, Case, When, QuerySet, Subquery, OuterRef, Prefetch
from django.http import Http404
from rest_framework import status, renderers
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView, Response

from .models import Tweet, TweetImage
from .serializers import TweetSerializer, TweetCreateSerializer
from .utils import merge_values, get_object_or_none


class TweetListApiView(ListCreateAPIView):
    """
    a function for getting all tweets
    with the possibility of pagination
    """

    pagination_class = LimitOffsetPagination

    def get_queryset(self):

        # i get a list of IDs of tweets that the user liked
        # user_likes_id = self.request.user.tweets_liked.values_list('id', flat=True)
        user_likes_id = []
        # i make a query to the database to get responses
        # with additional fields that are not in the tweet model,
        # use the select_related, prefetch_related and values methods to optimize the query
        queryset = Tweet.objects \
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
            ).order_by('-id')

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = merge_values(self.filter_queryset(self.get_queryset()))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TweetSerializer
        elif self.request.method == 'POST':
            return TweetCreateSerializer


class TweetDetailApiView(RetrieveAPIView):
    serializer_class = TweetSerializer

    def get_queryset(self):
        queryset = Tweet.objects \
            .select_related('user') \
            .prefetch_related('users_like') \
            .prefetch_related('images'). \
            values(
                'id', 'created_date', 'text',
                like_count=Count('users_like'),
                img=F('images__img'),
                is_liked=Case(When(id__in=[], then=True), default=False),
                user_name=F('user__name'),
                user_login=F('user__login'),
                user_avatar=F('user__avatar')
            )

        return queryset

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset().filter(**self.kwargs))

        obj = merge_values(queryset)
        if not obj:
            raise Http404
        return obj


class TweetLikeApiView(APIView):
    """
    implementation of adding like or removing like to a tweet
    """

    def post(self, request):
        tweet_id = request.data.get('id')
        action = request.data.get('action')

        tweet = get_object_or_none(Tweet, id=tweet_id)
        if tweet:
            if action == 'like':
                tweet.users_like.add(request.user.id)
            elif action == 'dislike':
                tweet.users_like.remove(request.user.id)
            return Response()
        return Response(status=status.HTTP_404_NOT_FOUND)
