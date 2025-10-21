
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import redis
from datetime import datetime
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view

# Conexão Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def get_next_id():
    return r.incr('tarefa_id')


# ==================== Schemas para Documentação ====================

tarefa_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID único da tarefa'),
        'titulo': openapi.Schema(type=openapi.TYPE_STRING, description='Título da tarefa'),
        'descricao': openapi.Schema(type=openapi.TYPE_STRING, description='Descrição detalhada'),
        'dataCriacao': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', description='Data de criação'),
        'concluida': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Status de conclusão'),
        'status': openapi.Schema(
            type=openapi.TYPE_STRING, 
            description='Status da tarefa',
            enum=['Pendente', 'Em Progresso', 'Concluida']
        ),
    }
)

criar_tarefa_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['titulo', 'descricao'],
    properties={
        'titulo': openapi.Schema(type=openapi.TYPE_STRING, description='Título da tarefa', example='Estudar Django'),
        'descricao': openapi.Schema(type=openapi.TYPE_STRING, description='Descrição da tarefa', example='Aprender sobre Redis'),
        'status': openapi.Schema(
            type=openapi.TYPE_STRING, 
            description='Status inicial da tarefa',
            enum=['Pendente', 'Em Progresso', 'Concluida'],
            default='Pendente'
        ),
    }
)

atualizar_tarefa_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'titulo': openapi.Schema(type=openapi.TYPE_STRING, description='Novo título'),
        'descricao': openapi.Schema(type=openapi.TYPE_STRING, description='Nova descrição'),
        'status': openapi.Schema(type=openapi.TYPE_STRING, enum=['Pendente', 'Em Progresso', 'Concluida']),
        'concluida': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Status de conclusão'),
    }
)


# ==================== Views Documentadas ====================

@swagger_auto_schema(
    method='post',
    operation_description="Cria uma nova tarefa no sistema",
    operation_summary="Criar Tarefa",
    request_body=criar_tarefa_request,
    responses={
        201: openapi.Response('Tarefa criada com sucesso', tarefa_response),
        400: 'Dados inválidos'
    },
    tags=['Tarefas']
)
@api_view(['POST'])
@csrf_exempt
def criar_tarefa(request):
    """Cria uma nova tarefa"""
    data = json.loads(request.body)
    tarefa_id = get_next_id()
    
    tarefa = {
        'id': tarefa_id,
        'titulo': data['titulo'],
        'descricao': data['descricao'],
        'dataCriacao': datetime.now().isoformat(),
        'concluida': False,
        'status': data.get('status', 'Pendente')
    }
    
    r.set(f'tarefa:{tarefa_id}', json.dumps(tarefa))
    return JsonResponse(tarefa, status=201)


@swagger_auto_schema(
    method='get',
    operation_description="Lista todas as tarefas cadastradas",
    operation_summary="Listar Tarefas",
    responses={
        200: openapi.Response(
            'Lista de tarefas',
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'tarefas': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=tarefa_response
                    )
                }
            )
        )
    },
    tags=['Tarefas']
)
@api_view(['GET'])
def listar_tarefas(request):
    """Lista todas as tarefas"""
    keys = r.keys('tarefa:*')
    tarefas = []
    for key in keys:
        if key != 'tarefa_id':
            tarefa = json.loads(r.get(key))
            tarefas.append(tarefa)
    return JsonResponse({'tarefas': tarefas})


@swagger_auto_schema(
    method='get',
    operation_description="Busca uma tarefa específica pelo ID",
    operation_summary="Buscar Tarefa",
    manual_parameters=[
        openapi.Parameter(
            'tarefa_id',
            openapi.IN_PATH,
            description="ID da tarefa",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={
        200: openapi.Response('Tarefa encontrada', tarefa_response),
        404: 'Tarefa não encontrada'
    },
    tags=['Tarefas']
)
@api_view(['GET'])
def buscar_tarefa(request, tarefa_id):
    """Busca uma tarefa por ID"""
    tarefa = r.get(f'tarefa:{tarefa_id}')
    if tarefa:
        return JsonResponse(json.loads(tarefa))
    return JsonResponse({'error': 'Não encontrada'}, status=404)


@swagger_auto_schema(
    methods=['put', 'patch'],
    operation_description="Atualiza uma tarefa existente",
    operation_summary="Atualizar Tarefa",
    manual_parameters=[
        openapi.Parameter(
            'tarefa_id',
            openapi.IN_PATH,
            description="ID da tarefa",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    request_body=atualizar_tarefa_request,
    responses={
        200: openapi.Response('Tarefa atualizada', tarefa_response),
        404: 'Tarefa não encontrada'
    },
    tags=['Tarefas']
)
@api_view(['PUT', 'PATCH'])
@csrf_exempt
def atualizar_tarefa(request, tarefa_id):
    """Atualiza uma tarefa"""
    tarefa = r.get(f'tarefa:{tarefa_id}')
    if not tarefa:
        return JsonResponse({'error': 'Não encontrada'}, status=404)
    
    tarefa = json.loads(tarefa)
    data = json.loads(request.body)
    tarefa.update(data)
    
    r.set(f'tarefa:{tarefa_id}', json.dumps(tarefa))
    return JsonResponse(tarefa)


@swagger_auto_schema(
    method='delete',
    operation_description="Remove uma tarefa do sistema",
    operation_summary="Deletar Tarefa",
    manual_parameters=[
        openapi.Parameter(
            'tarefa_id',
            openapi.IN_PATH,
            description="ID da tarefa",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={
        200: openapi.Response(
            'Tarefa deletada',
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        ),
        404: 'Tarefa não encontrada'
    },
    tags=['Tarefas']
)
@api_view(['DELETE'])
@csrf_exempt
def deletar_tarefa(request, tarefa_id):
    """Deleta uma tarefa"""
    deleted = r.delete(f'tarefa:{tarefa_id}')
    if deleted:
        return JsonResponse({'message': 'Deletada'})
    return JsonResponse({'error': 'Não encontrada'}, status=404)


# View para renderizar o frontend
def index(request):
    """Renderiza a página HTML do ToDo List"""
    return render(request, 'index.html')

