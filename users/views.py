from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import Registration,Login
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .tokens import account_token_generator
from .models import User
from django.utils.encoding import force_bytes
from django.utils.http  import urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.contrib.auth import login as auth_login
# Create your views here.

def register(request):
    if request.method == "POST":
        form = Registration(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            
            current_site = get_current_site(request)
            mail_subject  = "Activate your Account"

            message = render_to_string('email_activation.html',{
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')

            email = EmailMessage(mail_subject,message,to=[to_email])
            email.send()
            messages.success(request,"Pleae activate your account")
            return redirect('login')
    else:
            form = Registration()

    return render(request, 'Registration.html',{'form':form})


def login_view(request):
    if request.method == "POST":
          form = Login(request,data=request.POST)
          if form.is_valid():
               user= form.get_user()
               auth_login(request,user)
               if 'next'  in request.POST:
                   return redirect(request.POST.get('next'))
               return redirect('dashboard')
    else:
         form = Login()
    return render(request,'login.html',{'form':form})