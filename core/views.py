from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate,logout
from .forms import *
from .models import *
from django.contrib import messages


@login_required
def index(request):
    profile = Profile.objects.get(user=request.user)
    context = {
        'profile': profile,
    }

    if request.user.is_staff:
        patients = User.objects.filter(is_staff=False)
        context['patients'] = patients
    return render(request, 'core/index.html',context)

@login_required
def profile(request,id):
    user = User.objects.get(id=id)
    context = {
        'puser': user,
        'profile': Profile.objects.get(user=user)
    }
    return render(request, 'core/profile.html',context)




def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.is_staff = False  # Ensure is_staff is False for patients
            user.save()
            profile = Profile.objects.get(user=user)
            profile.city = profile_form.cleaned_data['city']
            profile.state = profile_form.cleaned_data['state']
            profile.pincode = profile_form.cleaned_data['pincode']
            profile.address = profile_form.cleaned_data['address']
            profile.profile_picture = profile_form.cleaned_data['profile_picture']
            profile.save()
            messages.success(request, 'Your account has been created successfully.')
            return redirect('login')
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileForm()
    
    return render(request, 'registration/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
    

@login_required
def register_doc(request):
    
    if not request.user.is_superuser:
        messages.success(request, 'You must be a superuser',extra_tags='danger')
        return redirect('index')
    
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.is_staff = True
            user.save()
            profile = Profile.objects.get(user=user)
            profile.city = profile_form.cleaned_data['city']
            profile.state = profile_form.cleaned_data['state']
            profile.pincode = profile_form.cleaned_data['pincode']
            profile.address = profile_form.cleaned_data['address']
            profile.profile_picture = profile_form.cleaned_data['profile_picture']
            profile.save()
            messages.success(request, f'Account has been created successfully for @{profile.user.username}.',extra_tags=['info'])
            return redirect('index')
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileForm()
    
    return render(request, 'registration/doctor_reg.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
   

def login_view(request):
    if request.method == 'POST':
        form = UserAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  
    else:
        form = UserAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})



@login_required
def logout_view(request):
    logout(request)
    return redirect('index')