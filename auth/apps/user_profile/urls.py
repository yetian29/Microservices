from django.urls import path
from .views import MyUserProfileView, EditUsernameView



urlpatterns = [
    path('my_profile', MyUserProfileView.as_view()),
    path('edit/username', EditUsernameView.as_view())
]