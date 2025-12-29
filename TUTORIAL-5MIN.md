# Guia Passo a Passo - Vendo o App Funcionar em 5 Minutos

## 🚀 Tutorial Rápido - Do Zero ao App Funcionando

### **Passo 1: Preparar o Ambiente** (1 minuto)

```bash
# Navegue até o diretório do projeto
cd /caminho/para/TATTOO-VIA-NEI

# Verifique se Docker está instalado
docker --version
# Se não tiver Docker, instale de: https://docs.docker.com/get-docker/

# Crie o arquivo de configuração
cp .env.example .env
```

✅ **Pronto!** Ambiente configurado.

---

### **Passo 2: Iniciar o Sistema** (2 minutos)

```bash
# Inicie o banco de dados e a aplicação
docker-compose up -d

# Aguarde ~30 segundos para o banco inicializar
# Você verá:
✔ Container postgres      Started
✔ Container fastapi-app   Started
```

**O que aconteceu:**
- PostgreSQL iniciou na porta 5432
- FastAPI iniciou na porta 8000
- Tudo rodando em background

✅ **Pronto!** Sistema no ar.

---

### **Passo 3: Criar as Tabelas** (30 segundos)

```bash
# Execute o script de criação de tabelas
python criar_tabelas.py

# Você verá:
🔨 Criando tabelas no banco de dados...
✅ Tabelas criadas com sucesso!

📋 Tabelas criadas:
  - clients
  - products
  - sellers
  - sales
  - sale_items
  - inventory_entries
  - costs
```

✅ **Pronto!** Banco de dados estruturado.

---

### **Passo 4: Adicionar Dados de Teste** (30 segundos)

```bash
# Popule o banco com dados de exemplo
python popular_db.py

# Você verá:
🌱 Populando banco de dados com dados de exemplo...

👥 Criando clientes...
✅ 3 clientes criados

💼 Criando vendedores...
✅ 2 vendedores criados

📦 Criando produtos...
✅ 4 produtos criados

📥 Registrando entradas de estoque...
✅ Entradas de estoque registradas

💰 Registrando custos...
✅ 4 custos registrados

🛒 Criando vendas de exemplo...
✅ 2 vendas criadas com sucesso

✨ Banco de dados populado com sucesso!

📊 Resumo:
  - Clientes: 3
  - Vendedores: 2
  - Produtos: 4
  - Vendas: 2
  - Custos: 4

🔗 Acesse a API em: http://localhost:8000/docs
```

✅ **Pronto!** Dados de teste adicionados.

---

### **Passo 5: Acessar a Interface** (1 minuto)

```bash
# Abra no navegador
open http://localhost:8000/docs

# Ou acesse manualmente:
# Chrome/Firefox/Safari → http://localhost:8000/docs
```

**Você verá a interface Swagger UI!** 🎉

---

## 📱 O Que Você Pode Fazer Agora

### **Teste 1: Ver Todos os Produtos**

1. Na interface Swagger, localize: `GET /api/v1/products`
2. Clique nele para expandir
3. Clique em **"Try it out"**
4. Clique em **"Execute"**
5. Veja a resposta com os 4 produtos:

```json
[
  {
    "id": 1,
    "name": "Camiseta Básica",
    "sku": "CAM001",
    "unit_price": 49.90,
    "cost_price": 25.00,
    "margin": 99.6,
    "stock_quantity": 100
  },
  {
    "id": 2,
    "name": "Calça Jeans",
    "sku": "CAL001",
    "unit_price": 129.90,
    "cost_price": 60.00,
    "margin": 116.5,
    "stock_quantity": 50
  },
  ...
]
```

✅ **Funcionou!** Sistema está lendo do banco.

---

### **Teste 2: Criar um Novo Cliente**

1. Localize: `POST /api/v1/clients`
2. Clique em **"Try it out"**
3. Edite o Request Body:

```json
{
  "name": "Seu Nome Aqui",
  "email": "seu.email@example.com",
  "phone": "11999999999",
  "document": "12345678900",
  "address": "Sua Rua, 123"
}
```

4. Clique em **"Execute"**
5. Veja a resposta 201 Created:

```json
{
  "id": 4,
  "client_id": "default-client",
  "name": "Seu Nome Aqui",
  "email": "seu.email@example.com",
  "phone": "11999999999",
  "document": "12345678900",
  "address": "Sua Rua, 123",
  "created_at": "2024-01-01T10:30:00",
  "updated_at": "2024-01-01T10:30:00"
}
```

✅ **Funcionou!** Você criou um cliente.

---

### **Teste 3: Fazer uma Venda**

1. Localize: `POST /api/v1/sales`
2. Clique em **"Try it out"**
3. Edite o Request Body:

```json
{
  "customer_id": 1,
  "seller_id": 1,
  "discount": 10.00,
  "payment_method": "credit",
  "items": [
    {
      "product_id": 1,
      "quantity": 2,
      "unit_price": 49.90
    },
    {
      "product_id": 4,
      "quantity": 1,
      "unit_price": 39.90
    }
  ]
}
```

4. Clique em **"Execute"**
5. Veja a venda criada:

```json
{
  "id": 3,
  "customer_id": 1,
  "seller_id": 1,
  "sale_date": "2024-01-01T10:35:00",
  "total_amount": 139.70,
  "discount": 10.00,
  "final_amount": 129.70,
  "payment_method": "credit",
  "status": "completed",
  "items": [...]
}
```

✅ **Funcionou!** Venda registrada, estoque atualizado automaticamente.

---

### **Teste 4: Ver Estoque Atualizado**

1. Volte em: `GET /api/v1/products`
2. Execute novamente
3. Note que as quantidades diminuíram:

```json
{
  "id": 1,
  "name": "Camiseta Básica",
  "stock_quantity": 98,  // Era 100, vendeu 2
  ...
},
{
  "id": 4,
  "name": "Boné Estampado",
  "stock_quantity": 74,  // Era 75, vendeu 1
  ...
}
```

✅ **Funcionou!** Controle de estoque automático.

---

### **Teste 5: Usar Analytics (via Python)**

Crie um arquivo `test_analytics.py`:

```python
from app.analytics.analytics_service import AnalyticsService
from app.core.database import SessionLocal
from app.core.config import settings

db = SessionLocal()
analytics = AnalyticsService(db, settings.CLIENT_ID)

# Resumo de vendas
summary = analytics.get_sales_summary()
print("📊 Resumo de Vendas:")
print(f"  Total de vendas: {summary['total_sales']}")
print(f"  Receita total: R$ {summary['total_revenue']:.2f}")
print(f"  Ticket médio: R$ {summary['average_ticket']:.2f}")

# Top produtos
print("\n🏆 Top Produtos:")
for product in analytics.get_top_products(3):
    print(f"  {product['product_name']}: R$ {product['total_revenue']:.2f}")

# Lucratividade
profit = analytics.get_profitability_analysis()
print("\n💰 Análise de Lucratividade:")
print(f"  Receita: R$ {profit['total_revenue']:.2f}")
print(f"  Lucro bruto: R$ {profit['gross_profit']:.2f}")
print(f"  Margem bruta: {profit['gross_margin_percent']:.1f}%")

db.close()
```

Execute:
```bash
python test_analytics.py
```

Saída:
```
📊 Resumo de Vendas:
  Total de vendas: 3
  Receita total: R$ 529.40
  Ticket médio: R$ 176.47

🏆 Top Produtos:
  Calça Jeans: R$ 129.90
  Tênis Esportivo: R$ 249.90
  Camiseta Básica: R$ 99.80

💰 Análise de Lucratividade:
  Receita: R$ 529.40
  Lucro bruto: R$ 260.00
  Margem bruta: 49.1%
```

✅ **Funcionou!** Analytics para upsell de consultoria.

---

## 🎯 Checklist - Você Conseguiu?

- [ ] Iniciar o Docker (`docker-compose up -d`)
- [ ] Criar tabelas (`python criar_tabelas.py`)
- [ ] Popular dados (`python popular_db.py`)
- [ ] Acessar Swagger UI (http://localhost:8000/docs)
- [ ] Listar produtos existentes
- [ ] Criar um novo cliente
- [ ] Fazer uma venda
- [ ] Ver estoque atualizado
- [ ] Testar analytics via Python

**Se marcou todos: PARABÉNS! 🎉**
**O app está 100% funcional como API backend.**

---

## 🛑 Problemas Comuns

### **Erro: "Port 8000 already in use"**

```bash
# Mate o processo na porta 8000
lsof -ti:8000 | xargs kill -9

# Ou use outra porta
# Edite docker-compose.yml: "8001:8000"
```

### **Erro: "Connection to database failed"**

```bash
# Aguarde mais tempo para o PostgreSQL inicializar
sleep 30

# Ou reinicie os containers
docker-compose down
docker-compose up -d
```

### **Erro: "ModuleNotFoundError: No module named 'app'"**

```bash
# Certifique-se de estar no diretório raiz
cd /caminho/para/TATTOO-VIA-NEI

# Adicione ao PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

---

## 📚 Próximos Passos

### **Agora que o backend funciona:**

1. **Explore mais endpoints**
   - Teste todos os módulos (sellers, costs, inventory)
   - Veja a documentação automática no Swagger

2. **Experimente criar cenários**
   - Cadastre seus próprios produtos
   - Simule vendas reais
   - Analise os dados

3. **Planeje o frontend**
   - Defina quais telas precisa
   - Escolha o design (Material-UI, Tailwind)
   - Liste funcionalidades prioritárias

4. **Deploy de teste**
   - Suba no Railway/DO para testar online
   - Configure um domínio teste
   - Convide alguém para testar

---

## 🎓 Recursos Adicionais

**Documentação no repositório:**
- `COMO-FUNCIONA.md` - Como o código funciona
- `ACESSO-SAAS.md` - Modelo SaaS explicado
- `DEPLOYMENT.md` - Como fazer deploy
- `QUICKSTART.md` - Guia rápido

**Para aprender mais:**
- FastAPI: https://fastapi.tiangolo.com
- SQLAlchemy: https://www.sqlalchemy.org
- Docker: https://docs.docker.com

---

**Está tudo funcionando! Explore e divirta-se! 🚀**
