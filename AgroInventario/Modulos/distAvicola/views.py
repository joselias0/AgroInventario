from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
# Create your views here.

@login_required
@csrf_protect
def salir(request):
    logout(request)
    return redirect('/')

@csrf_protect
@login_required
def index(request):
    return render(request, 'index.html')

