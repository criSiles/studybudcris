from django.shortcuts import redirect, render
from django.http import HttpResponse
# The Q lookup method allow us to make & and | statements in the query
from django.db.models import Q
# This is used to protect the views from unauthorized users
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Room, Topic, Message
from .forms import RoomForm
# This is used to send messages to the user
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    # this Room.objects.filter(xxxx__icontains=q) is used to get all the rooms from the database that contain the query of topic.name, name or descriptions
    # icontains is a value that searches if the query contains at least some of the letters in the name
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | 
        Q(name__icontains=q) | 
        Q(descriptions__icontains=q)
    )
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    # this Topic.objects.all() is used to get all the topics from the database, i means that is case insensitive
    topics = Topic.objects.all()
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    
    context = {'room': room, 'room_messages': room_messages, 'participants': participants} 
    return render(request, 'base/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)

# This is a decorator that if  the user is not logged in, it will redirect the user to the login page when try to create a room
@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        # If a topic does not exist, it will create a new one if exist it will get the topic
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            descriptions=request.POST.get('descriptions')
        )
        return redirect('home')
    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)

# To update a room we need to pass the primary key of the room
@login_required(login_url='login')
def updateRoom(request, pk):
    # This is going to get the room that we want to update from the database
    room = Room.objects.get(id=pk)
    # This is going to pass the instance of the form prefilled with the data of the room that we want to update
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('You are not allowed here!')
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.descriptions = request.POST.get('descriptions')
        room.save()
        return redirect('home')
    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You are not allowed here!')
    if request.method == 'POST':
        # This is going to delete the room from the database
        room.delete()
        return redirect('home')
    # I pass the obj key like this to make it reusable in the delete.html template
    return render(request, 'base/delete.html', {'obj':room})

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        print(username, password)

        try:
            # Use the User bulit-in model to see if the user exists
            user = User.objects.get(username=username)
        except Exception:
            # If the user does not exist, send a flash message to the user
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)
        # If the user exists, log the user in
        if user is not None:
            login(request, user)
            return redirect('home')
        # Else, send a flash message to the user
        else:
            messages.error(request, 'Username OR password does not exist')
    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error has occurred during registration')
    return render(request, 'base/login_register.html', {'form': form})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message= Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!') 
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})
