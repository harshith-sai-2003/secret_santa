from django.shortcuts import render
from django.http import JsonResponse
from .models import Room, Participant
import random
import string
import requests, json

# Create your views here.

def home(request):
    return render(request, 'santa/home.html')

def generate_room_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def create_room(request):
    room = Room.objects.create(code=generate_room_code())
    return JsonResponse({"room_code": room.code})

def send_invites(request):
    body = json.loads(request.body)
    participants = body.get('participants', [])
    # Shuffle participants to randomize Secret Santa assignment
    shuffled_participants = participants[:]
    random.shuffle(shuffled_participants)

    pairings = []
    for i in range(len(shuffled_participants)):
        pairings.append({"santa": shuffled_participants[i], "receiver": shuffled_participants[(i+1)%len(shuffled_participants)]})

    api_url = "https://www.fast2sms.com/dev/bulkV2?authorization=apiHere&route=q&message=messageHere&flash=0&numbers=numberHere&schedule_time="
    api_key = "P8D6GMtoUkLmaIxqZQzgCcepjb7RJEdSBn4HK9iy1XFw5f2hruJQVrZCGn1Befp2S5ciYg3Rzvj4W0yL"  # Replace with your actual API key

    for pairing in pairings:
        santa = pairing['santa']
        receiver = pairing['receiver']

        # Construct message
        message = (
            f"Hi {santa['email']},\n"
            f"You are the Secret Santa for {receiver['email']}!\n"
            f"Here are some details about them:\n"
            f"Address: {receiver['address']}\n"
            f"Hobby: {receiver['hobby']}\n"
            f"Budget: {receiver['budget']}\n"
            f"Happy gifting!"
        )
        # message = f"Hi {santa['email']}, you gotta gift {receiver['email']}"

        # Prepare payload for SMS API
        payload = {
            "api_key": api_key,
            "to": santa['phone'],
            "message": 'hello',
        }
        # api_url = api_url.replace('apiHere', api_key).replace('messageHere', 'HI').replace('numberHere', santa['phone'])
        # print(api_url)
        url = "https://www.fast2sms.com/dev/bulkV2"

        querystring = {
            "authorization":"P8D6GMtoUkLmaIxqZQzgCcepjb7RJEdSBn4HK9iy1XFw5f2hruJQVrZCGn1Befp2S5ciYg3Rzvj4W0yL",
            "message":message,
            "language":"english",
            "route":"q",
            "numbers":santa['phone']
            }

        headers = {
            'cache-control': "no-cache"
        }

        
        try:
            # Send the SMS
            # response = requests.request("GET", url, headers=headers, params=querystring)
            print(querystring)
            # print(response.text)

            # Check response status
            if response.status_code == 200:
                print(f"Message sent to {santa['email']} successfully.")
            else:
                print(f"Failed to send message to {santa['email']}. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error sending message to {santa['email']}: {e}")


# participants = [
#     {
#     "isPresentInBangalore": "True",
#     "address":"here",
#     "email":"here@gmail.com",
#     "phone":"9867695467",
#     "budget":"1000",
#     "hobby":"Eating"
#     },
#     {
#     "isPresentInBangalore": "True",
#     "address":"there",
#     "email":"there@gmail.com",
#     "phone":"6301673585",
#     "budget":"1000",
#     "hobby":"Dying"
#     },
#     {
#     "isPresentInBangalore": "True",
#     "address":"where",
#     "email":"where@gmail.com",
#     "phone":"9867695467",
#     "budget":"1000",
#     "hobby":"killing"
#     },
#     {
#     "isPresentInBangalore": "True",
#     "address":"inside",
#     "email":"inside@gmail.com",
#     "phone":"6301673585",
#     "budget":"1000",
#     "hobby":"Digesting"
#     }
# ]

# send_invites('',participants)


