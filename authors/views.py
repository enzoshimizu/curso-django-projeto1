from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import RegisterForm


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)

    form = RegisterForm(register_form_data)

    context = {
        'form': form,
        'form_action': reverse('authors:create'),
    }
    return render(request, 'authors/pages/register_view.html', context)


def register_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()

        messages.success(request, 'User created with success, please log in.')

        del (request.session['register_form_data'])

    return redirect('authors:register')
