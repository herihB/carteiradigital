from django.db import models
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Estudante(User):
    nome = models.CharField(
        max_length=100,
        blank = False,
        null = False,
    )

    data_nascimento = models.DateField(
        blank = False,
        null = False,
    )

    foto = models.ImageField(
        upload_to='pics/',
        blank = True,
        null = True,
    )

    class Meta:
        ordering = ['nome']

    def get_absolute_url(self): return reverse(
        'estudante-detail', args=[str(self.id)])

    def __str__(self):
        return f'({self.nome})'

    def get_cursos(self):
        cursos_list = EstudanteCurso.objects.filter(estudante=self.estudante)
        return cursos_list

    def get_notas(self):
        estudantecurso_list = EstudanteCurso.objects.filter(estudante=self.estudante)
        tensor = []

        for estudantecurso in estudantecurso_list:
            nota_list = Nota.objects.filter(estudantecurso=estudantecurso)
            if nota_list:
                tensor.append((estudantecurso, [nota_list]))

        return tensor


class Curso(models.Model):
    nome = models.CharField(
        max_length=100,
        blank = False,
        null = False,
    )

    data_inicio = models.DateField(
        blank = False,
        null = False,
    )

    data_termino = models.DateField(
        blank = False,
        null = False,
    )

    professor = models.CharField(
        max_length=200,
        blank = True,
        null = True,
    )

    class Meta:
        ordering = ['nome']

    def get_absolute_url(self): return reverse(
        'curso-detail', args=[str(self.id)])

    def __str__(self):
        return f'({self.nome})'



class EstudanteCurso(models.Model):
    curso = models.ForeignKey(
        Curso, on_delete=models.CASCADE, null=False, blank=False)

    estudante = models.ForeignKey(
        Estudante, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        ordering = ['estudante']

    def get_absolute_url(self): return reverse(
        'estudante-detail', args=[str(self.id)])

    def __str__(self):
        return f'({self.estudante}) - ({self.curso})'

class Nota(models.Model):
    estudantecurso = models.ForeignKey(
        EstudanteCurso, on_delete=models.CASCADE, null=False, blank=False)

    nota = models.IntegerField()

    data_avaliacao = models.DateField(
        blank = False,
        null = False,
    )

    class Meta:
        ordering = ['nota']

    def get_absolute_url(self): return reverse(
        'nota-detail', args=[str(self.id)])

    def __str__(self):
        return f'({self.nota}))'
