from django.shortcuts import render, get_object_or_404
import json, uuid
from rest_framework_api.views import StandardAPIView
from rest_framework import permissions
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from apps.user_profile.serializers import UserProfileSerializer
from django.core.cache import cache
from rest_framework import serializers
from apps.user_profile.models import UserProfile



User = get_user_model()

# Create your views here.

# Khi bạn cần chuyển đổi một đối tượng UUID thành một chuỗi để lưu trữ hoặc truyền qua mạng, bạn cần một cách để mã hóa UUID thành một kiểu dữ liệu có thể được lưu trữ hoặc truyền qua các giao thức truyền tải dữ liệu như JSON
class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            # Nếu đối tượng là UUID, chuyển thành chuỗi và trả về
            return str(obj)
        return json.JSONEncoder.default(self, obj)  # để xử lý các trường hợp khác một cách mặc định.
    
class ListAllUsersView(StandardAPIView):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        users = UserSerializer(users, many=True)
        if users.data is not None:
            return self.paginate_response(request, json.dumps(users.data, cls=UUIDEncoder)) # json.dumps()để chuyển đổi một đối tượng Python thành chuỗi JSON. 
        else:
            pass

#Sử Dụng Cache: Việc sử dụng cache là một kỹ thuật tuyệt vời để tối ưu hóa hiệu suất. Bằng cách lưu trữ dữ liệu đã truy vấn từ cơ sở dữ liệu, bạn giảm thiểu việc truy cập cơ sở dữ liệu liên tục, giúp giảm tải cho hệ thống và cải thiện đáng kể hiệu suất.
class GetUserView(StandardAPIView):
    def get(self, request, user_id, *args, **kwargs):
        cache_key = f'user_{user_id}'
        user_data = cache.get_or_set(cache_key, lambda:self.get_user_data(user_id), 60*15)
        return self.send_response(user_data)
    
    def get_user_data(self, user_id):
        user = get_object_or_404(User, id=user_id)
        user_data = UserSerializer(user).data
        return user_data
       


class GetUserDetailView(StandardAPIView):
    def get(self, request, user_id, *args, **kwargs):
        user = User.objects.prefetch_related('profile', 'wallet').get(id-user_id)
        serializer = UserProfileSerializer(user.profile)
        return self.send_response(serializer.data)


class GetUserProfileSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(source='user.id')
    email = serializers.EmailField(source='user.email')
    username = serializers.CharField(source='user.username') 
    slug = serializers.SlugField(source='user.slug')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    is_online = serializers.BooleanField(source='user.is_online')
    verified = serializers.BooleanField(source='user.verified')
    avatar = serializers.ImageField(source='user.profile.avatar')

    class Meta:
        model = UserProfile 
        fields = (
            'id',
            'email',
            'username',
            'slug',
            'first_name',
            'last_name',
            'is_online',
            'verified',
            'avatar',
        )




