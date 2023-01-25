from django.shortcuts import render, redirect
from core.models import Eventos
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime
from django.http.response import Http404

# Create your views here.
def index(request):
    return redirect('/agenda')

def submit_log(request):
    if request.POST:
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        usuario = authenticate(username=username, password=senha)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request, 'Usuario ou senha inválidos!')
    return redirect('/')

def login_user(request):
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/login/')
def listagem_agenda(request):
    usuario = request.user
    data_atual = datetime.now()
    eventos = Eventos.objects.filter(usuario=usuario,
                                     dataEvento__gt=data_atual)
    dados = {'eventos': eventos}
    return render(request, 'index.html', dados)

@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = Eventos.objects.get(id=id_evento)
    return render(request, 'evento.html', dados)

@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data')
        id_evento = request.POST.get('id')
        descricao = request.POST.get('descricao')
        usuario = request.user
        if id_evento:
            Eventos.objects.filter(id=id_evento).update(titulo=titulo,
                                                        dataEvento=data_evento,
                                                        descricao=descricao)
        else:
            Eventos.objects.create(titulo=titulo,
                                   dataEvento=data_evento,
                                   descricao=descricao,
                                   usuario=usuario)
    return redirect('/')

@login_required(login_url='/login/')
def delete_evento(request, id_usuario):
    usuario = request.user
    try:
        evento = Eventos.objects.get(id=id_usuario)
    except Exception:
        raise Http404()
    if usuario == evento.usuario:
        evento.delete()
    else:
        raise Http404()

    return redirect('/')