#!/usr/bin/env python3
"""
Script para adicionar um novo cliente (tenant) ao sistema
"""
import sys
import secrets
import string
from pathlib import Path

# Adiciona o diretório raiz ao path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

from app.core.database import SessionLocal
from app.models.models import Client

def generate_password(length=12):
    """Gera uma senha segura aleatória"""
    alphabet = string.ascii_letters + string.digits + "!@#$%&*"
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password

def generate_client_id(name):
    """Gera um client_id baseado no nome"""
    # Remove acentos e caracteres especiais, converte para lowercase
    import unicodedata
    normalized = unicodedata.normalize('NFKD', name)
    ascii_name = normalized.encode('ASCII', 'ignore').decode('ASCII')
    
    # Remove espaços e caracteres não alfanuméricos
    clean_name = ''.join(c for c in ascii_name if c.isalnum() or c.isspace())
    client_id = clean_name.lower().replace(' ', '-')
    
    # Adiciona timestamp para garantir unicidade
    import time
    timestamp = str(int(time.time()))[-4:]
    client_id = f"{client_id}-{timestamp}"
    
    return client_id

def adicionar_cliente():
    """Adiciona um novo cliente ao sistema"""
    print("=" * 60)
    print("🎯 ADICIONAR NOVO CLIENTE AO SISTEMA")
    print("=" * 60)
    print()
    
    # Coletar informações
    print("📝 Informações do Cliente:")
    name = input("  Nome/Razão Social: ").strip()
    if not name:
        print("❌ Nome é obrigatório!")
        sys.exit(1)
    
    email = input("  Email: ").strip()
    if not email:
        print("❌ Email é obrigatório!")
        sys.exit(1)
    
    phone = input("  Telefone (opcional): ").strip()
    document = input("  CPF/CNPJ (opcional): ").strip()
    address = input("  Endereço (opcional): ").strip()
    
    # Gerar client_id
    client_id = generate_client_id(name)
    print(f"\n🔑 ID do Cliente: {client_id}")
    
    # Gerar senha (para uso futuro com autenticação)
    password = generate_password()
    
    # Confirmar
    print("\n" + "=" * 60)
    print("📋 RESUMO:")
    print("=" * 60)
    print(f"Nome: {name}")
    print(f"Email: {email}")
    print(f"Phone: {phone or 'N/A'}")
    print(f"Document: {document or 'N/A'}")
    print(f"Client ID: {client_id}")
    print("=" * 60)
    
    confirm = input("\n✅ Confirmar criação? (s/n): ").strip().lower()
    if confirm != 's':
        print("❌ Operação cancelada.")
        sys.exit(0)
    
    # Criar no banco
    db = SessionLocal()
    
    try:
        # Verificar se email já existe
        existing = db.query(Client).filter(Client.email == email).first()
        if existing:
            print(f"❌ Erro: Email {email} já está cadastrado!")
            sys.exit(1)
        
        # Criar cliente
        novo_cliente = Client(
            client_id=client_id,
            name=name,
            email=email,
            phone=phone if phone else None,
            document=document if document else None,
            address=address if address else None
        )
        
        db.add(novo_cliente)
        db.commit()
        db.refresh(novo_cliente)
        
        print("\n" + "=" * 60)
        print("✅ CLIENTE CRIADO COM SUCESSO!")
        print("=" * 60)
        print(f"\n🆔 ID no Sistema: {novo_cliente.id}")
        print(f"🔑 Client ID: {client_id}")
        print(f"📧 Email: {email}")
        print(f"🔒 Senha (temporária): {password}")
        print("\n" + "-" * 60)
        print("📝 INSTRUÇÕES PARA O CLIENTE:")
        print("-" * 60)
        print(f"""
Bem-vindo ao Sistema de Gestão!

Seus dados de acesso:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
URL de Acesso: https://seu-dominio.com
            ou: http://localhost:8000/docs (teste)

Login: {email}
Senha: {password}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 Primeiros Passos:
1. Acesse a URL acima
2. Faça login com suas credenciais
3. Configure seus produtos
4. Comece a registrar vendas!

💡 Dica: Altere sua senha no primeiro acesso

📞 Suporte: seu-email@empresa.com
        """)
        
        print("\n" + "=" * 60)
        print("💾 Salve essas informações em local seguro!")
        print("=" * 60)
        
        # Salvar em arquivo
        filename = f"cliente_{client_id}.txt"
        with open(filename, 'w') as f:
            f.write(f"Cliente: {name}\n")
            f.write(f"Email: {email}\n")
            f.write(f"Client ID: {client_id}\n")
            f.write(f"Senha: {password}\n")
            f.write(f"Data: {novo_cliente.created_at}\n")
        
        print(f"\n📄 Informações salvas em: {filename}")
        
    except Exception as e:
        print(f"\n❌ Erro ao criar cliente: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    adicionar_cliente()
