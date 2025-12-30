"""
Página de Gerenciamento de Clientes
"""
import streamlit as st
from services.api import api_client


def show():
    """Display clients management page"""
    st.title("👥 Gerenciamento de Clientes")
    
    # Tabs for different views
    tab1, tab2 = st.tabs(["📋 Lista de Clientes", "➕ Adicionar Cliente"])
    
    with tab1:
        show_clients_list()
    
    with tab2:
        show_add_client_form()


def show_clients_list():
    """Display list of clients"""
    st.subheader("Lista de Clientes")
    
    try:
        clients = api_client.list_clients()
        
        if not clients:
            st.info("Nenhum cliente cadastrado. Adicione um novo cliente!")
            return
        
        # Search/filter
        search = st.text_input("🔍 Buscar cliente", placeholder="Digite o nome do cliente...")
        
        if search:
            clients = [c for c in clients if search.lower() in c['name'].lower()]
        
        # Display clients
        st.write(f"**Total:** {len(clients)} cliente(s)")
        
        for client in clients:
            with st.expander(f"👤 {client['name']}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**ID:** {client['id']}")
                    st.write(f"**Nome:** {client['name']}")
                    st.write(f"**Email:** {client.get('email', 'N/A')}")
                    st.write(f"**Telefone:** {client.get('phone', 'N/A')}")
                    st.write(f"**Documento:** {client.get('document', 'N/A')}")
                    st.write(f"**Endereço:** {client.get('address', 'N/A')}")
                    st.write(f"**Cadastrado em:** {client['created_at'][:10]}")
                
                with col2:
                    st.write("**Ações:**")
                    
                    # Edit button
                    if st.button("✏️ Editar", key=f"edit_{client['id']}", use_container_width=True):
                        st.session_state[f"editing_client_{client['id']}"] = True
                        st.rerun()
                    
                    # Delete button
                    if st.button("🗑️ Deletar", key=f"delete_{client['id']}", use_container_width=True, type="secondary"):
                        if st.session_state.get(f"confirm_delete_client_{client['id']}"):
                            try:
                                api_client.delete_client(client['id'])
                                st.success("✅ Cliente deletado com sucesso!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Erro ao deletar: {str(e)}")
                        else:
                            st.session_state[f"confirm_delete_client_{client['id']}"] = True
                            st.warning("⚠️ Clique novamente para confirmar")
                
                # Edit form
                if st.session_state.get(f"editing_client_{client['id']}"):
                    st.divider()
                    st.subheader("Editar Cliente")
                    show_edit_client_form(client)
    
    except Exception as e:
        st.error(f"❌ Erro ao carregar clientes: {str(e)}")


def show_add_client_form():
    """Display form to add new client"""
    st.subheader("Adicionar Novo Cliente")
    
    with st.form("add_client_form"):
        name = st.text_input("Nome *", placeholder="Ex: João Silva")
        email = st.text_input("Email", placeholder="Ex: joao@example.com")
        phone = st.text_input("Telefone", placeholder="Ex: (11) 98765-4321")
        document = st.text_input("CPF/CNPJ", placeholder="Ex: 123.456.789-00")
        address = st.text_area("Endereço", placeholder="Ex: Rua A, 123 - Bairro - Cidade/UF")
        
        submitted = st.form_submit_button("➕ Adicionar Cliente", use_container_width=True, type="primary")
        
        if submitted:
            if not name:
                st.error("❌ Nome é obrigatório!")
                return
            
            try:
                client_data = {
                    "name": name,
                    "email": email if email else None,
                    "phone": phone if phone else None,
                    "document": document if document else None,
                    "address": address if address else None
                }
                
                api_client.create_client(client_data)
                st.success("✅ Cliente adicionado com sucesso!")
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Erro ao adicionar cliente: {str(e)}")


def show_edit_client_form(client):
    """Display form to edit existing client"""
    
    with st.form(f"edit_client_form_{client['id']}"):
        name = st.text_input("Nome", value=client['name'])
        email = st.text_input("Email", value=client.get('email', ''))
        phone = st.text_input("Telefone", value=client.get('phone', ''))
        document = st.text_input("CPF/CNPJ", value=client.get('document', ''))
        address = st.text_area("Endereço", value=client.get('address', ''))
        
        col_a, col_b = st.columns(2)
        with col_a:
            submitted = st.form_submit_button("💾 Salvar", use_container_width=True, type="primary")
        with col_b:
            cancelled = st.form_submit_button("❌ Cancelar", use_container_width=True)
        
        if submitted:
            try:
                client_data = {
                    "name": name,
                    "email": email if email else None,
                    "phone": phone if phone else None,
                    "document": document if document else None,
                    "address": address if address else None
                }
                
                api_client.update_client(client['id'], client_data)
                st.session_state[f"editing_client_{client['id']}"] = False
                st.success("✅ Cliente atualizado com sucesso!")
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Erro ao atualizar cliente: {str(e)}")
        
        if cancelled:
            st.session_state[f"editing_client_{client['id']}"] = False
            st.rerun()
