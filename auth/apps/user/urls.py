from django.urls import path
from .views import ListAllUsersView, GetUserView, GetUserDetailView

urlpatterns = [
    path('list', ListAllUsersView.as_view()),
    path('get/<user_id>', GetUserView.as_view()),
    path('get_details/<user_id>', GetUserDetailView.as_view())
]