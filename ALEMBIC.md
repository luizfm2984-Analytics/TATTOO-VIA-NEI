# Alembic Setup Guide

## Inicializar Migrações

O Alembic está configurado para gerenciar as migrações do banco de dados.

### Criar estrutura inicial (já feito)
```bash
alembic init alembic
```

### Configurar env.py

Edite `alembic/env.py` e adicione:

```python
from app.core.database import Base
from app.models.models import *

target_metadata = Base.metadata
```

### Criar primeira migração

```bash
alembic revision --autogenerate -m "Initial tables"
```

### Aplicar migrações

```bash
alembic upgrade head
```

### Verificar status

```bash
alembic current
alembic history
```

## Comandos Úteis

```bash
# Criar nova migração
alembic revision --autogenerate -m "Add new field"

# Aplicar todas as migrações
alembic upgrade head

# Reverter última migração
alembic downgrade -1

# Ver histórico
alembic history --verbose
```

## Docker

No Docker, as migrações podem ser executadas automaticamente no startup ou manualmente:

```bash
# Manual
docker-compose exec app alembic upgrade head

# Automático: adicione ao Dockerfile
CMD alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000
```
