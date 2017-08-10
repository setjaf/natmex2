#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from inicio.form import LoginForm
from django.contrib.auth import authenticate, login

from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, cm

from .models import Personal



def index(request):
    message=None
    print(request.user)
    if request.user.is_authenticated:
        p=Personal.objects.get(usuario=request.user.id)
        context={'nombre':p.nombre,'admin':request.user.is_admin,'personal':request.user.is_personal}
        return HttpResponse(render(request, 'inicio/index.html',context))
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username,password=password)
            if user is not None:
                login (request,user)
                message = 'Te has autentificado correctamente'
            else:
                message = 'Usuario o contraseña erroneos'
        else:
            message = 'Nombre y password incorrectos'
    else:
        form = LoginForm()
    context={'messages':message, 'form':form}
    return HttpResponse(render(request, 'inicio/login.html', context))



def otra(request):
    print(request.COOKIES)
    if request.user.is_authenticated:
        p=Personal.objects.get(usuario=request.user.id)
        context={'nombre':p.nombre}

        buffer=BytesIO()

        c = canvas.Canvas(buffer,pagesize=A4)
        c.drawString(100,750,"Welcome to Reportlab!")
        c.save()
        pdf = buffer.getvalue()
        buffer.close()

        response=HttpResponse(content_type="application/pdf")
        response['Content-Dispositon']='attachment=filename=prueba.pdf'
        response.write(pdf)

        return response
    else:
        return redirect('/')



# Create your views here.
