from django.views import View
from django.http.response import HttpResponse
from django.views.generic.base import TemplateView
from django.shortcuts import render
from hypercar.settings import QUEUE

menu = {
    'change_oil' : 'Change oil',
    'inflate_tires': 'Inflate tires',
    'diagnostic': 'Get diagnostic test',
}


def check_time(queue, type_of_service):
    time = 0
    for item in queue:
        if item == 'change_oil':
            time += 2
        elif item == 'inflate_tires' and type_of_service != 'change_oil':
            time += 5
        elif item == 'diagnostic' and type_of_service != 'change_oil' and type_of_service != 'inflate_tires':
            time += 30
    return time


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/welcome.html')


class MenuView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/menu.html', context={'menu': menu})


class TicketView(TemplateView):
    template_name = 'tickets/ticket.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['number'] = len(QUEUE) + 1
        context['wait_time'] = check_time(QUEUE, kwargs['service'])
        QUEUE.append(kwargs['service'])
        return context
