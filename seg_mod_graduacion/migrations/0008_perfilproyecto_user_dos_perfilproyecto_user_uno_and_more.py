# Generated by Django 5.1 on 2024-09-24 15:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seg_mod_graduacion', '0007_alter_invcientifica_habilitar_users_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='perfilproyecto',
            name='user_dos',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='perfil_name_userdos', to=settings.AUTH_USER_MODEL, verbose_name='Tercer participante'),
        ),
        migrations.AddField(
            model_name='perfilproyecto',
            name='user_uno',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='perfil_name_useruno', to=settings.AUTH_USER_MODEL, verbose_name='Segundo participante'),
        ),
        migrations.AlterField(
            model_name='perfilproyecto',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='perfil_name_user', to=settings.AUTH_USER_MODEL, verbose_name='Usuario relacionado'),
        ),
    ]
