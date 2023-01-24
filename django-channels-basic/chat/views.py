from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from chat.forms import RoomForm
from chat.models import Room

def index(request):
    rooms = Room.objects.all()
    return render(request, 'chat/index.html', {
        "rooms": rooms,
    })

@login_required
def room_chat(request, room_pk):

    room = get_object_or_404(Room, pk=room_pk)
    return render(request, 'chat/room_chat.html', {
        "room" : room,
    })

@login_required
def room_new(request):
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            created_room = form.save()
            return redirect('chat:room_chat', created_room.pk)
    else:
        form = RoomForm()

    return render(request, 'chat/room_form.html', {
        "form": form,
    })