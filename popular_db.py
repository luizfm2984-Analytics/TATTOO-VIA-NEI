#!/usr/bin/env python3
"""
Script para popular o banco com dados de exemplo
"""
import sys
from pathlib import Path
from datetime import datetime

# Adiciona o diretório raiz ao path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

from app.core.database import SessionLocal
from app.core.config import settings
from app.models.models import (
    Client,
    Product,
    Seller,
    Sale,
    SaleItem,
    InventoryEntry,
    Cost
)

def populate_db():
    """Popula o banco com dados de exemplo"""
    db = SessionLocal()
    
    try:
        print("🌱 Populando banco de dados com dados de exemplo...")
        
        # 1. Criar clientes
        print("\n👥 Criando clientes...")
        clientes = [
            Client(
                client_id=settings.CLIENT_ID,
                name="João Silva",
                email="joao@example.com",
                phone="11999999999",
                document="12345678900",
                address="Rua A, 123 - São Paulo/SP"
            ),
            Client(
                client_id=settings.CLIENT_ID,
                name="Maria Santos",
                email="maria@example.com",
                phone="11988888888",
                document="98765432100",
                address="Av. B, 456 - São Paulo/SP"
            ),
            Client(
                client_id=settings.CLIENT_ID,
                name="Pedro Costa",
                email="pedro@example.com",
                phone="11977777777",
                document="11122233344",
                address="Rua C, 789 - São Paulo/SP"
            ),
        ]
        
        for cliente in clientes:
            db.add(cliente)
        db.commit()
        print(f"✅ {len(clientes)} clientes criados")
        
        # 2. Criar vendedores
        print("\n💼 Criando vendedores...")
        vendedores = [
            Seller(
                client_id=settings.CLIENT_ID,
                name="Ana Vendas",
                email="ana@example.com",
                phone="11966666666",
                commission_rate=5.0
            ),
            Seller(
                client_id=settings.CLIENT_ID,
                name="Carlos Comercial",
                email="carlos@example.com",
                phone="11955555555",
                commission_rate=7.5
            ),
        ]
        
        for vendedor in vendedores:
            db.add(vendedor)
        db.commit()
        print(f"✅ {len(vendedores)} vendedores criados")
        
        # 3. Criar produtos
        print("\n📦 Criando produtos...")
        produtos = [
            Product(
                client_id=settings.CLIENT_ID,
                name="Camiseta Básica",
                description="Camiseta 100% algodão",
                sku="CAM001",
                category="Vestuário",
                unit_price=49.90,
                cost_price=25.00,
                margin=99.6,  # (49.90 - 25) / 25 * 100
                stock_quantity=100,
                min_stock=20
            ),
            Product(
                client_id=settings.CLIENT_ID,
                name="Calça Jeans",
                description="Calça jeans tradicional",
                sku="CAL001",
                category="Vestuário",
                unit_price=129.90,
                cost_price=60.00,
                margin=116.5,
                stock_quantity=50,
                min_stock=10
            ),
            Product(
                client_id=settings.CLIENT_ID,
                name="Tênis Esportivo",
                description="Tênis para corrida",
                sku="TEN001",
                category="Calçados",
                unit_price=249.90,
                cost_price=120.00,
                margin=108.25,
                stock_quantity=30,
                min_stock=5
            ),
            Product(
                client_id=settings.CLIENT_ID,
                name="Boné Estampado",
                description="Boné com estampa personalizada",
                sku="BON001",
                category="Acessórios",
                unit_price=39.90,
                cost_price=15.00,
                margin=166.0,
                stock_quantity=75,
                min_stock=15
            ),
        ]
        
        for produto in produtos:
            db.add(produto)
        db.commit()
        print(f"✅ {len(produtos)} produtos criados")
        
        # 4. Criar entradas de estoque
        print("\n📥 Registrando entradas de estoque...")
        for produto in db.query(Product).filter(Product.client_id == settings.CLIENT_ID).all():
            entrada = InventoryEntry(
                client_id=settings.CLIENT_ID,
                product_id=produto.id,
                entry_type="purchase",
                quantity=produto.stock_quantity,
                unit_cost=produto.cost_price,
                total_cost=produto.stock_quantity * produto.cost_price,
                notes="Estoque inicial"
            )
            db.add(entrada)
        db.commit()
        print("✅ Entradas de estoque registradas")
        
        # 5. Criar custos
        print("\n💰 Registrando custos...")
        custos = [
            Cost(
                client_id=settings.CLIENT_ID,
                category="rent",
                description="Aluguel da loja",
                amount=3000.00,
                is_recurring=1,
                notes="Aluguel mensal do espaço comercial"
            ),
            Cost(
                client_id=settings.CLIENT_ID,
                category="utilities",
                description="Energia elétrica",
                amount=450.00,
                is_recurring=1,
                notes="Conta de luz mensal"
            ),
            Cost(
                client_id=settings.CLIENT_ID,
                category="salaries",
                description="Salários funcionários",
                amount=8500.00,
                is_recurring=1,
                notes="Folha de pagamento mensal"
            ),
            Cost(
                client_id=settings.CLIENT_ID,
                category="marketing",
                description="Campanha redes sociais",
                amount=1200.00,
                is_recurring=0,
                notes="Campanha promocional do mês"
            ),
        ]
        
        for custo in custos:
            db.add(custo)
        db.commit()
        print(f"✅ {len(custos)} custos registrados")
        
        # 6. Criar algumas vendas de exemplo
        print("\n🛒 Criando vendas de exemplo...")
        
        # Venda 1
        venda1 = Sale(
            client_id=settings.CLIENT_ID,
            customer_id=1,  # João Silva
            seller_id=1,    # Ana Vendas
            total_amount=99.80,
            discount=0.00,
            final_amount=99.80,
            payment_method="credit",
            status="completed"
        )
        db.add(venda1)
        db.flush()
        
        # Itens da venda 1
        item1 = SaleItem(
            sale_id=venda1.id,
            product_id=1,  # Camiseta
            quantity=2,
            unit_price=49.90,
            subtotal=99.80
        )
        db.add(item1)
        
        # Atualizar estoque
        produto1 = db.query(Product).filter(Product.id == 1).first()
        produto1.stock_quantity -= 2
        
        # Venda 2
        venda2 = Sale(
            client_id=settings.CLIENT_ID,
            customer_id=2,  # Maria Santos
            seller_id=2,    # Carlos Comercial
            total_amount=419.70,
            discount=20.00,
            final_amount=399.70,
            payment_method="pix",
            status="completed"
        )
        db.add(venda2)
        db.flush()
        
        # Itens da venda 2
        item2_1 = SaleItem(
            sale_id=venda2.id,
            product_id=2,  # Calça
            quantity=1,
            unit_price=129.90,
            subtotal=129.90
        )
        item2_2 = SaleItem(
            sale_id=venda2.id,
            product_id=3,  # Tênis
            quantity=1,
            unit_price=249.90,
            subtotal=249.90
        )
        item2_3 = SaleItem(
            sale_id=venda2.id,
            product_id=4,  # Boné
            quantity=1,
            unit_price=39.90,
            subtotal=39.90
        )
        db.add(item2_1)
        db.add(item2_2)
        db.add(item2_3)
        
        # Atualizar estoque
        db.query(Product).filter(Product.id == 2).first().stock_quantity -= 1
        db.query(Product).filter(Product.id == 3).first().stock_quantity -= 1
        db.query(Product).filter(Product.id == 4).first().stock_quantity -= 1
        
        db.commit()
        print("✅ 2 vendas criadas com sucesso")
        
        print("\n✨ Banco de dados populado com sucesso!")
        print("\n📊 Resumo:")
        print(f"  - Clientes: {db.query(Client).count()}")
        print(f"  - Vendedores: {db.query(Seller).count()}")
        print(f"  - Produtos: {db.query(Product).count()}")
        print(f"  - Vendas: {db.query(Sale).count()}")
        print(f"  - Custos: {db.query(Cost).count()}")
        
        print("\n🔗 Acesse a API em: http://localhost:8000/docs")
        
    except Exception as e:
        print(f"❌ Erro ao popular banco: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    populate_db()
