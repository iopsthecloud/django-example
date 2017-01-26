from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.http import Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
# from django.template import loader
from .models import Pregunta, Respuesta

class IndexView(generic.ListView):
    template_name = 'encuestas/index.html'
    context_object_name = 'lista_ultimas_preguntas'

    def get_queryset(self):
        """
        Return the last five published questions (not including those 
        set to be published in the future).
        Pregunta.objects.filter(fecha_publicacion__lte=timezone.now()) returns 
        a queryset containing Questions whose pub_date is less than or 
        equal to - that is, earlier than or equal to - timezone.now.
        """
        return Pregunta.objects.filter(
            fecha_publicacion__lte=timezone.now()
        ).order_by('-fecha_publicacion')[:5]

class DetailView(generic.DetailView):
    model = Pregunta
    template_name = 'encuestas/detalle.html'

    def get_queryset(self):
        #Excluye cualquier pregunta que no haya sido publicada aun
        return Pregunta.objects.filter(fecha_publicacion__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Pregunta
    template_name = 'encuestas/resultados.html'

def votes(request, question_id):
    pregunta = get_object_or_404(Pregunta, pk=question_id)
    try:
        selected_respuesta = pregunta.respuesta_set.get(pk=request.POST['respuesta'])
    except (KeyError, Respuesta.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'encuestas/detalle.html', {
            'pregunta': pregunta,
            'error_message': "No seleccionaste respuesta alguna",
        })
    else:
        selected_respuesta.votos += 1
        selected_respuesta.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('encuestas:results', args=(pregunta.id,)))
