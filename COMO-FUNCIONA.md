# Como Funciona o Código Python - Guia Completo

## 📚 Visão Geral da Arquitetura

O app foi construído usando **FastAPI**, um framework moderno de Python para APIs. Vamos entender cada parte:

## 1️⃣ Estrutura de Pastas e Arquivos

```
TATTOO-VIA-NEI/
├── app/                    # Código principal da aplicação
│   ├── main.py            # Ponto de entrada - inicia o servidor
│   ├── core/              # Configurações centrais
│   │   ├── config.py      # Variáveis de ambiente e configurações
│   │   └── database.py    # Conexão com banco de dados
│   ├── models/            # Estrutura das tabelas do banco
│   │   └── models.py      # Define como os dados são armazenados
│   ├── schemas/           # Validação de dados de entrada/saída
│   │   └── schemas.py     # Define formato dos dados na API
│   ├── api/               # Endpoints da API (rotas)
│   │   ├── clients.py     # CRUD de clientes
│   │   ├── products.py    # CRUD de produtos
│   │   ├── sales.py       # CRUD de vendas
│   │   ├── inventory.py   # CRUD de estoque
│   │   ├── sellers.py     # CRUD de vendedores
│   │   └── costs.py       # CRUD de custos
│   └── analytics/         # Serviço de análises (upsell)
│       └── analytics_service.py
├── requirements.txt       # Dependências do Python
├── Dockerfile            # Configuração do container
├── docker-compose.yml    # Orquestração de serviços
└── .env                  # Variáveis de ambiente (você cria)
```

---

## 2️⃣ Como o Código Funciona

### **A. app/main.py - O Coração da Aplicação**

```python
from fastapi import FastAPI
from app.api import clients, products, sales, inventory, sellers, costs

app = FastAPI(
    title="Management App API",
    description="Sistema de gestão...",
    version="0.1.0",
)

# Registra as rotas (endpoints)
app.include_router(clients.router, prefix="/api/v1/clients")
app.include_router(products.router, prefix="/api/v1/products")
# ... outros routers
```

**O que faz:**
- Cria o aplicativo FastAPI
- Registra todas as rotas (URLs) da API
- Quando você acessa `http://localhost:8000/api/v1/clients`, ele chama o código em `clients.py`

---

### **B. app/core/config.py - Configurações**

```python
class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://..."
    SECRET_KEY: str = "..."
    CLIENT_ID: str = "default-client"
```

**O que faz:**
- Lê variáveis de ambiente do arquivo `.env`
- Armazena configurações como URL do banco, chaves secretas, etc.
- Permite diferentes configurações para dev/produção

---

### **C. app/core/database.py - Conexão com Banco**

```python
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**O que faz:**
- Cria uma conexão com o PostgreSQL
- `get_db()` é uma função que dá acesso ao banco em cada requisição
- Fecha a conexão automaticamente após uso

---

### **D. app/models/models.py - Estrutura do Banco**

```python
class Client(Base):
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True)
    phone = Column(String)
    # ... mais campos
```

**O que faz:**
- Define como as tabelas são criadas no banco
- Cada classe = uma tabela
- Cada atributo = uma coluna
- SQLAlchemy converte isso em SQL automaticamente

**Exemplo de tabela criada:**
```sql
CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    email VARCHAR UNIQUE,
    phone VARCHAR,
    ...
);
```

---

### **E. app/schemas/schemas.py - Validação de Dados**

```python
class ClientCreate(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
```

**O que faz:**
- Define o formato esperado dos dados na API
- Valida automaticamente os dados recebidos
- Se alguém enviar email inválido, retorna erro automaticamente

---

### **F. app/api/clients.py - Lógica de Negócio**

```python
@router.post("/", response_model=Client)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    # Cria novo cliente no banco
    db_client = ClientModel(**client.model_dump(), client_id=settings.CLIENT_ID)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client
```

**O que faz:**
1. Recebe dados do cliente via POST
2. Valida usando `ClientCreate` schema
3. Salva no banco de dados
4. Retorna o cliente criado

**Fluxo completo:**
```
Cliente faz POST → FastAPI valida → Salva no banco → Retorna JSON
```

---

### **G. app/analytics/analytics_service.py - Análises**

```python
class AnalyticsService:
    def get_sales_summary(self, start_date, end_date):
        # Consulta vendas no período
        sales = db.query(Sale).filter(...)
        
        # Calcula métricas
        total_revenue = sum(sale.final_amount for sale in sales)
        avg_ticket = total_revenue / len(sales)
        
        return {
            "total_revenue": total_revenue,
            "average_ticket": avg_ticket
        }
```

**O que faz:**
- Consulta dados do banco
- Calcula métricas de negócio
- Retorna análises para o cliente (upsell de consultoria)

---

## 3️⃣ Fluxo de uma Requisição

Exemplo: **Criar um novo cliente**

```
1. Cliente faz requisição HTTP:
   POST http://localhost:8000/api/v1/clients
   Body: {"name": "João", "email": "joao@email.com"}

2. FastAPI recebe e direciona para clients.py
   └─> Função create_client() é chamada

3. Pydantic valida os dados
   └─> Se email for inválido, retorna erro 422

4. SQLAlchemy salva no PostgreSQL
   └─> INSERT INTO clients (name, email, ...) VALUES (...)

5. FastAPI retorna resposta JSON
   └─> {"id": 1, "name": "João", "email": "joao@email.com", ...}
```

---

## 4️⃣ Como Iniciar a Construção

### **Passo 1: Preparar o Ambiente**

```bash
# 1. Clone o repositório (se ainda não fez)
git clone <seu-repo>
cd TATTOO-VIA-NEI

# 2. Crie arquivo .env
cp .env.example .env

# 3. Edite o .env com suas configurações
nano .env
```

**No .env, configure:**
```env
DATABASE_URL=******localhost:5432/management_db
SECRET_KEY=minha-chave-super-secreta-aqui
CLIENT_ID=meu-primeiro-cliente
ENVIRONMENT=development
```

---

### **Passo 2: Escolher Método de Execução**

#### **Opção A: Docker (Recomendado - Mais Fácil)**

```bash
# Inicia tudo (banco + app)
docker-compose up -d

# Aguarde 30 segundos para o banco inicializar

# Verifique se está rodando
docker-compose ps

# Veja os logs
docker-compose logs -f app
```

**Pronto! Acesse:**
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

---

#### **Opção B: Local (Para Desenvolvimento)**

```bash
# 1. Instale PostgreSQL no seu computador
# Ubuntu/Debian:
sudo apt install postgresql postgresql-contrib
# macOS:
brew install postgresql

# 2. Crie o banco de dados
sudo -u postgres createdb management_db

# 3. Crie ambiente virtual Python
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# 4. Instale dependências
pip install -r requirements.txt

# 5. Inicie o servidor
uvicorn app.main:app --reload
```

---

### **Passo 3: Criar as Tabelas no Banco**

As tabelas do banco precisam ser criadas. Você tem duas opções:

#### **Opção 1: Criar manualmente com SQLAlchemy**

```python
# criar_tabelas.py
from app.core.database import engine, Base
from app.models.models import *

# Cria todas as tabelas
Base.metadata.create_all(bind=engine)
print("Tabelas criadas com sucesso!")
```

Execute:
```bash
python criar_tabelas.py
```

#### **Opção 2: Usar Alembic (Migrations - Recomendado)**

```bash
# 1. Inicialize o Alembic
alembic init alembic

# 2. Configure o alembic/env.py
# (adicione: from app.models.models import *)

# 3. Crie a migração inicial
alembic revision --autogenerate -m "Initial tables"

# 4. Aplique as migrações
alembic upgrade head
```

---

### **Passo 4: Testar a API**

#### **Via Documentação Interativa (Swagger)**

1. Acesse http://localhost:8000/docs
2. Você verá todos os endpoints
3. Clique em "POST /api/v1/clients"
4. Clique em "Try it out"
5. Preencha os dados:
```json
{
  "name": "João Silva",
  "email": "joao@example.com",
  "phone": "11999999999"
}
```
6. Clique em "Execute"
7. Veja a resposta!

#### **Via cURL (Terminal)**

```bash
curl -X POST "http://localhost:8000/api/v1/clients" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Maria Santos",
    "email": "maria@example.com",
    "phone": "11988888888"
  }'
```

#### **Via Python (Requests)**

```python
import requests

# Criar cliente
response = requests.post(
    "http://localhost:8000/api/v1/clients",
    json={
        "name": "Pedro Costa",
        "email": "pedro@example.com",
        "phone": "11977777777"
    }
)

print(response.json())
# {"id": 1, "name": "Pedro Costa", ...}

# Listar clientes
response = requests.get("http://localhost:8000/api/v1/clients")
print(response.json())
```

---

## 5️⃣ Próximos Passos no Desenvolvimento

### **Fase 1: Backend Funcional** ✅ (Já feito!)
- [x] Estrutura básica
- [x] Models do banco
- [x] APIs CRUD
- [x] Analytics service

### **Fase 2: Melhorias no Backend**
- [ ] Adicionar autenticação JWT
- [ ] Criar endpoints de analytics
- [ ] Adicionar testes automatizados
- [ ] Implementar paginação nas listagens

### **Fase 3: Frontend**
- [ ] Criar interface React
- [ ] Telas de cadastro
- [ ] Dashboards com gráficos
- [ ] Relatórios

### **Fase 4: Deploy**
- [ ] Deploy em Railway/DO
- [ ] Configurar domínio
- [ ] SSL/HTTPS
- [ ] Backups automáticos

---

## 6️⃣ Comandos Úteis

### **Ver dados no banco (via Docker)**
```bash
docker-compose exec db psql -U management_user management_db

# Dentro do PostgreSQL:
\dt                    # Listar tabelas
SELECT * FROM clients; # Ver clientes
\q                     # Sair
```

### **Logs e Debug**
```bash
# Ver logs em tempo real
docker-compose logs -f app

# Reiniciar apenas o app
docker-compose restart app

# Parar tudo
docker-compose down

# Limpar e recomeçar (CUIDADO: apaga dados!)
docker-compose down -v
docker-compose up -d
```

### **Testar Analytics**
```python
# test_analytics.py
from app.analytics.analytics_service import AnalyticsService
from app.core.database import SessionLocal

db = SessionLocal()
analytics = AnalyticsService(db, "default-client")

# Ver resumo de vendas
summary = analytics.get_sales_summary()
print(summary)

# Top produtos
top = analytics.get_top_products(5)
print(top)

# Lucratividade
profit = analytics.get_profitability_analysis()
print(profit)

db.close()
```

---

## 7️⃣ Arquitetura Visual

```
┌─────────────────────────────────────────────────────────┐
│                    Cliente (Browser/App)                 │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP Request
                     ▼
┌─────────────────────────────────────────────────────────┐
│                    FastAPI (main.py)                     │
│  ┌────────────────────────────────────────────────────┐ │
│  │              Routers (api/*.py)                    │ │
│  │  /clients  /products  /sales  /inventory  /costs  │ │
│  └────────────────────────────────────────────────────┘ │
└────────────────────┬────────────────────────────────────┘
                     │ SQLAlchemy ORM
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  PostgreSQL Database                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │ clients  │ │ products │ │  sales   │ │  costs   │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## 8️⃣ Dicas Importantes

### **Para Desenvolvimento:**
1. **Use o ambiente virtual** sempre que trabalhar no projeto
2. **Use `--reload`** no uvicorn para recarregar automaticamente
3. **Consulte os logs** quando algo não funcionar
4. **Use a documentação Swagger** em /docs para testar

### **Para Produção:**
1. **Nunca** use SECRET_KEY default
2. **Configure backups** do banco de dados
3. **Use HTTPS** sempre
4. **Monitore** uso de recursos

### **Para Aprender Mais:**
- FastAPI Docs: https://fastapi.tiangolo.com
- SQLAlchemy: https://www.sqlalchemy.org
- PostgreSQL: https://www.postgresql.org/docs

---

## 9️⃣ Troubleshooting Comum

### **Erro: "ModuleNotFoundError: No module named 'app'"**
```bash
# Solução: Certifique-se de estar no diretório raiz
cd /caminho/para/TATTOO-VIA-NEI
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### **Erro: "Connection refused" ao acessar banco**
```bash
# Solução: Certifique-se que o PostgreSQL está rodando
docker-compose ps
# Ou, se local:
sudo systemctl status postgresql
```

### **Erro: "Port 8000 already in use"**
```bash
# Solução: Mate o processo na porta 8000
lsof -ti:8000 | xargs kill -9
# Ou use outra porta:
uvicorn app.main:app --reload --port 8001
```

---

## 🎯 Resumo: Primeiros Passos

```bash
# 1. Configure o ambiente
cp .env.example .env
nano .env  # Edite as configurações

# 2. Inicie com Docker
docker-compose up -d

# 3. Aguarde e acesse
# Espere ~30 segundos
open http://localhost:8000/docs

# 4. Teste criando um cliente
# Use a interface Swagger em /docs

# 5. Explore o código
# Leia app/main.py
# Depois app/api/clients.py
# Depois app/models/models.py
```

**Agora você está pronto para começar! 🚀**
