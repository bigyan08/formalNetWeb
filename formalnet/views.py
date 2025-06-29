from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserRegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout 
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def index(request):
    return HttpResponse("This is index.")

def contact(request):
    return HttpResponse("This is contact.")

def register_page(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return render(request, 'formalnet/register_done.html', {'new_user': new_user})
    else:
        form = UserRegistrationForm()
    return render(request, 'formalnet/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('index')

    return render(request, 'formalnet/login.html', {'form': form})

def logoutUser(request):
    logout(request)
    return redirect('index')