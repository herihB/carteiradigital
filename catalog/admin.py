from django.contrib import admin
from .models import *

admin.site.register(Estudante)
admin.site.register(Curso)
admin.site.register(Nota)
admin.site.register(EstudanteCurso)