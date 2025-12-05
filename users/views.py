from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import Registration,Login,ProfileForm,ProfileEdit
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .tokens import account_token_generator
from .models import User
from django.utils.encoding import force_bytes,force_str
from django.utils.http  import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.contrib.auth import login as auth_login, get_user_model,logout
# Create your views here.

def register_view(request):
    if request.method == "POST":
        form =  Registration(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active =False
            user.save()

            email_head = "Activate your  account"
            current_site = get_current_site(request)
            to_mail = form.cleaned_data.get('email')

            message = render_to_string('email_activation.html',{
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_token_generator.make_token(user),

                                        })

            email = EmailMessage(email_head,message,to =[to_mail] )
            email.send()

            messages.success(request, "Registration successful! Please check your email to activate.")
            return redirect('login')
    else:
        form = Registration()
    return render(request, 'registration.html',{'form':form})

def login_view(request):
    if request.method == 'POST':
        form = Login(request,data= request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request,user)
            messages.success(request, "You have logged in successfuly")
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('dashboard')
        else:
            messages.error(request, 'Failed to login. Please check your credentials.')
    else:
        form = Login()
    return render(request, 'login.html',{"form":form})


def activate(request,uidb64,token):
    User = get_user_model()

    try:
        uid = urlsafe_base64_decode(force_str(uidb64))
        user = User.objects.get(pk=uid)

    except (ValueError,OverflowError,User.DoesNotExist):
        user = None

        if user is not None and account_token_generator.check_token(user,token):
            user.is_active =True
            user.save()

            messages.success('Thank You for confirming your email')
            return redirect('login')
        else:
            messages.error(request,"Link has expired")
            form = Registration()
            return render(request, 'registration.hmtl',{'form':form})
        
def logout_view(request):
    logout(request)
    messages.success(request,"You have been logged out successfully")
    return redirect('login')

@login_required
def profile_edit(request):
    user_form = ProfleForm
    