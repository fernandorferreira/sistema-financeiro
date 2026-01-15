import streamlit as st
import sqlite3
import hashlib
from db import conectar

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def login():
    st.title("🔐 Login")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        con = conectar()
        cur = con.cursor()

        cur.execute(
            "SELECT senha, perfil FROM usuarios WHERE usuario = ?",
            (usuario,)
        )
        resultado = cur.fetchone()
        con.close()

        if resultado and resultado[0] == hash_senha(senha):
            st.session_state["logado"] = True
            st.session_state["usuario"] = usuario
            st.session_state["perfil"] = resultado[1]
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos")
