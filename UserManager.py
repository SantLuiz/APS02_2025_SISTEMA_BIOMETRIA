import sqlite3
import numpy as np
from typing import List, Optional, Tuple
import config

class UserManager:
    """
        CLASSE RESPONSÁVEL POR GERENCIAR OS USUARIOS ADICIONADOS AO BANCO DE DADOS

        Attributes:
            db_path (str): Caminho para o banco de dados.
            conn (sqlite3.Connection): Ativar conexão com o banco de dados.
            cursor (sqlite3.Cursor): Cursor para executar comandos SQL.
    """
    def __init__(self, db_path: Optional[str] = None):
        """
        Inicializa o gerenciador de usuários e estabelece a conexão com o banco de dados.

        Args:
            db_path (str, opcional): Caminho para o banco de dados SQLite.
                                     Se não for fornecido, usa `config.DB_PATH`.
        """
        # resolve default path from config
        if db_path is None:
            # config.DB_PATH is a Path object; sqlite3 accepts path-like objects
            self.db_path = str(config.DB_PATH)
        else:
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
        self.cursor.execute("SELECT id FROM usuarios WHERE NOME = ?",(username.upper(),))
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def get_acess_lvl(self, username:str) -> Optional[int]:
        """
        Retorna o nivel de acesso de um usuário a partir do nome informado.

        Args:
            username (str): Nome do usuário.

        Returns:
            int | None: Retorna o nivel de acesso do usuário se encontrado, caso contrário None.
        """
        self.cursor.execute("SELECT nivel_acesso FROM usuarios WHERE NOME = ?",(username.upper(),))
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
    
    def get_links_by_access(self, user_level: int) -> List: 
        """
        Retorna uma lista de links disponíveis para o nível de acesso do usuário.

        Args
            user_level (int) : Nivel de Acesso do usuário
    
        Returns:
            list: Lista de links que o usuario pode acessar
        """
        
        self.cursor.execute("SELECT LINK FROM INFORMACOES WHERE CLASSIFICACAO <= ?", (user_level,))
        links = [row[0] for row in self.cursor.fetchall()]
        return links

    def close(self) -> None:
        """
        Encerra a conexão com o banco de dados.

        É importante chamar este método ao finalizar o uso da classe para
        liberar os recursos e evitar corrupção no banco de dados.
        """
        self.conn.close()

    

     
        