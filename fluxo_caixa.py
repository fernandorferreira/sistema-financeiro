import streamlit as st
import pandas as pd
from db import conectar

def tela_fluxo_caixa():
    st.subheader("📆 Fluxo de Caixa Mensal")

    con = conectar()

    df = pd.read_sql("""
        SELECT
            tipo,
            valor,
            vencimento,
            status
        FROM faturas
    """, con)

    con.close()

    if df.empty:
        st.info("Nenhuma fatura cadastrada.")
        return

    df["vencimento"] = pd.to_datetime(df["vencimento"])
    df["ano"] = df["vencimento"].dt.year
    df["mes"] = df["vencimento"].dt.month

    col1, col2 = st.columns(2)

    with col1:
        ano = st.selectbox("Ano", sorted(df["ano"].unique(), reverse=True))
    with col2:
        mes = st.selectbox(
            "Mês",
            {
                1: "Janeiro", 2: "Fevereiro", 3: "Março",
                4: "Abril", 5: "Maio", 6: "Junho",
                7: "Julho", 8: "Agosto", 9: "Setembro",
                10: "Outubro", 11: "Novembro", 12: "Dezembro"
            }.items(),
            format_func=lambda x: x[1]
        )[0]

    df_mes = df[(df["ano"] == ano) & (df["mes"] == mes)]

    entradas = df_mes[df_mes["tipo"] == "Cliente"]["valor"].sum()
    saidas = df_mes[df_mes["tipo"] == "Fornecedor"]["valor"].sum()
    saldo = entradas - saidas

    c1, c2, c3 = st.columns(3)
    c1.metric("💰 Entradas", f"R$ {entradas:,.2f}")
    c2.metric("💸 Saídas", f"R$ {saidas:,.2f}")
    c3.metric("📊 Saldo do mês", f"R$ {saldo:,.2f}")

    st.divider()

    resumo = pd.DataFrame({
        "Categoria": ["Entradas", "Saídas"],
        "Valor": [entradas, saidas]
    })

    st.bar_chart(resumo.set_index("Categoria"))

    st.divider()
    st.subheader("📋 Detalhamento do mês")
    st.dataframe(
        df_mes[["tipo", "valor", "vencimento", "status"]],
        use_container_width=True
    )
