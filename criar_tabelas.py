#!/usr/bin/env python3
"""
Script para criar as tabelas do banco de dados
"""
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

from app.core.database import engine, Base
from app.models.models import (
    Client,
    Product,
    Seller,
    Sale,
    SaleItem,
    InventoryEntry,
    Cost
)

def create_tables():
    """Cria todas as tabelas no banco de dados"""
    print("🔨 Criando tabelas no banco de dados...")
    
    try:
        # Cria todas as tabelas
        Base.metadata.create_all(bind=engine)
        print("✅ Tabelas criadas com sucesso!")
        
        # Lista as tabelas criadas
        print("\n📋 Tabelas criadas:")
        for table in Base.metadata.sorted_tables:
            print(f"  - {table.name}")
            
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_tables()
