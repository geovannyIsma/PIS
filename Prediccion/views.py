from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import IntegrityError
from django.http.response import JsonResponse
from django.shortcuts import render, redirect

from Prediccion.models import MallaCurricular


# Create your views here.
def index(request):
    return render(request, 'index.html')


def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')


# Función para registrar un usuario
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect('home')
                else:
                    return render(request, 'signup.html',
                                  {'form': form, 'error': 'Autenticación fallida. Inténtalo de nuevo.'})
            except IntegrityError as e:
                form.add_error(None, 'El nombre de usuario ya existe.')
        else:
            # Aquí puedes agregar errores personalizados si es necesario
            pass
        return render(request, 'signup.html', {'form': form})
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


# Función para cerrar sesión
@login_required
def signout(request):
    logout(request)
    return redirect('index')


# Función para iniciar sesión
def signin(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        return render(request, 'signin.html', {'form': form})
    else:
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('home')
            else:
                return render(request, 'signin.html', {
                    'form': form,
                    'error': 'Username or password incorrect'
                })
        else:
            return render(request, 'signin.html', {
                'form': form,
                'error': 'Username or password incorrect'
            })


def administracion_malla(request):
    return render(request, 'administracion_malla.html')


def list_malla(_request):
    mallaCurricular = list(MallaCurricular.objects.values())
    data = {'mallaCurricular': mallaCurricular}
    return JsonResponse(data)
