from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE






# Create your models here.

#This is a parent model to 'Room', a topic can have many rooms,while a room can have one topic 
class Topic(models.Model):
    name = models.CharField(max_length=200)
   
    # the string value 
    def __str__(self):
        return self.name






class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # hosts to open the room(first user)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)  #whenever a topic is deleted the room remains and the database remains empty
    name = models.CharField(max_length=200)  
    description = models.TextField(null=True, blank=True)   #null=true,allows submision of empty 
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)   #date&time of when a new topic of a room is updated 
    created = models.DateTimeField(auto_now_add=True) #date&time of when a room is creted

    class Meta:
        ordering = ['-updated','-created']   # (-) this sorts the posts from newest to oldest

    def __str__(self):
        return self.name
    


#This is a children class to class 'Room'-.ForeignKey
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)   #The allows multiple message from a single user
    room = models.ForeignKey(Room, on_delete= models.CASCADE)  #this "ondelete"ensures that whenever the room is deleted all the comments are deleted
    body = models.TextField()    
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-updated','-created']
    
    def __str__(self):
        return self.body[0:50]