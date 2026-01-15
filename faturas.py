import streamlit as st
import pandas as pd
from db import conectar, atualizar_status

def tela_faturas(tipo):
    atualizar_status()
    st.subheader(f"📄 Faturas – {tipo}")

    con = conectar()
    pessoas = pd.read_sql(
        "SELECT id, nome FROM pessoas WHERE tipo=? AND ativo=1",
        con, params=(tipo,)
    )

    if pessoas.empty:
        st.info("Cadastre uma pessoa primeiro.")
        con.close()
        return

    faturas = pd.read_sql(
        "SELECT * FROM faturas WHERE tipo=?",
        con, params=(tipo,)
    )

    with st.form("form_fatura"):
        id_edicao = st.selectbox(
            "Selecionar fatura (opcional)",
            ["Nova"] + faturas["id"].astype(str).tolist()
        )

        if id_edicao != "Nova":
            fat = faturas[faturas["id"] == int(id_edicao)].iloc[0]
            pessoa_id = st.selectbox(
                "Pessoa",
                pessoas["id"],
                format_func=lambda x: pessoas[pessoas["id"] == x]["nome"].values[0],
                index=pessoas[pessoas["id"] == fat["pessoa_id"]].index[0]
            )
            documento = st.text_input("Documento", fat["documento"])
            emissao = st.date_input("Emissão", pd.to_datetime(fat["emissao"]))
            vencimento = st.date_input("Vencimento", pd.to_datetime(fat["vencimento"]))
            valor = st.number_input("Valor", value=float(fat["valor"]))
            status = st.selectbox("Status", ["Em aberto", "Pago", "Atrasado"], index=["Em aberto","Pago","Atrasado"].index(fat["status"]))
            forma = st.selectbox("Forma", ["Pix","Boleto","Transferência"], index=["Pix","Boleto","Transferência"].index(fat["forma_pagamento"]))
        else:
            pessoa_id = st.selectbox(
                "Pessoa",
                pessoas["id"],
                format_func=lambda x: pessoas[pessoas["id"] == x]["nome"].values[0]
            )
            documento = st.text_input("Documento")
            emissao = st.date_input("Emissão")
            vencimento = st.date_input("Vencimento")
            valor = st.number_input("Valor", min_value=0.0)
            status = "Em aberto"
            forma = st.selectbox("Forma", ["Pix","Boleto","Transferência"])

        salvar = st.form_submit_button("💾 Salvar")

    if salvar:
        cur = con.cursor()
        if id_edicao == "Nova":
            cur.execute("""
                INSERT INTO faturas
                (tipo, pessoa_id, documento, emissao, vencimento, valor, status, forma_pagamento)
                VALUES (?,?,?,?,?,?,?,?)
            """, (tipo, pessoa_id, documento, emissao, vencimento, valor, status, forma))
            st.success("Fatura criada")
        else:
            cur.execute("""
                UPDATE faturas
                SET pessoa_id=?, documento=?, emissao=?, vencimento=?, valor=?, status=?, forma_pagamento=?
                WHERE id=?
            """, (pessoa_id, documento, emissao, vencimento, valor, status, forma, int(id_edicao)))
            st.success("Fatura atualizada")

        con.commit()
        st.rerun()

    st.divider()
    st.subheader("📋 Lista de faturas")

    df = pd.read_sql("""
        SELECT f.id, p.nome, f.documento, f.vencimento, f.valor, f.status
        FROM faturas f
        JOIN pessoas p ON p.id = f.pessoa_id
        WHERE f.tipo=?
        ORDER BY f.vencimento
    """, con, params=(tipo,))

    st.dataframe(df, use_container_width=True)
    con.close()
