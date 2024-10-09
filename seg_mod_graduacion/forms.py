from django import forms
from django.contrib.auth.models import Group
from gestion_usuarios.models import User 
from .models import InvCientifica, ComentarioInvCientifica, HabilitarProyectoFinal,HabilitarSeguimiento
from .models import PerfilProyecto, ComentarioPerfil, RepositorioTitulados, ProyectoFinal, ComentarioProFinal
from .models import ActaProyectoPerfil,HabilitarProyectoFinal, Modalidad, ActaPublica, ActaPrivada,Periodo
from django.utils.text import slugify
from django_select2.forms import ModelSelect2Widget

class ModalidadForm(forms.ModelForm):
    class Meta:
        model = Modalidad
        fields = ['nombre']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.slug = slugify(instance.nombre)
        if commit:
            instance.save()
        return instance
  
# área de investigación científica 
class InvCientificaForm(forms.ModelForm):
    class Meta:
        model = InvCientifica
        fields = ['user_uno', 'user_dos','habilitar_users','invtitulo', 'invdescripcion', 'invdocumentacion' ]
        widgets = {
            'invdescripcion': forms.Textarea(attrs={'class': 'descripcion-field'}),
        }
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        # Obtiene el grupo llamado 'Estudiantes'
        estudiantes_group = Group.objects.get(name='Estudiantes')
        estudiantes_users = User.objects.filter(groups=estudiantes_group, is_active=True)

        # Filtrar las investigaciones que tienen el estado 'Aprobado'
        investigaciones_aprobadas = InvCientifica.objects.filter(investado='Aprobado')

        # Obtener los usuarios que ya están relacionados en una investigación aprobada como user, user_uno o user_dos
        usuarios_con_inv = investigaciones_aprobadas.values_list('user', 'user_uno', 'user_dos')
        
        # Aplanar la lista de usuarios (eliminando duplicados con set) y excluir None
        usuarios_con_inv = set(
            usuario for usuarios in usuarios_con_inv for usuario in usuarios if usuario is not None
        )

        # Excluir los usuarios que ya tienen una investigación aprobada
        estudiantes_users = estudiantes_users.exclude(id__in=usuarios_con_inv)

        # Si el usuario autenticado está creando la investigación, exclúyelo también de las opciones de user_uno y user_dos
        if self.request and self.request.user.is_authenticated:
            estudiantes_users = estudiantes_users.exclude(id=self.request.user.id)

        # Establecer el queryset filtrado en los campos 'user_uno' y 'user_dos'
        self.fields['user_uno'].queryset = estudiantes_users
        self.fields['user_dos'].queryset = estudiantes_users
        # Marcar los campos como requeridos
        self.fields['invtitulo'].required = True
        self.fields['invdescripcion'].required = True
        self.fields['invdocumentacion'].required = True
        
        
class InvComentarioForm(forms.ModelForm):
    class Meta:
        model = ComentarioInvCientifica
        fields = ['invcomentario','invdocorregido'] 
        widgets = {
            'invcomentario': forms.Textarea(attrs={'class': 'comentari-field'}),
        }

class GlobalSettingsForm(forms.ModelForm):
    class Meta:
        model = HabilitarSeguimiento
        fields = ['habilitarInv']

    def __init__(self, *args, **kwargs):
        super(GlobalSettingsForm, self).__init__(*args, **kwargs)
        
# área de perfil de proyecto 
class PerfilForm(forms.ModelForm):
    class Meta:
        model = PerfilProyecto
        fields = ['user_uno', 'user_dos','habilitar_users','pertitulo', 'perdescripcion', 'perdocumentacion', 'permodalidad']
        widgets = {
            'perdescripcion': forms.Textarea(attrs={'class': 'descripcion-field'}),
        }
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        # Obtiene el grupo llamado 'Estudiantes'
        estudiantes_group = Group.objects.get(name='Estudiantes')
        estudiantes_users = User.objects.filter(groups=estudiantes_group, is_active=True)

        # Filtrar las investigaciones que tienen el estado 'Aprobado'
        perfiles_aprobadas = PerfilProyecto.objects.filter(perestado='Aprobado')

        # Obtener los usuarios que ya están relacionados en una investigación aprobada como user, user_uno o user_dos
        usuarios_con_perfil = perfiles_aprobadas.values_list('user', 'user_uno', 'user_dos')
        
        # Aplanar la lista de usuarios (eliminando duplicados con set) y excluir None
        usuarios_con_perfil = set(
            usuario for usuarios in usuarios_con_perfil for usuario in usuarios if usuario is not None
        )

        # Excluir los usuarios que ya tienen una investigación aprobada
        estudiantes_users = estudiantes_users.exclude(id__in=usuarios_con_perfil)

        # Si el usuario autenticado está creando la investigación, exclúyelo también de las opciones de user_uno y user_dos
        if self.request and self.request.user.is_authenticated:
            estudiantes_users = estudiantes_users.exclude(id=self.request.user.id)

        # Establecer el queryset filtrado en los campos 'user_uno' y 'user_dos'
        self.fields['user_uno'].queryset = estudiantes_users
        self.fields['user_dos'].queryset = estudiantes_users
        
         # Set all fields as required
        self.fields['pertitulo'].required = True
        self.fields['perdescripcion'].required = True
        self.fields['perdocumentacion'].required = True
        self.fields['permodalidad'].required = True
        
        INCLUDED_MODALITIES = ['Trabajo Dirigido', 'Proyecto de Grado', 'Tesis de Grado']
        self.fields['permodalidad'].choices = [
            (choice_value, choice_label)
            for choice_value, choice_label in self.fields['permodalidad'].choices
            if choice_label in INCLUDED_MODALITIES
        ]
      
      
class PerComentarioForm(forms.ModelForm):
    class Meta:
        model = ComentarioPerfil
        fields = ['percomentario','perdocorregido'] 
        widgets = {
            'percomentario': forms.Textarea(attrs={'class': 'comentari-field'}),
        }

#acta perfil de proyecto 
class ActaPerfilForm(forms.ModelForm):
    class Meta:
        model = ActaProyectoPerfil
        fields = [
            'perperiodo', 'acta', 'carrera', 'estudiante', 
            'estudiante_uno', 'estudiante_dos', 'titulo', 'lugar', 
            'fechadefensa', 'horainicio', 'horafin', 'tutor', 
            'jurado_1', 'jurado_2', 'jurado_3', 'modalidad', 
            'resultado', 'observacion_1', 'observacion_2', 'observacion_3'
        ]
        labels = {
            'perperiodo': 'Periodo y Gestión',
            'acta': 'Número de Acta',
          
            'carrera': 'Carrera',
            'estudiante': 'Postulante',
            'estudiante_uno': 'Postulante dos',
            'estudiante_dos': 'Postulante tres',
            'titulo': 'Título del Proyecto',
            'lugar': 'Lugar de Defensa',
            'fechadefensa': 'Fecha de Defensa',
            'horainicio': 'Hora de Inicio',
            'horafin': 'Hora de Finalización',
            'tutor': 'Seleccione al Tutor Designado',
            'jurado_1': 'Primer Tribunal Designado',
            'jurado_2': 'Segundo Tribunal Designado',
            'jurado_3': 'Tercer Tribunal Designado',
            'modalidad': 'Seleccione Modalidad',
            'resultado': 'Resultado de la Defensa',
            'observacion_1': 'Observación del Primer Tribunal',
            'observacion_2': 'Observación del Segundo Tribunal',
            'observacion_3': 'Observación del Tercer Tribunal',
        }
        widgets = {
            'perperiodo': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'acta': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'carrera': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'estudiante': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'estudiante_uno': forms.Select(attrs={'class': 'form-select'}),
            'estudiante_dos': forms.Select(attrs={'class': 'form-select'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'lugar': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'fechadefensa': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': 'required'}),
            'horainicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'required': 'required'}),
            'horafin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'required': 'required'}),
            'tutor': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'jurado_1': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'jurado_2': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'jurado_3': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'modalidad': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'resultado': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'observacion_1': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'required': 'required'}),
            'observacion_2': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'required': 'required'}),
            'observacion_3': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'required': 'required'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        # Filtrado de estudiantes y asignación a los campos correspondientes
        estudiantes_users = self._get_estudiantes_filtrados()
        
        # Establecer el queryset filtrado para los campos de estudiantes
        self.fields['estudiante_uno'].queryset = estudiantes_users
        self.fields['estudiante_dos'].queryset = estudiantes_users
        self.fields['estudiante'].queryset = estudiantes_users
        
        INCLUDED_MODALITIES = ['Trabajo Dirigido', 'Proyecto de Grado', 'Tesis de Grado']
        self.fields['modalidad'].choices = [
            (choice_value, choice_label)
            for choice_value, choice_label in self.fields['modalidad'].choices
            if choice_label in INCLUDED_MODALITIES
        ]
        # Filtrar los usuarios de los grupos de docentes
        docentes_group = Group.objects.get(name="Docentes")
        self.fields['tutor'].queryset = User.objects.filter(groups=docentes_group, is_active=True)
        self.fields['jurado_1'].queryset = User.objects.filter(groups=docentes_group, is_active=True)
        self.fields['jurado_2'].queryset = User.objects.filter(groups=docentes_group, is_active=True)
        self.fields['jurado_3'].queryset = User.objects.filter(groups=docentes_group, is_active=True)

        # Limitar las opciones del campo resultado
        self._filter_resultado_choices()
    # Obtiene el grupo llamado 'Estudiantes' y usuarios activos
    def _get_estudiantes_filtrados(self):
        estudiantes_group = Group.objects.get(name='Estudiantes')
        estudiantes_users = User.objects.filter(groups=estudiantes_group, is_active=True)
        # Filtrar los usuarios que ya tienen perfilproyecto aprobadas
        usuarios_con_perfil_aprobado = PerfilProyecto.objects.filter(perestado='Aprobado').values_list(
            'user', 'user_uno', 'user_dos')
        # Aplanar las tuplas para obtener solo los IDs de los usuarios
        usuarios_con_perfil = set(
            usuario for usuarios in usuarios_con_perfil_aprobado for usuario in usuarios if usuario is not None)
        # Filtrar los usuarios que ya tienen un resultado 'Suficiente' o que están en HabilitarProyectoFinal
        usuarios_con_actividad = HabilitarProyectoFinal.objects.values_list('estudiante', flat=True)
        usuarios_con_resultado_suficiente = ActaProyectoPerfil.objects.filter(resultado='Suficiente').values_list(
            'estudiante', 'estudiante_uno', 'estudiante_dos')
        # Aplanar las tuplas para obtener solo los IDs de los usuarios
        usuarios_a_excluir = set(usuarios_con_actividad).union(set(
            usuario for usuarios in usuarios_con_resultado_suficiente for usuario in usuarios if usuario is not None))
        # Excluir los usuarios que ya tienen un perfil aprobado y actividad finalizada
        estudiantes_filtrados = estudiantes_users.exclude(id__in=usuarios_a_excluir).filter(id__in=usuarios_con_perfil)
        return estudiantes_filtrados

    def _filter_resultado_choices(self):
        # Filtra las opciones del campo 'resultado' para incluir solo 'Suficiente' e 'Insuficiente'
        INCLUDED_RESULT = ['Insuficiente', 'Suficiente']
        self.fields['resultado'].choices = [
            (choice_value, choice_label)
            for choice_value, choice_label in self.fields['resultado'].choices
            if choice_label in INCLUDED_RESULT
        ]

    def clean(self):
        cleaned_data = super().clean()
        estudiante = cleaned_data.get("estudiante")
        estudiante_uno = cleaned_data.get("estudiante_uno")
        estudiante_dos = cleaned_data.get("estudiante_dos")
        
        # Validación para evitar que se repita el mismo estudiante en varios campos
        if estudiante and (estudiante == estudiante_uno or estudiante == estudiante_dos):
            raise forms.ValidationError("El postulante principal no puede ser igual a los otros postulantes.")
        
        if estudiante_uno and estudiante_uno == estudiante_dos:
            raise forms.ValidationError("El postulante dos no puede ser igual a postulante tres.")
        
        return cleaned_data
    
    
        
#actas defensa privada
class ActaPublicaForm(forms.ModelForm):
    class Meta:
        model = ActaPublica
        fields = [
            'perperiodo','acta', 'carrera', 'estudiante', 'estudiante_uno', 'estudiante_dos', 'titulo', 'lugar', 
            'fechadefensa', 'horainicio', 'horafin', 'tutor', 
            'jurado_1', 'jurado_2', 'jurado_3', 'modalidad', 
            'resultado','calificacion1', 'calificacion2','notatotal', 'presidenteacta'
        ]
        labels = {
            'perperiodo': 'Periodo y Gestión',
            'acta': 'Número de Acta',
           
            'carrera': 'Carrera',
            'estudiante': 'Postulante',
            'estudiante_uno': 'Postulante dos',
            'estudiante_dos': 'Postulante tres',
            'titulo': 'Título del Proyecto',
            'lugar': 'Lugar de Defensa',
            'fechadefensa': 'Fecha de Defensa',
            'horainicio': 'Hora de Inicio',
            'horafin': 'Hora de Finalización',
            'tutor': 'Seleccione al Tutor Designado',
            'jurado_1': 'Primer Tribunal Designado',
            'jurado_2': 'Segundo Tribunal Designado',
            'jurado_3': 'Tercer Tribunal Designado',
            'modalidad': 'Seleccione Modalidad',
            'resultado': 'Resultado de la Defensa',
            'calificacion1': '1er. Valor Cuantitativo',
            'calificacion2': '2do. Valor Cuantitativo',
            'notatotal': 'Calificación Total',
            'presidenteacta': 'Asignar Presidente',
        }
        widgets = {
            'perperiodo': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'acta': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
         
            'carrera': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'estudiante': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'estudiante_uno': forms.Select(attrs={'class': 'form-select'}),
            'estudiante_dos': forms.Select(attrs={'class': 'form-select'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'lugar': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'fechadefensa': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': 'required'}),
            'horainicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'required': 'required'}),
            'horafin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'required': 'required'}),
            'tutor': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'jurado_1': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'jurado_2': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'jurado_3': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'modalidad': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'resultado': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'calificacion1': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required', 'min': '0', 'max': '30'}),
            'calificacion2': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required', 'min': '0', 'max': '70'}),
            'notatotal': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required', 'min': '0', 'max': '100'}),
            'presidenteacta': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        calificacion1 = cleaned_data.get('calificacion1', 0)
        calificacion2 = cleaned_data.get('calificacion2', 0)
        notatotal = calificacion1 + calificacion2
        cleaned_data['notatotal'] = notatotal
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if not self.instance.pk:  # Only set notatotal if instance is new
            instance.notatotal = self.cleaned_data.get('notatotal', 0)
        # Asignamos automáticamente los valores a observacion_1, observacion_2 y observacion_3
        instance.observacion_1 = 'sin observacion'
        instance.observacion_2 = 'sin observacion'
        instance.observacion_3 = 'sin observacion'
        
        if commit:
            instance.save()
        return instance
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        estudiantes_group = Group.objects.get(name="Estudiantes")
        docentes_group = Group.objects.get(name="Docentes")
        presidentes_group = Group.objects.get(name="Presidentes Defensas")
        estudiantes_users = User.objects.filter(groups=estudiantes_group, is_active=True)
        
        usuarios_con_repositorio = RepositorioTitulados.objects.values_list('estudiante', flat=True) 
        usuarios_con_resultado_Suficiente = ActaPrivada.objects.filter(resultado='Suficiente').values_list('estudiante', flat=True).distinct() 
        usuarios_con_proyecto_final = ProyectoFinal.objects.filter(estado='Aprobado').values_list('estudiante', flat=True).distinct()
       
        usuarios_con_actapublica = ActaPublica.objects.filter(resultado='Aprobado').values_list('estudiante', flat=True)
        
        usuarios_uno_con_repositorio = RepositorioTitulados.objects.values_list('estudiante_uno', flat=True) 
        usuarios_uno_con_resultado_Suficiente = ActaPrivada.objects.filter(resultado='Suficiente').values_list('estudiante_uno', flat=True).distinct() 
        usuarios_uno_con_proyecto_final = ProyectoFinal.objects.filter(estado='Aprobado').values_list('estudiante_uno', flat=True).distinct()
       
        usuarios_uno_con_actapublica = ActaPublica.objects.filter(resultado='Aprobado').values_list('estudiante_uno', flat=True)
        
        usuarios_dos_con_repositorio = RepositorioTitulados.objects.values_list('estudiante_dos', flat=True) 
        usuarios_dos_con_resultado_Suficiente = ActaPrivada.objects.filter(resultado='Suficiente').values_list('estudiante_dos', flat=True).distinct() 
        usuarios_dos_con_proyecto_final = ProyectoFinal.objects.filter(estado='Aprobado').values_list('estudiante_dos', flat=True).distinct()
        
        usuarios_dos_con_actapublica = ActaPublica.objects.filter(resultado='Aprobado').values_list('estudiante_dos', flat=True)
        self.fields['estudiante'].queryset = User.objects.filter(
            groups=estudiantes_group
        ).exclude(
            id__in=usuarios_con_repositorio
        ).filter(
            id__in=estudiantes_users
        ).filter(
            id__in=usuarios_con_resultado_Suficiente
        ).filter(
            id__in=usuarios_con_proyecto_final
        ).exclude(
            id__in=usuarios_con_actapublica
        )
        
        self.fields['estudiante_uno'].queryset = User.objects.filter(
            groups=estudiantes_group
        ).exclude(
            id__in=usuarios_uno_con_repositorio
        ).filter(
            id__in=estudiantes_users
        ).filter(
            id__in=usuarios_uno_con_resultado_Suficiente
        ).filter(
            id__in=usuarios_uno_con_proyecto_final
        ).exclude(
            id__in=usuarios_uno_con_actapublica
        )
        
        self.fields['estudiante_dos'].queryset = User.objects.filter(
            groups=estudiantes_group
        ).exclude(
            id__in=usuarios_dos_con_repositorio
        ).filter(
            id__in=estudiantes_users
        ).filter(
            id__in=usuarios_dos_con_resultado_Suficiente
        ).filter(
            id__in=usuarios_dos_con_proyecto_final
        ).exclude(
            id__in=usuarios_dos_con_actapublica
        )
        
        INCLUDED_RESULT = ['Aprobado', 'Reprobado','Postergado']
        self.fields['resultado'].choices = [
            (choice_value, choice_label)
            for choice_value, choice_label in self.fields['resultado'].choices
            if choice_label in INCLUDED_RESULT
        ]
        
        INCLUDED_MODALITIES = ['Trabajo Dirigido', 'Proyecto de Grado', 'Tesis de Grado']
        self.fields['modalidad'].choices = [
            (choice_value, choice_label)
            for choice_value, choice_label in self.fields['modalidad'].choices
            if choice_label in INCLUDED_MODALITIES
        ]
        # Filtra los usuarios del grupo "Docentes"
        self.fields['tutor'].queryset = User.objects.filter(groups=docentes_group, is_active=True)
        self.fields['jurado_1'].queryset = User.objects.filter(groups=docentes_group, is_active=True)
        self.fields['jurado_2'].queryset = User.objects.filter(groups=docentes_group, is_active=True)
        self.fields['jurado_3'].queryset = User.objects.filter(groups=docentes_group, is_active=True)
        self.fields['presidenteacta'].queryset = User.objects.filter(groups=presidentes_group, is_active=True)

#actas defensa publica
class ActaPrivadaForm(forms.ModelForm):
    class Meta:
        model = ActaPrivada
        fields = [
            'perperiodo','acta', 'carrera', 'estudiante', 'estudiante_uno', 'estudiante_dos', 'titulo', 'lugar', 
            'fechadefensa', 'horainicio', 'horafin', 'tutor', 
            'jurado_1', 'jurado_2', 'jurado_3', 'modalidad', 
            'resultado','calificacion1', 'observacion_1', 'observacion_2', 'observacion_3'
        ]
        labels = {
            'perperiodo': 'Periodo y Gestión',
            'acta': 'Número de Acta',
            'carrera': 'Carrera',
            'estudiante': 'Postulante',
            'estudiante_uno': 'Postulante dos',
            'estudiante_dos': 'Postulante tres',
            'titulo': 'Título del Proyecto',
            'lugar': 'Lugar de Defensa',
            'fechadefensa': 'Fecha de Defensa',
            'horainicio': 'Hora de Inicio',
            'horafin': 'Hora de Finalización',
            'tutor': 'Seleccione al Tutor Designado',
            'jurado_1': 'Primer Tribunal Designado',
            'jurado_2': 'Segundo Tribunal Designado',
            'jurado_3': 'Tercer Tribunal Designado',
            'modalidad': 'Seleccione Modalidad',
            'resultado': 'Resultado de la Defensa',
            'calificacion1': 'Calificacion',
            'observacion_1': 'Observación del Primer Tribunal',
            'observacion_2': 'Observación del Segundo Tribunal',
            'observacion_3': 'Observación del Tercer Tribunal',
        }
        widgets = {
            'perperiodo': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'acta': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'carrera': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'estudiante': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'estudiante_uno': forms.Select(attrs={'class': 'form-select'}),
            'estudiante_dos': forms.Select(attrs={'class': 'form-select'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'lugar': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'fechadefensa': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': 'required'}),
            'horainicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'required': 'required'}),
            'horafin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'required': 'required'}),
            'tutor': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'jurado_1': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'jurado_2': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'jurado_3': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'modalidad': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'resultado': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'calificacion1': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required', 'min': '0', 'max': '30'}),
            'observacion_1': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'required': 'required'}),
            'observacion_2': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'required': 'required'}),
            'observacion_3': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'required': 'required'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        estudiantes_group = Group.objects.get(name="Estudiantes")
        estudiantes_users = User.objects.filter(groups=estudiantes_group, is_active=True)
        docentes_group = Group.objects.get(name="Docentes")
        
        usuarios_con_repositorio = RepositorioTitulados.objects.values_list('estudiante', flat=True) 
        usuarios_con_resultado_Suficiente = ActaPrivada.objects.filter(resultado='Suficiente').values_list('estudiante', flat=True).distinct() 
        usuarios_con_proyecto_final = ProyectoFinal.objects.filter(estado='Aprobado').values_list('estudiante', flat=True).distinct()
        usuarios_con_resultado_Suficienteperfil = ActaProyectoPerfil.objects.filter(resultado='Suficiente').values_list('estudiante', flat=True).distinct() 
        
        usuarios_uno_con_repositorio = RepositorioTitulados.objects.values_list('estudiante_uno', flat=True) 
        usuarios_uno_con_resultado_Suficiente = ActaPrivada.objects.filter(resultado='Suficiente').values_list('estudiante_uno', flat=True).distinct() 
        usuarios_uno_con_proyecto_final = ProyectoFinal.objects.filter(estado='Aprobado').values_list('estudiante_uno', flat=True).distinct()
        usuarios_uno_con_resultado_Suficienteperfil = ActaProyectoPerfil.objects.filter(resultado='Suficiente').values_list('estudiante_uno', flat=True).distinct() 
        
        usuarios_dos_con_repositorio = RepositorioTitulados.objects.values_list('estudiante_dos', flat=True) 
        usuarios_dos_con_resultado_Suficiente = ActaPrivada.objects.filter(resultado='Suficiente').values_list('estudiante_dos', flat=True).distinct() 
        usuarios_dos_con_proyecto_final = ProyectoFinal.objects.filter(estado='Aprobado').values_list('estudiante_dos', flat=True).distinct()
        usuarios_dos_con_resultado_Suficienteperfil = ActaProyectoPerfil.objects.filter(resultado='Suficiente').values_list('estudiante_dos', flat=True).distinct() 
        
        self.fields['estudiante'].queryset = User.objects.filter(
            groups=estudiantes_group
        ).exclude(
            id__in=usuarios_con_repositorio
        ).filter(
            id__in=estudiantes_users
        ).exclude(
            id__in=usuarios_con_resultado_Suficiente
        ).filter(
            id__in=usuarios_con_resultado_Suficienteperfil
        ).filter(
            id__in=usuarios_con_proyecto_final
        )
        self.fields['estudiante_uno'].queryset = User.objects.filter(
            groups=estudiantes_group
        ).exclude(
            id__in=usuarios_uno_con_repositorio
        ).filter(
            id__in=estudiantes_users
        ).exclude(
            id__in=usuarios_uno_con_resultado_Suficiente
        ).filter(
            id__in=usuarios_uno_con_resultado_Suficienteperfil
        ).filter(
            id__in=usuarios_uno_con_proyecto_final
        )
        self.fields['estudiante_dos'].queryset = User.objects.filter(
            groups=estudiantes_group
        ).exclude(
            id__in=usuarios_dos_con_repositorio
        ).filter(
            id__in=estudiantes_users
        ).exclude(
            id__in=usuarios_dos_con_resultado_Suficiente
        ).filter(
            id__in=usuarios_dos_con_resultado_Suficienteperfil
        ).filter(
            id__in=usuarios_dos_con_proyecto_final
        )
        
        INCLUDED_MODALITIES = ['Trabajo Dirigido', 'Proyecto de Grado', 'Tesis de Grado']
        self.fields['modalidad'].choices = [
            (choice_value, choice_label)
            for choice_value, choice_label in self.fields['modalidad'].choices
            if choice_label in INCLUDED_MODALITIES
        ]
        
        INCLUDED_RESULT = ['Insuficiente', 'Suficiente']
        self.fields['resultado'].choices = [
            (choice_value, choice_label)
            for choice_value, choice_label in self.fields['resultado'].choices
            if choice_label in INCLUDED_RESULT
        ]
        # Filtra los usuarios del grupo "Docentes"
        self.fields['tutor'].queryset = User.objects.filter(groups=docentes_group)
        self.fields['jurado_1'].queryset = User.objects.filter(groups=docentes_group)
        self.fields['jurado_2'].queryset = User.objects.filter(groups=docentes_group)
        self.fields['jurado_3'].queryset = User.objects.filter(groups=docentes_group)



class ActividadControlForm(forms.ModelForm):
    class Meta:
        model = HabilitarProyectoFinal
        fields = ['estudiante','estudiante_uno','estudiante_dos', 'tutor', 'jurado_1', 'jurado_2', 'jurado_3', 'modalidad']
        labels = {
            'estudiante': 'Postulante',
            'estudiante_uno': 'Postulante dos',
            'estudiante_dos': 'Postulante tres',
            'tutor': 'Seleccione al Tutor Designado',
            'jurado_1': 'Primero Tribunal Designado',
            'jurado_2': 'Segundo Tribunal Designado',
            'jurado_3': 'Tercer Tribunal Designado',
            'modalidad': 'Seleccione modalidad ',
        }
        widgets = {
            'estudiante': forms.Select(attrs={'class': 'form-select'}),
            'estudiante_uno': forms.Select(attrs={'class': 'form-select'}),
            'estudiante_dos': forms.Select(attrs={'class': 'form-select'}),
            'tutor': forms.Select(attrs={'class': 'form-select'}),
            'jurado_1': forms.Select(attrs={'class': 'form-select'}),
            'jurado_2': forms.Select(attrs={'class': 'form-select'}),
            'jurado_3': forms.Select(attrs={'class': 'form-select'}),
            'modalidad': forms.Select(attrs={'class': 'form-select'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        estudiantes_group = Group.objects.get(name="Estudiantes")
        docentes_group = Group.objects.get(name="Docentes")
        usuarios_con_actividad = HabilitarProyectoFinal.objects.values_list('estudiante', flat=True)
        usuarios_con_perfil_aprobado = ActaProyectoPerfil.objects.filter(resultado='Suficiente').values_list('estudiante', flat=True).distinct()
        self.fields['estudiante'].queryset = User.objects.filter(
        groups=estudiantes_group,
        is_active=True  # Solo usuarios activos
        ).exclude(id__in=usuarios_con_actividad).filter(id__in=usuarios_con_perfil_aprobado)
        # Filtra los estudiantes para 'estudiante_uno' y 'estudiante_dos'
        self.fields['estudiante_uno'].queryset = User.objects.filter(
            groups=estudiantes_group,
            is_active=True  # Solo usuarios activos
            ).exclude(id__in=usuarios_con_actividad)#.filter(id__in=usuarios_con_perfil_aprobado)
        self.fields['estudiante_dos'].queryset = User.objects.filter(
            groups=estudiantes_group,
            is_active=True  # Solo usuarios activos
            ).exclude(id__in=usuarios_con_actividad)#.filter(id__in=usuarios_con_perfil_aprobado)

        self.fields['tutor'].queryset = User.objects.filter(groups=docentes_group)
        self.fields['jurado_1'].queryset = User.objects.filter(groups=docentes_group)
        self.fields['jurado_2'].queryset = User.objects.filter(groups=docentes_group)
        self.fields['jurado_3'].queryset = User.objects.filter(groups=docentes_group)
          
class EditarActividadControlForm(forms.ModelForm):
    class Meta:
        model = HabilitarProyectoFinal
        fields = ['estudiante', 'estudiante_uno', 'estudiante_dos', 'tutor', 'jurado_1', 'jurado_2', 'jurado_3','modalidad']
        labels = {
            'estudiante': 'Postulante',
            'estudiante_uno': 'Postulante dos',
            'estudiante_dos': 'Postulante tres',
            'tutor': 'Seleccione al Tutor Designado',
            'jurado_1': 'Primero Tribumal Designado',
            'jurado_2': 'Segundo Tribumal Designado',
            'jurado_3': 'Tercer Tribumal Designado',
            'modalidad': 'Seleccione modalidad ',
        }
        widgets = {
            'estudiante': forms.Select(attrs={'class': 'form-select'}),
            'estudiante_uno': forms.Select(attrs={'class': 'form-select'}),
            'estudiante_dos': forms.Select(attrs={'class': 'form-select'}),
            'tutor': forms.Select(attrs={'class': 'form-select'}),
            'jurado_1': forms.Select(attrs={'class': 'form-select'}),
            'jurado_2': forms.Select(attrs={'class': 'form-select'}),
            'jurado_3': forms.Select(attrs={'class': 'form-select'}),
            'modalidad': forms.Select(attrs={'class': 'form-select'})
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        docentes_group = Group.objects.get(name="Docentes")
        self.fields['tutor'].queryset = User.objects.filter(groups=docentes_group)
        self.fields['jurado_1'].queryset = User.objects.filter(groups=docentes_group)
        self.fields['jurado_2'].queryset = User.objects.filter(groups=docentes_group)
        self.fields['jurado_3'].queryset = User.objects.filter(groups=docentes_group)
        
      
        if self.instance and self.instance.pk:
          self.fields['estudiante'].disabled = True
          self.fields['estudiante_uno'].disabled = True
          self.fields['estudiante_dos'].disabled = True
             
class ActividadForm(forms.ModelForm):
    class Meta:
        model = ProyectoFinal
        fields = ['estudiante', 'estudiante_uno', 'estudiante_dos', 'tutor', 'jurado_1', 'jurado_2', 'jurado_3', 'titulo', 'resumen', 'modalidad', 'guia_externo', 'documentacion']
        widgets = {
            'estudiante': forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'estudiante_uno': forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'estudiante_dos': forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'tutor': forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'jurado_1': forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'jurado_2': forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'jurado_3': forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'modalidad': forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'resumen': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'guia_externo': forms.TextInput(attrs={'class': 'form-control'}),
            'documentacion': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

class ActComentarioForm(forms.ModelForm):
    class Meta:
        model = ComentarioProFinal
        fields = ['actcomentario','actdocorregido'] 
        widgets = {
            'actcomentario': forms.Textarea(attrs={'class': 'comentari-field'}),
        }
        


