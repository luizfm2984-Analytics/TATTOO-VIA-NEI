# Diagramas de Arquitetura

## 🏗️ Arquitetura Geral do Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENTE                                  │
│  (Browser, Postman, App Mobile, Frontend React)                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ HTTP/HTTPS (REST API)
                         │ JSON
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                    FASTAPI APPLICATION                           │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                     app/main.py                            │ │
│  │              (Servidor Web - FastAPI)                      │ │
│  └────────────────────┬───────────────────────────────────────┘ │
│                       │                                          │
│  ┌────────────────────▼───────────────────────────────────────┐ │
│  │                   ROUTERS (app/api/)                       │ │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐     │ │
│  │  │ clients  │ │ products │ │  sales   │ │inventory │ ... │ │
│  │  │   .py    │ │   .py    │ │   .py    │ │   .py    │     │ │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘     │ │
│  └────────────────────┬───────────────────────────────────────┘ │
│                       │                                          │
│  ┌────────────────────▼───────────────────────────────────────┐ │
│  │              SCHEMAS (app/schemas/)                        │ │
│  │            (Validação de Dados - Pydantic)                 │ │
│  └────────────────────┬───────────────────────────────────────┘ │
│                       │                                          │
│  ┌────────────────────▼───────────────────────────────────────┐ │
│  │               MODELS (app/models/)                         │ │
│  │          (ORM - SQLAlchemy - Tabelas)                      │ │
│  └────────────────────┬───────────────────────────────────────┘ │
│                       │                                          │
│  ┌────────────────────▼───────────────────────────────────────┐ │
│  │              DATABASE (app/core/)                          │ │
│  │           (Conexão com PostgreSQL)                         │ │
│  └────────────────────┬───────────────────────────────────────┘ │
└────────────────────────┼───────────────────────────────────────┘
                         │
                         │ SQL Queries
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                   POSTGRESQL DATABASE                            │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│  │ clients  │ │ products │ │  sales   │ │inventory │          │
│  │  table   │ │  table   │ │  table   │ │  table   │   ...    │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

## 🔄 Fluxo de uma Requisição (Criar Cliente)

```
1. CLIENTE FAZ REQUISIÇÃO
   │
   │  POST http://localhost:8000/api/v1/clients
   │  Content-Type: application/json
   │  Body: {"name": "João", "email": "joao@email.com"}
   │
   ▼
2. FASTAPI RECEBE (app/main.py)
   │
   │  app.include_router(clients.router, prefix="/api/v1/clients")
   │  → Direciona para o router correto
   │
   ▼
3. ROUTER PROCESSA (app/api/clients.py)
   │
   │  @router.post("/", response_model=Client)
   │  def create_client(client: ClientCreate, db: Session = Depends(get_db))
   │  → Função create_client é chamada
   │
   ▼
4. VALIDAÇÃO (app/schemas/schemas.py)
   │
   │  class ClientCreate(BaseModel):
   │      name: str
   │      email: Optional[EmailStr] = None
   │  → Pydantic valida os dados
   │  → Se email inválido, retorna erro 422
   │
   ▼
5. CRIAÇÃO DO MODEL (app/models/models.py)
   │
   │  db_client = ClientModel(**client.model_dump(), client_id=settings.CLIENT_ID)
   │  → Cria objeto do banco de dados
   │
   ▼
6. SALVAR NO BANCO (app/core/database.py)
   │
   │  db.add(db_client)
   │  db.commit()
   │  → SQLAlchemy converte em SQL:
   │  → INSERT INTO clients (name, email, ...) VALUES (...)
   │
   ▼
7. POSTGRESQL EXECUTA
   │
   │  Tabela: clients
   │  ┌────┬──────────┬──────────────────┬─────────────┐
   │  │ id │   name   │      email       │    phone    │
   │  ├────┼──────────┼──────────────────┼─────────────┤
   │  │ 1  │  João    │ joao@email.com   │ 11999999999 │
   │  └────┴──────────┴──────────────────┴─────────────┘
   │
   ▼
8. RESPOSTA AO CLIENTE
   │
   │  HTTP 200 OK
   │  Content-Type: application/json
   │  {
   │    "id": 1,
   │    "name": "João",
   │    "email": "joao@email.com",
   │    "phone": "11999999999",
   │    "created_at": "2024-01-01T10:00:00",
   │    ...
   │  }
   │
   └─→ CLIENTE RECEBE RESPOSTA
```

## 🗃️ Estrutura do Banco de Dados

```
┌─────────────────────────────────────────────────────────────────┐
│                         DATABASE: management_db                  │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────────┐
│      clients             │
├──────────────────────────┤
│ id (PK)                  │
│ client_id                │◄────┐
│ name                     │     │
│ email                    │     │ Multi-tenancy
│ phone                    │     │ (Isola dados por cliente)
│ document                 │     │
│ created_at               │     │
└──────────────────────────┘     │
                                 │
┌──────────────────────────┐     │
│      products            │     │
├──────────────────────────┤     │
│ id (PK)                  │     │
│ client_id                │◄────┤
│ name                     │     │
│ sku                      │     │
│ unit_price               │     │
│ cost_price               │     │
│ margin (calculated)      │     │
│ stock_quantity           │     │
└──────────┬───────────────┘     │
           │                     │
           │ FK                  │
           │                     │
┌──────────▼───────────────┐     │
│   inventory_entries      │     │
├──────────────────────────┤     │
│ id (PK)                  │     │
│ client_id                │◄────┤
│ product_id (FK)          │     │
│ entry_type               │     │
│ quantity                 │     │
│ unit_cost                │     │
└──────────────────────────┘     │
                                 │
┌──────────────────────────┐     │
│      sellers             │     │
├──────────────────────────┤     │
│ id (PK)                  │     │
│ client_id                │◄────┤
│ name                     │     │
│ commission_rate          │     │
└──────────┬───────────────┘     │
           │                     │
           │ FK                  │
           │                     │
┌──────────▼───────────────┐     │
│        sales             │     │
├──────────────────────────┤     │
│ id (PK)                  │     │
│ client_id                │◄────┤
│ customer_id (FK)         │─────┘
│ seller_id (FK)           │
│ total_amount             │
│ discount                 │
│ final_amount             │
│ payment_method           │
└──────────┬───────────────┘
           │
           │ FK
           │
┌──────────▼───────────────┐
│      sale_items          │
├──────────────────────────┤
│ id (PK)                  │
│ sale_id (FK)             │
│ product_id (FK)          │
│ quantity                 │
│ unit_price               │
│ subtotal (calculated)    │
└──────────────────────────┘

┌──────────────────────────┐
│        costs             │
├──────────────────────────┤
│ id (PK)                  │
│ client_id                │◄────┐
│ category                 │     │
│ description              │     │ Todos conectados via client_id
│ amount                   │     │ para Multi-tenancy
│ is_recurring             │     │
└──────────────────────────┘     │
```

## 📊 Fluxo de Analytics (Upsell)

```
┌─────────────────────────────────────────────────────────────────┐
│                    CLIENTE SOLICITA ANÁLISE                      │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ GET /api/v1/analytics/sales-summary
                         │
┌────────────────────────▼────────────────────────────────────────┐
│              AnalyticsService (app/analytics/)                   │
│                                                                  │
│  def get_sales_summary(start_date, end_date):                   │
│      1. Consulta vendas no período                              │
│      2. Calcula métricas                                        │
│      3. Retorna análises                                        │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ SQL Query
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                    PostgreSQL Database                           │
│                                                                  │
│  SELECT                                                          │
│    COUNT(*) as total_sales,                                     │
│    SUM(final_amount) as revenue,                                │
│    AVG(final_amount) as avg_ticket                              │
│  FROM sales                                                      │
│  WHERE sale_date BETWEEN ? AND ?                                │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Resultados
                         │
┌────────────────────────▼────────────────────────────────────────┐
│              AnalyticsService (Processamento)                    │
│                                                                  │
│  • Calcula margens                                              │
│  • Identifica tendências                                        │
│  • Gera insights                                                │
│  • Cria recomendações                                           │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ JSON Response
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                     CLIENTE RECEBE                               │
│                                                                  │
│  {                                                               │
│    "total_revenue": 15000.00,                                   │
│    "total_sales": 45,                                           │
│    "average_ticket": 333.33,                                    │
│    "trend": "increasing",                                       │
│    "recommendations": [...]                                     │
│  }                                                               │
└──────────────────────────────────────────────────────────────────┘
```

## 🚀 Deploy Multi-Tenancy

```
OPÇÃO 1: Instância Compartilhada (Mais Barato)
═══════════════════════════════════════════════

┌─────────────────────────────────────────────────────────┐
│              1 Servidor (Railway/DO)                     │
│  ┌────────────────────────────────────────────────────┐ │
│  │           FastAPI App (1 instância)                │ │
│  └────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────┐ │
│  │         PostgreSQL (1 banco de dados)              │ │
│  │                                                     │ │
│  │  ┌──────────────────────────────────────────────┐ │ │
│  │  │ Cliente A (client_id=cliente-a)              │ │ │
│  │  │ - sales, products, clients...                │ │ │
│  │  └──────────────────────────────────────────────┘ │ │
│  │  ┌──────────────────────────────────────────────┐ │ │
│  │  │ Cliente B (client_id=cliente-b)              │ │ │
│  │  │ - sales, products, clients...                │ │ │
│  │  └──────────────────────────────────────────────┘ │ │
│  │  ┌──────────────────────────────────────────────┐ │ │
│  │  │ Cliente C (client_id=cliente-c)              │ │ │
│  │  │ - sales, products, clients...                │ │ │
│  │  └──────────────────────────────────────────────┘ │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘

Custo: R$150-200/mês para 5-10 clientes
Margem: 70-85%


OPÇÃO 2: Instâncias Isoladas (Mais Seguro)
═══════════════════════════════════════════

┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐
│ Servidor Cliente A   │  │ Servidor Cliente B   │  │ Servidor Cliente C   │
├──────────────────────┤  ├──────────────────────┤  ├──────────────────────┤
│ FastAPI Instance A   │  │ FastAPI Instance B   │  │ FastAPI Instance C   │
│ PostgreSQL DB A      │  │ PostgreSQL DB B      │  │ PostgreSQL DB C      │
│ client_id=cliente-a  │  │ client_id=cliente-b  │  │ client_id=cliente-c  │
└──────────────────────┘  └──────────────────────┘  └──────────────────────┘

Custo: R$50-100/mês por cliente
Margem: 60-70%
```

## 🎯 Próximos Passos no Desenvolvimento

```
FASE 1: Backend ✅ CONCLUÍDO
├── Estrutura FastAPI
├── Models e Schemas
├── API Endpoints CRUD
├── Analytics Service
└── Docker Setup

FASE 2: Banco de Dados (Você está aqui)
├── [ ] Criar tabelas (python criar_tabelas.py)
├── [ ] Popular com dados de teste (python popular_db.py)
├── [ ] Configurar Alembic (opcional)
└── [ ] Testar endpoints na API

FASE 3: Autenticação
├── [ ] Implementar JWT tokens
├── [ ] Login/Logout endpoints
├── [ ] Proteção de rotas
└── [ ] Gestão de usuários

FASE 4: Frontend
├── [ ] Setup React
├── [ ] Telas de CRUD
├── [ ] Dashboards
└── [ ] Gráficos com Plotly

FASE 5: Analytics Avançado (Upsell)
├── [ ] Endpoints de análise
├── [ ] Relatórios PDF
├── [ ] Previsões com ML
└── [ ] Dashboards executivos

FASE 6: Deploy
├── [ ] Deploy em Railway/DO
├── [ ] Configurar domínio
├── [ ] SSL/HTTPS
└── [ ] Monitoramento
```

## 📚 Recursos de Aprendizado

```
FastAPI:     https://fastapi.tiangolo.com
SQLAlchemy:  https://www.sqlalchemy.org
PostgreSQL:  https://www.postgresql.org/docs
Pydantic:    https://docs.pydantic.dev
Docker:      https://docs.docker.com
```
