from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect

from .forms import RegisterForm


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)

    form = RegisterForm(register_form_data)

    context = {
        'form': form,
    }
    return render(request, 'authors/pages/register_view.html', context)


def register_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        form.save()
        messages.success(request, 'User created with success, please log in.')

        del (request.session['register_form_data'])

    return redirect('authors:register')