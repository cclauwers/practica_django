from django.utils import timezone
from django.core import serializers
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateResponseMixin
from models import Botiga
from forms import *

# Create your views here.
class ConnegResponseMixin(TemplateResponseMixin):

    def render_json_object_response(self, objects, **kwargs):
        json_data = serializers.serialize(u"json", objects, **kwargs)
        return HttpResponse(json_data, content_type=u"application/json")

    def render_xml_object_response(self, objects, **kwargs):
        xml_data = serializers.serialize(u"xml", objects, **kwargs)
        return HttpResponse(xml_data, content_type=u"application/xml")

    def render_to_response(self, context, **kwargs):
        if 'extension' in self.kwargs:
            try:
                objects = [self.object]
            except AttributeError:
                objects = self.object_list
            if self.kwargs['extension'] == 'json':
                return self.render_json_object_response(objects=objects)
            elif self.kwargs['extension'] == 'xml':
                return self.render_xml_object_response(objects=objects)
        return super(ConnegResponseMixin, self).render_to_response(context)

class BotigaCreate(CreateView):
    model = Botiga
    template_name = 'icommerce/form.html'
    form_class = BotigaForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(BotigaCreate, self).form_valid(form)

class BotigaList(ListView, ConnegResponseMixin):
    model = Botiga
    queryset = Botiga.objects.filter(date__lte=timezone.now()).order_by('date')[:5]
    context_object_name = 'latest_botiga_list'
    template_name = 'icommerce/Botiga_list.html'

class BotigaDetail(DetailView, ConnegResponseMixin):
    model = Botiga
    template_name = 'icommerce/Botiga_detail.html'

    def get_context_data(self, **kwargs):
        context = super(BotigaDetail, self).get_context_data(**kwargs)
        #context['RATING_CHOICES'] = RestaurantReview.RATING_CHOICES
        return context

class MarcaList(ListView, ConnegResponseMixin):
    model =Marca
    #queryset = Botiga.objects.filter(date__lte=timezone.now()).order_by('date')[:1]
    #context_object_name = 'latest_marca_list'
    template_name = 'icommerce/Marca_list.html'

    def get_queryset(self):
        return Marca.objects.filter(botiga=self.kwargs['pk'])

class MarcaDetail(DetailView, ConnegResponseMixin):
    model = Marca
    template_name = 'icommerce/Marca_detail.html'

class MarcaCreate(CreateView):
    model = Marca
    template_name = 'icommerce/form.html'
    form_class = MarcaForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.botiga = Marca.objects.get(id=self.kwargs['pk'])
        return super(MarcaCreate, self).form_valid(form)

class PesaRobaList(ListView, ConnegResponseMixin):
    model = Pesa_roba
    #queryset = Botiga.objects.filter(date__lte=timezone.now()).order_by('date')[:1]
    #context_object_name = 'latest_marca_list'
    #template_name = 'icommerce/Marca_list.html'

    def get_queryset(self):
        return Pesa_roba.objects.filter(botiga=self.kwargs['pk'])