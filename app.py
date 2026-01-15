import streamlit as st
from db import criar_tabelas, criar_admin_padrao
from auth import login
from cadastro import tela_cadastro
from faturas import tela_faturas
from dashboard import tela_dashboard
from fluxo_caixa import tela_fluxo_caixa


st.set_page_config(page_title="Sistema Financeiro", layout="wide")

criar_tabelas()
criar_admin_padrao()

if "logado" not in st.session_state:
    login()
else:
    menu = st.sidebar.selectbox(
        "Menu",
        ["Dashboard", "Cadastro", "A Pagar", "A Receber", "Fluxo de Caixa"]
    )

    if menu == "Dashboard":
        tela_dashboard()
    elif menu == "Cadastro":
        tela_cadastro()
    elif menu == "A Pagar":
        tela_faturas("Fornecedor")
    elif menu == "A Receber":
        tela_faturas("Cliente")
    elif menu == "Fluxo de Caixa":
        tela_fluxo_caixa()


