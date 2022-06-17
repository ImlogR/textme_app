from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from goji.models import Room, Message
from cryptography.fernet import Fernet

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method== 'POST':
        username= request.POST['username']
        email= request.POST['email']
        password= request.POST['password']
        password_2= request.POST['password_2']

        if password== password_2:
            if User.objects.filter(email= email).exists():
                messages.info(request, 'Email used!!')
                return redirect('register')
            
            elif User.objects.filter(username= username).exists():
                messages.info(request, 'Existing Username!')
                return redirect('register')

            else:
                user= User.objects.create_user(username= username, email= email, password= password)
                user.save();
                return redirect('login')
        
        else:
            messages.info(request, 'Password not the same!!')
            return redirect('/')
    
    else:
        return render(request, 'register.html')

def login(request):
    if request.method== 'POST':
        username= request.POST['username']
        password= request.POST['password']

        user= auth.authenticate(username= username, password= password)

        if user is not None:
            auth.login(request, user)
            return redirect('textme')

        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')

    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def room(request, room):
    username= request.GET.get('username')
    room_details= Room.objects.get(name= room)
    return render(request, 'room.html', { 'username': username, 'room': room, 'room_details':room_details})

def checkview(request):
    room= request.POST['room_name']
    room= room.upper()
    room_pass= request.POST['room_password']
    username= request.POST['username']

    if Room.objects.filter(name= room, room_pass= room_pass).exists():
        return redirect('/' + room +'/?username='+username)

    else:
        new_room= Room.objects.create(name= room, room_pass= room_pass)
        new_room.save()
        return redirect('/'+ room +'/?username='+username)

fernet= Fernet(b'L7lPbExd3k4BA0inLlHR9pNi0nxSb7yCn1t8TB-5zE0=')

def encrypt(message):
    encMsg= fernet.encrypt(message.encode())
    return encMsg

def decrypt(message):
    decMsg= fernet.decrypt(message).decode()
    return decMsg  

def send(request):
    message= request.POST['message']
    username= request.POST['username']
    room_id= request.POST['room_id']

    new_message= Message.objects.create( value= message, User= username, room= room_id)
    new_message.save()
    return HttpResponse('Message sent !!')

def getMessages(request, room):
    room_details= Room.objects.get(name= room)
    messages= Message.objects.filter(room= room_details.id)
    return JsonResponse({"messages": list(messages.values())})