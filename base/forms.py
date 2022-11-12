from .models import Extract, Nutrition, Upload, User
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm


# For registration
class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']


# For Login
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email']


class ExtractForm(ModelForm):
    class Meta:
        model = Extract
        fields = '__all__'


class UploadForm(ModelForm):
    class Meta:
        model = Upload
        fields = ['photo']


class NutrtionForm(ModelForm):
    class Meta:
        model = Nutrition
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'id': 'editor'
        })