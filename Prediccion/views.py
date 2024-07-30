import locale

import numpy as np
import pandas as pd
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.db import IntegrityError
from django.db.models import Sum
from django.http import HttpResponseBadRequest
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from Prediccion.decorators import admin_required
from Prediccion.forms import MallaCurricularForm, ExcelUploadForm, PeriodoForm, CustomUserCreationForm, \
    CustomUserChangeForm, HistoricoPeriodoForm
from Prediccion.models import MallaCurricular, Ciclo, Asignatura, PeriodoAcademico, Historico, CustomUser, \
    Historico_Periodo


def index(request):
    return render(request, 'index.html')


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
                return render(request, 'signin.html', {'form': form, 'error': 'Username or password incorrect'})
        return render(request, 'signin.html', {'form': form, 'error': 'Username or password incorrect'})


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.role = CustomUser.CONSULTOR  # Asignar el rol por defecto
                user.save()
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect('home')
                else:
                    return render(request, 'signup.html',
                                  {'form': form, 'error': 'Autenticación fallida. Inténtalo de nuevo.'})
            except IntegrityError:
                form.add_error(None, 'El nombre de usuario ya existe.')
        return render(request, 'signup.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def signout(request):
    logout(request)
    return redirect('index')


@admin_required
def administracion_malla(request):
    return render(request, 'administracion_malla.html')


@admin_required
def list_malla(_request):
    mallas_Curricular = list(MallaCurricular.objects.values())
    data = {'mallas_Curricular': mallas_Curricular}
    return JsonResponse(data)


@admin_required
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


@admin_required
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


@admin_required
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


@admin_required
@require_http_methods(["DELETE"])
def eliminar_malla(request, malla_id):
    malla = get_object_or_404(MallaCurricular, id=malla_id)
    malla.delete()
    return JsonResponse({'message': 'Malla eliminada correctamente'}, status=200)


@admin_required
@csrf_exempt
def procesar_excel(request):
    if request.method == 'POST':
        file = request.FILES.get('archivo')
        if not file:
            return JsonResponse({'success': False, 'message': 'No se ha seleccionado ningún archivo.'})

        try:
            df = pd.read_excel(file, header=0, skiprows=4)
            valid_dates = df.dropna(subset=['fecha_inicio', 'fecha_fin'])
            if valid_dates.empty:
                return JsonResponse({'success': False, 'message': 'No se encontraron fechas válidas en el archivo.'})

            fecha_inicio = pd.to_datetime(valid_dates.iloc[-1]['fecha_inicio']).date()
            fecha_fin = pd.to_datetime(valid_dates.iloc[-1]['fecha_fin']).date()

            malla_id = request.POST.get('malla_id')
            if not malla_id:
                return JsonResponse({'success': False, 'message': 'Malla curricular no seleccionada.'})
            malla = MallaCurricular.objects.get(id=malla_id)

            ciclos_validos = Ciclo.objects.filter(malla_curricular=malla).values_list('nombre_ciclo', flat=True)

            historico_data = df.to_dict('records')
            historico = []
            for row in historico_data:
                if row['ciclo'] not in ciclos_validos:
                    return JsonResponse({'success': False,
                                         'message': f"El ciclo {row['ciclo']} no es válido para la malla seleccionada."})
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


@admin_required
def importar_datos_periodo_historico(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        historico_periodo_form = HistoricoPeriodoForm(request.POST)

        if form.is_valid():
            malla = form.cleaned_data['malla']
            archivo_excel = request.FILES['archivo_excel']

            fs = FileSystemStorage()
            filename = fs.save(archivo_excel.name, archivo_excel)
            file_url = fs.url(filename)

            try:
                df = pd.read_excel(fs.path(filename), header=0, skiprows=4)
                valid_dates = df.dropna(subset=['fecha_inicio', 'fecha_fin'])
                if valid_dates.empty:
                    return JsonResponse(
                        {'success': False, 'message': 'No se encontraron fechas válidas en el archivo.'})

                fecha_inicio = pd.to_datetime(valid_dates.iloc[-1]['fecha_inicio']).date()
                fecha_fin = pd.to_datetime(valid_dates.iloc[-1]['fecha_fin']).date()

                # Configurar el locale en español
                locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

                codigo_periodo = f"{fecha_inicio.strftime('%B %Y')} - {fecha_fin.strftime('%B %Y')}"

                # Restaurar el locale por defecto
                locale.setlocale(locale.LC_TIME, 'C')

                periodo, created = PeriodoAcademico.objects.update_or_create(
                    codigo_periodo=codigo_periodo,
                    defaults={'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin}
                )

                ciclos_validos = Ciclo.objects.filter(malla_curricular=malla).values_list('nombre_ciclo', flat=True)

                historicos = []
                for _, row in df.iterrows():
                    if row['ciclo'] not in ciclos_validos:
                        return JsonResponse({'success': False,
                                             'message': f"El ciclo {row['ciclo']} no es válido para la malla seleccionada."})

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
                            return JsonResponse(
                                {'success': False, 'message': f"Error en el ciclo {ciclo.nombre_ciclo}: {e}"})

                Historico.objects.bulk_create(historicos)

                if historico_periodo_form.is_valid():
                    historico_periodo = historico_periodo_form.save(commit=False)
                    historico_periodo.periodo_academico = periodo
                    historico_periodo.save()

                return JsonResponse({'success': True, 'message': 'Datos importados exitosamente.'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': f'Error al procesar el archivo: {e}'})
            finally:
                fs.delete(filename)
        else:
            return JsonResponse({'success': False, 'message': 'Formulario no válido.'})
    else:
        form = ExcelUploadForm()
        historico_periodo_form = HistoricoPeriodoForm()

    mallas = MallaCurricular.objects.all()
    return render(request, 'import_data.html',
                  {'form': form, 'historico_periodo_form': historico_periodo_form, 'mallas': mallas})


@admin_required
def list_periodos_historicos(request):
    periodos = list(PeriodoAcademico.objects.values())
    data = {'periodos': periodos}
    return JsonResponse(data)


@admin_required
def administracion_periodo(request):
    return render(request, 'administracion_registros_periodos.html')


@login_required
def editar_datos_periodo_historico(request, periodo_id):
    periodo = get_object_or_404(PeriodoAcademico, id=periodo_id)
    historico_periodo = get_object_or_404(Historico_Periodo, periodo_academico=periodo)

    if request.method == 'POST':
        periodo_form = PeriodoForm(request.POST, instance=periodo)
        historico_periodo_form = HistoricoPeriodoForm(request.POST, instance=historico_periodo)

        if periodo_form.is_valid() and historico_periodo_form.is_valid():
            periodo_form.save()
            historico_periodo_form.save()

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
                    return JsonResponse(
                        {'success': False, 'message': f"Error en el ciclo {historico.ciclo.nombre_ciclo}: {e}"})

            Historico.objects.bulk_update(historicos,
                                          ['matriculados', 'reprobados', 'abandonaron', 'aprobados', 'aplazadores',
                                           'desertores'])

            return JsonResponse({'success': True, 'message': 'Datos del periodo actualizados exitosamente.'})
        else:
            return JsonResponse({'success': False, 'message': 'Formulario no válido.'})
    else:
        periodo.fecha_inicio = periodo.fecha_inicio.strftime('%Y-%m-%d')
        periodo.fecha_fin = periodo.fecha_fin.strftime('%Y-%m-%d')
        periodo_form = PeriodoForm(instance=periodo)
        historico_periodo_form = HistoricoPeriodoForm(instance=historico_periodo)

    historicos = periodo.historico_set.all()
    context = {
        'periodo': periodo,
        'periodo_form': periodo_form,
        'historico_periodo_form': historico_periodo_form,
        'historicos': historicos
    }
    return render(request, 'editar_periodo.html', context)


@admin_required
def eliminar_datos_periodo_historico(request, periodo_id):
    periodo = get_object_or_404(PeriodoAcademico, id=periodo_id)
    periodo.delete()
    return JsonResponse({'message': 'Periodo eliminado correctamente'}, status=200)


def modelo_matematico(request):
    return render(request, 'modelo_matematico.html')


User = get_user_model()


@admin_required
def administracion_usuarios(request):
    return render(request, 'administracion_usuarios.html')


@admin_required
def list_usuarios(request):
    usuarios = list(User.objects.filter(is_superuser=False, is_staff=False).values())
    data = {'usuarios': usuarios}
    return JsonResponse(data)


@admin_required
def nuevo_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('administracion_usuarios')
    else:
        form = CustomUserCreationForm()
    return render(request, 'nuevo_usuario.html', {'form': form})


@admin_required
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id, is_superuser=False, is_staff=False)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('administracion_usuario')
    else:
        form = CustomUserChangeForm(instance=usuario)
    return render(request, 'edit_user.html', {'form': form, 'usuario': usuario})


@admin_required
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id, is_superuser=False, is_staff=False)
    usuario.delete()
    return JsonResponse({'message': 'Usuario eliminado correctamente'}, status=200)


def dashboard_view(request):
    historico_data = Historico.objects.aggregate(
        total_matriculados=Sum('matriculados'),
        total_reprobados=Sum('reprobados'),
        total_abandonaron=Sum('abandonaron'),
        total_aprobados=Sum('aprobados'),
        total_aplazadores=Sum('aplazadores'),
        total_desertores=Sum('desertores')
    )

    historicos = Historico.objects.order_by('periodo_academico__fecha_inicio')
    periodos = [h.periodo_academico.codigo_periodo for h in historicos]
    matriculados = [h.matriculados for h in historicos]
    desertores = [h.desertores for h in historicos]

    context = {
        'total_matriculados': historico_data['total_matriculados'] or 0,
        'total_reprobados': historico_data['total_reprobados'] or 0,
        'total_abandonaron': historico_data['total_abandonaron'] or 0,
        'total_aprobados': historico_data['total_aprobados'] or 0,
        'total_aplazadores': historico_data['total_aplazadores'] or 0,
        'total_desertores': historico_data['total_desertores'] or 0,
        'periodos': periodos,
        'matriculados': matriculados,
        'desertores': desertores,
    }

    return render(request, 'home.html', context)


def about(request):
    return render(request, 'about.html')


def mcmc(lista, num_sim=12):
    if len(lista) < 2:
        # Añadir variabilidad para listas muy pequeñas o constantes
        base_valor = lista[-1] if lista else 0
        variabilidad = base_valor * 0.05  # 5% de variabilidad
        valores_futuros = [base_valor + np.random.uniform(-variabilidad, variabilidad) for _ in range(num_sim)]
    else:
        difer = np.diff(lista)
        media = np.mean(difer)
        desviacion = np.std(difer)

        if desviacion == 0:  # Caso de datos constantes
            variabilidad = media * 0.05  # 5% de variabilidad
            valores_futuros = [lista[-1] + media + np.random.uniform(-variabilidad, variabilidad) for _ in
                               range(num_sim)]
        else:
            valores_futuros = []
            for _ in range(num_sim):
                nueva_diferencia = np.random.normal(media, desviacion)
                nuevo_valor = lista[-1] + nueva_diferencia
                valores_futuros.append(nuevo_valor)
    return valores_futuros


def predicciones_view(request):
    # Configurar el locale en español
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

    # Obtener lista de ciclos disponibles
    ciclos = Ciclo.objects.all()

    # Obtener ciclo seleccionado
    ciclo_id = request.GET.get('ciclo', ciclos.first().id)
    ciclo_seleccionado = get_object_or_404(Ciclo, id=ciclo_id)

    # Filtrar datos históricos por ciclo seleccionado
    historicos = Historico.objects.filter(ciclo=ciclo_seleccionado).order_by('id')

    if historicos.exists():
        periodos_ciclo = [h.periodo_academico.codigo_periodo for h in historicos]
        matriculados_ciclo = [h.matriculados for h in historicos]
        reprobados_ciclo = [h.reprobados for h in historicos]
        abandonaron_ciclo = [h.abandonaron for h in historicos]
        aprobados_ciclo = [h.aprobados for h in historicos]
        aplazadores_ciclo = [h.aplazadores for h in historicos]
        desertores_ciclo = [h.desertores for h in historicos]

        # Realizar predicciones por ciclo
        prediccion_matriculados_ciclo = mcmc(matriculados_ciclo)
        prediccion_reprobados_ciclo = mcmc(reprobados_ciclo)
        prediccion_abandonaron_ciclo = mcmc(abandonaron_ciclo)
        prediccion_aprobados_ciclo = mcmc(aprobados_ciclo)
        prediccion_aplazadores_ciclo = mcmc(aplazadores_ciclo)
        prediccion_desertores_ciclo = mcmc(desertores_ciclo)

        # Generar nuevos periodos para ciclo
        ultimos_periodo_ciclo = historicos.last().periodo_academico
        fecha_inicio = ultimos_periodo_ciclo.fecha_fin
        nuevos_periodos_ciclo = [
            f"{(fecha_inicio + pd.DateOffset(months=i * 6)).strftime('%B %Y')} - {(fecha_inicio + pd.DateOffset(months=(i + 1) * 6 - 1)).strftime('%B %Y')}"
            for i in range(12)
        ]
    else:
        periodos_ciclo = []
        matriculados_ciclo = []
        reprobados_ciclo = []
        abandonaron_ciclo = []
        aprobados_ciclo = []
        aplazadores_ciclo = []
        desertores_ciclo = []
        nuevos_periodos_ciclo = []
        prediccion_matriculados_ciclo = []
        prediccion_reprobados_ciclo = []
        prediccion_abandonaron_ciclo = []
        prediccion_aprobados_ciclo = []
        prediccion_aplazadores_ciclo = []
        prediccion_desertores_ciclo = []

    # Obtener datos históricos por período académico
    historicos_periodo = Historico_Periodo.objects.all().order_by('periodo_academico__fecha_inicio')

    if historicos_periodo.exists():
        periodos_periodo = [h.periodo_academico.codigo_periodo for h in historicos_periodo]
        matriculados_periodo = [h.matriculados for h in historicos_periodo]
        reprobados_periodo = [h.reprobados for h in historicos_periodo]
        abandonaron_periodo = [h.abandonaron for h in historicos_periodo]
        aprobados_periodo = [h.aprobados for h in historicos_periodo]
        aplazadores_periodo = [h.aplazadores for h in historicos_periodo]
        desertores_periodo = [h.desertores for h in historicos_periodo]

        # Realizar predicciones por período académico
        prediccion_matriculados_periodo = mcmc(matriculados_periodo)
        prediccion_reprobados_periodo = mcmc(reprobados_periodo)
        prediccion_abandonaron_periodo = mcmc(abandonaron_periodo)
        prediccion_aprobados_periodo = mcmc(aprobados_periodo)
        prediccion_aplazadores_periodo = mcmc(aplazadores_periodo)
        prediccion_desertores_periodo = mcmc(desertores_periodo)

        # Generar nuevos periodos para período académico
        ultimos_periodo_periodo = historicos_periodo.last().periodo_academico
        fecha_inicio = ultimos_periodo_periodo.fecha_fin
        nuevos_periodos_periodo = [
            f"{(fecha_inicio + pd.DateOffset(months=i * 6)).strftime('%B %Y')} - {(fecha_inicio + pd.DateOffset(months=(i + 1) * 6 - 1)).strftime('%B %Y')}"
            for i in range(12)
        ]
    else:
        periodos_periodo = []
        matriculados_periodo = []
        reprobados_periodo = []
        abandonaron_periodo = []
        aprobados_periodo = []
        aplazadores_periodo = []
        desertores_periodo = []
        nuevos_periodos_periodo = []
        prediccion_matriculados_periodo = []
        prediccion_reprobados_periodo = []
        prediccion_abandonaron_periodo = []
        prediccion_aprobados_periodo = []
        prediccion_aplazadores_periodo = []
        prediccion_desertores_periodo = []

    context = {
        'ciclos': ciclos,
        'ciclo_seleccionado': ciclo_seleccionado,
        'periodos_ciclo': periodos_ciclo,
        'matriculados_ciclo': matriculados_ciclo,
        'reprobados_ciclo': reprobados_ciclo,
        'abandonaron_ciclo': abandonaron_ciclo,
        'aprobados_ciclo': aprobados_ciclo,
        'aplazadores_ciclo': aplazadores_ciclo,
        'desertores_ciclo': desertores_ciclo,
        'nuevos_periodos_ciclo': nuevos_periodos_ciclo,
        'prediccion_matriculados_ciclo': prediccion_matriculados_ciclo,
        'prediccion_reprobados_ciclo': prediccion_reprobados_ciclo,
        'prediccion_abandonaron_ciclo': prediccion_abandonaron_ciclo,
        'prediccion_aprobados_ciclo': prediccion_aprobados_ciclo,
        'prediccion_aplazadores_ciclo': prediccion_aplazadores_ciclo,
        'prediccion_desertores_ciclo': prediccion_desertores_ciclo,
        'periodos_periodo': periodos_periodo,
        'matriculados_periodo': matriculados_periodo,
        'reprobados_periodo': reprobados_periodo,
        'abandonaron_periodo': abandonaron_periodo,
        'aprobados_periodo': aprobados_periodo,
        'aplazadores_periodo': aplazadores_periodo,
        'desertores_periodo': desertores_periodo,
        'nuevos_periodos_periodo': nuevos_periodos_periodo,
        'prediccion_matriculados_periodo': prediccion_matriculados_periodo,
        'prediccion_reprobados_periodo': prediccion_reprobados_periodo,
        'prediccion_abandonaron_periodo': prediccion_abandonaron_periodo,
        'prediccion_aprobados_periodo': prediccion_aprobados_periodo,
        'prediccion_aplazadores_periodo': prediccion_aplazadores_periodo,
        'prediccion_desertores_periodo': prediccion_desertores_periodo,
    }

    # Restaurar el locale por defecto
    locale.setlocale(locale.LC_TIME, 'C')

    return render(request, 'prediccion.html', context)
