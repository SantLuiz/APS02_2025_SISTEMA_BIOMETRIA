import sqlite3
import os
from verifica import *

# Nome do arquivo do banco de dados
DB_NAME = "biometria.db"

# Conectar (ou criar se não existir)
conn = sqlite3.connect(DB_NAME)
cur = conn.cursor()

# Script SQL de criação das tabelas
sql_script = """
-- Tabela de Informações
CREATE TABLE IF NOT EXISTS INFORMACOES (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    CLASSIFICACAO INTEGER CHECK (CLASSIFICACAO IN (1, 2, 3)),
    LINK TEXT NOT NULL
);

-- Tabela de Usuários
CREATE TABLE IF NOT EXISTS USUARIOS (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NOME TEXT NOT NULL,
    NIVEL_ACESSO INTEGER CHECK (NIVEL_ACESSO IN (1, 2, 3)) NOT NULL
);

-- Tabela de Digitais
CREATE TABLE IF NOT EXISTS DIGITAIS (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    ID_USUARIO INTEGER NOT NULL,
    DESCRICAO_DEDO TEXT NOT NULL,
    TEMPLATE BLOB NOT NULL,
    FOREIGN KEY (ID_USUARIO) REFERENCES USUARIOS (ID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
"""

# Executar o script SQL
cur.executescript(sql_script)

# Confirmar e fechar
conn.commit()

print("✅ Banco de dados 'biometria.db' criado com sucesso!")

cur.execute("INSERT INTO USUARIOS (NOME, NIVEL_ACESSO) VALUES (?, ?)", ("Alice Admin", 3))
cur.execute("INSERT INTO USUARIOS (NOME, NIVEL_ACESSO) VALUES (?, ?)", ("Bruno Operador", 2))
cur.execute("INSERT INTO USUARIOS (NOME, NIVEL_ACESSO) VALUES (?, ?)", ("Carla Leitura", 1))

# Inserção de informações com links reais relacionados ao meio ambiente
cur.execute("INSERT INTO INFORMACOES (CLASSIFICACAO, LINK) VALUES (?, ?)",
            (1, "https://www.theguardian.com/uk/environment"))  # fonte geral de notícias ambientais :contentReference[oaicite:0]{index=0}
cur.execute("INSERT INTO INFORMACOES (CLASSIFICACAO, LINK) VALUES (?, ?)",
            (2, "https://www.epa.gov/system/files/documents/2022-10/EID%20Outline.pdf"))  # documento PDF da EPA :contentReference[oaicite:1]{index=1}
cur.execute("INSERT INTO INFORMACOES (CLASSIFICACAO, LINK) VALUES (?, ?)",
            (3, "https://sustainabledevelopment.un.org/content/documents/Agenda21.pdf"))  # documento da ONU “Agenda 21” :contentReference[oaicite:2]{index=2}

conn.commit()

print("✅ Dados de exemplo inseridos com sucesso!")

# === Base directory ===
BASE_DIR = r"C:\Users\LuizS\Desktop\APS02_2025_SISTEMA_BIOMETRIA\ImpressoesControle\Nivel1"  # Folder containing users user_1, user_2, user_3

# === Loop through users and images ===
for user_folder in os.listdir(BASE_DIR):
    user_path = os.path.join(BASE_DIR, user_folder)
    if not os.path.isdir(user_path):
        continue

    # Extract user ID from folder name (e.g. user_1 -> 1)
    user_id = int(user_folder.split("_")[1])

    for file_name in os.listdir(user_path):
        if not file_name.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tif")):
            continue

        image_path = os.path.join(user_path, file_name)
        print(f"Processing {image_path} ...")

        # Extract minutiae and template
        minutiae = extract_minutiae(image_path)
        template = generate_template(minutiae)

        if template.size == 0:
            print(f"No minutiae found for {image_path}, skipping.")
            continue

        # Convert to bytes
        template_blob = template.tobytes()

        # Use filename (without extension) as finger description
        descricao_dedo = os.path.splitext(file_name)[0]

        # Insert into DIGITAIS table
        cur.execute("""
            INSERT INTO DIGITAIS (ID_USUARIO, DESCRICAO_DEDO, TEMPLATE)
            VALUES (?, ?, ?)
        """, (user_id, descricao_dedo, template_blob))

# Commit and close
conn.commit()
conn.close()
print("✅ Templates successfully generated and stored for Nivel1 users!")
