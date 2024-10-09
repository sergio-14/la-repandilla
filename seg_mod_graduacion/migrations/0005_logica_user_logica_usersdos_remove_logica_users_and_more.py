# Generated by Django 5.1 on 2024-09-22 13:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seg_mod_graduacion', '0004_alter_invcientifica_invdocumentacion_logica'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='logica',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='logica_user', to=settings.AUTH_USER_MODEL, verbose_name='Usuario relacionado'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='logica',
            name='usersdos',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='logica_usersdos', to=settings.AUTH_USER_MODEL, verbose_name='Usuarios relacionados'),
        ),
        migrations.RemoveField(
            model_name='logica',
            name='users',
        ),
        migrations.AddField(
            model_name='logica',
            name='users',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='logica_users', to=settings.AUTH_USER_MODEL, verbose_name='Usuarios relacionados'),
        ),
    ]
