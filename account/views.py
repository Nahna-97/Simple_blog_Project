from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings
from .forms import UserUpdateForm
from .forms import ProfileForm
from .models import Profile

def register_view(request):
    if request.method=='POST':
        form= RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration  Successfull. Please log in")
            return redirect('login')

        else:
            print(form.errors)
            messages.error(request,'please correct the errors.')

    else:
        form=RegisterForm()
    return render(request,'account/register.html',{'form':form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)

            # Handle redirect to ?next= if exists
            next_url = request.GET.get('next')
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect('home')  # Fallback
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'account/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


def dashboard(request):
    return render(request, 'account/dashboard.html')

@login_required
def home_view(request):
    return render(request,'account/home.html')

def profile_view(request):
    if request.method=='POST':
        form=UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,"Profile Updated Successfully!")
            return redirect('profile')
        else:
            messages.error(request,"Please correct the errors")
    else:
        form=UserUpdateForm(instance=request.user)

    return render(request,'account/profile.html',{'form':form})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('dashboard')  # or 'edit_profile' to stay on the same page
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileForm(instance=request.user.profile)

    return render(request, 'account/edit_profile.html', {
        'u_form': u_form,
        'p_form': p_form
    })