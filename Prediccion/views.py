from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import IntegrityError
from django.shortcuts import render, redirect
import numpy as np
from scipy.integrate import odeint
import plotly.graph_objs as go
from .forms import SEIRForm


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


def seir_model(y, t, lmbda, beta, gamma, alpha):
    S, R, D, A = y

    # Ecuaciones diferenciales
    dSdt = -lmbda * S
    dRdt = gamma * S - alpha * R
    dDdt = alpha * R - beta * D
    dAdt = beta * D

    return [dSdt, dRdt, dDdt, dAdt]


def simulate_seir(M, A0, R0, D0, days):
    lmbda = D0 / M  # Tasa de deserción λ
    beta = A0 / M  # Tasa de aprobación β
    gamma = R0 / M  # Tasa de reprobación γ
    alpha = D0 / R0  # Tasa de abandono α

    # Población inicial
    S0 = M

    # Condiciones iniciales
    y0 = [S0, R0, D0, A0]

    # Vector de tiempo (en días)
    t = np.linspace(0, days, days)

    # Integrar las ecuaciones diferenciales
    result = odeint(seir_model, y0, t, args=(lmbda, beta, gamma, alpha))

    return t, result


def seir_graph(request):
    if request.method == 'POST':
        form = SEIRForm(request.POST)
        if form.is_valid():
            # Obtener los datos del formulario
            M = form.cleaned_data['M']
            A0 = form.cleaned_data['A0']
            R0 = form.cleaned_data['R0']
            D0 = form.cleaned_data['D0']
            days = form.cleaned_data['days']

            # Simulacion del modelo SEIR
            t, result = simulate_seir(M, A0, R0, D0, days)

            # Crear los datos para Plotly
            trace1 = go.Scatter(x=t, y=result[:, 0], mode='lines', name='Matriculados')
            trace2 = go.Scatter(x=t, y=result[:, 1], mode='lines', name='Reprobados')
            trace3 = go.Scatter(x=t, y=result[:, 2], mode='lines', name='Desertores')
            trace4 = go.Scatter(x=t, y=result[:, 3], mode='lines', name='Aprobados')

            # Configurar el diseño del gráfico
            layout = go.Layout(title='Modelo SEIR', xaxis=dict(title='Días'), yaxis=dict(title='Población'))

            #Rango de los ejes
            layout.update(xaxis=dict(range=[0, days]), yaxis=dict(range=[0, 700]))


            # Crear la figura Plotly
            fig = go.Figure(data=[trace1, trace2, trace3, trace4], layout=layout)

            # Convertir la figura Plotly a JSON
            graph_json = fig.to_json()

            # Pasar la figura JSON a la plantilla
            context = {'graph_json': graph_json}
            return render(request, 'home.html', context)
    else:
        form = SEIRForm()
    return render(request, 'seir_form.html', {'form': form})
