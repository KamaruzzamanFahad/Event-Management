from django.urls import path
from users.views import signup, signin, signout, activate, ProfileView, UpdateProfileView, ChangePasswordView, CustomPasswordResetView, CustomPasswordResetConfirmView
urlpatterns = [
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),
    path('activate/<int:user_id>/<str:token>/', activate, name='activate'),
    path('<str:username>/', ProfileView.as_view(), name='profile'),
    path('<str:username>/update/', UpdateProfileView.as_view(), name='update_profile'),
    path('<str:username>/change-password/', ChangePasswordView.as_view(), name='change_password'),
    
]   