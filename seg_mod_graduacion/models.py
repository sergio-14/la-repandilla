from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import date
from django.conf import settings
from django.core.exceptions import ValidationError  

User = get_user_model()

ESTADO_CHOICES = [
    ('Aprobado', 'Aprobado'),
    ('Pendiente', 'Pendiente'),
    ('Rechazado', 'Rechazado'),
]

RESULTADO_CHOICES = [
    ('Suficiente', 'Suficiente'),
    ('Insuficiente', 'Insuficiente'),
    ('Aprobado', 'Aprobado'),
    ('Reprobado', 'Reprobado'),
    ('Postergado', 'Postergado')
]

class Modalidad(models.Model):
    nombre = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name_plural = "Modalidades"
        verbose_name = "Modalidad"


    def __str__(self):
        return self.nombre

class Estudiante(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dni = models.CharField(max_length=20)
    carrera = models.CharField(max_length=100)
    
class Docente(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dni = models.CharField(max_length=20)
    especialidad = models.CharField(max_length=100)
    titulo = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.user.nombre}'

class Facultad(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    
    def __str__(self):
        return self.nombre


# Modelo de Carreras
class Carrera(models.Model):
    nombre_carrera = models.CharField(max_length=150)
    facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre_carrera

# Modelo de Semestre
class Semestre(models.Model):
    S_Semestre=models.CharField(max_length=100,verbose_name='Semestre')
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.S_Semestre

# Modelo de Materia
class Materia(models.Model):
    nombre_materia = models.CharField(max_length=150)
    codigo = models.CharField(max_length=50, unique=True)
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre_materia

# Modelo de Gestión
class Gestion(models.Model):
    anio = models.IntegerField(unique=True)
    
    def __str__(self):
         return str(self.anio)

# Modelo de Periodos
class Periodo(models.Model):
    numero = models.IntegerField()
    gestion = models.ForeignKey(Gestion, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-numero','-gestion__anio']  
    
    def __str__(self):
        return f'{self.numero}/{self.gestion.anio}'  


class InvCientifica(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Usuario relacionado', related_name='name_user')
    user_uno = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Segundo participante', blank=True, null=True, related_name='name_useruno')
    user_dos = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Tercer participante', blank=True, null=True, related_name='name_userdos')
    habilitar_users = models.BooleanField(default=False, verbose_name='¡Mas de un Estudiante click aqui!')
    invtitulo = models.CharField(max_length=450, verbose_name='Agregar Título')
    slug = models.SlugField(unique=True)
    invfecha_creacion = models.DateTimeField(auto_now_add=True)
    invdescripcion = models.TextField(verbose_name='Agregar una Descripción Breve', blank=True)
    invdocumentacion = models.FileField(upload_to='documento/investigacion', verbose_name='Agregar Documentacion', null=True, blank=True)
    investado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='Pendiente')
    
    class Meta:
        verbose_name_plural = "Investicaciones cientificas"
        verbose_name = "Investigacion cientifica"


    def __str__(self):
        return self.invtitulo

class ComentarioInvCientifica(models.Model):
    invcomentario = models.TextField(max_length=1000, help_text='', verbose_name='Ingrese Comentario Retroalimentativo')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    invfecha_post = models.DateTimeField(auto_now_add=True)
    invproyecto_relacionado = models.ForeignKey(InvCientifica, on_delete=models.CASCADE)
    invdocorregido = models.FileField(upload_to='documento/investigacion', verbose_name='Agregar Documentacion', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Comentario InvCientifica"
        verbose_name = "Comentario Inv"
        ordering = ['-invfecha_post']

    def __str__(self):
        return self.invcomentario[:15] + '...' if len(self.invcomentario) > 15 else self.invcomentario

class HabilitarSeguimiento(models.Model):
    habilitarInv = models.BooleanField(default=True, verbose_name='Habilitar Formulario')
    
    class Meta:
        verbose_name_plural = "Habilitacion Inv"
        verbose_name = "Habilitar Inv"

    def __str__(self):
        return "Configuración Global"

class PerfilProyecto(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Usuario relacionado', related_name='perfil_name_user')
    user_uno = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Segundo participante', blank=True, null=True, related_name='perfil_name_useruno')
    user_dos = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Tercer participante', blank=True, null=True, related_name='perfil_name_userdos')
    habilitar_users = models.BooleanField(default=False, verbose_name='¡Mas de un Estudiante click aqui!')
    pertitulo = models.CharField(max_length=450, verbose_name='Agregar Título Perfil')
    slug = models.SlugField(unique=True)
    perfecha_creacion = models.DateTimeField(auto_now_add=True)
    perdescripcion = models.TextField(verbose_name='Agregar una Descripción', blank=True)
    perdocumentacion = models.FileField(upload_to='documento/perfil', verbose_name='Agregar Documentación', null=True, blank=True)
    permodalidad = models.ForeignKey(Modalidad, on_delete=models.CASCADE, verbose_name='Seleccione Una Modalidad')
    perestado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='Pendiente')
    
    class Meta:
        verbose_name_plural = "Perfil de Proyectos"
        verbose_name = "Perfil Proyecto"

    def __str__(self):
        return self.pertitulo

class ComentarioPerfil(models.Model):
    percomentario = models.TextField(max_length=1000, help_text='', verbose_name='Ingrese Comentario Retroalimentativo')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    perfecha_post = models.DateTimeField(auto_now_add=True)
    perproyecto_relacionado = models.ForeignKey(PerfilProyecto, on_delete=models.CASCADE, related_name='comentarios')
    perdocorregido = models.FileField(upload_to='documento/perfil', verbose_name='Agregar Documentacion', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Comentario Perfiles"
        verbose_name = "Comentario Perfil"
        ordering = ['-perfecha_post']

    def __str__(self):
        return self.percomentario[:15] + '...' if len(self.percomentario) > 15 else self.percomentario


class ActaGeneral(models.Model):
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    perperiodo = models.ForeignKey(Periodo, on_delete=models.CASCADE, null=True)
    acta = models.CharField(max_length=30)
    estudiante = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='acta_estudiante', on_delete=models.CASCADE)
    estudiante_uno = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Segundo participante', blank=True, null=True, related_name='acta_estudianteuno')
    estudiante_dos = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Tercer participante', blank=True, null=True, related_name='acta_estudiantedos')
    titulo = models.CharField(max_length=450)
    lugar = models.CharField(max_length=50)
    fechadefensa = models.DateField(default=timezone.now)
    horainicio = models.TimeField()
    horafin = models.TimeField()
    tutor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='acta_tutor', on_delete=models.CASCADE)
    jurado_1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='acta_jurado_1', on_delete=models.CASCADE)
    jurado_2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='acta_jurado_2', on_delete=models.CASCADE)
    jurado_3 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='acta_jurado_3', on_delete=models.CASCADE)
    modalidad = models.ForeignKey('Modalidad', on_delete=models.CASCADE, verbose_name='Seleccione Una Modalidad')
    resultado = models.CharField(max_length=15, choices=RESULTADO_CHOICES, default='Suficiente')
    observacion_1 = models.TextField(max_length=200)
    observacion_2 = models.TextField(max_length=200)
    observacion_3 = models.TextField(max_length=200)
    
    class Meta:
        verbose_name_plural = "Actas Base General"
        verbose_name = "Base Actas"
        
    def __str__(self):
        return self.acta
    
class ActaProyectoPerfil(ActaGeneral):
    pass
    
    class Meta:
        verbose_name_plural = "Actas Defensa Perfiles"
        verbose_name = "Acta Perfil"
        
    def save(self, *args, **kwargs):
        if not self.pk:  # Es una nueva instancia
            self.acta # Personaliza según tu lógica
        super(ActaGeneral, self).save(*args, **kwargs)

class ActaPrivada(ActaGeneral):
    calificacion1 = models.IntegerField()
    
    class Meta:
        verbose_name_plural = "Actas defensa Privada"
        verbose_name = "Acta Privada"
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Es una nueva instancia
            self.acta  # Personaliza según tu lógica
        super(ActaGeneral, self).save(*args, **kwargs)
    
class ActaPublica(ActaGeneral):
    calificacion1 = models.IntegerField()
    calificacion2 = models.IntegerField()
    notatotal = models.IntegerField()
    presidenteacta = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='acta_presidente_Asig', on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = "Actas Defensa Publica"
        verbose_name = "Acta Publica"
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Es una nueva instancia
            self.acta # Personaliza según tu lógica
        super(ActaGeneral, self).save(*args, **kwargs)

class HabilitarProyectoFinal(models.Model):
    estudiante = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='actividad_estudiante', on_delete=models.CASCADE)
    estudiante_uno = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Segundo participante', blank=True, null=True, related_name='actividad_estudiante_uno')
    estudiante_dos = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Tercer participante', blank=True, null=True, related_name='actividad_estudiante_dos')
    tutor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='actividad_tutor', on_delete=models.CASCADE)
    jurado_1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='actividad_jurado_1', on_delete=models.CASCADE)
    jurado_2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='actividad_jurado_2', on_delete=models.CASCADE)
    jurado_3 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='actividad_jurado_3', on_delete=models.CASCADE)
    modalidad = models.ForeignKey(Modalidad, on_delete=models.CASCADE,  verbose_name='Seleccione Una Modalidad')

    def habilitar_actividad(self):
        actividad, created = ProyectoFinal.objects.get_or_create(
            estudiante=self.estudiante,
            defaults={
                'estudiante_uno': self.estudiante_uno,
                'estudiante_dos': self.estudiante_dos,
                'tutor': self.tutor,
                'jurado_1': self.jurado_1,
                'jurado_2': self.jurado_2,
                'jurado_3': self.jurado_3,
                'modalidad': self.modalidad,
                'habilitada': True
            }
        )
        if not created:
            actividad.estudiante_uno = self.estudiante_uno
            actividad.estudiante_dos = self.estudiante_dos
            actividad.tutor = self.tutor
            actividad.jurado_1 = self.jurado_1
            actividad.jurado_2 = self.jurado_2
            actividad.jurado_3 = self.jurado_3
            actividad.modalidad = self.modalidad
            actividad.habilitada = True
            actividad.save()
        return actividad
    
    class Meta:
        verbose_name_plural = "Habilitar Proyectos Final"
        verbose_name = "Habilitar Proyecto Final"
    
    def __str__(self):
        return f"HabilitarProyectoFinal for {self.estudiante}"
    
class ProyectoFinal(models.Model):
    estudiante = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='actividades_estudiante', on_delete=models.CASCADE)
    estudiante_uno = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Segundo participante', blank=True, null=True, related_name='actividades_estudiante_uno')
    estudiante_dos = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Tercer participante', blank=True, null=True, related_name='actividades_estudiante_dos')
    tutor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='actividades_tutor', on_delete=models.CASCADE)
    jurado_1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='actividades_jurado_1', on_delete=models.CASCADE)
    jurado_2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='actividades_jurado_2', on_delete=models.CASCADE)
    jurado_3 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='actividades_jurado_3', on_delete=models.CASCADE)
    modalidad = models.ForeignKey(Modalidad, on_delete=models.CASCADE)
    habilitada = models.BooleanField(default=False)
    titulo = models.CharField(max_length=450)
    resumen = models.TextField(max_length=500)
    fecha = models.DateField(default=timezone.now)
    guia_externo = models.CharField(max_length=250, default='Ninguno')
    documentacion = models.FileField(upload_to='documento/proyectofinal', verbose_name='Agregar Documentacion', null=True, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='Pendiente')
    jurado_1_aprobado = models.BooleanField(default=False)
    jurado_2_aprobado = models.BooleanField(default=False)
    jurado_3_aprobado = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Proyectos Finales"
        verbose_name = "Proyecto Final"

    def __str__(self):
        return f"ProyectoFinal for {self.estudiante}"
    
    @property
    def latest_comments(self):
        return self.comentarios.order_by('-actfecha_post')[:9]
    
    def save(self, *args, **kwargs):
        if self.estado in ['Aprobada', 'Rechazada']:
            # Verificar que todos los jurados han aprobado
            if not (self.jurado_1_aprobado and self.jurado_2_aprobado and self.jurado_3_aprobado):
                raise ValidationError("No se puede cambiar el estado sin la aprobación de todos los jurados.")
        
        super().save(*args, **kwargs)
    
    def transferir_a_repositorio(self, periodo, numero_acta, nota_aprobacion):
        repo_actividad, created = RepositorioTitulados.objects.get_or_create(
            estudiante=self.estudiante,
            estudiante_uno=self.estudiante_uno,
            estudiante_dos=self.estudiante_dos,
            tutor=self.tutor,
            jurado_1=self.jurado_1,
            jurado_2=self.jurado_2,
            jurado_3=self.jurado_3,
            titulo=self.titulo,
            resumen=self.resumen,
            modalidad=self.modalidad,
            fecha=self.fecha,
            guia_externo=self.guia_externo,
            documentacion=self.documentacion,
            estado=self.estado,
            jurado_1_aprobado=self.jurado_1_aprobado,
            jurado_2_aprobado=self.jurado_2_aprobado,
            jurado_3_aprobado=self.jurado_3_aprobado,
            periodo=periodo,
            numero_acta=numero_acta,
            nota_aprobacion=nota_aprobacion
        )
        return repo_actividad
    
class ComentarioProFinal(models.Model):
    actcomentario = models.TextField(max_length=1000, help_text='', verbose_name='Ingrese Comentario Retroalimentativo')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    actfecha_post = models.DateTimeField(auto_now_add=True)
    actproyecto_relacionado = models.ForeignKey(ProyectoFinal, on_delete=models.CASCADE, related_name='comentarios')
    actdocorregido = models.FileField(upload_to='documento/proyectofinal', verbose_name='Agregar Documento', null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Comentarios Proyecto Final"
        verbose_name = "Comentario Proyecto Final"
        ordering = ['-actfecha_post']

    def __str__(self):
        return self.actcomentario[:15] + '...' if len(self.actcomentario) > 15 else self.actcomentario
   
class RepositorioTitulados(models.Model):
    estudiante = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='repo_estudiante', on_delete=models.CASCADE)
    estudiante_uno = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Segundo participante', blank=True, null=True, related_name='repo_estudiante_uno')
    estudiante_dos = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Tercer participante', blank=True, null=True, related_name='repo_estudiante_dos')
    tutor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='repo_tutor', on_delete=models.CASCADE)
    jurado_1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='repo_jurado_1', on_delete=models.CASCADE)
    jurado_2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='repo_jurado_2', on_delete=models.CASCADE)
    jurado_3 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='repo_jurado_3', on_delete=models.CASCADE)
    habilitada = models.BooleanField(default=False)
    titulo = models.CharField(max_length=450 )
    resumen = models.TextField(max_length=500 )
    modalidad = models.ForeignKey(Modalidad, on_delete=models.CASCADE, default=1, verbose_name='Seleccione Una Modalidad')
    fecha = models.DateField(default=timezone.now)
    guia_externo = models.CharField(max_length=250)
    documentacion = models.FileField(upload_to='documento/repositorios', verbose_name='Agregar Documentacion', null=True, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='Pendiente')
    jurado_1_aprobado = models.BooleanField(default=False)
    jurado_2_aprobado = models.BooleanField(default=False)
    jurado_3_aprobado = models.BooleanField(default=False)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    numero_acta = models.CharField(max_length=50)
    nota_aprobacion = models.IntegerField()
    
    class Meta:
        verbose_name_plural = "Repositorio de Proyectos"
        verbose_name = "Repositorio"

    def __str__(self):
        return f"Repositorio Actividad for {self.estudiante}"



