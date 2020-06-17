from django.contrib.auth.models import User
from django.shortcuts import HttpResponse, redirect, render
from core.models import Event
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse


def login_user(request):
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        messages.error(request, "Invalid username or password")
    return redirect('/')

# Create your views here.
def date_event(request, event_title):
    event = Event.objects.get(title=event_title)
    return HttpResponse('<h1>{}</h1>'.format(event.event_date))

@login_required(login_url='/login/')
def event_list(request):
    user = request.user
    current_date = datetime.now() - timedelta(hours=1)
    event = Event.objects.filter(user=user,
                                event_date__gt=current_date)
    data = {'events': event}
    return render(request, 'agenda.html', data)

@login_required(login_url='/login/')
def event(request):
    event_id = request.GET.get('id')
    data = {}
    if event_id:
        data['event'] = Event.objects.get(id=event_id)
        print(data['event'].event_date)
    return render(request, 'event.html', data)

@login_required(login_url='/login/')
def submit_event(request):
    if request.POST:
        title = request.POST.get('title')
        event_date = request.POST.get('event_date')
        description = request.POST.get('description')
        event_place = request.POST.get('event_place')
        user = request.user
        event_id = request.POST.get('event_id')
        if event_id:
            event = Event.objects.get(id=event_id)
            event.title = title
            event.event_date = event_date
            event.description = description
            event.event_place = event_place
            event.save()
            # Event.objects.filter(id=event_id).update(title=title,
            #                                         event_date=event_date,
            #                                         description=description)
        else:
            Event.objects.create(title=title,
                            event_date=event_date, description=description,
                            event_place=event_place,
                            user=user)
       
    return redirect('/')

@login_required(login_url='/login/')
def delete_event(request, event_id):
    user = request.user
    try:
        event = Event.objects.get(id=event_id)
    except Exception:
        raise Http404()
    if user == event.user:
        event.delete()
    else:
        raise Http404()
    return redirect('/')

@login_required(login_url='/login/')
def json_event_list(request, user_id):
    user = User.objects.get(id=user_id)
    event = Event.objects.filter(user=user).values('id', 'title')
    return JsonResponse(list(event), safe=False)
