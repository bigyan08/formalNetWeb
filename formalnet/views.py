from django.shortcuts import render,redirect
from .forms import UserRegistrationForm 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout 
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
import requests
from .models import Prompts
from django.shortcuts import get_object_or_404
# Create your views here.

def index(request):
    output = None
    informal_text = request.GET.get("informal","")

    if request.method == "POST":
        input_text = request.POST.get("input_text", "")
        if input_text:
            try:
                response = requests.post(
                    "http://localhost:8000/convert/",
                    json={"text": input_text,"user-id":request.user.id if request.user.is_authenticated else None}
                )
                if response.status_code == 200:
                    output = response.json().get("output")
                else:
                    output = f"Error: {response.status_code}"
            except requests.exceptions.RequestException as e:
                output = f"Connection error: {e}"

    return render(request, "formalnet/index.html", {"output": output,"user_id":request.user.id if request.user.is_authenticated else None,"informal_text":informal_text})

def register_page(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return render(request, 'formalnet/register_done.html', {'new_user': new_user})
        else:
            messages.error(request,'User registration invalid!')
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

@login_required
def save_prompt(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            informal = data.get("input")
            formal = data.get("output")

            if not informal or not formal:
                return JsonResponse({"error": "Missing data."}, status=400)

            Prompts.objects.create(
                author=request.user,
                input_text=informal,
                output_text=formal
            )

            return JsonResponse({"message": "Prompt saved."}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid method"}, status=405)


@login_required
def profile_view(request,pk):
    user = User.objects.get(id=pk)
    prompts = Prompts.objects.filter(author=request.user).order_by('-created_at')
    paginate = 5
    context = {'user': user, 'prompts':prompts}
    return render(request,'formalnet/profile.html',context)

@login_required
def delete_prompt(request,prompt_id):
    prompt = get_object_or_404(Prompts,id=prompt_id,author=request.user)
    if request.method == 'POST':
        prompt.delete()
        return redirect('user-profile',request.user.id)

    return redirect('user-profile',request.user.id)
  

