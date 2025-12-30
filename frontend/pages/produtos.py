"""
Página de Gerenciamento de Produtos
"""
import streamlit as st
from services.api import api_client


def show():
    """Display products management page"""
    st.title("📦 Gerenciamento de Produtos")
    
    # Tabs for different views
    tab1, tab2 = st.tabs(["📋 Lista de Produtos", "➕ Adicionar Produto"])
    
    with tab1:
        show_products_list()
    
    with tab2:
        show_add_product_form()


def show_products_list():
    """Display list of products"""
    st.subheader("Lista de Produtos")
    
    try:
        products = api_client.list_products()
        
        if not products:
            st.info("Nenhum produto cadastrado. Adicione um novo produto!")
            return
        
        # Search/filter
        search = st.text_input("🔍 Buscar produto", placeholder="Digite o nome do produto...")
        
        if search:
            products = [p for p in products if search.lower() in p['name'].lower()]
        
        # Display products
        st.write(f"**Total:** {len(products)} produto(s)")
        
        for product in products:
            with st.expander(f"📦 {product['name']} - R$ {product['unit_price']:.2f}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**ID:** {product['id']}")
                    st.write(f"**Nome:** {product['name']}")
                    st.write(f"**SKU:** {product.get('sku', 'N/A')}")
                    st.write(f"**Categoria:** {product.get('category', 'N/A')}")
                    st.write(f"**Descrição:** {product.get('description', 'N/A')}")
                    
                    st.write("---")
                    
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.metric("💰 Preço Venda", f"R$ {product['unit_price']:.2f}")
                    with col_b:
                        st.metric("💵 Preço Custo", f"R$ {product['cost_price']:.2f}")
                    with col_c:
                        margin = product.get('margin', 0) or 0
                        st.metric("📈 Margem", f"{margin:.1f}%")
                    
                    col_d, col_e = st.columns(2)
                    with col_d:
                        stock = product.get('stock_quantity', 0) or 0
                        st.metric("📊 Estoque", stock)
                    with col_e:
                        min_stock = product.get('min_stock', 0) or 0
                        st.metric("⚠️ Estoque Mín.", min_stock)
                
                with col2:
                    st.write("**Ações:**")
                    
                    # Edit button
                    if st.button("✏️ Editar", key=f"edit_{product['id']}", use_container_width=True):
                        st.session_state[f"editing_{product['id']}"] = True
                        st.rerun()
                    
                    # Delete button
                    if st.button("🗑️ Deletar", key=f"delete_{product['id']}", use_container_width=True, type="secondary"):
                        if st.session_state.get(f"confirm_delete_{product['id']}"):
                            try:
                                api_client.delete_product(product['id'])
                                st.success("✅ Produto deletado com sucesso!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Erro ao deletar: {str(e)}")
                        else:
                            st.session_state[f"confirm_delete_{product['id']}"] = True
                            st.warning("⚠️ Clique novamente para confirmar")
                
                # Edit form
                if st.session_state.get(f"editing_{product['id']}"):
                    st.divider()
                    st.subheader("Editar Produto")
                    show_edit_product_form(product)
    
    except Exception as e:
        st.error(f"❌ Erro ao carregar produtos: {str(e)}")


def show_add_product_form():
    """Display form to add new product"""
    st.subheader("Adicionar Novo Produto")
    
    with st.form("add_product_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Nome *", placeholder="Ex: Camiseta Básica")
            sku = st.text_input("SKU", placeholder="Ex: CAM001")
            category = st.text_input("Categoria", placeholder="Ex: Vestuário")
            description = st.text_area("Descrição", placeholder="Descrição detalhada do produto")
        
        with col2:
            unit_price = st.number_input("Preço de Venda (R$) *", min_value=0.01, value=10.0, step=0.01)
            cost_price = st.number_input("Preço de Custo (R$) *", min_value=0.01, value=5.0, step=0.01)
            stock_quantity = st.number_input("Quantidade em Estoque", min_value=0, value=0, step=1)
            min_stock = st.number_input("Estoque Mínimo", min_value=0, value=0, step=1)
        
        # Calculate and display margin
        if cost_price > 0:
            margin = ((unit_price - cost_price) / cost_price) * 100
            st.info(f"📈 Margem calculada: **{margin:.2f}%**")
        
        submitted = st.form_submit_button("➕ Adicionar Produto", use_container_width=True, type="primary")
        
        if submitted:
            if not name:
                st.error("❌ Nome é obrigatório!")
                return
            
            try:
                product_data = {
                    "name": name,
                    "sku": sku if sku else None,
                    "category": category if category else None,
                    "description": description if description else None,
                    "unit_price": unit_price,
                    "cost_price": cost_price,
                    "stock_quantity": stock_quantity,
                    "min_stock": min_stock
                }
                
                api_client.create_product(product_data)
                st.success("✅ Produto adicionado com sucesso!")
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Erro ao adicionar produto: {str(e)}")


def show_edit_product_form(product):
    """Display form to edit existing product"""
    
    with st.form(f"edit_product_form_{product['id']}"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Nome", value=product['name'])
            sku = st.text_input("SKU", value=product.get('sku', ''))
            category = st.text_input("Categoria", value=product.get('category', ''))
            description = st.text_area("Descrição", value=product.get('description', ''))
        
        with col2:
            unit_price = st.number_input("Preço de Venda (R$)", min_value=0.01, value=float(product['unit_price']), step=0.01)
            cost_price = st.number_input("Preço de Custo (R$)", min_value=0.01, value=float(product['cost_price']), step=0.01)
            stock_quantity = st.number_input("Quantidade em Estoque", min_value=0, value=product.get('stock_quantity', 0), step=1)
            min_stock = st.number_input("Estoque Mínimo", min_value=0, value=product.get('min_stock', 0), step=1)
        
        col_a, col_b = st.columns(2)
        with col_a:
            submitted = st.form_submit_button("💾 Salvar", use_container_width=True, type="primary")
        with col_b:
            cancelled = st.form_submit_button("❌ Cancelar", use_container_width=True)
        
        if submitted:
            try:
                product_data = {
                    "name": name,
                    "sku": sku if sku else None,
                    "category": category if category else None,
                    "description": description if description else None,
                    "unit_price": unit_price,
                    "cost_price": cost_price,
                    "stock_quantity": stock_quantity,
                    "min_stock": min_stock
                }
                
                api_client.update_product(product['id'], product_data)
                st.session_state[f"editing_{product['id']}"] = False
                st.success("✅ Produto atualizado com sucesso!")
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Erro ao atualizar produto: {str(e)}")
        
        if cancelled:
            st.session_state[f"editing_{product['id']}"] = False
            st.rerun()
