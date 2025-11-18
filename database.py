import sqlite3
from sqlite3 import Error, Connection, Cursor
from typing import Optional, Any, Tuple, List

# Dependências de MySQL/dotenv removidas.
# O SQLite é nativo do Python (sqlite3).

class Database:
    """
    Classe para gerenciar a conexão e operações com um banco de dados SQLite.
    
    A conexão é estabelecida com um arquivo local. Os resultados SELECT 
    são retornados como objetos sqlite3.Row, que se comportam como dicionários.
    """
    def __init__(self, db_file: str = 'database.sqlite') -> None:
        """
        Inicializa com o nome do arquivo do banco de dados SQLite.
        Por padrão, 'database.sqlite'.
        """
        self.db_file: str = db_file
        self.connection: Optional[Connection] = None
        self._cursor: Optional[Cursor] = None

    def conectar(self) -> None:
        """Estabelece uma conexão com o banco de dados SQLite."""
        try:
            # Conecta ou cria o arquivo DB
            self.connection = sqlite3.connect(self.db_file)
            
            # Configura para que os resultados SELECT venham como dicionários (Row objects)
            self.connection.row_factory = sqlite3.Row
            
            self._cursor = self.connection.cursor()
            print(f'Conexão ao banco de dados SQLite ({self.db_file}) realizada com sucesso!')
            
        except Error as e:
            print(f'Erro de conexão com SQLite: {e}')
            self.connection = None
            self._cursor = None

    def desconectar(self) -> None:
        """Encerra a conexão com o banco de dados e o cursor, se existirem."""
        try:
            if self._cursor:
                self._cursor.close()
            if self.connection:
                self.connection.close()
            print('Conexão com o banco de dados SQLite encerrada com sucesso!')
        except Error as e:
            print(f"Erro ao encerrar conexão com SQLite: {e}")

    def executar(self, sql: str, params: Optional[Tuple[Any, ...]] = None) -> Optional[Any]:
        """
        Executa uma instrução SQL no banco de dados.
        Retorna os resultados para SELECT ou o número de linhas afetadas para outros comandos.
        """
        if not self.connection or not self._cursor:
            raise ConnectionError("Conexão ao banco de dados não estabelecida.")
        
        try:
            # No SQLite, o placeholder é '?'
            self._cursor.execute(sql, params or ())

            sql_upper = sql.strip().upper()

            if sql_upper.startswith("SELECT"):
                # Retorna todos os resultados da consulta
                return self._cursor.fetchall()
            else:
                # Comandos que modificam dados (INSERT, UPDATE, DELETE, CREATE, DROP) precisam de commit
                self.connection.commit()
                # Retorna o número de linhas afetadas
                return self._cursor.rowcount 

        except Error as e:
            if self.connection:
                self.connection.rollback()
            raise RuntimeError(f"Erro ao executar SQL no SQLite: {e}")

    def fetchone(self) -> Optional[sqlite3.Row]:
        """Retorna o próximo resultado da consulta (como objeto Row)."""
        if self._cursor:
            return self._cursor.fetchone()
        return None

    def fetchall(self) -> Optional[List[sqlite3.Row]]:
        """Retorna todos os resultados da consulta (como lista de objetos Row)."""
        if self._cursor:
            return self._cursor.fetchall()
        return None

    def is_connected(self) -> bool:
        """Verifica se a conexão está ativa."""
        return self.connection is not None

    def __enter__(self):
        self.conectar()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.desconectar()