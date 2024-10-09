from django.contrib import admin
from .models import InvCientifica, Modalidad, ComentarioInvCientifica, ComentarioPerfil, PerfilProyecto

from .models import ProyectoFinal, HabilitarProyectoFinal,ComentarioProFinal,RepositorioTitulados,Facultad,Gestion
from .models import ActaProyectoPerfil, ActaGeneral,ActaPrivada, ActaPublica, Estudiante, Docente, Carrera,Periodo

admin.site.register(ProyectoFinal)
admin.site.register(HabilitarProyectoFinal)

# Registra tus modelos aquí
admin.site.register(InvCientifica)
admin.site.register(Modalidad)
admin.site.register(ComentarioInvCientifica)
admin.site.register(ComentarioPerfil)
admin.site.register(PerfilProyecto)
admin.site.register(ComentarioProFinal)
admin.site.register(RepositorioTitulados)
admin.site.register(ActaGeneral)
admin.site.register(ActaPublica)
admin.site.register(ActaPrivada)
admin.site.register(ActaProyectoPerfil)
admin.site.register(Estudiante)
admin.site.register(Docente)
admin.site.register(Carrera)
admin.site.register(Periodo)
admin.site.register(Gestion)
admin.site.register(Facultad)
