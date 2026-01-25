from datetime import date
from django.http import HttpResponse
from django.shortcuts import redirect, render
from events.models import Event, Category, Participant
from django.db.models import Q, Count

from events.forms import CreateCategory, CreateEvent, CreateParticipant
# Create your views here.
def home(request):
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

    
def event_details(request, event_id):
    event = Event.objects.prefetch_related('participants').select_related('category').get(event_id=event_id)
    return render(request, 'eventDetails.html', {'event': event})

def dashboard(request):
    mainquery = Event.objects.prefetch_related('participants').select_related('category')
    deleteid = request.GET.get('deleteid')
    if deleteid:
            event_to_delete = mainquery.get(event_id=deleteid)
            event_to_delete.delete()
        
    
    participant_id = request.GET.get('participant_id')
    if participant_id:
            participant_to_delete = Participant.objects.get(participant_id=participant_id)
            participant_to_delete.delete()
            return redirect('/dashboard/?event=all_Participant')

    catagory_id = request.GET.get('catagoryid')
    if catagory_id:
            catagory_to_delete = Category.objects.get(id=catagory_id)
            catagory_to_delete.delete()
            return redirect('/dashboard/?event=all_category')
        

    # total_events = mainquery.count()
    # total_categories = Category.objects.count()
    # total_participants = Participant.objects.count()
    # upcoming_events = mainquery.filter(date__gt=date.today()).count()
    # past_events = mainquery.filter(date__lt=date.today()).count()

    count = mainquery.aggregate(
        total_events=Count('event_id'),
        total_categories=Count('category'),
        total_participants=Count('participants'),
        upcoming_events=Count('event_id', filter=Q(date__gt=date.today())),
        past_events=Count('event_id', filter=Q(date__lt=date.today()))
    )

    context = {
        'events': [],
        'is_category': False,
        'is_participant': False,
        'total_events': count['total_events'],
        'total_categories': count['total_categories'],
        'total_participants': count['total_participants'],
        'upcoming_events': count['upcoming_events'],
        'past_events': count['past_events']
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
        context['events'] = Participant.objects.all()
        context['is_participant'] = True
    else:
        context['events'] = mainquery.all()

    return render(request, 'dashboard.html', context)

def create(request):
    create = request.GET.get('create')
    
    if create == 'category':
        if request.method == 'POST':
            form = CreateCategory(request.POST)
            if form.is_valid():
                form.save()
                return render(request, 'create.html', {'form': CreateCategory(), 'message': "Category created successfully!"})
            else:
                return render(request, 'create.html', {'form': form})
        form = CreateCategory()
        return render(request, 'create.html', {'form': form})
    elif create == 'event':
        if request.method == 'POST':
            form = CreateEvent(request.POST)
            if form.is_valid():
                form.save()
                return render(request, 'create.html', {'form': CreateEvent(), 'message': "Event created successfully!"})
            else:
                return render(request, 'create.html', {'form': form})
        form = CreateEvent()
        return render(request, 'create.html', {'form': form})
    elif create == 'participant':
        if request.method == 'POST':
            form = CreateParticipant(request.POST)
            if form.is_valid():
                form.save()
                return render(request, 'create.html', {'form': CreateParticipant(), 'message': "Participant created successfully!"})
            else:
                return render(request, 'create.html', {'form': form})   
        form = CreateParticipant()
        return render(request, 'create.html', {'form': form})
    
    else:
        return render(request, 'create.html', {'form': None})
    



def update(request):
    editid = request.GET.get('editid')
    catagoryid = request.GET.get('catagoryid')
    participant_id = request.GET.get('participant_id')
    if editid:
        event = Event.objects.get(event_id=editid)
        eventfrom  =  CreateEvent(instance=event)
        if request.method == 'POST':
            form = CreateEvent(request.POST, instance=event)
            if form.is_valid():
                form.save()
                return render(request, 'create.html', {'form': CreateEvent(), 'message': "Event updated successfully!", 'update': True})
            else:
                return render(request, 'create.html', {'form': form, 'update': True})
        return render(request, 'create.html', {'form': eventfrom, 'update': True})
    elif catagoryid:
        category = Category.objects.get(id=catagoryid)
        categoryform  =  CreateCategory(instance=category)
        if request.method == 'POST':
            form = CreateCategory(request.POST, instance=category)
            if form.is_valid():
                form.save()
                return render(request, 'create.html', {'form': CreateCategory(), 'message': "Category updated successfully!", 'update': True})
            else:
                return render(request, 'create.html', {'form': form, 'update': True})
        return render(request, 'create.html', {'form': categoryform, 'update': True})
    elif participant_id:
        participant = Participant.objects.get(participant_id=participant_id)
        participantform  =  CreateParticipant(instance=participant)
        if request.method == 'POST':
            form = CreateParticipant(request.POST, instance=participant)
            if form.is_valid():
                form.save()
                return render(request, 'create.html', {'form': CreateParticipant(), 'message': "Participant updated successfully!", 'update': True})
            else:
                return render(request, 'create.html', {'form': form, 'update': True})
        return render(request, 'create.html', {'form': participantform, 'update': True})
    else:
        return HttpResponse("No event ID provided for update.")
