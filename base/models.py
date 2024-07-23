from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str___(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # TIP: If you want to use a class inside of another class, you have to define the class first or put it like this 'Topic' in quotes.
    topic= models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)

    # This attribute is type CharField, it only stores strings, we have to specify the max_length of the string.
    name = models.CharField(max_length=200)
    # This attribute is type TextField, it only stores large strings (text), 
    # null=True means that the db can have a instance of this model if this attribute is empty, by default is set to False.
    # blank=True means that the form can be submitted without this attribute, by default is set to False.
    descriptions = models.TextField(null=True, blank=True)

    # participants = 
    # Every time an instance of this model is updated, this attribute will be set to the current time everytime.
    updated = models.DateTimeField(auto_now=True)
    # Every time a new instance of this model is created, this attribute will be set to the current time only the first time.
    created = models.DateTimeField(auto_now_add=True)

    def __str___(self):
        return self.name


# one to many relationship, one user can have many messages, but one message can only have one user.
class Message(models.Model):
    # Django has a built-in user model, we can use it by importing it.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # on_delete=models.CASCADE means that if the user is deleted, all the messages from that user will be deleted. 
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:50]