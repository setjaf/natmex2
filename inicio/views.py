#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from inicio.form import LoginForm
from django.contrib.auth import authenticate, login, logout

# importar librerias de reportlab
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
#fin librerias reportlab

from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, cm

from .models import Personal



def index(request):
    message=None
    print(request.user)
    form = LoginForm()

    if request.user.is_authenticated:
        if request.method == "POST":
            if "salir" in request.POST:
                logout(request)
                context={'form':form}
                return HttpResponse(render(request, 'inicio/recepcion.html', context))

        p=Personal.objects.get(usuario=request.user.id)
        context={'nombre':p.nombre,'admin':request.user.is_admin,'personal':request.user.is_personal}
        return HttpResponse(render(request, 'inicio/inicio.html',context))

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
    return HttpResponse(render(request, 'inicio/recepcion.html', context))



def otra(request):
    print(request.COOKIES)
    if request.user.is_authenticated:
        '''p=Personal.objects.get(usuario=request.user.id)
        context={'nombre':p.nombre}
        response=HttpResponse(content_type="application/pdf")
        response['Content-Disposition'] = 'filename="somefilename.pdf"'
        buffer=BytesIO()

        c = canvas.Canvas(buffer,pagesize=A4)
        c.drawString(100,750,p.nombre)
        c.save()
        pdf = buffer.getvalue()
        buffer.close()


        response.write(pdf)

        return response
'''
        print "Genero el PDF"
        response = HttpResponse(content_type='application/pdf')
        pdf_name = "clientes.pdf"  # llamado clientes
        # la linea 26 es por si deseas descargar el pdf a tu computadora
        # response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
        buff = BytesIO()
        doc = SimpleDocTemplate(buff,
                                pagesize=letter,
                                rightMargin=40,
                                leftMargin=40,
                                topMargin=60,
                                bottomMargin=18,
                                )
        personal = []
        styles = getSampleStyleSheet()
        header = Paragraph("Listado de Personal", styles['Heading1'])
        personal.append(header)
        headings = ('Nombre', 'Ape Pat', 'Ape Mat')
        allpersonal = [(p.nombre, p.apellido_paterno, p.apellido_materno) for p in Personal.objects.all()]
        print allpersonal

        t = Table([headings] + allpersonal)
        t.setStyle(TableStyle(
            [
                ('GRID', (0, 0), (3, -1), 1, colors.dodgerblue),
                ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
                ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
            ]
        ))
        personal.append(t)
        doc.build(personal)
        response.write(buff.getvalue())
        buff.close()
        return response
    else:
        return redirect('/')



# Create your views here.
