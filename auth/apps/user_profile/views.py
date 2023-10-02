from django.shortcuts import render, get_object_or_404
from rest_framework_api.views import StandardAPIView
from rest_framework import permissions
from .models import UserProfile
from .serializers import UserProfileSerializer
from rest_framework import status
from django.contrib.auth import get_user_model
import re

User = get_user_model()


# Create your views here.


class MyUserProfileView(StandardAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, ** kwargs):
        user = self.request.user
        profile = get_object_or_404(UserProfile, user=user)
        profile = UserProfileSerializer(profile).data
        return self.send_response({'profile': profile}, status=status.HTTP_200_OK)
    

class GetUserProfileView(StandardAPIView):
    def get(self, request, slug, *args, **kwargs):
        print(slug)
        return self.send_response('profile_data')
    



pattern_special_characters = r'\badmin\b|[!@#$%^&*()_+-=[]{}|;:",.<>/?]|\s'

class EditUsernameView(StandardAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        user = self.request.user
        data = self.request.data
        username = data['username']
        user_model = User.objects.get(id=user.id)

        if re.search(pattern_special_characters, username, re.IGNORECASE) is None:
            user_model.user_name = username
            user_model.slug = username
            user_model.save()
            return self.send_response('Success', status=status.HTTP_200_OK)
        else:
            return self.send_error('Error', status=status.HTTP_400_BAD_REQUEST)




