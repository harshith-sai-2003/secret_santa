from django.shortcuts import render
from django.http import JsonResponse
from .models import Room, Participant
import random
import string
import requests

# Create your views here.

def home(request):
    return render(request, 'santa/home.html')

def generate_room_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def create_room(request):
    room = Room.objects.create(code=generate_room_code())
    return JsonResponse({"room_code": room.code})

def send_invites(request):
    room_code = request.POST.get("room_code")
    emails = request.POST.getlist("emails[]")
    room = Room.objects.get(code=room_code)
    # Use Mailmodo API to send invites
    API_KEY = "your-mailmodo-api-key"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }
    data = {
        "to": emails,
        "subject": "Join the Secret Santa Room!",
        "template_name": "your-template-name",
        "variables": {
            "room_code": room_code,
        },
    }
    response = requests.post(
        "https://api.mailmodo.com/api/v1/campaigns/send", headers=headers, json=data
    )
    if response.status_code == 200:
        return JsonResponse({"message": "Invitations sent successfully!"})
    else:
        return JsonResponse({"error": "Failed to send emails."}, status=500)
    
def rooms(request):
    return render(request, 'rooms.html') 

