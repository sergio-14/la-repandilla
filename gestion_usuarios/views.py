from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from .forms import CustomLoginForm, CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import GroupForm
from django.contrib.auth.models import Group
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail

User = get_user_model()

# Página Principal
def home(request):
    return render(request, 'home.html')

# Iniciar Sesion
def iniciar_sesion(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
        else:
            # Verificar si los campos están vacíos
            if form.cleaned_data.get('email') or form.cleaned_data.get('password'):
                form.first_attempt = False
            else:
                form.first_attempt = True
    else:
        form = CustomLoginForm()
    return render(request, 'IniciarSesion.html', {'form': form})

# Registrar
def registrar(request):
    errors = None
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('iniciar_sesion')
        else:
            errors = form.errors  # Captura los errores
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'Registrar.html', {'form': form, 'errors': errors})

# Cerrar Sesión
def signout(request):
    logout(request)
    return redirect('home')

from django.core.exceptions import PermissionDenied

# DashBoard
def dashboard(request):
   return render(request, "dashboard.html")

#Correspondencia de la aplicacion
@login_required
def enviar_mensaje(request):
    if request.method == 'POST':
        destinatario_id = request.POST.get('destinatario')
        destinatario = User.objects.get(id=destinatario_id)
        asunto = request.POST.get('asunto')
        mensaje = request.POST.get('mensaje')

        # Envía el correo electrónico
        send_mail(asunto, mensaje, 'shuerkk.14@gmail.com', [destinatario.email])

        return redirect('dashboard')

    # Obtener todos los usuarios excepto el usuario actual
    usuarios = User.objects.exclude(id=request.user.id)
    return render(request, 'enviar_mensaje.html', {'usuarios': usuarios})

# Listar Usuarios
def listar_usuarios(request):
    query = request.GET.get('q')
    if query:
        usuarios = User.objects.filter(
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query) |
            Q(email__icontains=query)
        )
    else:
        usuarios = User.objects.filter(is_active=True)

    paginator = Paginator(usuarios, 5)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('Gestion_Usuarios/usuarios_list.html', {'page_obj': page_obj})
        return JsonResponse({'html': html})

    return render(request, 'Gestion_Usuarios/listar_usuarios.html', {'page_obj': page_obj, 'query': query})

# Crear Usuario
@login_required
def crear_usuario(request):
    errors = None
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            # Registrar la acción de creación
            LogEntry.objects.log_action(
                user_id=request.user.pk,
                content_type_id=ContentType.objects.get_for_model(usuario).pk,
                object_id=usuario.pk,
                object_repr=str(usuario),
                action_flag=ADDITION
            )

            usuario.save()
            selected_groups = form.cleaned_data.get('groups')
            print("Grupos seleccionados:", selected_groups)  # Depuración

            if selected_groups:
                usuario.groups.set(selected_groups)

                if 'Estudiantes' in selected_groups.values_list('name', flat=True):
                    Estudiante.objects.create(user=usuario)
                elif 'Docentes' in selected_groups.values_list('name', flat=True):
                    Docente.objects.create(user=usuario)

            return redirect('listar_usuarios')
        else:
            errors = form.errors  # Captura los errores
            print("Errores en el formulario:", errors)  # Depuración
    else:
        form = CustomUserCreationForm()

        # Verificar si se están cargando los grupos correctamente
        all_groups = Group.objects.all()
        print("Todos los grupos disponibles:", all_groups)  # Depuración

    return render(request, 'Gestion_Usuarios/crear_usuario.html', {'form': form, 'errors': errors})

# Actualizar Usuario
@login_required
def actualizar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    
    # Obtener todos los grupos disponibles
    all_groups = Group.objects.all()
    # Obtener los grupos a los que pertenece el usuario
    user_groups = usuario.groups.all()
    
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            usuario = form.save()
            # Actualizar los grupos del usuario
            groups_ids = request.POST.getlist('groups')  # Obtener los grupos seleccionados
            
            # Limpiar grupos existentes y agregar los nuevos
            usuario.groups.clear()
            for group_id in groups_ids:
                grupo = Group.objects.get(id=group_id)
                usuario.groups.add(grupo)
            
            # Registrar la acción de actualización
            LogEntry.objects.log_action(
                user_id=request.user.pk,
                content_type_id=ContentType.objects.get_for_model(usuario).pk,
                object_id=usuario.pk,
                object_repr=str(usuario),
                action_flag=CHANGE
            )
            
            messages.success(request, 'El usuario ha sido actualizado.')
            return redirect('listar_usuarios')
    else:
        form = CustomUserChangeForm(instance=usuario)

    return render(request, 'Gestion_Usuarios/actualizar_usuario.html', {
        'form': form,
        'usuario': usuario,
        'all_groups': all_groups,
        'user_groups': user_groups,
    })

#editar user
from .forms import UserUpdateForm, EstudianteUpdateForm, DocenteUpdateForm
from seg_mod_graduacion.models import Estudiante, Docente


@login_required
def update_profile(request):
    user = request.user
    user_form = UserUpdateForm(instance=user)

    estudiante_form = None
    docente_form = None
    estudiante = None
    docente = None

    # Verificamos si el usuario pertenece al grupo Estudiantes o Docentes
    if user.groups.filter(name='Estudiantes').exists():
        try:
            estudiante = Estudiante.objects.get(user=user)
            estudiante_form = EstudianteUpdateForm(instance=estudiante)
        except Estudiante.DoesNotExist:
            estudiante = None  # No hay instancia de Estudiante para este usuario
    elif user.groups.filter(name='Docentes').exists():
        try:
            docente = Docente.objects.get(user=user)
            docente_form = DocenteUpdateForm(instance=docente)
        except Docente.DoesNotExist:
            docente = None  # No hay instancia de Docente para este usuario

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, request.FILES, instance=user)

        if estudiante:
            estudiante_form = EstudianteUpdateForm(request.POST, instance=estudiante)
        elif docente:
            docente_form = DocenteUpdateForm(request.POST, instance=docente)

        if user_form.is_valid() and (estudiante_form is None or estudiante_form.is_valid()) and (docente_form is None or docente_form.is_valid()):
            user_form.save()
            if estudiante_form:
                estudiante_form.save()
            if docente_form:
                docente_form.save()
            return redirect('dashboard')

    context = {
        'user_form': user_form,
        'estudiante_form': estudiante_form,
        'docente_form': docente_form,
        'estudiante': estudiante,
        'docente': docente,
    }
    return render(request, 'Gestion_Usuarios/update_profile.html', context)

# Eliminar Usuario
@login_required
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    usuario.is_active = False
    usuario.save()
    
    # Registrar la acción de eliminación
    LogEntry.objects.log_action(
        user_id=request.user.pk,
        content_type_id=ContentType.objects.get_for_model(usuario).pk,
        object_id=usuario.pk,
        object_repr=str(usuario),
        action_flag=DELETION
    )
    
    messages.success(request, 'El usuario ha sido eliminado.')
    return redirect('listar_usuarios')

@login_required
def listar_usuarios_inactivos(request):
    usuarios_inactivos = User.objects.filter(is_active=False)
    
    paginator = Paginator(usuarios_inactivos, 7)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'Gestion_Usuarios/listar_usuarios_inactivos.html', {'page_obj': page_obj})

@login_required
def reactivar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    usuario.is_active = True
    usuario.save()
        # Registrar la acción de reactivación
    LogEntry.objects.log_action(
        user_id=request.user.pk,
        content_type_id=ContentType.objects.get_for_model(usuario).pk,
        object_id=usuario.pk,
        object_repr=str(usuario),
        action_flag=ADDITION
    )
    messages.success(request, 'El usuario ha sido reactivado.')
    return redirect('listar_usuarios_inactivos')  
    
# Listar Grupos
@login_required
def listar_grupos(request):
    grupos = Group.objects.all()
    return render(request, 'Gestion_Usuarios/listar_grupos.html', {'grupos': grupos})

# Crear Grupos
@login_required
def crear_grupo(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            grupo = form.save()
            
            # Registrar la acción de creación
            LogEntry.objects.log_action(
                user_id=request.user.pk,
                content_type_id=ContentType.objects.get_for_model(grupo).pk,
                object_id=grupo.pk,
                object_repr=str(grupo),
                action_flag=ADDITION
            )
            
            messages.success(request, f'Grupo {grupo.name} creado exitosamente.')
            return redirect('listar_grupos')
    else:
        form = GroupForm()
    return render(request, 'Gestion_Usuarios/crear_grupo.html', {'form': form})

#Actualizar Grupos
@login_required
def actualizar_grupo(request, pk):
    grupo = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=grupo)
        if form.is_valid():
            form.save()
            messages.success(request, 'El grupo ha sido actualizado con éxito.')
            return redirect('listar_grupos')
    else:
        form = GroupForm(instance=grupo)
    return render(request, 'Gestion_Usuarios/actualizar_grupo.html', {'form': form, 'grupo': grupo})

# Eliminar Grupos
@login_required
def eliminar_grupo(request, pk):
    grupo = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        grupo.delete()
        messages.success(request, 'El grupo ha sido eliminado con éxito.')
        return redirect('listar_grupos')
    return render(request, 'Gestion_Usuarios/eliminar_grupo.html', {'grupo': grupo})
