from django import forms
from .models import MyUser
class MyUserForm(forms.ModelForm):
    class Meta:
        model = MyUser
        widgets = {'password': forms.PasswordInput(),'cpassword': forms.PasswordInput(), }
        fields = ['userName', 'password','cpassword','fname','lname','dob','mobno','email']




