from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .forms import *
from .models import *
from django.contrib import messages
import markdown
from .utils import *
from django.conf import settings
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from datetime import datetime, timedelta
from django.utils import timezone

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

SCOPES = ['https://www.googleapis.com/auth/calendar']

@login_required
def index(request):
    profile = Profile.objects.get(user=request.user)
    context = {
        'profile': profile,
    }

    if request.user.is_staff:
        patients = User.objects.filter(is_staff=False)
        context['patients'] = patients
    return render(request, 'core/index.html', context)

@login_required
def profile(request, id):
    user = User.objects.get(id=id)
    context = {
        'puser': user,
        'profile': Profile.objects.get(user=user)
    }
    return render(request, 'core/profile.html', context)

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
            messages.success(request, 'Account has been created successfully.',extra_tags='success')
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
        messages.success(request, 'You must be a superuser', extra_tags='danger')
        return redirect('index')
    
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.is_staff = True
            user.save()
            Doctor.objects.create(user=user)
            profile = Profile.objects.get(user=user)
            profile.city = profile_form.cleaned_data['city']
            profile.state = profile_form.cleaned_data['state']
            profile.pincode = profile_form.cleaned_data['pincode']
            profile.address = profile_form.cleaned_data['address']
            profile.profile_picture = profile_form.cleaned_data['profile_picture']
            profile.save()
            messages.success(request, f'Account has been created successfully for @{profile.user.username}.', extra_tags=['info'])
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

# TASK 2:

@login_required
def create_blog(request):
    if not request.user.is_staff:
        messages.success(request, "Invalid Access!!", extra_tags="danger")
        return redirect('index')
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            is_draft = True if request.POST.get('is_draft') == 'on' else False
            blog = form.save(is_draft=is_draft)
            if is_draft:
                messages.success(request, f"{form.cleaned_data['title']} saved as draft.", extra_tags="info")
            else:
                messages.success(request, f"{form.cleaned_data['title']} posted.", extra_tags="success")
            return redirect('view_blog', blog.id)
    else:
        form = BlogForm(user=request.user)
    context = {
        'form': form,
    }
    return render(request, 'blog/create.html', context)

@login_required
def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    if not (request.user == blog.user or request.user.is_staff):
        messages.success(request, "You do not have permission to edit this blog.", extra_tags="danger")
        return redirect('view_blog', blog.id)

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog, user=request.user)
        if form.is_valid():
            is_draft = request.POST.get('is_draft') == 'on'
            blog = form.save(is_draft=is_draft)
            if is_draft:
                messages.success(request, f"{form.cleaned_data['title']} saved as draft.", extra_tags="info")
            else:
                messages.success(request, f"{form.cleaned_data['title']} updated.", extra_tags="success")
            return redirect('view_blog', blog.id)
        else:
            messages.success(request, "There was an error with your submission. Please correct the errors below.", extra_tags="danger")
    else:
        form = BlogForm(instance=blog, user=request.user)

    context = {
        'form': form,
        'blog': blog,
    }
    return render(request, 'blog/edit.html', context)

@login_required
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    if not (request.user == blog.user or request.user.is_staff):
        messages.success(request, "You do not have permission to delete this blog.", extra_tags="danger")
        return redirect('view_blog', blog.id)

    if request.method == 'POST':
        blog.delete()
        messages.success(request, f"'{blog.title}' has been deleted.", extra_tags="success")
        return redirect('index')
    context = {
        'blog': blog,
    }
    return render(request, 'blog/delete.html', context)

def blog_view(request, id):
    context = {}
    blog = Blog.objects.get(id=id)
    context['blog'] = blog
    context['content'] = markdown.markdown(blog.content)
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST, user=request.user)
        if form.is_valid():
            comment = form.save()
            blog.comments.add(comment)
            blog.save()
            messages.success(request, "Comment posted successfully.", extra_tags='success')
            return redirect('view_blog', blog.id)
    else:
        form = CommentForm(user=request.user)
    
    context['cform'] = form
    context['is_liked'] = blog.likes.filter(id=request.user.id).exists()
    
    return render(request, 'blog/view.html', context)

@login_required
def like_blog(request, id):
    context = {}
    blog = Blog.objects.get(id=id)
    context['blog'] = blog
    context['is_liked'] = blog.likes.filter(id=request.user.id).exists()
    
    if request.method == 'POST':
        blog.add_like(request.user)
        blog.save()
    return render(request, 'blog/partials/like.html', context)

@login_required
def my_blogs(request):
    context = {}
    
    if request.user.is_staff:
        context['blogs'] = Blog.objects.filter(user=request.user)
    
    return render(request, 'blog/my_blogs.html', context)

def all_blogs(request):
    context = {
        'cat': CATOGORIES,
        'blogs': Blog.objects.filter(is_draft=False)  
    }
    
    if request.method == 'POST':
        f = request.POST.get("filter", 'all')
        if f != 'all':
            context['blogs'] = context['blogs'].filter(cat=f)
        
        # Render the filtered results in a partial template
        return render(request, 'blog/partials/filter-res.html', context)
    
    return render(request, 'blog/all_blogs.html', context)

# TASK 3

@login_required
def all_doctors(request):
    context = {}
    context['doctors'] = Doctor.objects.filter(user__is_staff=True)
    return render(request, 'core/doc-list.html', context)


def search_doctor(request):
    context = {
        'doctors':Doctor.objects.filter(user__is_staff=True)
    }
    
    if  request.method == 'POST':
        key = request.POST.get("speciality","all")
        if key and key!='':
            context['doctors'] = context['doctors'].filter(
            models.Q(speciality__icontains=key) |
            models.Q(user__first_name__icontains=key) |
            models.Q(user__last_name__icontains=key)
        )

        
    return render(request,'core/partial/doctor-res.html',context)

@login_required
def appointment_form(request, id):
    context = {}
    
    doctor = get_object_or_404(Doctor, id=id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.doctor = doctor
            appointment.end_time = calculate_end_time(appointment.start_time)
            appointment.save()

            # Check for credentials and perform OAuth flow if necessary
            if 'credentials' not in request.session:
                request.session['appointment_id'] = appointment.id
                return redirect('google_calendar_init')
            else:
                create_calendar_event(appointment, request)
                messages.success(request, "Appointment booked successfully!!", extra_tags='success')
                return redirect('appointment_confirmation', id=appointment.id)
    else:
        form = AppointmentForm()
    context['form'] = form
    context['doctor'] = doctor
    return render(request, 'core/appointment_form.html', context)

@login_required
def appointment_confirmation(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    return render(request, 'core/appointment_confirmation.html', {'appointment': appointment})


@login_required
def visit_appointment(request,id):
    app = get_object_or_404(Appointment, id=id)
    if request.method == 'POST':
        app.is_visited = True
        app.save()
        return HttpResponse("""<button type="submit" disabled class="w-100 btn btn-secondary">Visited</button>""")
    return HttpResponse("""<button type="submit" class="w-100 btn btn-success">Mark as Visited</button>""")
    
# Google Calendar OAuth2

def google_calendar_init_view(request):
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_OAUTH2_CLIENT_ID,
                "client_secret": settings.GOOGLE_OAUTH2_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "redirect_uris": [settings.GOOGLE_OAUTH2_REDIRECT_URI],
            }
        },
        scopes=['https://www.googleapis.com/auth/calendar']
    )
    flow.redirect_uri = settings.GOOGLE_OAUTH2_REDIRECT_URI

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    request.session['state'] = state
    return redirect(authorization_url)

def google_calendar_redirect_view(request):
    state = request.session['state']
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_OAUTH2_CLIENT_ID,
                "client_secret": settings.GOOGLE_OAUTH2_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "redirect_uris": [settings.GOOGLE_OAUTH2_REDIRECT_URI],
            }
        },
        scopes=['https://www.googleapis.com/auth/calendar'],
        state=state
    )
    flow.redirect_uri = settings.GOOGLE_OAUTH2_REDIRECT_URI

    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    request.session['credentials'] = credentials_to_dict(credentials)

    appointment_id = request.session.get('appointment_id')
    print("Appoinment ID : ",appointment_id)

    if appointment_id:
        appointment = get_object_or_404(Appointment, id=appointment_id)
        create_calendar_event(appointment, request)
        del request.session['appointment_id']
        messages.success(request, "Appointment booked successfully!!",extra_tags='success')
        return redirect('appointment_confirmation', id=appointment.id)


    return redirect('all_doctors')


def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

def calculate_end_time(start_time):
    end_time = (datetime.combine(datetime.today(), start_time) + timedelta(minutes=45)).time()
    return end_time

def create_calendar_event(appointment, request):
    credentials = Credentials(**request.session['credentials'])

    service = build('calendar', 'v3', credentials=credentials)

    event = {
        'summary': f'Appointment with {appointment.doctor.user.get_full_name()}',
        'start': {
            'dateTime': f'{appointment.date}T{appointment.start_time}',
            'timeZone': settings.TIME_ZONE,  # replace with your timezone
        },
        'end': {
            'dateTime': f'{appointment.date}T{appointment.end_time}',
            'timeZone': settings.TIME_ZONE,  # replace with your timezone
        },
        'attendees': [
            {'email': appointment.patient.email},
            {'email': appointment.doctor.user.email},
        ],
    }

    service.events().insert(calendarId='primary', body=event).execute()


@login_required
def my_appoinments(request):
    
    
    context = {
        'current_time': timezone.now()
    }
    
    if request.user.is_staff:
        doc = get_object_or_404(Doctor,user=request.user)
        context['appoinments'] = Appointment.objects.filter(doctor=doc).order_by('-created')
    else:
        context['appoinments'] = Appointment.objects.filter(patient=request.user).order_by('-created')
    
    return render(request, 'core/my_appoinments.html',context)

