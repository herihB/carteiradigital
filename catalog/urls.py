from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]

#Generic Routes
urlpatterns += [
    path('estudante/', views.EstudanteListView.as_view(), name='estudante_list'),
    path('estudante/<int:pk>', views.EstudanteDetailView.as_view(), name='estudante-detail'),
    path('estudante/<int:pk>/delete/', views.EstudanteDelete.as_view(success_url="/catalog/estudante"), name='estudante-delete'),
    path('estudante/<int:pk>/matricula', views.matricular_estudante, name='matricular_estudante'),
    path('estudante/<int:pk>/matricula/<int:id>/deletar', views.deletar_matricula, name='deletar_matricula'),
    path('estudante/<int:pk>/matricula/<int:id>/update', views.update_matricula, name='update_matricula'),
    path('estudante/<int:pk>/matricula/<int:id>/notas', views.nota_list, name='nota_list'),
    path('estudante/<int:pk>/matricula/<int:id>/notas/create', views.notas_create, name='notas_create'),
]   



urlpatterns += [
    path('curso/', views.CursoListView.as_view(), name='curso_list'),
    path('curso/<int:pk>', views.CursoDetailView.as_view(), name='curso-detail'),
    path('curso/<int:pk>/delete/', views.CursoDelete.as_view(success_url="/catalog/curso"), name='curso-delete'),
]

urlpatterns += [
    path('nota/<int:pk>', views.NotaDetailView.as_view(), name='nota-detail'),
    path('nota/<int:pk>/update/', views.nota_update, name='nota_update'),
    path('nota/<int:pk>/delete/', views.NotaDelete.as_view(success_url="/catalog/estudante"), name='nota-delete'),
    re_path(r'^curso-autocomplete/$', views.CursoAutocomplete.as_view(), name='curso-autocomplete'),
]

#Create and Update
urlpatterns += [
    path('estudante/create', views.estudante_create, name='estudante_form'),
    path('estudante/<int:pk>/update/', views.estudante_update, name='estudante_update'),
]

urlpatterns += [
    path('curso/create', views.curso_create, name='curso_form'),
    path('curso/<int:pk>/update/', views.curso_update, name='curso_update'),
]

urlpatterns += [
    path('nota/create', views.nota_create, name='nota_form'),
]