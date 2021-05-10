from django.shortcuts import render
from django.forms import modelform_factory
from django.views.generic import FormView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.core import serializers
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
import json
from .models import ZOO
from .models import animals
from .models import Aviary


class CreateZooView(FormView):
    template_name = 'create_zoo.html'
    form_class = modelform_factory(ZOO,
                                   fields=('title', 'total_area', 'unit'),
                                   labels={'title': 'Zoo name'},
                                   help_texts={'total_area': 'The total area of the zoo'})

    def get_form(self, form_class=None):
        self.object = super().get_form(form_class)
        return self.object

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('index')


def index(request):
    template_name = 'zoo_list.html'
    zoos = ZOO.objects.all()
    context = {'zoos': zoos}
    return render(request, template_name, context)


def zoo_view(request, pk):
    template_name = 'zoo_view.html'
    context = {}
    zoo = ZOO.objects.get(pk=pk)
    context['zoo'] = zoo
    context['animalTypes'] = [a[0] for a in animals]
    if request.method == 'POST':
        available_aviaries: list = []
        for av in ZOO.objects.get(pk=pk).aviaries.all():
            available_aviaries.append(av.typeOfAnimals)
        if request.POST['newAvType'] in available_aviaries:
            messages.add_message(request, messages.ERROR, _('An unknown error has occurred'))
            return HttpResponseRedirect(reverse_lazy('zoo', kwargs={'pk': pk}))

        newAv = Aviary()
        newAv.zoo = ZOO.objects.get(pk=pk)
        newAv.total_area = int(request.POST['newAvTotalArea'])
        newAv.typeOfAnimals = request.POST['newAvType']
        newAv.required_area = int(request.POST['newAvReqArea'])
        newAv.save()
        return HttpResponseRedirect(reverse_lazy('zoo', kwargs={'pk': pk}))

    return render(request, template_name, context=context)


def task_info(request):
    template_name = 'task_info.html'
    return render(request, template_name)


def update_changes(request):
    if request.method == 'POST':
        if request.is_ajax():
            data = json.loads(request.POST['newData'])
            zoo_id = data['zooId']
            new_data = data['aviaries']
            all_data_saved: bool = True
            for av in new_data:
                animals_type = av
                new_amount = int(new_data[av]['amountAnimals'])
                new_total_area = float(new_data[av]['totalArea'])
                aviary = Aviary.objects.get(zoo_id=zoo_id, typeOfAnimals=animals_type)
                aviary.amount_animals = new_amount
                aviary.total_area = new_total_area
                try:
                    aviary.full_clean()
                except ValidationError as e:
                    all_data_saved = False
                aviary.save()
            return JsonResponse({'success': True,
                                 'allSaved': all_data_saved
                                 })
        return JsonResponse({'success': False})














