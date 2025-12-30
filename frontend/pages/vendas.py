"""
Página de Gerenciamento de Vendas
"""
import streamlit as st
from services.api import api_client
from datetime import datetime


def show():
    """Display sales management page"""
    st.title("🛒 Gerenciamento de Vendas")
    
    # Tabs for different views
    tab1, tab2 = st.tabs(["📋 Lista de Vendas", "➕ Nova Venda"])
    
    with tab1:
        show_sales_list()
    
    with tab2:
        show_add_sale_form()


def show_sales_list():
    """Display list of sales"""
    st.subheader("Lista de Vendas")
    
    try:
        sales = api_client.list_sales()
        
        if not sales:
            st.info("Nenhuma venda registrada. Adicione uma nova venda!")
            return
        
        # Display sales
        st.write(f"**Total:** {len(sales)} venda(s)")
        
        # Calculate totals
        total_revenue = sum(sale['final_amount'] for sale in sales)
        st.metric("💰 Receita Total", f"R$ {total_revenue:.2f}")
        
        st.divider()
        
        for sale in reversed(sales):  # Show most recent first
            status_emoji = "✅" if sale['status'] == "completed" else "❌"
            with st.expander(f"{status_emoji} Venda #{sale['id']} - R$ {sale['final_amount']:.2f} - {sale['sale_date'][:10]}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**ID:** {sale['id']}")
                    st.write(f"**Data:** {sale['sale_date'][:19].replace('T', ' ')}")
                    st.write(f"**Cliente ID:** {sale['customer_id']}")
                    st.write(f"**Vendedor ID:** {sale.get('seller_id', 'N/A')}")
                    st.write(f"**Status:** {sale['status']}")
                    st.write(f"**Forma de Pagamento:** {sale.get('payment_method', 'N/A')}")
                    st.write(f"**Observações:** {sale.get('notes', 'N/A')}")
                    
                    st.write("---")
                    
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.metric("💵 Total", f"R$ {sale['total_amount']:.2f}")
                    with col_b:
                        st.metric("🏷️ Desconto", f"R$ {sale['discount']:.2f}")
                    with col_c:
                        st.metric("✅ Final", f"R$ {sale['final_amount']:.2f}")
                    
                    # Show items
                    if sale.get('items'):
                        st.write("**Itens da Venda:**")
                        for item in sale['items']:
                            st.write(f"- Produto ID {item['product_id']}: {item['quantity']}x R$ {item['unit_price']:.2f} = R$ {item['subtotal']:.2f}")
                
                with col2:
                    st.write("**Ações:**")
                    
                    # View details button
                    if st.button("👁️ Detalhes", key=f"view_{sale['id']}", use_container_width=True):
                        show_sale_details(sale['id'])
                    
                    # Cancel button (only for completed sales)
                    if sale['status'] == "completed":
                        if st.button("❌ Cancelar", key=f"cancel_{sale['id']}", use_container_width=True, type="secondary"):
                            if st.session_state.get(f"confirm_cancel_{sale['id']}"):
                                try:
                                    api_client.cancel_sale(sale['id'])
                                    st.success("✅ Venda cancelada e estoque restaurado!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"❌ Erro ao cancelar: {str(e)}")
                            else:
                                st.session_state[f"confirm_cancel_{sale['id']}"] = True
                                st.warning("⚠️ Clique novamente para confirmar")
    
    except Exception as e:
        st.error(f"❌ Erro ao carregar vendas: {str(e)}")


def show_add_sale_form():
    """Display form to add new sale"""
    st.subheader("Registrar Nova Venda")
    
    try:
        # Load clients and products for selection
        clients = api_client.list_clients()
        products = api_client.list_products()
        sellers = api_client.list_sellers()
        
        if not clients:
            st.warning("⚠️ Você precisa cadastrar clientes primeiro!")
            return
        
        if not products:
            st.warning("⚠️ Você precisa cadastrar produtos primeiro!")
            return
        
        with st.form("add_sale_form"):
            # Customer selection
            client_options = {f"{c['id']} - {c['name']}": c['id'] for c in clients}
            selected_client = st.selectbox("Cliente *", options=list(client_options.keys()))
            customer_id = client_options[selected_client]
            
            # Seller selection (optional)
            seller_options = {"Nenhum": None}
            seller_options.update({f"{s['id']} - {s['name']}": s['id'] for s in sellers})
            selected_seller = st.selectbox("Vendedor", options=list(seller_options.keys()))
            seller_id = seller_options[selected_seller]
            
            # Payment method
            payment_method = st.selectbox(
                "Forma de Pagamento",
                ["Dinheiro", "Cartão de Crédito", "Cartão de Débito", "PIX", "Boleto"]
            )
            
            # Discount
            discount = st.number_input("Desconto (R$)", min_value=0.0, value=0.0, step=0.01)
            
            # Notes
            notes = st.text_area("Observações", placeholder="Observações sobre a venda...")
            
            st.divider()
            st.subheader("Itens da Venda")
            
            # Initialize items in session state if not exists
            if 'sale_items' not in st.session_state:
                st.session_state.sale_items = []
            
            # Add item section
            col1, col2, col3, col4 = st.columns([3, 1, 2, 1])
            
            with col1:
                product_options = {f"{p['id']} - {p['name']} (Estoque: {p.get('stock_quantity', 0)})": p for p in products}
                selected_product = st.selectbox("Produto", options=list(product_options.keys()), key="product_select")
            
            with col2:
                quantity = st.number_input("Qtd", min_value=1, value=1, step=1, key="quantity_input")
            
            with col3:
                product = product_options[selected_product]
                unit_price = st.number_input("Preço Unit. (R$)", min_value=0.01, value=float(product['unit_price']), step=0.01, key="price_input")
            
            with col4:
                st.write("")
                st.write("")
                if st.form_submit_button("➕ Adicionar", use_container_width=True):
                    # Check stock
                    if quantity > product.get('stock_quantity', 0):
                        st.error(f"❌ Estoque insuficiente! Disponível: {product.get('stock_quantity', 0)}")
                    else:
                        st.session_state.sale_items.append({
                            "product_id": product['id'],
                            "product_name": product['name'],
                            "quantity": quantity,
                            "unit_price": unit_price,
                            "subtotal": quantity * unit_price
                        })
                        st.rerun()
            
            # Display added items
            if st.session_state.sale_items:
                st.write("**Itens Adicionados:**")
                
                total_sale = 0
                for idx, item in enumerate(st.session_state.sale_items):
                    col_a, col_b = st.columns([4, 1])
                    with col_a:
                        st.write(f"**{item['product_name']}** - {item['quantity']}x R$ {item['unit_price']:.2f} = R$ {item['subtotal']:.2f}")
                    with col_b:
                        if st.form_submit_button("🗑️", key=f"remove_{idx}", use_container_width=True):
                            st.session_state.sale_items.pop(idx)
                            st.rerun()
                    total_sale += item['subtotal']
                
                st.divider()
                col_total1, col_total2, col_total3 = st.columns(3)
                with col_total1:
                    st.metric("Subtotal", f"R$ {total_sale:.2f}")
                with col_total2:
                    st.metric("Desconto", f"R$ {discount:.2f}")
                with col_total3:
                    final = total_sale - discount
                    st.metric("Total Final", f"R$ {final:.2f}")
            
            # Submit sale
            st.divider()
            col_submit1, col_submit2 = st.columns(2)
            
            with col_submit1:
                submitted = st.form_submit_button("✅ Finalizar Venda", use_container_width=True, type="primary")
            
            with col_submit2:
                cancelled = st.form_submit_button("❌ Cancelar", use_container_width=True)
            
            if submitted:
                if not st.session_state.sale_items:
                    st.error("❌ Adicione pelo menos um item à venda!")
                    return
                
                try:
                    # Prepare sale data
                    sale_data = {
                        "customer_id": customer_id,
                        "seller_id": seller_id,
                        "discount": discount,
                        "payment_method": payment_method.lower().replace(" ", "_"),
                        "status": "completed",
                        "notes": notes if notes else None,
                        "items": [
                            {
                                "product_id": item['product_id'],
                                "quantity": item['quantity'],
                                "unit_price": item['unit_price']
                            }
                            for item in st.session_state.sale_items
                        ]
                    }
                    
                    api_client.create_sale(sale_data)
                    st.session_state.sale_items = []  # Clear items
                    st.success("✅ Venda registrada com sucesso!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Erro ao registrar venda: {str(e)}")
            
            if cancelled:
                st.session_state.sale_items = []
                st.rerun()
    
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {str(e)}")


def show_sale_details(sale_id):
    """Display detailed view of a sale"""
    try:
        sale = api_client.get_sale(sale_id)
        
        st.write("### Detalhes da Venda")
        st.json(sale)
        
    except Exception as e:
        st.error(f"❌ Erro ao carregar detalhes: {str(e)}")
