from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from .forms import UserRegisterForm, PriorityForm
from django.http import JsonResponse

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            gender = form.cleaned_data['gender']
            user = User.objects.create_user(username=username, password=password)
            Profile.objects.create(user=user, gender=gender)
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def dashboard_view(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = PriorityForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
    else:
        form = PriorityForm(instance=profile)

    matches_count = Profile.objects.exclude(user=request.user).count()
    return render(request, 'dashboard.html', {'form': form, 'matches_count': matches_count})

@login_required
def update_priority(request):
    if request.method == 'POST':
        value = request.POST.get('priority')
        profile = Profile.objects.get(user=request.user)
        profile.priority = int(value)
        profile.save()
        matches = Profile.objects.exclude(user=request.user).count()
        return JsonResponse({'matches': matches})
