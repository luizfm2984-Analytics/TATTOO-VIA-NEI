# Quick Start Guide

Este guia rápido te ajuda a começar a usar o Lead Scraper em menos de 5 minutos.

## 📥 Instalação Rápida

```bash
# 1. Clone o repositório
git clone https://github.com/luizfm2984-Analytics/TATTOO-VIA-NEI.git
cd TATTOO-VIA-NEI

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute o scraper
python main.py
```

Pronto! Os resultados serão salvos em `output/leads_YYYYMMDD_HHMMSS.csv`

## 🎯 Uso Básico

### Executar com configurações padrão
```bash
python main.py
```

### Exportar como JSON
```bash
OUTPUT_FORMAT=json python main.py
```

### Limitar número de resultados
```bash
MAX_RESULTS_PER_PLATFORM=20 python main.py
```

## 🔍 Entendendo os Resultados

Cada lead retornado contém:
- **name**: Nome do criador/curso
- **platform**: Plataforma onde foi encontrado (Hotmart, Instagram, Google)
- **url**: Link direto para o perfil/produto
- **engagement_score**: Score de 0 a 1 indicando o nível de engajamento
- **followers**: Número de seguidores/reviews
- **description**: Descrição breve
- **mentions_mec**: Se menciona ou não o MEC (sempre False nos resultados)

## 📊 Interpretando o Engagement Score

- **0.8 - 1.0**: Alto engajamento (excelente lead)
- **0.5 - 0.8**: Médio engajamento (bom lead)
- **0.0 - 0.5**: Baixo engajamento (filtrado por padrão)

## 💡 Dicas Rápidas

1. **Filtrar MEC está ativado por padrão** - O scraper já exclui automaticamente qualquer lead que mencione MEC
2. **Engagement mínimo é 0.5** - Apenas leads com engajamento razoável são retornados
3. **Dados são simulados** - Esta versão usa dados de exemplo. Para produção, integre com APIs reais
4. **Output ignorado no git** - Os arquivos CSV/JSON gerados não são commitados

## 🚀 Próximos Passos

Veja o arquivo `examples.py` para casos de uso mais avançados:
```bash
python examples.py
```

Ou leia a documentação completa no `README.md`.

## ❓ Problemas Comuns

### Erro ao instalar dependências
```bash
# Use pip com sudo se necessário
sudo pip install -r requirements.txt

# Ou use um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Python não encontrado
Certifique-se de ter Python 3.7+ instalado:
```bash
python --version
# ou
python3 --version
```

## 📞 Suporte

Para dúvidas ou problemas, consulte:
- README.md - Documentação completa
- examples.py - Exemplos de código
- test_mec_filter.py - Testes do filtro MEC
