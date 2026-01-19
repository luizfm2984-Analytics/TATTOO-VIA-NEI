# TATTOO-VIA-NEI - Lead Scraper

Web scraping application to find course creator leads on multiple platforms (Hotmart, Instagram, Google) with focus on finding high-engagement creators who don't mention MEC accreditation.

## 🎯 Objetivo

Encontrar leads de criadores de cursos que:
- Oferecem cursos via Hotmart, Instagram, Google e outras plataformas
- NÃO mencionam MEC (Ministério da Educação)
- Têm alto engajamento e volume de vendas/influência

## 📋 Funcionalidades

- ✅ Scraping de múltiplas plataformas (Hotmart, Instagram, Google)
- ✅ Filtro automático de leads que mencionam MEC
- ✅ Avaliação de métricas de engajamento e influência
- ✅ Exportação de resultados em CSV ou JSON
- ✅ Configuração flexível via arquivo .env

## 🚀 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/luizfm2984-Analytics/TATTOO-VIA-NEI.git
cd TATTOO-VIA-NEI
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas credenciais
```

## ⚙️ Configuração

Crie um arquivo `.env` baseado no `.env.example`:

```bash
# Credenciais do Instagram (opcional)
INSTAGRAM_USERNAME=seu_usuario
INSTAGRAM_PASSWORD=sua_senha

# Google Custom Search API (opcional)
GOOGLE_API_KEY=sua_api_key
GOOGLE_CSE_ID=seu_cse_id

# Configurações gerais
OUTPUT_FORMAT=csv          # csv ou json
MAX_RESULTS_PER_PLATFORM=50
```

## 📖 Uso

### Uso Básico

Execute o scraper principal:

```bash
python main.py
```

### Uso Avançado

```python
from main import LeadScraper

# Inicializar o scraper
scraper = LeadScraper(max_results_per_platform=50)

# Fazer scraping de todas as plataformas
# filter_mec=True: exclui leads que mencionam MEC
# min_engagement=0.5: apenas leads com engajamento >= 0.5
leads = scraper.scrape_all_platforms(filter_mec=True, min_engagement=0.5)

# Visualizar resumo
scraper.print_summary()

# Exportar resultados
scraper.export_to_csv()  # ou scraper.export_to_json()
```

### Scraping Individual por Plataforma

```python
from hotmart_scraper import HotmartScraper
from instagram_scraper import InstagramScraper
from google_scraper import GoogleScraper

# Hotmart
hotmart = HotmartScraper(max_results=50)
hotmart_leads = hotmart.get_leads(filter_mec=True, min_engagement=0.5)

# Instagram
instagram = InstagramScraper(max_results=50)
instagram_leads = instagram.get_leads(filter_mec=True, min_engagement=0.5)

# Google
google = GoogleScraper(max_results=50)
google_leads = google.get_leads(filter_mec=True, min_engagement=0.5)
```

## 📊 Estrutura de Dados

Cada lead contém as seguintes informações:

```python
{
    'name': 'Nome do criador/curso',
    'platform': 'Hotmart | Instagram | Google Search',
    'url': 'URL do perfil/produto',
    'engagement_score': 0.0-1.0,  # Score de engajamento
    'followers': 0,                # Seguidores/reviews
    'description': 'Descrição',
    'mentions_mec': False          # Se menciona MEC
}
```

## 📁 Estrutura do Projeto

```
TATTOO-VIA-NEI/
├── base_scraper.py         # Classe base para todos os scrapers
├── hotmart_scraper.py      # Scraper do Hotmart
├── instagram_scraper.py    # Scraper do Instagram
├── google_scraper.py       # Scraper do Google
├── main.py                 # Script principal
├── requirements.txt        # Dependências Python
├── .env.example           # Exemplo de configuração
├── .gitignore             # Arquivos a ignorar
└── output/                # Diretório de saída (gerado automaticamente)
    ├── leads_YYYYMMDD_HHMMSS.csv
    └── leads_YYYYMMDD_HHMMSS.json
```

## 🔍 Filtros e Métricas

### Filtro MEC
O sistema automaticamente filtra leads que mencionam:
- "mec"
- "ministério da educação"
- "autorizado mec"
- "reconhecido mec"
- "credenciado mec"
- E outras variações

### Score de Engajamento
Calculado com base em:
- **Hotmart**: Reviews e ratings
- **Instagram**: Taxa de engajamento e número de seguidores
- **Google**: Autoridade de domínio e relevância

## 📝 Notas Importantes

### Implementação Atual
Esta é uma implementação de demonstração com dados simulados. Para uso em produção, você precisará:

1. **Hotmart**: Integração com API oficial ou scraping do marketplace
2. **Instagram**: Instagram Graph API ou ferramentas como `instaloader`
3. **Google**: Google Custom Search API com chave válida

### Considerações Legais
- Sempre respeite os termos de serviço das plataformas
- Use APIs oficiais quando disponíveis
- Implemente rate limiting e delays apropriados
- Considere aspectos legais de web scraping na sua jurisdição

## 🛠️ Desenvolvimento Futuro

- [ ] Integração com APIs oficiais
- [ ] Suporte para mais plataformas (Udemy, Eduzz, etc.)
- [ ] Dashboard web para visualização
- [ ] Sistema de notificações para novos leads
- [ ] Machine learning para scoring avançado
- [ ] Banco de dados para armazenamento persistente

## 📄 Licença

Este projeto é para uso interno e educacional.
