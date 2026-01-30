from datetime import date
from django.http import HttpResponse
from django.shortcuts import redirect, render
from events.models import Event, Category, RSVP
from django.db.models import Q, Count
from django.contrib.auth.models import Group
from events.forms import AssignRoleForm,CreateGroupForm
from events.forms import CreateCategory, CreateEvent
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import DetailView, CreateView, UpdateView, ListView, TemplateView
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
User = get_user_model()





class GroupRequiredMixin(UserPassesTestMixin):
    group_required = None
    login_url = '/users/signin/'
    def test_func(self):
        user = self.request.user
        if user.is_authenticated:
            if self.group_required is None:
                return True
            if isinstance(self.group_required, str):
                groups = [self.group_required]
            else:
                groups = self.group_required
            return user.groups.filter(name__in=groups).exists() or user.is_superuser
        return False
    
    def handle_no_permission(self):
        return redirect(self.login_url)

def check_privilege(user, group_name):
    return user.groups.filter(name=group_name).exists()

def send_rsvp_email(user, event):
    subject = "RSVP to Event"
    message =  f"Hi {user.username} You have benn successfully RSVPed to this event {event.name}"
    recipient_list =[user.email]

    try:
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
    except Exception as e:
        print(f"Faild to send email to: {user.email} : {str(e)}")
    
# Create your views here.
def home(request):
    rsvp = request.GET.get('rsvp')
    if rsvp:
        if request.user.is_authenticated:
            event = Event.objects.get(event_id=rsvp)
            if event.participants.filter(id=request.user.id).exists():
                messages.error(request, "You have already RSVPed to this event!")
                return redirect('/')
            event.participants.add(request.user)
            send_rsvp_email(request.user, event)
            messages.success(request, "RSVPed successfully!")
            return redirect('/')    
        else:
            messages.error(request, "You need to login to RSVP!")
            return redirect('/users/signin/')
    keword = request.GET.get('keyword')
    date = request.GET.get('date') 

    events=[]
    mainquery = Event.objects.prefetch_related('participants').select_related('category')

    if date and keword:
         events = mainquery.filter(
            Q(name__icontains=keword) |
            Q(location__icontains=keword) |
            Q(description__icontains=keword),
            date__exact=date
        )

    elif keword:
        events = mainquery.filter(
            Q(name__icontains=keword) |
            Q(location__icontains=keword) |
            Q(description__icontains=keword)
        )
    elif date:
        events = mainquery.filter(date__exact=date)
    else:
        events = mainquery.all()

    return render(request, 'home.html', {'events': events})

    
# def event_details(request, event_id):
#     event = Event.objects.prefetch_related('participants').select_related('category').get(event_id=event_id)
#     return render(request, 'eventDetails.html', {'event': event})

class EventDetails(LoginRequiredMixin,DetailView):
    login_url = '/users/signin/'
    model = Event
    template_name = 'eventDetails.html'
    context_object_name = 'event'
    pk_url_kwarg = 'event_id'
    queryset = Event.objects.prefetch_related('participants').select_related('category')


@user_passes_test(lambda user: check_privilege(user, 'Organizer') or check_privilege(user, 'Admin'), login_url='/users/signin/')
def organizer_dashboard(request):

    participant_id = request.GET.get('participant_id')
    event_id = request.GET.get('event_id')
    if participant_id and event_id:
        try:
            participant = RSVP.objects.get(user_id=participant_id, event_id=event_id)
            participant.delete()
            messages.success(request, "Participant deleted successfully!")
        except RSVP.DoesNotExist:
            messages.error(request, "Participant not found for this event!")

    rsvp = request.GET.get('rsvp')
    if rsvp:
        if request.user.is_authenticated:
            event = Event.objects.get(event_id=rsvp)
            if event.participants.filter(id=request.user.id).exists():
                messages.error(request, "You have already RSVPed to this event!")
                return redirect('/dashboard/organizer/')
            event.participants.add(request.user)
            send_rsvp_email(request.user, event)
            messages.success(request, "RSVPed successfully!")
            return redirect('/dashboard/organizer/')    
        else:
            messages.error(request, "You need to login to RSVP!")
            return redirect('/users/signin/')

    mainquery = Event.objects.prefetch_related('participants').select_related('category')
    deleteid = request.GET.get('deleteid')
    if deleteid:
            event_to_delete = mainquery.get(event_id=deleteid)
            event_to_delete.delete()
            messages.success(request, "Event deleted successfully!")
        
    
    # participant_id = request.GET.get('participant_id')
    # if participant_id:
    #         participant_to_delete = Participant.objects.get(participant_id=participant_id)
    #         participant_to_delete.delete()
    #         return redirect('/dashboard/?event=all_Participant')

    catagory_id = request.GET.get('catagoryid')
    if catagory_id:
            catagory_to_delete = Category.objects.get(id=catagory_id)
            catagory_to_delete.delete()
            return redirect('/dashboard/?event=all_category')
        

    # total_events = mainquery.count()
    total_categories = Category.objects.count()
    # total_participants = Event.objects.aggregate(total_participants=Count('participants'))['total_participants']
    # upcoming_events = mainquery.filter(date__gt=date.today()).count()
    # past_events = mainquery.filter(date__lt=date.today()).count()

    count = mainquery.aggregate(
        total_events=Count('event_id'),
        past_events=Count('event_id', filter=Q(date__lt=date.today())),
        upcoming_events=Count('event_id', filter=Q(date__gt=date.today())),
        total_participants=Count('participants')
    )

    context = {
        'events': [],
        'is_category': False,
        'is_participant': False,
        'total_events': count['total_events'],
        'total_categories': total_categories,
        'total_participants': count['total_participants'],
        'upcoming_events': count['upcoming_events'],
        'past_events': count['past_events'],
        'is_admin': check_privilege(request.user, 'Admin')
    }
    event = request.GET.get('event')
    if event == 'total_events':
        events = mainquery.all()
        context['events'] = events
    elif event == 'upcoming_events':
        events = mainquery.filter(date__gt=date.today())
        context['events'] = events
    elif event == 'past_events':
        events = mainquery.filter(date__lt=date.today())
        context['events'] = events
    elif event == 'all_category':
        context['events'] = Category.objects.all()
        context['is_category'] = True
    elif event == 'all_Participant':
        participants = RSVP.objects.select_related('event', 'user').values(
            'user__username',
            'user__email',
            'user__id',
            'event__event_id',
            'event__name',
        )
        context['events'] = participants
        context['is_participant'] = True
    else:
        context['events'] = mainquery.all()

    return render(request, 'dashboard.html', context)

# @user_passes_test(lambda user: check_privilege(user, 'Organizer') or check_privilege(user, 'Admin'), login_url='/users/signin/')
# def create(request):
#     create = request.GET.get('create')
    
#     if create == 'category':
#         if request.method == 'POST':
#             form = CreateCategory(request.POST)
#             if form.is_valid():
#                 form.save()
#                 return render(request, 'create.html', {'form': CreateCategory(), 'message': "Category created successfully!"})
#             else:
#                 return render(request, 'create.html', {'form': form})
#         form = CreateCategory()
#         return render(request, 'create.html', {'form': form})
#     elif create == 'event':
#         if request.method == 'POST':
#             form = CreateEvent(request.POST, request.FILES)
#             if form.is_valid():
#                 form.save()
#                 return render(request, 'create.html', {'form': CreateEvent(), 'message': "Event created successfully!"})
#             else:
#                 return render(request, 'create.html', {'form': form})
#         form = CreateEvent()
#         return render(request, 'create.html', {'form': form})
#     # elif create == 'participant':
#     #     if request.method == 'POST':
#     #         form = CreateParticipant(request.POST)
#     #         if form.is_valid():
#     #             form.save()
#     #             return render(request, 'create.html', {'form': CreateParticipant(), 'message': "Participant created successfully!"})
#     #         else:
#     #             return render(request, 'create.html', {'form': form})   
#     #     form = CreateParticipant()
#     #     return render(request, 'create.html', {'form': form})
    
#     else:
#         return render(request, 'create.html', {'form': None})




class CreateTaskAndCatagory(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    permission_required = ['events.add_event', 'events.add_category']
    template_name = 'create.html'
    login_url = '/users/signin/'

    def get_form_class(self):
        create = self.request.GET.get('create')
        if create == 'category':
            self.success_url = '/dashboard/organizer/?event=all_category'
            return CreateCategory
        elif create == 'event':
            self.success_url = '/dashboard/organizer/?event=total_events'
            return CreateEvent
        else:
            self.success_url = '/dashboard/organizer/?event=all_category'
            return CreateCategory

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == 'POST':
            kwargs.update({'files': self.request.FILES})
        return kwargs

    def form_valid(self, form):
        create = self.request.GET.get('create')
        form.save()
        messages.success(self.request, 'created successfully!')
        return HttpResponseRedirect(self.success_url)
    
    def form_invalid(self, form):
        return render(self.request, self.template_name,{
            form: self.get_form_class(),
        })





# @user_passes_test(lambda user: check_privilege(user, 'Organizer') or check_privilege(user, 'Admin'), login_url='/users/signin/')
# def update(request):
#     editid = request.GET.get('editid')
#     catagoryid = request.GET.get('catagoryid')
#     if editid:
#         event = Event.objects.get(event_id=editid)
#         eventfrom  =  CreateEvent(instance=event)
#         if request.method == 'POST':
#             form = CreateEvent(request.POST, request.FILES, instance=event)
#             if form.is_valid():
#                 form.save()
#                 return render(request, 'create.html', {'form': CreateEvent(), 'message': "Event updated successfully!", 'update': True})
#             else:
#                 return render(request, 'create.html', {'form': form, 'update': True})
#         return render(request, 'create.html', {'form': eventfrom, 'update': True})
#     elif catagoryid:
#         category = Category.objects.get(id=catagoryid)
#         categoryform  =  CreateCategory(instance=category)
#         if request.method == 'POST':
#             form = CreateCategory(request.POST, instance=category)
#             if form.is_valid():
#                 form.save()
#                 return render(request, 'create.html', {'form': CreateCategory(), 'message': "Category updated successfully!", 'update': True})
#             else:
#                 return render(request, 'create.html', {'form': form, 'update': True})
#         return render(request, 'create.html', {'form': categoryform, 'update': True})
#     else:
#         return HttpResponse("No event ID provided for update.")


class UpdateEventAndCatagory(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    template_name = 'create.html'
    login_url = '/users/signin/'
    permission_required = ['events.change_event', 'events.change_category']

    def get_object(self, queryset=None):
        editid = self.request.GET.get('editid')
        catagoryid = self.request.GET.get('catagoryid')

        if editid:
            return Event.objects.get(event_id=editid)
        elif catagoryid:
            return Category.objects.get(id=catagoryid)
        return None


    def get_form_class(self):
        obj = self.get_object()
        if isinstance(obj, Event):
            return CreateEvent
        elif isinstance(obj, Category):
            return CreateCategory
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = True
        return context

    def form_valid(self, form):
        form.save()
        obj_name = "Event" if isinstance(self.object, Event) else "Category"
        messages.success(self.request, f"{obj_name} updated successfully!")
        return_url = "/dashboard/organizer/?event=total_events" if isinstance(self.object, Event) else "/dashboard/organizer/?event=all_category"
        return redirect(return_url)
    
    def form_invalid(self, form):
        return render(self.request, self.template_name, {
            'form': form,
            'update': True
        })
        
    




class ParticipantDaashboard(LoginRequiredMixin,ListView):
    login_url = '/users/signin/'
    model = Event
    template_name = 'dashboard/participant.html'
    context_object_name = 'events'

    def get_queryset(self):
        return Event.objects.filter(participants=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rsvp = self.request.GET.get('rsvp')
        if rsvp:
            messages.error(self.request, "You have already RSVP'd to this event.")
        return context
        



# @user_passes_test(lambda user: check_privilege(user, 'Admin'), login_url='/users/signin/')
# def admin_dashboard(request, path):
#     participant_id = request.GET.get('participant_id')
#     event_id = request.GET.get('event_id')
#     if participant_id and event_id:
#         try:
#             participant = RSVP.objects.get(user_id=participant_id, event_id=event_id)
#             participant.delete()
#             messages.success(request, "Participant deleted successfully!")
#         except RSVP.DoesNotExist:
#             messages.error(request, "Participant not found for this event!")


#     users = None
#     groups = None
#     participants = None
#     if path == 'users':
#         users = User.objects.all()
#     elif path == 'groups':
#         groups = Group.objects.all()
#     elif path == 'participant':
#         participants = RSVP.objects.select_related('event', 'user').values(
#             'user__username',
#             'user__email',
#             'user__id',
#             'event__event_id',
#             'event__name',
#         )
#     return render(request, 'dashboard/admin.html', {'path': path, 'users': users, 'groups': groups, 'participants': participants, 'is_admin': True})




class AdminDashboard(LoginRequiredMixin,GroupRequiredMixin,PermissionRequiredMixin,TemplateView):
    template_name = 'dashboard/admin.html'
    login_url = '/users/signin/'
    permission_required = ['events.change_event', 'events.delete_event', 'events.change_category', 'events.delete_category']
    group_required = 'Admin'

    def get(self, request, *args, **kwargs):
        participant_id = request.GET.get('participant_id')
        event_id = request.GET.get('event_id')

        if participant_id and event_id:
            try:
                rsvp_entry = RSVP.objects.get(user_id=participant_id, event_id=event_id)
                rsvp_entry.delete()
                messages.success(request, "Participant deleted successfully!")
            except RSVP.DoesNotExist:
                messages.error(request, "Participant not found for this event!")

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        path = kwargs.get('path')
        
        context['path'] = path
        context['is_admin'] = True
        context['users'] = None
        context['groups'] = None
        context['participants'] = None

        if path == 'users':
            context['users'] = User.objects.all()
        elif path == 'groups':
            context['groups'] = Group.objects.all()
        elif path == 'participant':
            context['participants'] = RSVP.objects.select_related('event', 'user').values(
                'user__username',
                'user__email',
                'user__id',
                'event__event_id',
                'event__name',
            )
        
        return context





@user_passes_test(lambda user: check_privilege(user, 'Admin'), login_url='/users/signin/')
def assign_role(request, user_id):
    user = User.objects.get(id = user_id)
    form = AssignRoleForm()

    if request.method == "POST":
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            messages.success(request, f"user {user.username} has been assign role {role.name}")
            return redirect("/dashboard/admin/users")
    return render(request, "dashboard/assign_role.html", {'form': form})


@user_passes_test(lambda user: check_privilege(user, 'Admin'), login_url='/users/signin/')
def create_group(request):
    form = CreateGroupForm()

    if request.method == "POST":
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f"gorup name {group.name} has created succesfylly")
            return redirect("create-group")
    
    return render(request, "dashboard/create_group.html", {'form': form})


@user_passes_test(lambda user: check_privilege(user, 'Admin'), login_url='/users/signin/')
def delete_group(request, group_id):
    group = Group.objects.get(id = group_id)
    group.delete()
    messages.success(request, f"gorup name {group.name} has deleted succesfylly")
    return redirect("/dashboard/admin/groups")
    

def access_denied(request):
    return HttpResponse("Access Denied")



def dashboard_redirect(request):
    if check_privilege(request.user, 'Admin'):
        return redirect('/dashboard/admin/users')
    elif check_privilege(request.user, 'Organizer'):
        return redirect('/dashboard/organizer')
    elif check_privilege(request.user, 'Participant'):
        return redirect('/dashboard/participant')
    else:
        return redirect('/dashboard/access-denied')



