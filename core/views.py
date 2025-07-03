from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def home(request):
    # This path still works perfectly!
    return render(request, "core/home.html")