# O que é django? => Framework Python que facilita a criacao de sites. É responsavel por fazer tarefas dificeis  para o desenvolvedor se concertar na construcao do site. Enfatiza a reutilizacao de componentes e vem com recursos prontos para uso, como sistema de login, conexao com banco de dados, painel administrativo e operacoes crud especialmente util para sites baseados em banco de dados.

# O padrao de arquitetura do django é o MVT (Model-View-Template)
# Model => Representa a estrutura dos dados e a logica de negocio. Define como os dados sao armazenados, recuperados e manipulados. Em django, os modelos sao definidos como classes que herdam de django.db.models.Model.
# View => Responsavel por processar as requisicoes do usuario, interagir com os modelos e retornar respostas apropriadas. As views sao definidas como funcoes ou classes que recebem uma requisicao HTTP e retornam uma resposta HTTP.
# Template => Define a apresentacao dos dados. Em django, os templates sao arquivos HTML que podem conter marcadores especiais para inserir dados dinamicos.

# URLs => Em django, as URLs sao mapeadas para views usando o sistema de roteamento. As URLs sao definidas em um arquivo urls.py, onde cada padrao de URL e associado a uma view especifica.

# Configuracao do ambiente
# 1. Instalar o python
# python -m venv venv servira para criar o ambiente virtual
# 2. Ativar o ambiente virtual
# No windows: venv\Scripts\activate
# No linux/mac: source venv/bin/activate
# 3. Instalar o django
# python3 -m pip install django

##Criar Projeto
# python3 -m django startproject Projeto . 

###Fazer Migração
#python3 manage.py makemigrations


###Criação das tabelas apos as migrações no arquivo db.sqlite3
#python3 manage.py migrate

###Inserir dados via de comando
#python3 manage.py shell

###Importar a tabela que voce quer usar
#from app.models import Desenvolvedor