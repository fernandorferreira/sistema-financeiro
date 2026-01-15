import streamlit as st
import pandas as pd
from db import conectar

def tela_dashboard():
    st.subheader("📊 Dashboard Financeiro")

    con = conectar()

    pagar = pd.read_sql(
        "SELECT valor FROM faturas WHERE tipo = 'Fornecedor'",
        con
    )

    receber = pd.read_sql(
        "SELECT valor FROM faturas WHERE tipo = 'Cliente'",
        con
    )

    con.close()

    total_pagar = pagar["valor"].sum() if not pagar.empty else 0
    total_receber = receber["valor"].sum() if not receber.empty else 0
    saldo = total_receber - total_pagar

    col1, col2, col3 = st.columns(3)
    col1.metric("💸 Total a pagar", f"R$ {total_pagar:,.2f}")
    col2.metric("💰 Total a receber", f"R$ {total_receber:,.2f}")
    col3.metric("📈 Saldo", f"R$ {saldo:,.2f}")

    st.divider()

    st.write("Resumo visual")

    df = pd.DataFrame({
        "Tipo": ["A Pagar", "A Receber"],
        "Valor": [total_pagar, total_receber]
    })

    st.bar_chart(df.set_index("Tipo"))
