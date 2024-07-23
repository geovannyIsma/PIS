import json
import pandas as pd
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.messages import get_messages
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.db import IntegrityError
from django.http import HttpResponseBadRequest
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from Prediccion.forms import MallaCurricularForm, ExcelUploadForm, PeriodoForm
from Prediccion.models import MallaCurricular, Ciclo, Asignatura, PeriodoAcademico, Historico


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

                return render(request, 'confirmar_malla.html', {'success': True})
            except Exception as e:
                return render(request, 'confirmar_malla.html', {'error': str(e)})
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

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': malla_form.errors})

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

@login_required
@require_http_methods(["DELETE"])
def eliminar_malla(request, malla_id):
    malla = get_object_or_404(MallaCurricular, id=malla_id)
    malla.delete()
    return JsonResponse({'message': 'Malla eliminada correctamente'}, status=200)


@login_required
@csrf_exempt
def procesar_excel(request):
    if request.method == 'POST':
        file = request.FILES.get('archivo')
        if not file:
            return JsonResponse({'success': False, 'message': 'No se ha seleccionado ningún archivo.'})

        try:
            df = pd.read_excel(file, header=0, skiprows=8)
            valid_dates = df.dropna(subset=['fecha_inicio', 'fecha_fin'])
            if valid_dates.empty:
                return JsonResponse({'success': False, 'message': 'No se encontraron fechas válidas en el archivo.'})

            fecha_inicio = valid_dates.iloc[-1]['fecha_inicio']
            fecha_fin = valid_dates.iloc[-1]['fecha_fin']

            # Obtener la malla seleccionada desde el frontend
            malla_id = request.POST.get('malla_id')
            if not malla_id:
                return JsonResponse({'success': False, 'message': 'Malla curricular no seleccionada.'})
            malla = MallaCurricular.objects.get(id=malla_id)

            ciclos_validos = Ciclo.objects.filter(malla_curricular=malla).values_list('nombre_ciclo', flat=True)

            historico_data = df.to_dict('records')
            historico = []
            for row in historico_data:
                if row['ciclo'] not in ciclos_validos:
                    return JsonResponse({'success': False, 'message': f"El ciclo {row['ciclo']} no es válido para la malla seleccionada."})
                historico.append(
                    {
                        'ciclo': row['ciclo'],
                        'matriculados': row['matriculados'],
                        'aprobados': row['aprobados'],
                        'reprobados': row['reprobados'],
                        'aplazadores': row['aplazadores'],
                        'abandonaron': row['abandonaron'],
                        'desertores': row['desertores']
                    }
                )

            response_data = {
                'success': True,
                'fecha_inicio': fecha_inicio.isoformat(),
                'fecha_fin': fecha_fin.isoformat(),
                'historico': historico,
                'message': 'Archivo procesado exitosamente.'
            }
            return JsonResponse(response_data)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return JsonResponse({'success': False, 'message': 'Método no permitido.'})


@login_required
def importar_datos_periodo_historico(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            malla = form.cleaned_data['malla']
            archivo_excel = request.FILES['archivo_excel']

            fs = FileSystemStorage()
            filename = fs.save(archivo_excel.name, archivo_excel)
            file_url = fs.url(filename)

            try:
                df = pd.read_excel(fs.path(filename), header=0, skiprows=8)
                valid_dates = df.dropna(subset=['fecha_inicio', 'fecha_fin'])
                if valid_dates.empty:
                    return JsonResponse({'success': False, 'message': 'No se encontraron fechas válidas en el archivo.'})

                fecha_inicio = valid_dates.iloc[-1]['fecha_inicio']
                fecha_fin = valid_dates.iloc[-1]['fecha_fin']

                periodo, created = PeriodoAcademico.objects.update_or_create(
                    codigo_periodo=f"{fecha_inicio.year}-{malla.codigo}",
                    defaults={'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin}
                )

                ciclos_validos = Ciclo.objects.filter(malla_curricular=malla).values_list('nombre_ciclo', flat=True)

                historicos = []
                for _, row in df.iterrows():
                    if row['ciclo'] not in ciclos_validos:
                        return JsonResponse({'success': False, 'message': f"El ciclo {row['ciclo']} no es válido para la malla seleccionada."})

                    ciclo = Ciclo.objects.filter(nombre_ciclo=row['ciclo'], malla_curricular=malla).first()

                    if ciclo:
                        historico = Historico(
                            matriculados=row['matriculados'],
                            reprobados=row['reprobados'],
                            abandonaron=row['abandonaron'],
                            aprobados=row['aprobados'],
                            aplazadores=row['aplazadores'],
                            desertores=row['desertores'],
                            ciclo=ciclo,
                            periodo_academico=periodo
                        )
                        try:
                            historico.clean()
                            historicos.append(historico)
                        except ValidationError as e:
                            return JsonResponse({'success': False, 'message': f"Error en el ciclo {ciclo.nombre_ciclo}: {e}"})

                Historico.objects.bulk_create(historicos)

                return JsonResponse({'success': True, 'message': 'Datos importados exitosamente.'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': f'Error al procesar el archivo: {e}'})
            finally:
                fs.delete(filename)
        else:
            return JsonResponse({'success': False, 'message': 'Formulario no válido.'})
    else:
        form = ExcelUploadForm()

    mallas = MallaCurricular.objects.all()
    return render(request, 'import_data.html', {'form': form, 'mallas': mallas})


def list_periodos_historicos(request):
    periodos = list(PeriodoAcademico.objects.values())
    data = {'periodos': periodos}
    return JsonResponse(data)


def administracion_periodo(request):
    return render(request, 'administracion_registros_periodos.html')


@login_required
def editar_datos_periodo_historico(request, periodo_id):
    periodo = get_object_or_404(PeriodoAcademico, id=periodo_id)
    if request.method == 'POST':
        periodo_form = PeriodoForm(request.POST, instance=periodo)
        if periodo_form.is_valid():
            periodo_form.save()

            historicos = []
            for historico in periodo.historico_set.all():
                historico.matriculados = request.POST.get(f'matriculados_{historico.id}')
                historico.reprobados = request.POST.get(f'reprobados_{historico.id}')
                historico.abandonaron = request.POST.get(f'abandonaron_{historico.id}')
                historico.aprobados = request.POST.get(f'aprobados_{historico.id}')
                historico.aplazadores = request.POST.get(f'aplazadores_{historico.id}')
                historico.desertores = request.POST.get(f'desertores_{historico.id}')

                try:
                    historico.clean()
                    historicos.append(historico)
                except ValidationError as e:
                    return JsonResponse({'success': False, 'message': f"Error en el ciclo {historico.ciclo.nombre_ciclo}: {e}"})

            Historico.objects.bulk_update(historicos, ['matriculados', 'reprobados', 'abandonaron', 'aprobados', 'aplazadores', 'desertores'])

            return JsonResponse({'success': True, 'message': 'Datos del periodo actualizados exitosamente.'})
        else:
            return JsonResponse({'success': False, 'message': 'Formulario no válido.'})

    else:
        periodo_form = PeriodoForm(instance=periodo)

    historicos = periodo.historico_set.all()
    context = {
        'periodo': periodo,
        'periodo_form': periodo_form,
        'historicos': historicos
    }
    return render(request, 'editar_periodo.html', context)


@login_required
def eliminar_datos_periodo_historico(request, periodo_id):
    periodo = get_object_or_404(PeriodoAcademico, id=periodo_id)
    periodo.delete()
    return JsonResponse({'message': 'Periodo eliminado correctamente'}, status=200)


def modelo_matematico(request):
    return render(request, 'modelo_matematico.html')