from __future__ import unicode_literals

import datetime
from django.db import models
from django.utils import timezone

class Pregunta(models.Model):
    texto_pregunta = models.CharField(max_length=200)
    fecha_publicacion = models.DateTimeField('fecha de publicacion')
    def __str__(self):
        return self.texto_pregunta
    def fue_publicado_recientemente(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.fecha_publicacion <= now #returns TRUE
    fue_publicado_recientemente.admin_order_field = 'fecha_publicacion'
    fue_publicado_recientemente.boolean = True
    fue_publicado_recientemente.short_description = 'Fue publicada recientemente?'

class Respuesta(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    texto_respuesta = models.CharField(max_length=200)
    votos = models.IntegerField(default=0)
    def __str__(self):
        return self.texto_respuesta