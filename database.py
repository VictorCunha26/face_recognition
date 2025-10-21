import mysql.connector as mc
from mysql.connector import Error, MySQLConnection
from dotenv import load_dotenv
from os import getenv
from typing import Optional, Any, Tuple, List

class Database:
    def __init__(self) -> None:
        load_dotenv()
        self.host: str = getenv('DB_HOST')
        self.username: str = getenv('DB_USER')
        self.password: str = getenv('DB_PSWD')
        self.database: str = getenv('DB_NAME')
        self.connection: Optional[MySQLConnection] = None
        self._cursor = None

    def conectar(self) -> None:
        """Estabelece uma conexão com o banco de dados."""
        try:
            self.connection = mc.connect(
                host=self.host,
                database=self.database,
                user=self.username,
                password=self.password
            )
            if self.connection.is_connected():
                self._cursor = self.connection.cursor(dictionary=True)
                print('Conexão ao banco de dados realizada com sucesso!')
        except Error as e:
            print(f'Erro de conexão: {e}')
            self.connection = None
            self._cursor = None

    def desconectar(self) -> None:
        """Encerra a conexão com o banco de dados e o cursor, se existirem."""
        try:
            if self._cursor:
                self._cursor.close()
            if self.connection and self.connection.is_connected():
                self.connection.close()
            print('Conexão com o banco de dados encerrada com sucesso!')
        except Error as e:
            print(f"Erro ao encerrar conexão: {e}")

    def executar(self, sql: str, params: Optional[Tuple[Any, ...]] = None) -> Optional[Any]:
        """Executa uma instrução (SELECT/INSERT/UPDATE/DELETE) no banco de dados."""
        if not self.connection or not self._cursor or not self.connection.is_connected():
            raise ConnectionError("Conexão ao banco de dados não estabelecida.")
        

        try:
            self._cursor.execute(sql, params)
            if sql.strip().upper().startswith("SELECT"):
                return self._cursor.fetchall()
            else:
                self.connection.commit()
                return self._cursor.rowcount  # Retorna o número de linhas afetadas
        except Error as e:
            raise RuntimeError(f"Erro ao executar SQL: {e}")

    def fetchone(self) -> Optional[dict]:
        """Retorna o próximo resultado da consulta."""
        if self._cursor:
            return self._cursor.fetchone()
        return None

    def fetchall(self) -> Optional[List[dict]]:
        """Retorna todos os resultados da consulta."""
        if self._cursor:
            return self._cursor.fetchall()
        return None

    def is_connected(self) -> bool:
        """Verifica se a conexão está ativa."""
        return self.connection is not None and self.connection.is_connected()

    def __enter__(self):
        self.conectar()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.desconectar()
        
Database().conectar()

