from django.urls import path
from events.views import home, EventDetails,organizer_dashboard, ParticipantDaashboard, CreateTaskAndCatagory, UpdateEventAndCatagory, AdminDashboard, assign_role, create_group, delete_group,access_denied, dashboard_redirect
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', home, name='home'),
    path('event/', home, name='home'),
    path('event/<int:event_id>/', EventDetails.as_view(), name='event_details'),
    path('dashboard/organizer/', organizer_dashboard, name='organizer_dashboard'),
    path('dashboard/participant/', ParticipantDaashboard.as_view(), name='participant_dashboard'),
    path('create/', CreateTaskAndCatagory.as_view(), name='create'),
    path('update/', UpdateEventAndCatagory.as_view(), name='update'),
    path('dashboard/', dashboard_redirect, name="dashboard_redirect"),
    path("dashboard/admin/create-group/", create_group, name="create-group"),
    path('dashboard/admin/<str:path>/', AdminDashboard.as_view(), name='admin_dashboard'),
    path("dashboard/admin/<int:user_id>/assign-role/", assign_role, name="assign_role"),
    path("dashboard/admin/<int:group_id>/delete-group/", delete_group, name="delete-group"),
    path("dashboard/access-denied/", access_denied, name="access_denied"),
]
