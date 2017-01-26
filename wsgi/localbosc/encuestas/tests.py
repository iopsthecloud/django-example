import datetime
from django.utils import timezone
from django.test import TestCase
from .models import Pregunta
from django.urls import reverse

class PreguntaMethodTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        fue_publicado_recientemente() debera regresar FALSE para preguntas 
        cuya fecha_de_publicacion es en el futuro.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Pregunta(fecha_publicacion=time)
        self.assertIs(future_question.fue_publicado_recientemente(), False)

    def test_was_published_recently_with_old_question(self):
        """
	    fue_publicado_recientemente() debera regresar FALSE para preguntas 
	    cuya fecha_de_publicacion es hace mas de un dia/mes?.
	    """
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Pregunta(fecha_publicacion=time)
        self.assertIs(old_question.fue_publicado_recientemente(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        fue_publicado_recientemente() debera regresar TRUE para preguntas
	    cuya fecha_de_publicacion fue dentro del dia inmediatamente anterior.
        """
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Pregunta(fecha_publicacion=time)
        self.assertIs(recent_question.fue_publicado_recientemente(), True)

#Metodo para crear preguntas
def crear_pregunta(texto_pregunta, days):
    """
    Creates a question with the given `texto_pregunta` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Pregunta.objects.create(texto_pregunta=texto_pregunta, fecha_publicacion=time)


class PreguntaViewTests(TestCase):

    def test_index_view_with_no_questions(self):
    	#Si no hay preguntas, debe mostrarse un mensaje apropiado.
        response = self.client.get(reverse('encuestas:index'))
        self.assertEqual(response.status_code, 200)
        #Verifica que se despliegue el mensaje "No hay encuestas disponibles."
        self.assertContains(response, "No hay encuestas disponibles.")
        #Verifica que lista_ultimas_preguntas este vacio
        self.assertQuerysetEqual(response.context['lista_ultimas_preguntas'], [])

    def test_index_view_with_a_past_question(self):
    	# Preguntas con fecha_publicacion en el pasado seran mostradas en la pagina 'index'.
        crear_pregunta(texto_pregunta="Pregunta en el pasado.", days=-30)
        response = self.client.get(reverse('encuestas:index'))
        #Verificamos que la pregunta creada aparezca en la lista.
        self.assertQuerysetEqual(
            response.context['lista_ultimas_preguntas'],
            ['<Pregunta: Past question.>']
        )

    def test_index_view_with_a_future_question(self):
    	# Preguntas con una fecha de creacion en el futuro no deben ser mostradas en el indice.
        crear_pregunta(texto_pregunta="Pregunta en el futuro.", days=30)
        response = self.client.get(reverse('encuestas:index'))
        self.assertContains(response, "No hay encuestas disponibles.")
        self.assertQuerysetEqual(response.context['lista_ultimas_preguntas'], [])

#La base de datos se reinicia por cada metodo de test, asi que la primer pregunta no esta mas aqui
#por lo que el indice no debera tener ninguna pregunta

    def test_index_view_with_future_question_and_past_question(self):
    	# Si existen ambas preguntas, en el pasado y en el futuro, solo la del pasado puede mostrarse.
        crear_pregunta(texto_pregunta="Pregunta en el pasado.", days=-30)
        crear_pregunta(texto_pregunta="Pregunta en el futuro.", days=30)
        response = self.client.get(reverse('encuestas:index'))
        self.assertQuerysetEqual(
            response.context['lista_ultimas_preguntas'],
            ['<Pregunta: Past question.>']
        )

    def test_index_view_with_two_past_questions(self):
        # El indice puede desplegar multiples preguntas.
        crear_pregunta(texto_pregunta="Pregunta en el pasado 1.", days=-30)
        crear_pregunta(texto_pregunta="Pregunta en el pasado 2.", days=-5)
        response = self.client.get(reverse('encuestas:index'))
        self.assertQuerysetEqual(
            response.context['lista_ultimas_preguntas'],
            ['<Pregunta: Pregunta en el pasado 2.>', '<Pregunta: Pregunta en el pasado 1.>']
        )

class PreguntaIndexDetailTests(TestCase):
    def test_detail_view_with_a_future_question(self):
        """
        The detail view of a question with a pub_date in the future should
        return a 404 not found.
        """
        future_question = crear_pregunta(texto_pregunta='Pregunta en el futuro.', days=5)
        url = reverse('encuestas:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_question(self):
        """
        The detail view of a question with a pub_date in the past should
        display the question's text.
        """
        past_question = crear_pregunta(texto_pregunta='Pregunta en el pasado.', days=-5)
        url = reverse('encuestas:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.texto_pregunta)