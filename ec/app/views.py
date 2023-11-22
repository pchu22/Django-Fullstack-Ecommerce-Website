from django.shortcuts import render
from django.contrib import messages
from django.views import View
from .forms import SignupForm

# Create your views here.

def home(request):
    return render(request, 'app/home.html')

class CostumerRegistration(View):
    def get(self, request):
        form = SignupForm
        return render(request, 'app/signup.html', locals())
    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User signup successfully!")
        else:
            messages.warning(request, "Invalid input data")
        return render(request, 'app/signup.html', locals())
    
class Profile(View):
    def get(self, request):
        return render(request, 'app/profile.html', locals())
    def post(self, request):
        return render(request, 'app/profile.html', locals())