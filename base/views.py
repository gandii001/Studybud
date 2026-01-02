from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from .models import Room,Topic,Message
from .forms import RoomForm, UserForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout 
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

#rooms = [
 #   {'id':1, 'name':'Java developers lets connect'},
  #  {'id':2, 'name':'python developers lets connect'},
   # {'id':3, 'name':'javascript developers lets connect'},
#]


def Home(request):

    q = request.GET.get('q') if request.GET.get('q')!= None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)       # 'icontains' allows unfinished url detect similar topic
    )  # Q is a module that lets you use '|'-OR,'&'
    room_count = rooms.count()                            
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q))


    #rooms = Room.objects.all()
    topics = Topic.objects.all()[0:4 ]
    context = {'rooms':rooms, 'topics':topics,
                'room_count':room_count, 'room_messages':room_messages}
    return render(request, 'base/home.html', context)
 
def room(request,pk): 
    room = Room.objects.get(id=pk)
    #for i in rooms :
     #   if i['id'] == int(pk):
      #      room = i
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        # this allows users from different room participate in another room
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {'room':room, 'room_messages':room_messages, 'participants':participants}
    return render(request, 'base/room.html', context)  


@login_required(login_url='login')
def createRoom(request):
    
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        #gets the value of topic checks if it was previously created  if yes "created" will be false and vice versa
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        Room.objects.create(
            host = request.user,
            topic = topic,
            name= request.POST.get('name'),
            description = request.POST.get('description'),
        )
        #form = RoomForm(request.POST)
        #if form.is_valid():
         ##  room.host = request.user
           # room.save()
        return redirect('Home')
    context = {'form':form, 'topics':topics}
    return render(request, 'base/room_form.html', context)



def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user, 'rooms':rooms, 
               'room_messages':room_messages, 'topics':topics}
    return render(request, 'base/profile.html', context)


@login_required(login_url= 'login')
#added to be able to edit a particular/distinct post
def updateRoom(request,pk):  
    room = Room.objects.get(id=pk)
    # added instance so the form will be filled up with initial data to be edited
    form = RoomForm(instance=room)   
    topics = Topic.objects.all()
    #this restricts a user from editing other users post
    if request.user != room.host :
        return HttpResponse('You do not have the permission to do this!!')


    if request.method == 'POST':
        form = RoomForm(request.POST,instance=room)
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        #if form.is_valid():
         #   form.save()
        return redirect('Home')
    context = {'form':form, 'topics':topics, 'room':room}
    return render(request, 'base/room_form.html',context)


@login_required(login_url= 'login')
def deleteRoom(request,pk):
    obj = Room.objects.get(id=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('Home')
    context = {'obj':obj}
    return render(request, 'base/delete.html',context)



def loginPage(request): 
    page = 'login'
    if request.user.is_authenticated:
            return redirect('Home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        
        try:

            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user  is not None:
            login(request, user)
            return redirect('Home')
        else:
            messages.error(request, 'Username or password does not exist')  

    context = {'page':page}

    return render(request, 'base/login_register.html', context)




def logoutUser(request):
    logout(request)
    return redirect('Home') 


def registerUser(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)   
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('Home')
        else:
            messages.error(request, 'Error occurred during registration')
    context = {'form':form}
    return render(request, 'base/login_register.html', context)

@login_required(login_url='login')
def deleteMessage(request,pk):
    selMessage = Message.objects.get(id=pk)

    #if request.user != selMessage.user:
     #   return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        selMessage.delete()
        context = {'selMessage':selMessage}
        return redirect('Home')
    context = {'obj':selMessage}
    return render(request, 'base/delete.html', context)
            
@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form':form})
    
    


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q')!= None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics':topics})


def activityPage(request):
    q = request.GET.get('q') if request.GET.get('q')!= None else '' 
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q))
    return render(request, 'base/activity.html', {'room_messages':room_messages})