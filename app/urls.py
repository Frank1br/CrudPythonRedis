from django.urls import path
from . import views

urlpatterns = [
    path('tarefas/', views.listar_tarefas),
    path('tarefas/criar/', views.criar_tarefa),
    path('tarefas/<int:tarefa_id>/', views.buscar_tarefa),
    path('tarefas/<int:tarefa_id>/atualizar/', views.atualizar_tarefa),
    path('tarefas/<int:tarefa_id>/deletar/', views.deletar_tarefa),
    path('', views.index)  # Página inicial
]

# ==================== Uso ====================
# Instalar: pip install redis

# Criar:
# POST /tarefas/criar/
# {"titulo": "Tarefa 1", "descricao": "Descrição"}

# Listar: GET /tarefas/
# Buscar: GET /tarefas/1/
# Atualizar: PUT /tarefas/1/atualizar/ {"concluida": true}
# Deletar: DELETE /tarefas/1/deletar/

###Swagger
'''
🏠 Frontend: http://localhost:8000/
📚 Swagger UI: http://localhost:8000/swagger/
📖 ReDoc: http://localhost:8000/redoc/
'''