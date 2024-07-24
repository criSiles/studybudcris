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

def home(request):
    # this Room.objects.all() is used to get all the rooms from the database
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'base/room.html', context)

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