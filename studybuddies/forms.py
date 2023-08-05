from .models import Profile, Course, StudySessions
from django import forms
import requests

#MODIFY LATER
class CreateProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'computing_id', 'year', 'time_availability', 'courses']
    first_name = forms.CharField()
    last_name = forms.CharField()
    computing_id = forms.CharField()
    year = forms.CharField()
    time_availability =forms.CharField() 
    def __init__(self, *args, **kwargs):
        super(CreateProfile, self).__init__(*args, **kwargs)
        # self.user = user
        # print(self.user)
        self.fields['courses'] = forms.ModelMultipleChoiceField(
            queryset=Course.objects.all(),
            widget=forms.SelectMultiple(attrs={'size':9})
        )
    
class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class CreateStudySession(forms.ModelForm):
    class Meta:
        model = StudySessions
        fields = ['capacity', 'date', 'time']
        widgets = {
            'date': DateInput(),
            'time': TimeInput(),
        }
    capacity = forms.IntegerField()
    
    

    