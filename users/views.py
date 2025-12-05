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
from django.views.generic import ListView,DetailView,DeleteView,CreateView,UpdateView
from users.models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from projects.models import Project
from discussions.models import Discussion
from bugs.models import Bug
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
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except (ValueError,OverflowError,User.DoesNotExist):
        user = None

    if user is not None and account_token_generator.check_token(user,token):
            user.is_active =True
            user.save()

            messages.success(request,'Thank You for confirming your email')
            return redirect('login')
    else:
            messages.error(request,"Link has expired")
            form = Registration()
            return render(request, 'registration.html',{'form':form})
        
def logout_view(request):
    logout(request)
    messages.success(request,"You have been logged out successfully")
    return redirect('login')

@login_required
def profile_edit(request):
    user_form = ProfileEdit(request.POST,instance=request.user)
    profile_form = ProfileForm(request.POST,request.FILES,instance=request.user.profile)

    if user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()

        messages.success(request,'Your form has been updated successfully')
        return redirect('profile_detail')
    else:
        user_form = ProfileEdit(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

        context = {
            'user_form':user_form,
            'profile_form':profile_form,
        }
    return render (request,'profile_edit.html',context)



class ProjectDetailView(LoginRequiredMixin,DetailView):
    model = Project
    template_name = 'profile.html'
    context_object_name = 'profile'

class ProjectListView(LoginRequiredMixin,ListView):
    model = Profile
    template_name = 'project_list.html'
    context_object_name = 'project_list'
    paginate_by = 10


    def get_queryset(self):
        return super().get_queryset()



class ProjectUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Project
    template_name = 'project_update.html'
    context_object_name = 'project_update'

class ProjectCreateView(LoginRequiredMixin,CreateView):
    model = Project
    template_name = 'project_create.html'
    context_object_name = 'project_create'

class ProfileDeleteView(LoginRequiredMixin,DeleteView):
    model = Profile
    template_name = 'profile_delete.html'
    context_object_name = 'profile_delete'

class ProfileCreateView(LoginRequiredMixin,CreateView):
    model = Profile
    template_name = 'profile_create.html'
    context_object_name = 'profile_create.html'

class ProfileDetailView(LoginRequiredMixin,DetailView):
    model = Profile
    template_name = 'profile_detail.html'
    context_object_name = 'profile_detail'

    
    def get_object(self):
        profile = self.request.user.profile
        return profile

class CreateBugView(LoginRequiredMixin,CreateView):
    model = Bug
    template_name = 'Create_bug.html'
    context_object_name = 'create_bug'

class BugDetailView(LoginRequiredMixin,DetailView):
    model = Bug
    template_name = "bug_detail.html"
    context_object_name = 'bug_detail'

class BugDeleteView(LoginRequiredMixin,DeleteView):
    model = Bug
    template_name = 'bug_delete.html'
    context_object_name = 'bug_delete'

class BugListView(LoginRequiredMixin,ListView):
    model = Bug
    template_name = 'bug_list.html'
    context_object_name = 'bug_list'

class DiscussionCreateView(LoginRequiredMixin,CreateView):
    model = Discussion
    template_name = 'create_discussion.html'
    context_object_name = 'create discussion'

class DiscussionDetailView(LoginRequiredMixin,DetailView):
    model = Discussion
    template_name = 'discussion_detail.html'
    context_object_name = 'discussion_detail'

class DiscussionDeleteView(LoginRequiredMixin,DeleteView):
    model = Discussion
    template_name = 'discussion_delete.html'
    context_object_name = 'discussion_delete'

class DiscussionUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Discussion
    template_name = 'discussion_update.html'
    context_object_name = 'discussion_update'