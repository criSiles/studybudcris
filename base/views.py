# This was used to render the home page and room page before the templates were created.
# from django.http import HttpResponse
from django.shortcuts import render
from .models import Room

# Create your views here.

# OLD CODE, before the db
# rooms = [
#     {'id': 1, 'name': 'Lets learn Python!'},
#     {'id': 2, 'name': 'Design with me'},
#     {'id': 3, 'name': 'Frontend Development'}, 
# ]

def home(request):
    # this Room.objects.all() is used to get all the rooms from the database
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'base/room.html', context)
