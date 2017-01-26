from django.contrib import admin

from .models import Pregunta, Respuesta

# class ChoiceInline(admin.StackedInline):
#     model = Respuesta
#     extra = 2

class ChoiceInline(admin.TabularInline):
    model = Respuesta
    extra = 2

class PreguntaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['texto_pregunta']}),
        ('Informacion de fecha', {'fields': ['fecha_publicacion'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('texto_pregunta', 'fecha_publicacion', 'fue_publicado_recientemente')
    list_filter = ['fecha_publicacion']
    search_fields = ['texto_pregunta']

admin.site.register(Pregunta, PreguntaAdmin)
