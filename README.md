# Management App - Sistema de Gestão

Sistema completo de gestão empresarial desenvolvido em Python com FastAPI, projetado para venda como SaaS com consultoria de análise de dados como upsell.

## Características Principais

### Módulos Implementados
- **Clientes**: Cadastro e gestão de clientes
- **Produtos**: Controle de produtos com cálculo automático de margens
- **Vendas**: Sistema completo de vendas com controle de estoque
- **Estoque**: Entradas e saídas com histórico completo
- **Vendedores**: Gestão de equipe de vendas com comissões
- **Custos**: Controle de custos operacionais
- **Analytics**: Análises e insights para consultoria (upsell)

### Funcionalidades de Analytics (Upsell de Consultoria)
- Resumo de vendas por período
- Top produtos mais vendidos
- Análise de lucratividade (margem bruta e líquida)
- Tendências mensais de vendas
- Alertas de estoque baixo
- Análise de comportamento de clientes
- Dashboards personalizados

## Arquitetura Técnica

### Stack Tecnológico
- **Backend**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy
- **Analytics**: Pandas, NumPy, Scikit-learn
- **Containerização**: Docker & Docker Compose

### Estrutura do Projeto
```
app/
├── api/              # Endpoints REST
│   ├── clients.py
│   ├── products.py
│   ├── sales.py
│   ├── inventory.py
│   ├── sellers.py
│   └── costs.py
├── models/           # Modelos do banco de dados
│   └── models.py
├── schemas/          # Schemas Pydantic
│   └── schemas.py
├── core/             # Configurações principais
│   ├── config.py
│   └── database.py
├── analytics/        # Serviços de análise (upsell)
│   └── analytics_service.py
└── main.py          # Aplicação principal
```

## Modelo de Negócio

### Monetização
1. **Licença do Software**: Valor único por implementação
2. **Manutenção Mensal**: Taxa recorrente para manter o sistema rodando
3. **Consultoria Analytics** (Upsell): Análises personalizadas e insights de negócio

### Multi-Tenancy
O sistema usa o campo `client_id` em todas as tabelas para permitir múltiplos clientes no mesmo banco de dados, reduzindo custos de infraestrutura.

## Deployment

### Opção 1: DigitalOcean App Platform
**Custo**: ~$12-25/mês por cliente (app + database)

### Opção 2: Railway
**Custo**: ~$10-20/mês por cliente

### Opção 3: Docker Self-Hosted
**Custo**: Variável (VPS a partir de $5/mês)

Ver [DEPLOYMENT.md](./DEPLOYMENT.md) para instruções detalhadas.

## Instalação Local (Desenvolvimento)

### Pré-requisitos
- Python 3.11+
- PostgreSQL 15+
- Docker (opcional)

### Setup

1. **Clone o repositório**:
```bash
git clone <repo-url>
cd TATTOO-VIA-NEI
```

2. **Crie um ambiente virtual**:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instale as dependências**:
```bash
pip install -r requirements.txt
```

4. **Configure o banco de dados**:
```bash
# Crie um banco PostgreSQL
createdb management_db

# Configure a URL no .env
cp .env.example .env
# Edite DATABASE_URL no .env
```

5. **Inicie com Docker** (recomendado):
```bash
docker-compose up -d
```

6. **Ou inicie localmente**:
```bash
uvicorn app.main:app --reload
```

7. **Acesse a documentação**:
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Clientes
- `GET /api/v1/clients` - Listar clientes
- `POST /api/v1/clients` - Criar cliente
- `GET /api/v1/clients/{id}` - Obter cliente
- `PUT /api/v1/clients/{id}` - Atualizar cliente
- `DELETE /api/v1/clients/{id}` - Deletar cliente

### Produtos
- `GET /api/v1/products` - Listar produtos
- `POST /api/v1/products` - Criar produto
- `GET /api/v1/products/{id}` - Obter produto
- `PUT /api/v1/products/{id}` - Atualizar produto
- `DELETE /api/v1/products/{id}` - Deletar produto

### Vendas
- `GET /api/v1/sales` - Listar vendas
- `POST /api/v1/sales` - Criar venda
- `GET /api/v1/sales/{id}` - Obter venda
- `DELETE /api/v1/sales/{id}` - Cancelar venda

### Estoque
- `GET /api/v1/inventory` - Listar entradas
- `POST /api/v1/inventory` - Registrar entrada
- `GET /api/v1/inventory/{id}` - Obter entrada
- `GET /api/v1/inventory/product/{id}` - Histórico do produto

### Vendedores
- `GET /api/v1/sellers` - Listar vendedores
- `POST /api/v1/sellers` - Criar vendedor
- `GET /api/v1/sellers/{id}` - Obter vendedor
- `PUT /api/v1/sellers/{id}` - Atualizar vendedor
- `DELETE /api/v1/sellers/{id}` - Deletar vendedor

### Custos
- `GET /api/v1/costs` - Listar custos
- `POST /api/v1/costs` - Criar custo
- `GET /api/v1/costs/{id}` - Obter custo
- `PUT /api/v1/costs/{id}` - Atualizar custo
- `DELETE /api/v1/costs/{id}` - Deletar custo

## Próximos Passos

### Desenvolvimento
- [ ] Implementar autenticação JWT
- [ ] Criar API endpoints para analytics
- [ ] Desenvolver frontend React
- [ ] Implementar relatórios em PDF
- [ ] Adicionar exportação para Excel
- [ ] Criar dashboards interativos com Plotly
- [ ] Implementar websockets para atualizações em tempo real

### Deploy & Distribuição
- [ ] Configurar CI/CD com GitHub Actions
- [ ] Criar scripts de migração de dados
- [ ] Documentar processo de onboarding de clientes
- [ ] Criar templates de contratos
- [ ] Definir SLAs e políticas de suporte

### Upsell de Consultoria
- [ ] Desenvolver relatórios avançados de análise
- [ ] Implementar previsão de vendas com ML
- [ ] Criar análise de ABC de produtos
- [ ] Desenvolver análise de churn de clientes
- [ ] Implementar recomendações automáticas

## Precificação Sugerida

Baseado nos custos de infraestrutura:

1. **Setup Inicial**: R$ 2.000 - 5.000
   - Implementação e configuração
   - Treinamento da equipe

2. **Mensalidade**: R$ 200 - 500/mês
   - Hospedagem e manutenção
   - Suporte técnico básico

3. **Consultoria Analytics** (Upsell): R$ 500 - 2.000/mês
   - Relatórios customizados
   - Análises avançadas
   - Insights estratégicos

**Margem de Lucro:** 60-80% após custos de infraestrutura

## Suporte e Contato

Para dúvidas sobre implementação ou consultoria de analytics, entre em contato.

## Licença

Proprietary - Todos os direitos reservados
