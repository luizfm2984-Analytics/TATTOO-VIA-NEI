"""
Sistema de Gestão - Frontend Streamlit
"""
import streamlit as st
from services.api import api_client

# Configure page
st.set_page_config(
    page_title="Sistema de Gestão",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None
if "token" not in st.session_state:
    st.session_state.token = None


def login():
    """Display login page"""
    st.title("🔐 Login - Sistema de Gestão")
    
    st.markdown("""
    Bem-vindo ao Sistema de Gestão! 
    
    **Nota:** Como a API ainda não possui autenticação JWT implementada, 
    este é um login simulado para demonstração da interface.
    """)
    
    with st.form("login_form"):
        username = st.text_input("Usuário", placeholder="Digite seu usuário")
        password = st.text_input("Senha", type="password", placeholder="Digite sua senha")
        submit = st.form_submit_button("Entrar", use_container_width=True)
        
        if submit:
            if username and password:
                # Simulated login - check API connectivity
                try:
                    api_client.health_check()
                    
                    # Simulate successful login
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.token = "simulated-token"  # Placeholder for future JWT
                    api_client.set_token(st.session_state.token)
                    
                    st.success("✅ Login realizado com sucesso!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Erro ao conectar à API: {str(e)}")
                    st.info("""
                    **Como resolver:**
                    1. Certifique-se de que a API está rodando: `docker-compose up -d`
                    2. Verifique se a URL está correta no arquivo `.env`
                    3. URL padrão: http://localhost:8000
                    """)
            else:
                st.warning("⚠️ Por favor, preencha usuário e senha")
    
    # Display API status
    st.divider()
    st.subheader("Status da API")
    
    try:
        health = api_client.health_check()
        st.success(f"✅ API Online: {health.get('status', 'healthy')}")
    except Exception as e:
        st.error(f"❌ API Offline: {str(e)}")


def main_app():
    """Display main application"""
    
    # Sidebar navigation
    with st.sidebar:
        st.title("📊 Sistema de Gestão")
        st.write(f"👤 Usuário: **{st.session_state.username}**")
        st.divider()
        
        # Navigation menu
        page = st.radio(
            "Navegação",
            ["🏠 Dashboard", "📦 Produtos", "👥 Clientes", "🛒 Vendas"],
            label_visibility="collapsed"
        )
        
        st.divider()
        
        if st.button("🚪 Sair", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.session_state.token = None
            st.rerun()
    
    # Route to selected page
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "📦 Produtos":
        from pages import produtos
        produtos.show()
    elif page == "👥 Clientes":
        from pages import clientes
        clientes.show()
    elif page == "🛒 Vendas":
        from pages import vendas
        vendas.show()


def show_dashboard():
    """Display dashboard page"""
    st.title("🏠 Dashboard")
    
    st.markdown("""
    Bem-vindo ao Sistema de Gestão!
    
    Use o menu lateral para navegar entre as diferentes funcionalidades:
    - **Produtos**: Gerenciar catálogo de produtos
    - **Clientes**: Gerenciar cadastro de clientes
    - **Vendas**: Registrar e visualizar vendas
    """)
    
    # Display statistics
    col1, col2, col3 = st.columns(3)
    
    try:
        products = api_client.list_products()
        clients = api_client.list_clients()
        sales = api_client.list_sales()
        
        with col1:
            st.metric("📦 Total de Produtos", len(products))
        
        with col2:
            st.metric("👥 Total de Clientes", len(clients))
        
        with col3:
            st.metric("🛒 Total de Vendas", len(sales))
        
        # Recent sales
        if sales:
            st.subheader("📊 Últimas Vendas")
            
            for sale in sales[-5:]:  # Show last 5 sales
                with st.expander(f"Venda #{sale['id']} - R$ {sale['final_amount']:.2f}"):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.write(f"**Data:** {sale['sale_date'][:10]}")
                        st.write(f"**Total:** R$ {sale['total_amount']:.2f}")
                        st.write(f"**Desconto:** R$ {sale['discount']:.2f}")
                    with col_b:
                        st.write(f"**Final:** R$ {sale['final_amount']:.2f}")
                        st.write(f"**Status:** {sale['status']}")
                        st.write(f"**Pagamento:** {sale['payment_method'] or 'N/A'}")
        
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")


# Main execution
if __name__ == "__main__":
    if not st.session_state.authenticated:
        login()
    else:
        main_app()
