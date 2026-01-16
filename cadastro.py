import streamlit as st
import pandas as pd
from db import conectar

def tela_cadastro():
    st.subheader("👥 Cadastro de Clientes e Fornecedores")

    con = conectar()
    df = pd.read_sql("SELECT * FROM pessoas", con)

    with st.form("form_cadastro"):
        st.write("➕ Novo cadastro / ✏️ Editar existente")

        id_edicao = st.selectbox(
            "Selecionar para editar (opcional)",
            ["Novo"] + df["id"].astype(str).tolist()
        )

        if id_edicao != "Novo":
            pessoa = df[df["id"] == int(id_edicao)].iloc[0]
            tipo = st.selectbox("Tipo", ["Cliente", "Fornecedor"], index=0 if pessoa["tipo"] == "Cliente" else 1)
            nome = st.text_input("Nome / Razão Social", pessoa["nome"])
            documento = st.text_input("Documento", pessoa["documento"])
            email = st.text_input("Email", pessoa["email"])
            telefone = st.text_input("Telefone", pessoa["telefone"])
            endereço = st.text_input("Endereço", pessoa["endereço"])
            ativo = st.checkbox("Ativo", value=bool(pessoa["ativo"]))
        else:
            tipo = st.selectbox("Tipo", ["Cliente", "Fornecedor"])
            nome = st.text_input("Nome / Razão Social")
            documento = st.text_input("Documento")
            email = st.text_input("Email")
            telefone = st.text_input("Telefone")
            endereço = st.text_input("Endereço")
            ativo = st.checkbox("Ativo", value=True)

        salvar = st.form_submit_button("💾 Salvar")

    if salvar:
        cur = con.cursor()
        if id_edicao == "Novo":
            cur.execute("""
                INSERT INTO pessoas (tipo, nome, documento, email, telefone, endereço, ativo)
                VALUES (?,?,?,?,?,?,?)
            """, (tipo, nome, documento, email, telefone, endereço, int(ativo)))
            st.success("Cadastro criado com sucesso")
        else:
            cur.execute("""
                UPDATE pessoas
                SET tipo=?, nome=?, documento=?, email=?, telefone=?, ativo=?, endereço=?
                WHERE id=?
            """, (tipo, nome, documento, email, telefone, edereço, int(ativo), int(id_edicao)))
            st.success("Cadastro atualizado com sucesso")

        con.commit()
        st.rerun()

    st.divider()
    st.subheader("📋 Cadastros existentes")
    st.dataframe(df, use_container_width=True)

    con.close()

