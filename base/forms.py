from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        # This is the model that we're going to use to create the form, with the meta data of the Room model
        model = Room
        # This is going to create all the fields from the model Room that we want to display in the form, for now is all
        fields = '__all__'