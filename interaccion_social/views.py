from gestion_usuarios.models import models
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required,permission_required
from django.shortcuts import render, redirect,get_object_or_404
from .forms import T_ProyectosForm, IntSocSettingsForm, FaseProyectoForm,TipoProyectoForm
from .forms import FaseProyectoForm, GestionForm, SemestreForm,MateriaForm, EditarT_ProyectosForm
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.paginator import Paginator
from .models import T_Proyectos_IIISP, T_Gestion, T_Semestre, T_Materia, HabilitarFechas, T_Tipo, T_Fase
from django.contrib.auth.models import User
from datetime import date

#permisos de grupo
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator   
from django.core.exceptions import PermissionDenied  

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from datetime import date


User = get_user_model()

#docentes interaccion social permigroup
def permiso_I_S(user, ADMIIISP):
    try:
        grupo = Group.objects.get(name=ADMIIISP)
    except Group.DoesNotExist:
        raise PermissionDenied(f"El grupo '{ADMIIISP}' no existe.")
    
    if grupo in user.groups.all():
        return True
    else:
        raise PermissionDenied

#permiso para docentes  
def permiso_Docentes(user, Docentes):
    try:
        grupo = Group.objects.get(name=Docentes)
    except Group.DoesNotExist:
        raise PermissionDenied(f"El grupo '{Docentes}' no existe.")
    
    if grupo in user.groups.all():
        return True
    else:
        raise PermissionDenied

#vista 403
def handle_permission_denied(request, exception):
    return render(request, '403.html', status=403)

# vista de acceso publico
def hometrabajos(request):
    return render(request, 'homesocial/hometrabajos.html')

#formulario de agregacion docentes I.S.
@user_passes_test(lambda u: permiso_Docentes(u, 'Docentes')) 
def proyecto_detail(request):
    settings = HabilitarFechas.objects.first()
    hoy = date.today()
    habilitado = settings and (settings.fecha_inicio_habilitacion <= hoy <= settings.fecha_fin_habilitacion)
    tiempo_restante = settings.tiempo_restante() if settings else "0 tiempo"

    if request.method == 'POST':
        form = T_ProyectosForm(request.POST, request.FILES)
        if habilitado and form.is_valid():
            proyecto = form.save(commit=False)  # No guardar todavía la instancia del modelo
            proyecto.S_persona = User.objects.get(nombre=request.user.nombre)  # Asignar la persona relacionada con el usuario autenticado
            proyecto.save()  # Ahora guardar la instancia del modelo
            return redirect('dashboard')  # Asegúrate de que 'dashboard' sea el nombre correcto de tu vista para el dashboard
    else:
        form = T_ProyectosForm()

    return render(request, 'homesocial/proyecto_detail.html', {
        'form': form,
        'habilitado': habilitado,
        'tiempo_restante': tiempo_restante,
    })
#editar proyectos 
@login_required
def editar_proyecto(request, Id_Proyect):
    # Obtener el proyecto específico o devolver un 404 si no se encuentra
    proyecto = get_object_or_404(T_Proyectos_IIISP, Id_Proyect=Id_Proyect)
    
    # Obtener las configuraciones de fechas
    settings = HabilitarFechas.objects.first()
    hoy = date.today()
    habilitado = settings and (settings.fecha_inicio_habilitacion <= hoy <= settings.fecha_fin_habilitacion)
    
    if request.method == 'POST':
        form = EditarT_ProyectosForm(request.POST, request.FILES, instance=proyecto)
        if habilitado and form.is_valid():
            form.save()  # Guardar los cambios
            return redirect('proyectosin_so')  # Redirigir al dashboard u otra vista adecuada
    else:
        form = EditarT_ProyectosForm(instance=proyecto)
    
    return render(request, 'homesocial/editar_proyecto.html', {
        'form': form,
        'habilitado': habilitado,
    })

#clasificacion de enviados y no enviados
@user_passes_test(lambda u: permiso_I_S(u, 'ADMIIISP')) 
def clasificar_proyectos(request):
    gestion_id = request.GET.get('gestion')
    materias = T_Materia.objects.all()
    gestiones = T_Gestion.objects.all()

    materias_con_proyectos = []
    materias_sin_proyectos = []

    for materia in materias:
        if gestion_id:
            proyectos = T_Proyectos_IIISP.objects.filter(T_Materia=materia, T_Gestion_id=gestion_id)
        else:
            proyectos = T_Proyectos_IIISP.objects.filter(T_Materia=materia)

        if proyectos.exists():
            materias_con_proyectos.append(materia)
        else:
            materias_sin_proyectos.append(materia)
    
    return render(request, 'homesocial/clasificar_proyectos.html', {
        'materias_con_proyectos': materias_con_proyectos,
        'materias_sin_proyectos': materias_sin_proyectos,
        'gestiones': gestiones,
        'selected_gestion': gestion_id
    })
    
#asignacion de fechas para subir trabajos
@user_passes_test(lambda u: permiso_I_S(u, 'ADMIIISP')) 
def inv_soc_settings(request):
    settings = HabilitarFechas.objects.first()
    if not settings:
        settings =  HabilitarFechas()

    if request.method == 'POST':
        form = IntSocSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = IntSocSettingsForm(instance=settings)
    
    return render(request, 'homesocial/inv_soc_settings.html', {'form': form})

#vista del proyecto I.S. para docentes
@login_required
@user_passes_test(lambda u: permiso_Docentes(u, 'Docentes')) 
def proyectosin_so(request):
    persona = request.user
    proyectos = T_Proyectos_IIISP.objects.filter(S_persona=persona).order_by('-Id_Proyect')
    
    paginator = Paginator(proyectos, 1)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'persona': persona,
        'page_obj': page_obj
    }
    return render(request, 'homesocial/proyectosin_so.html', context)

#poryectos interacion social vista general publica
def repoin(request):
    t_gestion_id = request.GET.get('T_Gestion')
    t_semestre_id = request.GET.get('T_Semestre')
    
    # Inicializar listaproyectos como vacío
    listaproyectos = T_Proyectos_IIISP.objects.none()
    
    if t_gestion_id or t_semestre_id:
        listaproyectos = T_Proyectos_IIISP.objects.all()
        
        if t_gestion_id:
            listaproyectos = listaproyectos.filter(T_Gestion_id=t_gestion_id)
        
        if t_semestre_id:
            listaproyectos = listaproyectos.filter(T_Materia__T_Semestre_id=t_semestre_id)
        
        listaproyectos = listaproyectos.order_by('Id_Proyect')  # Ordenar para garantizar el primer proyecto
    
    # Obtener el primer proyecto si existe, de lo contrario None
    primer_proyecto = listaproyectos.first() if listaproyectos.exists() else None
    
    context = {
        'primer_proyecto': primer_proyecto,
        't_gestiones': T_Gestion.objects.all(),
        't_semestres': T_Semestre.objects.all(),
        'listaproyectos': listaproyectos,
        'selected_t_gestion': t_gestion_id,
        'selected_t_semestre': t_semestre_id,
    }
    
    return render(request, 'homesocial/repoin.html', context)

######## TAREAS #########

#Tipo croud
@user_passes_test(lambda u: permiso_I_S(u, 'ADMIIISP')) 
def listart(request):
    tipos = T_Tipo.objects.all()
    return render(request, 'Tareas/Tipo/listart.html', {'tipos': tipos})

@user_passes_test(lambda u: permiso_I_S(u, 'ADMIIISP')) 
def creart(request):
    if request.method == "POST":
        form = TipoProyectoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listart')
    else:
        form = TipoProyectoForm()
    return render(request, 'Tareas/Tipo/creart.html', {'form': form})

@user_passes_test(lambda u: permiso_I_S(u, 'ADMIIISP')) 
def editart(request, pk):
    tipo = get_object_or_404(T_Tipo, pk=pk)
    if request.method == "POST":
        form = TipoProyectoForm(request.POST, instance=tipo)
        if form.is_valid():
            form.save()
            return redirect('listart')
    else:
        form = TipoProyectoForm(instance=tipo)
    return render(request, 'Tareas/Tipo/editart.html', {'form': form})

@user_passes_test(lambda u: permiso_I_S(u, 'ADMIIISP')) 
def eliminart(request, pk):
    tipo = get_object_or_404(T_Tipo, pk=pk)
    if request.method == "POST":
        tipo.delete()
        return redirect('listart')
    return render(request, 'Tareas/Tipo/eliminart.html', {'object': tipo})

#Fase croud
@user_passes_test(lambda u: permiso_I_S(u, 'ADMIIISP')) 
def listarf(request):
    fase = T_Fase.objects.all()
    return render(request, 'Tareas/FaseEtapa/listarf.html', {'fase': fase})

@user_passes_test(lambda u: permiso_I_S(u, 'ADMIIISP')) 
def crearf(request):
    if request.method == "POST":
        formf = FaseProyectoForm(request.POST)
        if formf.is_valid():
            formf.save()
            return redirect('listarf')
    else:
        formf = FaseProyectoForm()
    return render(request, 'Tareas/FaseEtapa/crearf.html', {'formf': formf})
@user_passes_test(lambda u: permiso_I_S(u, 'ADMIIISP')) 
def editarf(request, pk):
    fase = get_object_or_404(T_Fase, pk=pk)
    if request.method == "POST":
        formf = FaseProyectoForm(request.POST, instance=fase)
        if formf.is_valid():
            formf.save()
            return redirect('listarf')
    else:
        formf = FaseProyectoForm(instance=fase)
    return render(request, 'Tareas/FaseEtapa/editarf.html', {'formf': formf})

@user_passes_test(lambda u: permiso_I_S(u, 'ADMIIISP')) 
def eliminarf(request, pk):
    fase = get_object_or_404(T_Fase, pk=pk)
    if request.method == "POST":
        fase.delete()
        return redirect('listarf')
    return render(request, 'Tareas/FaseEtapa/eliminarf.html', {'object': fase})

#Gestion croud
@user_passes_test(lambda u: permiso_I_S(u, 'ADMIIISP')) 
def listarg(request):
    gestion_list = T_Gestion.objects.all().order_by('-Id_Ges')
    paginator = Paginator(gestion_list, 5) 
    page_number = request.GET.get('page')
    gestion = paginator.get_page(page_number)
    return render(request, 'Tareas/Gestion/listarg.html', {'gestion': gestion})

@user_passes_test(lambda u: permiso_I_S(u, 'ADMIIISP')) 
def crearg(request):
    if request.method == "POST":
        formg = GestionForm(request.POST)
        if formg.is_valid():
            formg.save()
            return redirect('listarg')
    else:
        formg = GestionForm()
    return render(request, 'Tareas/Gestion/crearg.html', {'formg': formg})
@user_passes_test(lambda u: permiso_I_S(u, 'ADMIIISP')) 
def editarg(request, pk):
    gestion = get_object_or_404(T_Gestion, pk=pk)
    if request.method == "POST":
        formg = GestionForm(request.POST, instance=gestion)
        if formg.is_valid():
            formg.save()
            return redirect('listarg')
    else:
        formg = GestionForm(instance=gestion)
    return render(request, 'Tareas/Gestion/editarg.html', {'formg': formg})
@user_passes_test(lambda u: permiso_I_S(u, 'ADMIIISP')) 
def eliminarg(request, pk):
    gestion = get_object_or_404(T_Gestion, pk=pk)
    if request.method == "POST":
        gestion.delete()
        return redirect('listarg')
    return render(request, 'Tareas/Gestion/eliminarg.html', {'object': gestion})

#Semestre croud
@user_passes_test(lambda u: permiso_I_S(u, 'ADMIIISP')) 
def listars(request):
    semestre = T_Semestre.objects.all()
    return render(request, 'Tareas/Semestre/listars.html', {'semestre': semestre})
@user_passes_test(lambda u: permiso_I_S(u, 'ADMIIISP')) 
def crears(request):
    if request.method == "POST":
        forms = SemestreForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('listars')
    else:
        forms = SemestreForm()
    return render(request, 'Tareas/Semestre/crears.html', {'forms': forms})
@user_passes_test(lambda u: permiso_I_S(u, 'ADMIIISP')) 
def editars(request, pk):
    semestre = get_object_or_404(T_Semestre, pk=pk)
    if request.method == "POST":
        forms = SemestreForm(request.POST, instance=semestre)
        if forms.is_valid():
            forms.save()
            return redirect('listars')
    else:
        forms = SemestreForm(instance=semestre)
    return render(request, 'Tareas/Semestre/editars.html', {'forms': forms})
@user_passes_test(lambda u: permiso_I_S(u, 'ADMIIISP')) 
def eliminars(request, pk):
    semestre = get_object_or_404(T_Semestre, pk=pk)
    if request.method == "POST":
        semestre.delete()
        return redirect('listars')
    return render(request, 'Tareas/Semestre/eliminars.html', {'object': semestre})

#Materia cruod
@user_passes_test(lambda u: permiso_I_S(u, 'ADMIIISP')) 
def listarm(request):
    materia = T_Materia.objects.all()
    return render(request, 'Tareas/Materia/listarm.html', {'materia': materia})
@user_passes_test(lambda u: permiso_I_S(u, 'ADMIIISP')) 
def crearm(request):
    if request.method == 'POST':
        formm = MateriaForm(request.POST)
        if formm.is_valid():
            formm.save()
            return redirect('listarm')
    else:
        formm = MateriaForm()
    return render(request, 'Tareas/Materia/crearm.html', {'formm': formm})
@user_passes_test(lambda u: permiso_I_S(u, 'ADMIIISP')) 
def editarm(request, pk):
    materia = get_object_or_404(T_Materia, pk=pk)
    if request.method == 'POST':
        formm = MateriaForm(request.POST, instance=materia)
        if formm.is_valid():
            formm.save()
            return redirect('listarm')
    else:
        formm = MateriaForm(instance=materia)
    return render(request, 'Tareas/Materia/editarm.html', {'formm': formm})
@user_passes_test(lambda u: permiso_I_S(u, 'ADMIIISP')) 
def eliminarm(request, pk):
    materia = get_object_or_404(T_Materia, pk=pk)
    if request.method == 'POST':
        materia.delete()
        return redirect('listarm')
    return render(request, 'Tareas/Materia/eliminarm.html', {'materia': materia})
