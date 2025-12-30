# Quick Start Guide - Management App

Guia rápido para começar a usar o sistema de gestão.

## 🚀 Start Rápido com Docker

### 1. Pré-requisitos
- Docker instalado
- Docker Compose instalado

### 2. Clonar e Iniciar

```bash
# Clone o repositório
git clone <repo-url>
cd TATTOO-VIA-NEI

# Copie o arquivo de configuração
cp .env.example .env

# Inicie os containers
docker-compose up -d

# Aguarde ~30 segundos para o banco inicializar
```

### 3. Acessar

- **API**: http://localhost:8000
- **Documentação Interativa**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📝 Primeiro Uso

### 1. Criar um Cliente

```bash
curl -X POST "http://localhost:8000/api/v1/clients" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Silva",
    "email": "joao@example.com",
    "phone": "11999999999",
    "document": "12345678900"
  }'
```

### 2. Criar um Produto

```bash
curl -X POST "http://localhost:8000/api/v1/products" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Produto Exemplo",
    "sku": "PROD001",
    "category": "Categoria A",
    "unit_price": 100.00,
    "cost_price": 60.00,
    "stock_quantity": 50,
    "min_stock": 10
  }'
```

### 3. Registrar uma Entrada de Estoque

```bash
curl -X POST "http://localhost:8000/api/v1/inventory" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "entry_type": "purchase",
    "quantity": 100,
    "unit_cost": 60.00,
    "notes": "Compra inicial"
  }'
```

### 4. Criar um Vendedor

```bash
curl -X POST "http://localhost:8000/api/v1/sellers" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Maria Vendedora",
    "email": "maria@example.com",
    "phone": "11988888888",
    "commission_rate": 5.0
  }'
```

### 5. Fazer uma Venda

```bash
curl -X POST "http://localhost:8000/api/v1/sales" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "seller_id": 1,
    "discount": 10.00,
    "payment_method": "credit",
    "items": [
      {
        "product_id": 1,
        "quantity": 2,
        "unit_price": 100.00
      }
    ]
  }'
```

### 6. Registrar um Custo

```bash
curl -X POST "http://localhost:8000/api/v1/costs" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "rent",
    "description": "Aluguel do mês",
    "amount": 2000.00,
    "is_recurring": 1
  }'
```

## 🔍 Usando a Interface Interativa

A forma mais fácil de testar a API é usando a documentação interativa:

1. Acesse http://localhost:8000/docs
2. Clique em qualquer endpoint
3. Clique em "Try it out"
4. Preencha os dados
5. Clique em "Execute"

## 📊 Testando Analytics (Python)

Crie um script Python para testar as análises:

```python
from app.analytics.analytics_service import AnalyticsService
from app.core.database import SessionLocal
from datetime import datetime, timedelta

# Criar sessão do banco
db = SessionLocal()

# Criar instância do serviço
analytics = AnalyticsService(db, client_id="default-client")

# Obter resumo de vendas
sales_summary = analytics.get_sales_summary(
    start_date=datetime.now() - timedelta(days=30)
)
print("Resumo de Vendas:", sales_summary)

# Top produtos
top_products = analytics.get_top_products(limit=5)
print("Top 5 Produtos:", top_products)

# Análise de lucratividade
profitability = analytics.get_profitability_analysis()
print("Análise de Lucratividade:", profitability)

# Alertas de estoque
alerts = analytics.get_inventory_alerts()
print("Alertas de Estoque:", alerts)

db.close()
```

## 🛠️ Comandos Úteis

### Ver logs
```bash
docker-compose logs -f
```

### Parar serviços
```bash
docker-compose down
```

### Reiniciar serviços
```bash
docker-compose restart
```

### Acessar shell do container
```bash
docker-compose exec app bash
```

### Acessar PostgreSQL
```bash
docker-compose exec db psql -U management_user management_db
```

## 📦 Desenvolvimento Local (sem Docker)

### 1. Instalar PostgreSQL

```bash
# Ubuntu/Debian
sudo apt install postgresql postgresql-contrib

# macOS
brew install postgresql

# Criar banco
createdb management_db
```

### 2. Setup Python

```bash
# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt
```

### 3. Configurar .env

```env
DATABASE_URL=postgresql://seu_usuario:sua_senha@localhost:5432/management_db
SECRET_KEY=sua-chave-secreta-aqui
CLIENT_ID=default-client
ENVIRONMENT=development
```

### 4. Iniciar servidor

```bash
uvicorn app.main:app --reload
```

## 🔐 Configuração para Produção

### 1. Variáveis de Ambiente Importantes

```env
# NUNCA use valores default em produção!
SECRET_KEY=gere-uma-chave-muito-segura-aqui
DATABASE_URL=postgresql://user:pass@host:5432/db
CLIENT_ID=cliente-unico-id
ENVIRONMENT=production
ALLOWED_ORIGINS=https://seu-dominio.com
```

### 2. Gerar SECRET_KEY Segura

```python
import secrets
print(secrets.token_urlsafe(32))
```

## 🐛 Troubleshooting

### Porta 8000 já em uso
```bash
# Mudar porta no docker-compose.yml
ports:
  - "8001:8000"  # Use 8001 ao invés de 8000
```

### Erro de conexão com banco
```bash
# Verificar se PostgreSQL está rodando
docker-compose ps

# Recriar banco
docker-compose down -v
docker-compose up -d
```

### Importação de módulos falha
```bash
# Certifique-se de estar no diretório raiz
cd /caminho/para/TATTOO-VIA-NEI

# E que o Python path está correto
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

## 📚 Próximos Passos

1. ✅ Sistema funcionando localmente
2. ⬜ Configurar Alembic migrations
3. ⬜ Adicionar autenticação JWT
4. ⬜ Criar interface frontend
5. ⬜ Deploy em produção
6. ⬜ Configurar domínio personalizado
7. ⬜ Implementar backups automáticos

## 🆘 Precisa de Ajuda?

- Veja a documentação completa no README.md
- Guia de deployment no DEPLOYMENT.md
- Migrations no ALEMBIC.md
- Abra uma issue no repositório

---

**Boa sorte com seu app de gestão! 🚀**
