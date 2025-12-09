from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import Registration,Login,ProfileForm,ProfileEdit,ProjectSearchForm,ProjectForm,ProjectImageFormSet
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
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin,PermissionRequiredMixin
from projects.models import Project
from django.urls import reverse_lazy
from discussions.models import Discussion
from bugs.models import Bug
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.db import transaction
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

def create_project(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        formset = ProjectImageFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            form.save_m2m()

            formset.instance = project
            formset.save()
            messages.success(request,"You have created a project successfully")
            return redirect('project_list')
            
        else:
            form = ProfileForm()
            formset = ProjectImageFormSet()

            context = {
                'form':form,
                'formset':formset
            }

    return render(request,"create_project.html",context)

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
@transaction.atomic
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

    def get_object(self):
        #get the user profile 
        return self.request.user.project
    
    def get_queryset(self):
        return Project.objects.select_related('user','category').prefetch_related('technologies','images'),

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['open_bugs_count'] =self.object.bugs.filter(status='OPEN').count()
        context['discussions'] = self.object.discussions.all()[:5]
        return context
        
class ProjectDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Project
    template_name = 'project_delete.html'
    context_object_name = 'project delete'

    def get_object(self):
        return self.request.user.project
    def test_func(self):
        return self.request.user.project
    
    def delete(self, request, *args, **kwargs):
        messages.success(request,"Project deleted successfully")
        return super().delete(request, *args, **kwargs)
    
class ProjectListView(LoginRequiredMixin,ListView):
    model = Profile
    template_name = 'project_list.html'
    context_object_name = 'project_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = Project.objects.select_related('user','category').prefetch_related('technologies')
        form = ProjectSearchForm(self.request.GET)

        if form.is_valid():
            q =  form.cleaned_data.get('q')
            if q:
               queryset= queryset.filter(Q(title__icontains=q)| Q(description__icontains=q))

            category = form.cleaned_data.get('category')
            if category:
                queryset=queryset.filter(category=category)

            status = form.cleaned_data.get('status')
            if status:
                queryset=queryset.filter(category=category)

        return queryset.distinct()
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['search_form'] = ProjectSearchForm(self.request.GET)
        return context

class ProjectUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Project
    template_name = 'project_update.html'
    context_object_name = 'project_update'

    def test_func(self):
        project = self.get_object()
        return self.request.user == project.user or self.request.user.is_superuser

class ProjectCreateView(LoginRequiredMixin,CreateView):
    model = Project
    template_name = 'project_create.html'
    context_object_name = 'project_create'
    success_url = reverse_lazy('profile_detail')


class ProfileDeleteView(LoginRequiredMixin,DeleteView):
    model = Profile
    template_name = 'profile_delete.html'
    context_object_name = 'profile_delete'
    success_url = reverse_lazy('login')

    def get_object(self):
        return self.request.user.profile
    
    def test_func(self):
        return self.request.user  == self.get_object().user
    
    def delete(self, request, *args, **kwargs):
        messages.success(request,'You have successfully deleted your profile')
        return super().delete(request, *args, **kwargs)

class ProfileCreateView(LoginRequiredMixin,CreateView):
    model = Profile
    template_name = 'profile_create.html'
    context_object_name = 'profile_create.html'
    form_class = ProfileForm
    success_url = reverse_lazy('profile_detail')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

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

    def dispatch(self, request, *args, **kwargs):
        self.project  = get_object_or_404(Project,pk=kwargs.get('project_id'))
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        self.project = form.instance.project
        self.request.user = form.instance.reporter
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.project
        return context
        
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

class VerifyProfileView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    model = Profile
    permission_required = 'users.can_verify_profile'