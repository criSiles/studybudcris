from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name','username', 'email', 'password1', 'password2']

class RoomForm(ModelForm):
    class Meta:
        # This is the model that we're going to use to create the form, with the meta data of the Room model
        model = Room
        # This is going to create all the fields from the model Room that we want to display in the form, for now is all
        fields = '__all__'
        exclude = ['host', 'participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name','username', 'email', 'avatar', 'bio']