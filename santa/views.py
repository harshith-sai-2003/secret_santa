from django.shortcuts import render
from django.http import JsonResponse
from .models import Room, Participant
import random
import string
import requests, json

# Create your views here.

def home(request):
    return render(request, 'santa/home.html')

def register(request):
    if request.method == "POST":
        # Extract data from the form
        name = request.POST.get('name', '')
        isPresentInBangalore = request.POST.get('isPresentInBangalore', 'false').lower() == 'true'
        address = request.POST.get('address', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        budget = int(request.POST.get('budget', 0))  # Default to 0 if not provided
        hobby = request.POST.get('hobby', '')

        # Save data to the database
        try:
            Participant.objects.create(
                name=name,
                isPresentInBangalore=isPresentInBangalore,
                address=address,
                email=email,
                phone=phone,
                budget=budget,
                hobby=hobby
            )
            return JsonResponse({"status": "success", "message": "User registered successfully!"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    # Render the registration form for GET request
    return render(request, 'santa/register.html')

def send_invites(request):
    # Fetch participants data from the database
    participants_queryset = Participant.objects.all()
    participants = []

    # Convert queryset to a list of dictionaries
    for p in participants_queryset:
        participants.append({
            "name": p.name,
            "isPresentInBangalore": p.isPresentInBangalore,
            "address": p.address,
            "email": p.email,
            "phone": p.phone,
            "budget": p.budget,
            "hobby": p.hobby
        })

    # Default budget
    budget = float('inf')  # Set to a large value initially
    for x in participants:
        budget = min(x['budget'], budget)
    # Shuffle participants to randomize Secret Santa assignment
    shuffled_participants = participants[:]
    random.shuffle(shuffled_participants)

    pairings = []
    for i in range(len(shuffled_participants)):
        pairings.append({"santa": shuffled_participants[i], "receiver": shuffled_participants[(i+1)%len(shuffled_participants)]})

    api_url = "https://www.fast2sms.com/dev/bulkV2?authorization=apiHere&route=q&message=messageHere&flash=0&numbers=numberHere&schedule_time="
    api_key = ""  # Replace with your actual API key

    for pairing in pairings:
        santa = pairing['santa']
        receiver = pairing['receiver']

        # Construct message
        message = (
            f"Hi {santa['name']},\n"
            f"You are the Secret Santa for {receiver['name']}!\n"
            f"Here are some details about them:\n"
            f"Address: {receiver['address']}\n"
            f"Hobby: {receiver['hobby']}\n"
            f"Budget: {budget}/-\n"
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
            response = ''
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


