from django.urls import path

from authapp.views import RegisterView, LogoutView, LoginView, EditProfileView, UserView

# UserView
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/<int:user_id>', UserView.as_view(), name='user'),
    path('edit_profile/', EditProfileView.as_view(), name='edit_profile'),
]
