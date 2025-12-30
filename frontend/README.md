# Frontend - Sistema de Gestão com Streamlit

Interface web completa em Python usando Streamlit que consome a API FastAPI existente.

## 📋 Pré-requisitos

- Python 3.8+
- API FastAPI rodando em http://localhost:8000
- Banco de dados populado com dados

## 🚀 Instalação

### 1. Navegue até o diretório frontend

```bash
cd frontend
```

### 2. Crie e ative um ambiente virtual (recomendado)

```bash
# Linux/Mac
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o .env se necessário (URL da API)
# Por padrão: API_BASE_URL=http://localhost:8000
```

## ▶️ Como Executar

### 1. Certifique-se de que a API backend está rodando

```bash
# No diretório raiz do projeto
cd ..
docker-compose up -d
python criar_tabelas.py  # Se ainda não criou as tabelas
python popular_db.py     # Para adicionar dados de exemplo
```

### 2. Execute o Streamlit

```bash
# No diretório frontend
streamlit run app.py
```

### 3. Acesse no navegador

O Streamlit abrirá automaticamente em: **http://localhost:8501**

## 🎯 Funcionalidades

### 🔐 Login
- Tela de login simulada (sem JWT por enquanto)
- Verificação de conectividade com a API
- Armazenamento de sessão

### 📦 Gerenciamento de Produtos
- ✅ Listar todos os produtos
- ✅ Adicionar novo produto
- ✅ Editar produto existente
- ✅ Deletar produto
- ✅ Buscar produtos por nome
- ✅ Visualizar margem de lucro calculada automaticamente

### 👥 Gerenciamento de Clientes
- ✅ Listar todos os clientes
- ✅ Adicionar novo cliente
- ✅ Editar cliente existente
- ✅ Deletar cliente
- ✅ Buscar clientes por nome

### 🛒 Gerenciamento de Vendas
- ✅ Listar todas as vendas
- ✅ Registrar nova venda (com múltiplos itens)
- ✅ Cancelar venda (restaura estoque automaticamente)
- ✅ Visualizar detalhes da venda
- ✅ Cálculo automático de totais e descontos
- ✅ Validação de estoque disponível

### 🏠 Dashboard
- Estatísticas gerais (total de produtos, clientes, vendas)
- Últimas vendas realizadas

## 📁 Estrutura do Projeto

```
frontend/
├── app.py                 # Aplicação principal (login e navegação)
├── services/
│   ├── __init__.py
│   └── api.py            # Cliente HTTP para consumir a API
├── pages/
│   ├── __init__.py
│   ├── produtos.py       # Página de produtos
│   ├── clientes.py       # Página de clientes
│   └── vendas.py         # Página de vendas
├── requirements.txt      # Dependências Python
├── .env.example          # Exemplo de variáveis de ambiente
└── README.md            # Este arquivo
```

## 🔧 Configuração

### Variáveis de Ambiente (.env)

```env
API_BASE_URL=http://localhost:8000
```

### Endpoints Consumidos da API

O frontend consome os seguintes endpoints da API FastAPI:

**Health Check:**
- `GET /health`

**Clientes:**
- `GET /api/v1/clients` - Listar clientes
- `POST /api/v1/clients` - Criar cliente
- `GET /api/v1/clients/{id}` - Obter cliente
- `PUT /api/v1/clients/{id}` - Atualizar cliente
- `DELETE /api/v1/clients/{id}` - Deletar cliente

**Produtos:**
- `GET /api/v1/products` - Listar produtos
- `POST /api/v1/products` - Criar produto
- `GET /api/v1/products/{id}` - Obter produto
- `PUT /api/v1/products/{id}` - Atualizar produto
- `DELETE /api/v1/products/{id}` - Deletar produto

**Vendas:**
- `GET /api/v1/sales` - Listar vendas
- `POST /api/v1/sales` - Criar venda
- `GET /api/v1/sales/{id}` - Obter venda
- `DELETE /api/v1/sales/{id}` - Cancelar venda

**Vendedores:**
- `GET /api/v1/sellers` - Listar vendedores

## ⚠️ Tratamento de Erros

O frontend trata os seguintes erros da API:

- **401**: Não autorizado (redirect para login)
- **404**: Recurso não encontrado
- **400**: Erro de validação (exibe mensagem detalhada)
- **500**: Erro no servidor
- **Connection Error**: API não disponível

## 🎨 Características da Interface

- ✅ Interface limpa e intuitiva
- ✅ Feedback visual para todas as ações (success, error, warning)
- ✅ Confirmação dupla para ações destrutivas (deletar)
- ✅ Recarregamento automático após operações CRUD
- ✅ Formulários com validação
- ✅ Layout responsivo
- ✅ Ícones intuitivos

## 🐛 Troubleshooting

### Erro: "Não foi possível conectar à API"

**Solução:**
1. Verifique se a API está rodando: `docker-compose ps`
2. Verifique a URL no `.env`: deve ser `http://localhost:8000`
3. Teste a API diretamente: `curl http://localhost:8000/health`

### Erro: "ModuleNotFoundError"

**Solução:**
```bash
pip install -r requirements.txt
```

### Erro: "Port 8501 already in use"

**Solução:**
```bash
# Use outra porta
streamlit run app.py --server.port 8502
```

### Dados não aparecem

**Solução:**
```bash
# Certifique-se de que o banco tem dados
cd ..
python popular_db.py
```

## 📝 Notas

- **Login:** Atualmente é simulado. Quando a API implementar JWT, o frontend já está preparado para usar o token.
- **Autenticação:** O campo `Authorization: Bearer {token}` já está implementado no cliente da API.
- **Vendedores:** A listagem está implementada, mas o CRUD completo pode ser adicionado facilmente seguindo o mesmo padrão.

## 🎓 Próximos Passos (Sugestões)

- [ ] Implementar autenticação JWT real quando disponível na API
- [ ] Adicionar gráficos e dashboards com plotly
- [ ] Implementar filtros avançados
- [ ] Adicionar exportação de relatórios (PDF/Excel)
- [ ] Implementar paginação para listas grandes
- [ ] Adicionar modo escuro
- [ ] Melhorar validações de formulários
- [ ] Adicionar upload de imagens de produtos

## 📞 Suporte

Para problemas ou dúvidas:
1. Verifique se a API está rodando e acessível
2. Verifique os logs do Streamlit no terminal
3. Consulte a documentação da API em http://localhost:8000/docs

---

**Desenvolvido com Python + Streamlit + FastAPI** 🐍✨
