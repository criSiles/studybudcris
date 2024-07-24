# This was used to render the home page and room page before the templates were created.
# from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Room
from .forms import RoomForm

# Create your views here.

# OLD CODE, before the db
# rooms = [
#     {'id': 1, 'name': 'Lets learn Python!'},
#     {'id': 2, 'name': 'Design with me'},
#     {'id': 3, 'name': 'Frontend Development'}, 
# ]

# HOME VIEW
def home(request):
    # this Room.objects.all() is used to get all the rooms from the database
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'base/home.html', context)

# ROOM VIEW
def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'base/room.html', context)

# CREATE ROOM VIEW
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        print('Printing POST:', request.POST)
        form = RoomForm(request.POST)
        # This is going to check if the form is valid
        if form.is_valid():
            # This is going to save the form in the database
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

# UPDATE ROOM VIEW
# To update a room we need to pass the primary key of the room
def updateRoom(request, pk):
    # This is going to get the room that we want to update from the database
    room = Room.objects.get(id=pk)
    # This is going to pass the instance of the form prefilled with the data of the room that we want to update
    form = RoomForm(instance=room)
    if request.method == 'POST':
        # This is going to rewrite the form with the new data
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            # This is going to save the form in the database
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

# DELETE ROOM VIEW
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        # This is going to delete the room from the database
        room.delete()
        return redirect('home')
    # I pass the obj key like this to make it reusable in the delete.html template
    return render(request, 'base/delete.html', {'obj':room})