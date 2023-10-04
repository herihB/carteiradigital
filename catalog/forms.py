from logging import raiseExceptions
from pickle import GET
from webbrowser import get
from django import forms
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth import password_validation
from . import models
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import *
from dal import autocomplete
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404


class EstudanteFormCadastro(forms.Form):
    email = forms.EmailField(
        label='E-mail', 
        widget=forms.EmailInput(
            attrs={
                'class': 'input is-primary'
            }
        )
    )

    password1 = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(
            attrs={
                'class': 'input is-primary'
            }
        )
    )

    password2 = forms.CharField(
        label='Confirmação de senha',
        widget=forms.PasswordInput(
            attrs={
                'class': 'input is-primary'
            }
        )
    )

    nome = forms.CharField(
        label='Nome completo', 
        min_length=4, 
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'input is-primary'
            }
        )
    )

    data_nascimento = forms.DateField(
        required = True, 
        widget=forms.DateInput(
            attrs={
                'type': 'date'
            }
        )    
    )

    foto = forms.ImageField(
        required = False, 
    )

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        checa_email = User.objects.filter(email=email)
        if checa_email.count():
            raise ValidationError('E-mail já cadastrado')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Senhas diferentes informadas')
        password_validation.validate_password(password2, None)
        return make_password(password2)

    def save(self):
        if self.is_valid():
            estudante = Estudante(
                username=self.cleaned_data['email'],
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password2'],
                nome=self.cleaned_data['nome'].upper(),
                data_nascimento=self.cleaned_data['data_nascimento'],
                foto=self.cleaned_data['foto'],
            )
        estudante.save()
        return estudante

    def _init_(self, *args, **kwargs):
        super(EstudanteFormCadastro, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = ''


class EstudanteFormUpdate(forms.Form):
    email = forms.EmailField(
        label='E-mail', 
        widget=forms.EmailInput(
            attrs={
                'class': 'input is-primary'
            }
        )
    )

    nome = forms.CharField(
        label='Nome completo', 
        min_length=4, 
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'input is-primary'
            }
        )
    )

    data_nascimento = forms.DateField(
        required = True, 
        widget=forms.DateInput(
            attrs={
                'type': 'date'
            }
        )    
    )

    foto = forms.ImageField(
        required = False, 
    )

    def save(self):
        if self.is_valid():
            estudante = Estudante(
                username=self.cleaned_data['email'],
                email=self.cleaned_data['email'],
                nome=self.cleaned_data['nome'].upper(),
                data_nascimento=self.cleaned_data['data_nascimento'],
                foto=self.cleaned_data['foto'],
            )
        estudante.save()
        return estudante

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'estudante-update'
        self.helper.form_method = 'post'
        self.helper.form_action = ''

class CursoFormCadastro(forms.Form):
    nome = forms.CharField(
        label='Nome do Curso', 
        min_length=4, 
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'input is-primary'
            }
        )
    )

    data_inicio = forms.DateField(
        required = True, 
        widget=forms.DateInput(
            attrs={
                'type': 'date'
            }
        )    
    )
    
    data_termino = forms.DateField(
        required = True, 
        widget=forms.DateInput(
            attrs={
                'type': 'date'
            }
        )    
    )

    professor = forms.CharField(
        label='Professor', 
        min_length=4, 
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'input is-primary'
            }
        )
    )

    def clean_data_termino(self):
        data_termino = self.cleaned_data['data_termino']
        data_inicio = self.cleaned_data['data_inicio']
        if data_inicio >= data_termino:
            raise forms.ValidationError("Data inválida")
        return data_termino

    def save(self):
        if self.is_valid():
            curso = Curso(
                nome=self.cleaned_data['nome'].upper(),
                data_inicio=self.cleaned_data['data_inicio'],
                data_termino=self.cleaned_data['data_termino'],
                professor=self.cleaned_data['professor'].upper(),
            )
        curso.save()
        return curso

    def _init_(self, *args, **kwargs):
        super(CursoFormCadastro, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = ''

class NotaFormCadastro(forms.Form):
    estudantecurso = forms.ModelChoiceField(
        queryset=EstudanteCurso.objects.all(),
        widget=autocomplete.ModelSelect2(attrs={'data-minimum-input-length': 3, }, ),
    )

    nota = forms.IntegerField()
    nota.widget.attrs.update(
        {'class': 'input is-primary', 'step': '0.01', 'min': '0', 'max': '10'})
    
    data_avaliacao = forms.DateField(
        required = True, 
        widget=forms.DateInput(
            attrs={
                'type': 'date'
            }
        )    
    )

    def save(self):
        if self.is_valid():
            nota = Nota(
                estudantecurso=self.cleaned_data['estudantecurso'],
                nota=self.cleaned_data['nota'],
                data_avaliacao=self.cleaned_data['data_avaliacao'],
            )
        nota.save()
        return nota

    def _init_(self, *args, **kwargs):
        super(NotaFormCadastro, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = ''

class EstudanteCursoFormCadastro(forms.Form):
    estudante = forms.ModelChoiceField(
        required=True,
        queryset=Estudante.objects.all(),
        widget=autocomplete.ModelSelect2(attrs={'data-minimum-input-length': 3,}),
    )

    curso = forms.ModelChoiceField(
        required=True, 
        queryset=Curso.objects.all(),
        widget=autocomplete.ModelSelect2(attrs={'data-minimum-input-length': 3}),
    )

    def save(self):
        if self.is_valid():
            estudante_curso = EstudanteCurso(
                curso=self.cleaned_data['curso'],
                estudante=self.cleaned_data['estudante'],
            )
            estudante_curso.save()
            return estudante_curso

    def __init__(self, *args, **kwargs):
        super(EstudanteCursoFormCadastro, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = ''