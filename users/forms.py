from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re
class Registration(UserCreationForm):
    username = forms.CharField(required=True,widget=forms.TextInput(attrs={
        'placeholder':'Enter your username',
        'autofocus':True
    }))
    first_name = forms.CharField(max_length=150,required=True,widget=forms.TextInput(attrs={
                'placeholder':'First name',
                }),help_text= "Enter your first name")
    last_name = forms.CharField(max_length=150,required=True, widget=forms.TextInput(attrs=
                                                                                     {
                'placeholder':'last name'                                                                         
                                                                                     }))
    email = forms.EmailField(max_length=150, required=True, widget=forms.EmailInput(attrs={
        'placeholder':'johndoe@gmail.com'
    }))

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update(
            {
                'placeholder':'Enter your password'
            }
        )
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm Password'
        })
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name','').strip()

        if not first_name:
            raise ValidationError("First name is required")
        
        if len(first_name) < 2:
            raise ValidationError("First name has to be more than 2 characters")
        
        if not re.match(r"^[a-zA-Z\s\-']+$",first_name):
            raise ValidationError("Invalid characters")
        
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name','').strip()

        if not last_name:
            raise ValidationError("Last name is required")
        
        if len(last_name) < 2:
            raise ValidationError("last name has to be more than 2 characters")
        
        
        if not re.match(r"^[a-zA-Z]+$",last_name):
            raise ValidationError("Invalid input")
        
        return last_name
        
    def clean_username(self):
        username = self.cleaned_data.get('username','').lower().strip()

        if not username:
            raise ValidationError('Username required')
        
        if len(username) < 2 :
            raise ValidationError("Username has to be more than 2 characters")
        
        if not re.match(r"^[a-zA-Z0-9.\-_]"):
            raise ValidationError("Invalid Email")
        
        u_name = ['hero','root','admin','administrator','admin123']
        if username in u_name:
            raise ValidationError("Forbidden username")
        
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username already exists")
        
        return username
        
    def clean_email(self):
        email = self.cleaned_data.get('email','').strip()

        if not email:
            raise ValidationError("Email is required")
        
        if not re.match(r"^[\w.\-_]+@[a-zA-Z0-9._]+[a-zA-Z]{2,}$",email):
            raise ValidationError ("Invalid email")
        
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email already exists ")

        return email
    
    def clean(self):
        return super().clean()

class Login(AuthenticationForm):
    username = forms.CharField(required=True,widget=forms.TextInput(
        attrs={
            'placeholder':"Enter your Username",
            'autofocus':True
        }
    ))

    password = forms.CharField(required=True,widget=forms.PasswordInput(attrs={
        'placeholder':"Enter your Password"
    })
            )


class ProfileEdit(UserChangeForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder':'Enter your username',
                'autofocus':True
            }),
            'first_name':forms.TextInput(attrs={
                'placeholder':"Enter your first name"
            }),
            
            'last_name':forms.TextInput(attrs={
                'placeholder':"Enter your last name"
            }),
            'email': forms.EmailInput(attrs={
                "placeholder":"Enter your email",
                'autocomplete':True
            })
        }

    def clean_username(self):
        username = self.cleaned_data.get('username','').strip()
        if not username: raise ValidationError("username required")
        if User.objects.filter(username=username).exclude(id=self.instance.id).exists():
            raise ValidationError("This username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email','').strip()
        if not email: raise ValidationError("email required")
        if User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise ValidationError("This username already exists")
        return email

        
