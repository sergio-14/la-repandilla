# Generated by Django 5.1 on 2024-10-09 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seg_mod_graduacion', '0024_alter_invcientifica_habilitar_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfilproyecto',
            name='habilitar_users',
            field=models.BooleanField(default=False, verbose_name='¡Mas de un Estudiante click aqui!'),
        ),
    ]
