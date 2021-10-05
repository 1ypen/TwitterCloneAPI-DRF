from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.core.exceptions import ObjectDoesNotExist

from .models import Relationship


class FollowOrUnfollow(APIView):

    def post(self, request):
        user_id = request.data.get('id')
        action = request.data.get('action')
        if user_id and action:
            try:
                relationship = Relationship.objects.get(user=request.user, following_id=user_id)
            except ObjectDoesNotExist:
                relationship = None
            
            if action == 'follow' and relationship is None:
                relationship = Relationship.objects.create(user=request.user, following_id=user_id)
            elif action == 'unfollow' and relationship is not None:
                relationship.delete()

            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)
