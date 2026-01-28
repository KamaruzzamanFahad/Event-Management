from django.urls import path
from users.views import signup, signin, signout, activate
urlpatterns = [

    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),
    path('activate/<int:user_id>/<str:token>/', activate, name='activate'),
]   