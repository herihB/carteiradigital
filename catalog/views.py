from .models import *
from django.shortcuts import redirect, render
from django.views import generic
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def index(request):
    context = {}

    if request.user.is_authenticated and not request.user.is_staff:
        estudante = get_object_or_404(Estudante, email=request.user)

        context = {
            'estudante': estudante,
        }

    return render(request, 'index.html', context=context)

# Detail Generic
class EstudanteDetailView(generic.DetailView):
    model = Estudante

class CursoDetailView(generic.DetailView):
    model = Curso

class NotaDetailView(generic.DetailView):
    model = Nota

# Delete Generic
class EstudanteDelete(generic.DeleteView):
    model = Estudante

class CursoDelete(generic.DeleteView):
    model = Curso

class NotaDelete(generic.DeleteView):
    model = Nota

# List Generic
class EstudanteListView(generic.ListView):
    model = Estudante
    paginate_by = 5

class CursoListView(generic.ListView):
    model = Curso
    paginate_by = 5

class NotaListView(generic.ListView):
    model = Nota
    paginate_by = 5

#Create
@login_required
def estudante_create(request):
    if request.method == "POST":
        form = EstudanteFormCadastro(request.POST)
        if form.is_valid():
            post = form.save()
            post.author = request.user
            post.save()
            return redirect('estudante-detail', pk=post.pk)
    else:
        form = EstudanteFormCadastro()
    return render(request, 'catalog/estudante_form.html', {'form': form})

@login_required
def nota_update(request, pk):
    nota = get_object_or_404(Nota, pk=pk)
    form = NotaFormCadastro(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            nota.estudantecurso = form.cleaned_data['estudantecurso']
            nota.data_avaliacao = form.cleaned_data['data_avaliacao']
            nota.nota = form.cleaned_data['nota']
            nota.save()
            return redirect('estudante_list')
    else:
        form = NotaFormCadastro(
            initial={
                'estudantecurso': nota.estudantecurso,
                'data_avaliacao': nota.data_avaliacao,
                'nota': nota.nota,
            }
        )

    context = {
        'form': form,
        'nota': nota,
    }

    return render(request, 'catalog/nota_update.html', context)

@login_required
def curso_create(request):
    if request.method == "POST":
        form = CursoFormCadastro(request.POST)
        if form.is_valid():
            post = form.save()
            post.author = request.user
            post.save()
            return redirect('curso-detail', pk=post.pk)
    else:
        form = CursoFormCadastro()
    return render(request, 'catalog/curso_form.html', {'form': form})

@login_required
def matricular_estudante(request, pk):
    estudante = get_object_or_404(Estudante, pk=pk)
    form = EstudanteCursoFormCadastro(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            post = form.save()
            post.author = request.user
            post.save()
            return redirect('estudante-detail', pk=pk)
    else:
        form = EstudanteCursoFormCadastro(
            initial={
                'estudante': estudante,
            }
        )

    context = {
        'form': form,
    }
    
    return render(request, 'catalog/matricular_estudante.html', context)

@login_required
def nota_create(request):
    if request.method == "POST":
        form = NotaFormCadastro(request.POST)
        if form.is_valid():
            post = form.save()
            post.author = request.user
            post.save()
            return redirect('nota-detail', pk=post.pk)
    else:
        form = NotaFormCadastro()
    return render(request, 'catalog/nota_form.html', {'form': form})

#Update
@login_required
@user_passes_test(lambda user: user.is_staff)
def curso_update(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    form = CursoFormCadastro(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            curso.nome = form.cleaned_data['nome']
            curso.data_inicio = form.cleaned_data['data_inicio']
            curso.data_termino = form.cleaned_data['data_termino']
            curso.professor = form.cleaned_data['professor']
            curso.save()
            return redirect('curso_list')
    else:
        form = CursoFormCadastro(
            initial={
                'nome': curso.nome,
                'data_inicio': curso.data_inicio,
                'data_termino': curso.data_termino,
                'professor': curso.professor,
            }
        )

    context = {
        'form': form,
        'curso': curso,
    }

    return render(request, 'catalog/curso_update.html', context)

@login_required
def update_matricula(request, pk, id):
    estudantecurso = get_object_or_404(EstudanteCurso, id=id)
    form = EstudanteCursoFormCadastro(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            estudantecurso.estudante = form.cleaned_data['estudante']
            estudantecurso.curso = form.cleaned_data['curso']
            estudantecurso.save()
            return redirect('estudante-detail', pk=pk)
    else:
        form = EstudanteCursoFormCadastro(
            initial={
                'estudante': estudantecurso.estudante,
                'curso': estudantecurso.curso,
            }
        )

    context = {
        'estudantecurso': estudantecurso,
        'form': form,
    }
    return render(request, 'catalog/matricula_estudante_update.html', context)

@login_required
def nota_list(request, pk, id):
    estudantecurso = get_object_or_404(EstudanteCurso, id=id)
    nota_list = Nota.objects.filter(estudantecurso=estudantecurso)
    context = {
        'nota_list': nota_list,
    }
    
    return render(request, 'catalog/nota_list.html', context)

@login_required
def notas_create(request, pk, id):
    estudantecurso = get_object_or_404(EstudanteCurso, id=id)
    form = NotaFormCadastro(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            post = form.save()
            post.author = request.user
            post.save()
            return redirect('estudante-detail', pk=pk)
    else:
        form = NotaFormCadastro(
            initial={
                'estudantecurso': estudantecurso,
            }
        )

    context = {
        'form': form,
    }
    return render(request, 'catalog/nota_form.html', context)

@login_required
def deletar_matricula(request, pk, id):
    estudantecurso = get_object_or_404(EstudanteCurso, id=id)
    if request.method == 'POST':
        estudantecurso.delete()
        return redirect('estudante-detail', pk=pk)

    context = {
        'estudantecurso': estudantecurso,
    }
    return render(request, 'catalog/estudante_curso_confirm_delete.html', context)

#Update
@login_required
def estudante_update(request, pk):
    estudante = get_object_or_404(Estudante, pk=pk)
    form = EstudanteFormUpdate(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            estudante.nome = form.cleaned_data['nome'].upper()
            estudante.email = form.cleaned_data['email']
            estudante.data_nascimento = form.cleaned_data['data_nascimento']
            estudante.foto = form.cleaned_data['foto']
            estudante.save()
            return redirect('estudante-detail', pk=pk)
    else:
        form = EstudanteFormUpdate(
            initial={
                'nome': estudante.nome,
                'email': estudante.username,
                'data_nascimento': estudante.data_nascimento,
                'email': estudante.email,
                'foto': estudante.foto,
            }
        )

    context = {
        'form': form,
        'estudante': estudante,
    }

    return render(request, 'catalog/estudante_update.html', context)

class CursoAutocomplete(LoginRequiredMixin, UserPassesTestMixin, autocomplete.Select2QuerySetView):
    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Curso.objects.none()

        qs = Curso.objects.distinct().filter()

        if self.q:
            qs = qs.filter(nome__istartswith=self.q)
        return qs