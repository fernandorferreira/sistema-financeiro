import os
import sqlite3
from datetime import date
import hashlib

DB_PATH = os.path.join(os.getcwd(), "database.db")

def conectar():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def criar_tabelas():
    con = conectar()
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS pessoas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT,
        nome TEXT,
        documento TEXT,
        email TEXT,
        telefone TEXT,
        ativo INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS faturas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT,
        pessoa_id INTEGER,
        documento TEXT,
        emissao DATE,
        vencimento DATE,
        valor REAL,
        status TEXT,
        forma_pagamento TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE,
        senha TEXT,
        perfil TEXT
    )
    """)

    con.commit()
    con.close()

def criar_admin_padrao():
    con = conectar()
    cur = con.cursor()

    senha_hash = hashlib.sha256("123".encode()).hexdigest()

    cur.execute("""
        INSERT OR IGNORE INTO usuarios (usuario, senha, perfil)
        VALUES (?, ?, ?)
    """, ("admin", senha_hash, "admin"))

    con.commit()
    con.close()

def atualizar_status():
    con = conectar()
    cur = con.cursor()
    hoje = date.today()

    cur.execute("""
        UPDATE faturas
        SET status = 'Atrasado'
        WHERE vencimento < ? AND status != 'Pago'
    """, (hoje,))

    con.commit()
    con.close()
