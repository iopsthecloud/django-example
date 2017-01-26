# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-18 10:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Respuesta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto_respuesta', models.CharField(max_length=200)),
                ('votos', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto_pregunta', models.CharField(max_length=200)),
                ('fecha_publicacion', models.DateTimeField(verbose_name='fecha de publicacion')),
            ],
        ),
        migrations.AddField(
            model_name='respuesta',
            name='pregunta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='encuestas.Pregunta'),
        ),
    ]
