# Generated by Django 5.1 on 2024-10-01 16:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seg_mod_graduacion', '0014_proyectofinal_estudiante_dos_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_carrera', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Facultad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Gestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anio', models.IntegerField(unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='actageneral',
            name='facultad',
        ),
        migrations.AlterField(
            model_name='actageneral',
            name='carrera',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seg_mod_graduacion.carrera'),
        ),
        migrations.CreateModel(
            name='Docente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dni', models.CharField(max_length=20, unique=True)),
                ('especialidad', models.CharField(max_length=100)),
                ('titulo', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='actageneral',
            name='jurado_1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acta_jurado_1', to='seg_mod_graduacion.docente'),
        ),
        migrations.AlterField(
            model_name='actageneral',
            name='jurado_2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acta_jurado_2', to='seg_mod_graduacion.docente'),
        ),
        migrations.AlterField(
            model_name='actageneral',
            name='jurado_3',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acta_jurado_3', to='seg_mod_graduacion.docente'),
        ),
        migrations.AlterField(
            model_name='actageneral',
            name='tutor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acta_tutor', to='seg_mod_graduacion.docente'),
        ),
        migrations.AlterField(
            model_name='actapublica',
            name='presidenteacta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acta_presidente_Asig', to='seg_mod_graduacion.docente'),
        ),
        migrations.AlterField(
            model_name='comentarioinvcientifica',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='seg_mod_graduacion.docente'),
        ),
        migrations.AlterField(
            model_name='comentarioperfil',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='seg_mod_graduacion.docente'),
        ),
        migrations.AlterField(
            model_name='comentarioprofinal',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='seg_mod_graduacion.docente'),
        ),
        migrations.AlterField(
            model_name='habilitarproyectofinal',
            name='jurado_1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actividad_jurado_1', to='seg_mod_graduacion.docente'),
        ),
        migrations.AlterField(
            model_name='habilitarproyectofinal',
            name='jurado_2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actividad_jurado_2', to='seg_mod_graduacion.docente'),
        ),
        migrations.AlterField(
            model_name='habilitarproyectofinal',
            name='jurado_3',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actividad_jurado_3', to='seg_mod_graduacion.docente'),
        ),
        migrations.AlterField(
            model_name='habilitarproyectofinal',
            name='tutor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actividad_tutor', to='seg_mod_graduacion.docente'),
        ),
        migrations.AlterField(
            model_name='proyectofinal',
            name='jurado_1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actividades_jurado_1', to='seg_mod_graduacion.docente'),
        ),
        migrations.AlterField(
            model_name='proyectofinal',
            name='jurado_2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actividades_jurado_2', to='seg_mod_graduacion.docente'),
        ),
        migrations.AlterField(
            model_name='proyectofinal',
            name='jurado_3',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actividades_jurado_3', to='seg_mod_graduacion.docente'),
        ),
        migrations.AlterField(
            model_name='proyectofinal',
            name='tutor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actividades_tutor', to='seg_mod_graduacion.docente'),
        ),
        migrations.AlterField(
            model_name='repositoriotitulados',
            name='jurado_1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='repo_jurado_1', to='seg_mod_graduacion.docente'),
        ),
        migrations.AlterField(
            model_name='repositoriotitulados',
            name='jurado_2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='repo_jurado_2', to='seg_mod_graduacion.docente'),
        ),
        migrations.AlterField(
            model_name='repositoriotitulados',
            name='jurado_3',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='repo_jurado_3', to='seg_mod_graduacion.docente'),
        ),
        migrations.AlterField(
            model_name='repositoriotitulados',
            name='tutor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='repo_tutor', to='seg_mod_graduacion.docente'),
        ),
        migrations.CreateModel(
            name='Estudiante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dni', models.CharField(max_length=20, unique=True)),
                ('carrera', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='actageneral',
            name='estudiante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acta_estudiante', to='seg_mod_graduacion.estudiante'),
        ),
        migrations.AlterField(
            model_name='actageneral',
            name='estudiante_dos',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='acta_estudiantedos', to='seg_mod_graduacion.estudiante', verbose_name='Tercer participante'),
        ),
        migrations.AlterField(
            model_name='actageneral',
            name='estudiante_uno',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='acta_estudianteuno', to='seg_mod_graduacion.estudiante', verbose_name='Segundo participante'),
        ),
        migrations.AlterField(
            model_name='habilitarproyectofinal',
            name='estudiante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actividad_estudiante', to='seg_mod_graduacion.estudiante'),
        ),
        migrations.AlterField(
            model_name='habilitarproyectofinal',
            name='estudiante_dos',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='actividad_estudiante_dos', to='seg_mod_graduacion.estudiante', verbose_name='Tercer participante'),
        ),
        migrations.AlterField(
            model_name='habilitarproyectofinal',
            name='estudiante_uno',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='actividad_estudiante_uno', to='seg_mod_graduacion.estudiante', verbose_name='Segundo participante'),
        ),
        migrations.AlterField(
            model_name='invcientifica',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='name_user', to='seg_mod_graduacion.estudiante', verbose_name='Usuario relacionado'),
        ),
        migrations.AlterField(
            model_name='invcientifica',
            name='user_dos',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='name_userdos', to='seg_mod_graduacion.estudiante', verbose_name='Tercer participante'),
        ),
        migrations.AlterField(
            model_name='invcientifica',
            name='user_uno',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='name_useruno', to='seg_mod_graduacion.estudiante', verbose_name='Segundo participante'),
        ),
        migrations.AlterField(
            model_name='perfilproyecto',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='perfil_name_user', to='seg_mod_graduacion.estudiante', verbose_name='Usuario relacionado'),
        ),
        migrations.AlterField(
            model_name='perfilproyecto',
            name='user_dos',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='perfil_name_userdos', to='seg_mod_graduacion.estudiante', verbose_name='Tercer participante'),
        ),
        migrations.AlterField(
            model_name='perfilproyecto',
            name='user_uno',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='perfil_name_useruno', to='seg_mod_graduacion.estudiante', verbose_name='Segundo participante'),
        ),
        migrations.AlterField(
            model_name='proyectofinal',
            name='estudiante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actividades_estudiante', to='seg_mod_graduacion.estudiante'),
        ),
        migrations.AlterField(
            model_name='proyectofinal',
            name='estudiante_dos',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='actividades_estudiante_dos', to='seg_mod_graduacion.estudiante', verbose_name='Tercer participante'),
        ),
        migrations.AlterField(
            model_name='proyectofinal',
            name='estudiante_uno',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='actividades_estudiante_uno', to='seg_mod_graduacion.estudiante', verbose_name='Segundo participante'),
        ),
        migrations.AlterField(
            model_name='repositoriotitulados',
            name='estudiante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='repo_estudiante', to='seg_mod_graduacion.estudiante'),
        ),
        migrations.AlterField(
            model_name='repositoriotitulados',
            name='estudiante_dos',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='repo_estudiante_dos', to='seg_mod_graduacion.estudiante', verbose_name='Tercer participante'),
        ),
        migrations.AlterField(
            model_name='repositoriotitulados',
            name='estudiante_uno',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='repo_estudiante_uno', to='seg_mod_graduacion.estudiante', verbose_name='Segundo participante'),
        ),
        migrations.AddField(
            model_name='carrera',
            name='facultad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seg_mod_graduacion.facultad'),
        ),
        migrations.CreateModel(
            name='Periodo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField()),
                ('gestion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seg_mod_graduacion.gestion')),
            ],
        ),
        migrations.AlterField(
            model_name='actageneral',
            name='perperiodo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='seg_mod_graduacion.periodo'),
        ),
        migrations.AlterField(
            model_name='repositoriotitulados',
            name='periodo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seg_mod_graduacion.periodo'),
        ),
        migrations.CreateModel(
            name='Semestre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('S_Semestre', models.CharField(max_length=100, verbose_name='Semestre')),
                ('carrera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seg_mod_graduacion.carrera')),
            ],
        ),
        migrations.CreateModel(
            name='Materia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_materia', models.CharField(max_length=150)),
                ('codigo', models.CharField(max_length=50, unique=True)),
                ('carrera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seg_mod_graduacion.carrera')),
                ('semestre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seg_mod_graduacion.semestre')),
            ],
        ),
        migrations.DeleteModel(
            name='logica',
        ),
    ]
