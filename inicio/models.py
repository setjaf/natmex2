# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from datetime import datetime

from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=200,unique=True)
    email = models.EmailField(_('email address'), unique=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=False)
    is_admin = models.BooleanField(_('administrador'), default=False)
    is_personal = models.BooleanField(_('Personal'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.username

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

# Create your models here.

class Personal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    nombre = models.CharField(max_length=100, blank=True)
    apellido_paterno = models.CharField(max_length=100, blank=True)
    apellido_materno = models.CharField(max_length=100, blank=True)
    fecha_creacion = models.DateTimeField('dia_creado', auto_now_add=True)
    puesto = models.CharField(max_length=100, blank=True)
    usuario = models.ForeignKey('User',on_delete=models.CASCADE, blank=True, unique=True, null=True)
    class Meta:
        verbose_name = _('persona')
        verbose_name_plural = _('Personal')

    def __str__(self):
        return self.nombre
