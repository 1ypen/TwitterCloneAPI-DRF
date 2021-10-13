from django.db.models import F
from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import LimitOffsetPagination

from .models import Comment
from .serializers import CommentSerializer


class CommentListApiView(ListCreateAPIView):
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        queryset = Comment.objects.filter(tweet=self.kwargs['pk']) \
            .select_related('user') \
            .values(
                'id', 'created_date', 'text', 'user_id',
                user_name=F('user__name'),
                user_login=F('user__login'),
                user_avatar=F('user__avatar')
            )
        return queryset
