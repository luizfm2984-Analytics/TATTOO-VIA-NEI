# Guia de Deployment - Management App

## Opções de Hospedagem

### Comparativo de Custos

| Plataforma | Custo/mês | Pros | Contras |
|------------|-----------|------|---------|
| Railway | $10-20 | Fácil deploy, PostgreSQL incluso | Limites de recursos |
| DigitalOcean App Platform | $12-25 | Escalável, confiável | Requer configuração |
| Render | $7-21 | Free tier disponível | Performance limitada no free |
| AWS Lightsail | $10-20 | Controle total, AWS ecosystem | Mais complexo |
| VPS Self-hosted | $5-15 | Custo mais baixo | Requer manutenção manual |

## Recomendação: Railway ou DigitalOcean

Para começar, recomendamos **Railway** pela facilidade de uso e custo-benefício.

---

## Deploy no Railway

### 1. Preparação

```bash
# Instale o Railway CLI
npm i -g @railway/cli

# Faça login
railway login
```

### 2. Deploy do Projeto

```bash
# No diretório do projeto
railway init

# Faça o deploy
railway up

# Adicione PostgreSQL
railway add postgresql

# Configure as variáveis de ambiente
railway variables set SECRET_KEY="your-secret-key-here"
railway variables set CLIENT_ID="client-unique-id"
railway variables set ENVIRONMENT="production"
```

### 3. Configuração Automática

O Railway detecta automaticamente o `Dockerfile` e faz o build.

### 4. Acesso ao App

```bash
# Obtenha a URL do app
railway domain
```

---

## Deploy no DigitalOcean App Platform

### 1. Via GitHub (Recomendado)

1. Acesse [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
2. Clique em "Create App"
3. Conecte seu repositório GitHub
4. Configure:
   - **Branch**: main/master
   - **Source Directory**: /
   - **Autodeploy**: Enabled

### 2. Configuração do App

**Build Configuration:**
- **Type**: Docker
- **Dockerfile**: `./Dockerfile`

**Environment Variables:**
```
DATABASE_URL=${db.DATABASE_URL}
SECRET_KEY=generate-a-secure-key
CLIENT_ID=client-unique-id
ENVIRONMENT=production
```

### 3. Adicionar Database

1. Clique em "Add Resource"
2. Selecione "Database"
3. Escolha "PostgreSQL"
4. Tamanho: Basic ($15/mês)

### 4. Deploy

Clique em "Create Resources" e aguarde o deploy (5-10 min).

---

## Deploy com Docker (VPS)

### 1. Requisitos

- VPS com Docker instalado (Ubuntu 20.04+)
- Domínio configurado (opcional)

### 2. Preparação do VPS

```bash
# Instale Docker e Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Instale Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 3. Clone e Configure

```bash
# Clone o repositório
git clone <repo-url>
cd TATTOO-VIA-NEI

# Crie e configure .env
cp .env.example .env
nano .env
```

**Edite .env:**
```env
DATABASE_URL=postgresql://management_user:management_pass@db:5432/management_db
SECRET_KEY=generate-a-very-secure-secret-key-here
CLIENT_ID=unique-client-identifier
ENVIRONMENT=production
ALLOWED_ORIGINS=https://yourdomain.com
```

### 4. Inicie os Serviços

```bash
# Inicie em background
docker-compose up -d

# Verifique os logs
docker-compose logs -f

# Verifique status
docker-compose ps
```

### 5. Configure Nginx (Opcional)

```bash
sudo apt install nginx

# Crie configuração
sudo nano /etc/nginx/sites-available/management-app
```

**Conteúdo:**
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Ative a configuração
sudo ln -s /etc/nginx/sites-available/management-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 6. SSL com Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

---

## Estratégias de Multi-Client

### Opção 1: Instância Compartilhada (Multi-Tenancy)

**Vantagens:**
- Menor custo (1 servidor para múltiplos clientes)
- Fácil manutenção

**Configuração:**
```bash
# Cada cliente usa CLIENT_ID diferente
# Mesmo banco de dados, dados isolados por client_id
CLIENT_ID=cliente-001
CLIENT_ID=cliente-002
```

**Custo Total:** $20-30/mês para 5-10 clientes

### Opção 2: Instância Isolada por Cliente

**Vantagens:**
- Máxima segurança e isolamento
- Personalização completa

**Configuração:**
```bash
# Deploy separado para cada cliente
railway init --name cliente-001
railway init --name cliente-002
```

**Custo Total:** $15-20/mês por cliente

---

## Distribuição para Clientes

### Modelo 1: Hospedagem Gerenciada (Recomendado)

**Você hospeda e gerencia:**
1. Cliente se cadastra
2. Você cria uma instância (ou adiciona ao multi-tenant)
3. Cliente recebe credenciais de acesso
4. Você gerencia atualizações e manutenção

**Vantagem:** Controle total, receita recorrente

### Modelo 2: Self-Hosted pelo Cliente

**Cliente hospeda:**
1. Você fornece o código (Docker image)
2. Cliente faz deploy no próprio servidor
3. Você oferece suporte técnico (cobrado à parte)

**Vantagem:** Cliente tem controle total

---

## Backup e Manutenção

### Backup Automático (Railway/DigitalOcean)

Configurado automaticamente pela plataforma.

### Backup Manual (VPS)

```bash
# Backup do banco de dados
docker-compose exec db pg_dump -U management_user management_db > backup_$(date +%Y%m%d).sql

# Restaurar backup
docker-compose exec -T db psql -U management_user management_db < backup_20240101.sql
```

### Atualizações

```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up -d --build

# Ou no Railway/DO: Push to GitHub triggers auto-deploy
```

---

## Monitoramento

### DigitalOcean

- Métricas integradas no painel
- Alertas de CPU, memória, disco

### Railway

- Dashboard com logs e métricas
- Alerts via email

### Self-Hosted

```bash
# Instale Grafana + Prometheus (opcional)
docker-compose -f docker-compose.monitoring.yml up -d
```

---

## Custos Estimados por Modelo

### 1 Cliente
- Railway/DO: $15-20/mês
- VPS Self-hosted: $10/mês

### 5 Clientes (Multi-tenant)
- Railway/DO: $30-40/mês total
- VPS: $20/mês total

### 5 Clientes (Isolados)
- Railway/DO: $75-100/mês total
- VPS: $50-75/mês total

---

## Precificação Sugerida

Baseado nos custos:

1. **Setup Inicial**: R$ 2.000 - 5.000
   - Implementação
   - Configuração
   - Treinamento

2. **Mensalidade**: R$ 200 - 500/mês
   - Hospedagem
   - Manutenção
   - Suporte básico

3. **Consultoria Analytics** (Upsell): R$ 500 - 2.000/mês
   - Relatórios customizados
   - Análises avançadas
   - Insights estratégicos

**Margem de Lucro:** 60-80% após custos de infraestrutura

---

## Próximos Passos

1. ✅ Escolher plataforma de hospedagem
2. ⬜ Fazer deploy de teste
3. ⬜ Configurar domínio
4. ⬜ Testar com dados reais
5. ⬜ Definir processo de onboarding
6. ⬜ Criar documentação para clientes
7. ⬜ Preparar materiais de venda

---

## Suporte

Para dúvidas sobre deployment, abra uma issue ou entre em contato.
