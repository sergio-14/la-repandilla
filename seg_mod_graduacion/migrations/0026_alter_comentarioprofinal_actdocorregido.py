# Generated by Django 5.1 on 2024-10-09 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seg_mod_graduacion', '0025_alter_perfilproyecto_habilitar_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentarioprofinal',
            name='actdocorregido',
            field=models.FileField(blank=True, null=True, upload_to='documento/proyectofinal', verbose_name='Agregar Documento'),
        ),
    ]
