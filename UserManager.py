import sqlite3
import numpy as np
from typing import List, Optional, Tuple

class UserManager:
    """
        CLASSE RESPONSÁVEL POR GERENCIAR OS USUARIOS ADICIONADOS AO BANCO DE DADOS

        Attributes:
            db_path (str): Caminho para o banco de dados.
            conn (sqlite3.Connection): Ativar conexão com o banco de dados.
            cursor (sqlite3.Cursor): Cursor para executar comandos SQL.
    """
    def __init__(self, db_path: str = "biometria.db"):
        """
        Inicializa o gerenciador de usuários e estabelece a conexão com o banco de dados.

        Args:
            db_path (str, opcional): Caminho para o banco de dados SQLite.
                                     O padrão é 'biometria.db'.
        """

        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def list_users(self) -> List[Tuple[int, str]]:
        """
        Retorna uma lista com todos os usuários cadastrados no banco de dados.

        Returns:
            list[tuple]: Lista de tuplas contendo (ID, NOME) de cada usuário.
        """
        self.cursor.execute("SELECT ID, NOME FROM usuarios")
        return self.cursor.fetchall()
    
    def get_user_id(self, username:str) -> Optional[int]:
        """
        Retorna o ID de um usuário a partir do nome informado.

        Args:
            username (str): Nome do usuário.

        Returns:
            int | None: Retorna o ID do usuário se encontrado, caso contrário None.
        """
        self.cursor.execute("SELECT id FROM usuarios WHERE NOME = ?",(username,))
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def get_fingerprints(self, user_id: int) -> List[np.ndarray]:
        """
        Obtém todas as digitais (templates biométricos) associadas a um usuário.

        Cada template é convertido de BLOB para um array NumPy com formato (-1, 3).

        Args:
            user_id (int): ID do usuário cujas digitais serão recuperadas.

        Returns:
            list[np.ndarray]: Lista de templates biométricos do usuário.
        """

        self.cursor.execute("SELECT template FROM DIGITAIS WHERE ID_USUARIO = ?", (user_id,))
        rows = self.cursor.fetchall()
        return [np.frombuffer(row[0], dtype=np.float32).reshape(-1, 3) for row in rows]
    
    def close(self) -> None:
        """
        Encerra a conexão com o banco de dados.

        É importante chamar este método ao finalizar o uso da classe para
        liberar os recursos e evitar corrupção no banco de dados.
        """
        self.conn.close()

    

     
        