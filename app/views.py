from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import redis
from datetime import datetime

# Conexão Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def get_next_id():
    return r.incr('tarefa_id')

@csrf_exempt
def criar_tarefa(request):
    if request.method == 'POST':
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

def listar_tarefas(request):
    keys = r.keys('tarefa:*')
    tarefas = []
    for key in keys:
        if key != 'tarefa_id':
            tarefa = json.loads(r.get(key))
            tarefas.append(tarefa)
    return JsonResponse({'tarefas': tarefas})

def buscar_tarefa(request, tarefa_id):
    tarefa = r.get(f'tarefa:{tarefa_id}')
    if tarefa:
        return JsonResponse(json.loads(tarefa))
    return JsonResponse({'error': 'Não encontrada'}, status=404)

@csrf_exempt
def atualizar_tarefa(request, tarefa_id):
    if request.method in ['PUT', 'PATCH']:
        tarefa = r.get(f'tarefa:{tarefa_id}')
        if not tarefa:
            return JsonResponse({'error': 'Não encontrada'}, status=404)
        
        tarefa = json.loads(tarefa)
        data = json.loads(request.body)
        tarefa.update(data)
        
        r.set(f'tarefa:{tarefa_id}', json.dumps(tarefa))
        return JsonResponse(tarefa)

@csrf_exempt
def deletar_tarefa(request, tarefa_id):
    if request.method == 'DELETE':
        deleted = r.delete(f'tarefa:{tarefa_id}')
        if deleted:
            return JsonResponse({'message': 'Deletada'})
        return JsonResponse({'error': 'Não encontrada'}, status=404)
    
    # ==================== Uso ====================
# Instalar: pip install redis

# Criar:
# POST /tarefas/criar/
# {"titulo": "Tarefa 1", "descricao": "Descrição"}

# Listar: GET /tarefas/
# Buscar: GET /tarefas/1/
# Atualizar: PUT /tarefas/1/atualizar/ {"concluida": true}
# Deletar: DELETE /tarefas/1/deletar/