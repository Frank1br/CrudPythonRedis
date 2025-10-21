"""
URL configuration for Projeto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API de Tarefas - Django + Redis",
        default_version='v1',
        description="""
        ## 📋 API para gerenciamento de tarefas usando Django e Redis
        
        Esta API permite criar, listar, atualizar e deletar tarefas armazenadas no Redis.
        
        ### Funcionalidades:
        - ✅ Criar novas tarefas
        - 📋 Listar todas as tarefas
        - 🔍 Buscar tarefa específica por ID
        - ✏️ Atualizar tarefas existentes
        - 🗑️ Deletar tarefas
        
        ### Status disponíveis:
        - Pendente
        - Em Progresso
        - Concluída
        """,
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contato@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    
    # Swagger URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]

'''
🏠 Frontend: http://localhost:8000/
📚 Swagger UI: http://localhost:8000/swagger/
📖 ReDoc: http://localhost:8000/redoc/
'''