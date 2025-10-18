import os
import sqlite3

# Caminho da pasta principal e do banco de dados
base_path = r"C:\Users\LuizS\Desktop\APS02_2025_SISTEMA_BIOMETRIA\ImpressoesControle\GERAL"
db_path = os.path.join(base_path, "fingerprints.db")

# Criação da conexão e tabela
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS fingerprints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        acesslevel INTEGER DEFAULT "1",
        filename TEXT NOT NULL,
        image BLOB NOT NULL
    )
''')
conn.commit()

# Função para ler a imagem como bytes
def read_image_as_blob(file_path):
    with open(file_path, 'rb') as file:
        return file.read()

# Percorrer todas as subpastas (user_1, user_2, etc.)
for user_folder in os.listdir(base_path):
    user_path = os.path.join(base_path, user_folder)
    
    if not os.path.isdir(user_path):
        continue  # ignora arquivos que não são pastas
    
    print(f"📁 Processando {user_folder}...")
    
    # Percorrer todos os arquivos de imagem dentro de cada pasta
    for filename in os.listdir(user_path):
        file_path = os.path.join(user_path, filename)
        
        if not os.path.isfile(file_path):
            continue
        
        # Lê a imagem e insere no banco
        try:
            blob = read_image_as_blob(file_path)
            cursor.execute('''
                INSERT INTO fingerprints (username, filename, image)
                VALUES (?, ?, ?)
            ''', (user_folder, filename, blob))
        except Exception as e:
            print(f"❌ Erro ao processar {filename}: {e}")

conn.commit()
conn.close()
print("✅ Banco de dados criado e todas as imagens foram salvas com sucesso!")
