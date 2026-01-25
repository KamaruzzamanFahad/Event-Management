from django.urls import path
from events.views import event_details, home, dashboard, create, update

urlpatterns = [
    path('', home, name='home'),
    path('event/', home, name='home'),
    path('event/<int:event_id>/', event_details, name='event_details'),
    path('dashboard/', dashboard, name='dashboard'),
    path('create/', create, name='create'),
    path('update/', update, name='update'),

]
