from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import IntegrityError
from django.http import HttpResponseBadRequest
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from Prediccion.forms import MallaCurricularForm
from Prediccion.models import MallaCurricular, Ciclo, Asignatura


def index(request):
    """
    Renderiza la página de inicio.

    Esta función de vista maneja la renderización de la página de inicio. No requiere
    ningún contexto o parámetro específico y siempre renderiza la plantilla 'index.html'.

    Args:
        request: Objeto HttpRequest que representa la solicitud actual.

    Returns:
        Objeto HttpResponse con la plantilla 'index.html' renderizada.
    """
    return render(request, 'index.html')


def home(request):
    """
    Renderiza la página de inicio para usuarios autenticados.

    Esta vista verifica si el usuario está autenticado. Si el usuario está autenticado,
    renderiza la plantilla 'home.html'. Si el usuario no está autenticado, no devuelve
    nada, denegando implícitamente el acceso a la página de inicio para usuarios no autenticados.

    Args:
        request: Objeto HttpRequest que representa la solicitud actual.

    Returns:
        Objeto HttpResponse con la plantilla 'home.html' renderizada si el usuario está autenticado.
    """
    if request.user.is_authenticated:
        return render(request, 'home.html')


def signup(request):
    """
    Maneja las solicitudes de registro de usuarios.

    Este método de vista procesa tanto solicitudes GET como POST. Para una solicitud GET, muestra
    el formulario de registro. Para una solicitud POST, intenta crear un nuevo usuario basado en los datos del formulario.
    Si el usuario se crea y autentica con éxito, se redirige a la página de inicio. Si hay un error
    (por ejemplo, el nombre de usuario ya existe), el formulario de registro se vuelve a renderizar con
    un mensaje de error apropiado.

    Args:
        request: Objeto HttpRequest que representa la solicitud actual.

    Returns:
        Objeto HttpResponse que renderiza la plantilla 'signup.html'. Para un registro exitoso,
        redirige a la vista 'home'. Para una solicitud GET o un intento de registro fallido, renderiza el
        formulario de registro con cualquier mensaje de error relevante.
    """
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
    mallas_Curricular = list(MallaCurricular.objects.values())
    data = {'mallas_Curricular': mallas_Curricular}
    return JsonResponse(data)

@login_required
def nueva_malla(request):
    if request.method == 'POST':
        malla_form = MallaCurricularForm(request.POST)
        if malla_form.is_valid():
            malla = malla_form.save(commit=False)

            num_cycles = int(request.POST.get('num_cycles'))
            ciclos_data = []

            for ciclo_index in range(1, num_cycles + 1):
                num_subjects = int(request.POST.get(f'num_subjects_{ciclo_index}'))
                subjects = []

                for subject_index in range(1, num_subjects + 1):
                    codigo_asignatura = request.POST.get(f'codigo_asignatura_{ciclo_index}_{subject_index}')
                    nombre_asignatura = request.POST.get(f'nombre_asignatura_{ciclo_index}_{subject_index}')

                    subjects.append({
                        'codigo_asignatura': codigo_asignatura,
                        'nombre_asignatura': nombre_asignatura
                    })

                ciclo_data = {
                    'nombre_ciclo': f'Ciclo {ciclo_index}',
                    'subjects': subjects
                }
                ciclos_data.append(ciclo_data)

            request.session['malla_data'] = {
                'codigo': malla.codigo,
                'nombre_malla': malla.nombre_malla,
                'tituloOtorgado': malla.tituloOtorgado
            }
            request.session['ciclos_data'] = ciclos_data

            return redirect('confirmar_malla')

    else:
        malla_form = MallaCurricularForm()

    return render(request, 'nueva_malla.html', {'malla_form': malla_form})


@login_required
def confirmar_malla(request):
    if request.method == 'POST':
        malla_data = request.session.get('malla_data')
        ciclos_data = request.session.get('ciclos_data')

        if malla_data and ciclos_data:
            try:
                malla = MallaCurricular.objects.create(
                    codigo=malla_data['codigo'],
                    nombre_malla=malla_data['nombre_malla'],
                    tituloOtorgado=malla_data['tituloOtorgado']
                )

                for ciclo_data in ciclos_data:
                    ciclo = Ciclo.objects.create(
                        nombre_ciclo=ciclo_data['nombre_ciclo'],
                        malla_curricular=malla
                    )
                    for subject_data in ciclo_data['subjects']:
                        Asignatura.objects.create(
                            codigo_asignatura=subject_data['codigo_asignatura'],
                            nombre_asignatura=subject_data['nombre_asignatura'],
                            ciclo=ciclo
                        )

                request.session.pop('malla_data')
                request.session.pop('ciclos_data')

                return redirect('administracion_malla')
            except Exception as e:
                return HttpResponseBadRequest("Error al guardar la malla curricular: " + str(e))
        else:
            return HttpResponseBadRequest("No se encontraron datos de malla o ciclos en la sesión.")
    else:
        malla_data = request.session.get('malla_data')
        ciclos_data = request.session.get('ciclos_data')

        if malla_data and ciclos_data:
            return render(request, 'confirmar_malla.html', {
                'malla_data': malla_data,
                'ciclos_data': ciclos_data
            })
        else:
            return HttpResponseBadRequest("No se encontraron datos de malla o ciclos en la sesión.")


@login_required
def editar_malla(request, malla_id):
    malla = get_object_or_404(MallaCurricular, id=malla_id)

    if request.method == 'POST':
        malla_form = MallaCurricularForm(request.POST, instance=malla)

        if malla_form.is_valid():
            malla_form.save()

            for ciclo in malla.ciclo_set.all():
                nombre_ciclo = request.POST.get(f'nombre_ciclo_{ciclo.id}')
                ciclo.nombre_ciclo = nombre_ciclo
                ciclo.save()

                for asignatura in ciclo.asignatura_set.all():
                    codigo_asignatura = request.POST.get(f'codigo_asignatura_{asignatura.id}')
                    nombre_asignatura = request.POST.get(f'nombre_asignatura_{asignatura.id}')
                    asignatura.codigo_asignatura = codigo_asignatura
                    asignatura.nombre_asignatura = nombre_asignatura
                    asignatura.save()

            messages.success(request, 'Malla curricular actualizada exitosamente.')
            return redirect('administracion_malla')

    else:
        malla_form = MallaCurricularForm(instance=malla)

    ciclos_data = [
        {
            'id': ciclo.id,
            'nombre_ciclo': ciclo.nombre_ciclo,
            'subjects': [
                {
                    'id': asignatura.id,
                    'codigo_asignatura': asignatura.codigo_asignatura,
                    'nombre_asignatura': asignatura.nombre_asignatura
                } for asignatura in ciclo.asignatura_set.all()
            ]
        } for ciclo in malla.ciclo_set.all()
    ]

    return render(request, 'editar_malla.html', {
        'malla_form': malla_form,
        'malla': malla,
        'ciclos_data': ciclos_data,
    })


@require_http_methods(["DELETE"])
def eliminar_malla(request, malla_id):
    malla = get_object_or_404(MallaCurricular, id=malla_id)
    malla.delete()
    return JsonResponse({'message': 'Malla eliminada correctamente'}, status=200)
