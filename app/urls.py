from django.urls import path
from . import views

urlpatterns = [
    path('tarefas/', views.listar_tarefas),
    path('tarefas/criar/', views.criar_tarefa),
    path('tarefas/<int:tarefa_id>/', views.buscar_tarefa),
    path('tarefas/<int:tarefa_id>/atualizar/', views.atualizar_tarefa),
    path('tarefas/<int:tarefa_id>/deletar/', views.deletar_tarefa),
]