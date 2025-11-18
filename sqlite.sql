-- Criação da tabela 'alunos'
-- SQLite não possui o comando CREATE DATABASE.
-- A base de dados é criada automaticamente quando você tenta
-- abrir um arquivo de banco de dados que não existe.
-- Também não suporta as cláusulas de CHARACTER SET e COLLATE.

-- Remoção da tabela, se existir
DROP TABLE IF EXISTS alunos;

-- Criação da tabela 'alunos'
CREATE TABLE alunos (
  idalunos INTEGER PRIMARY KEY AUTOINCREMENT,
  nome_aluno TEXT NOT NULL,
  data_horario TEXT NOT NULL
);

-- Inserção de dados
INSERT INTO alunos (idalunos, nome_aluno, data_horario) VALUES (1, 'Victor', '2025-11-17 14:28:28');
-- Note: Em SQLite, é comum omitir o 'idalunos' na inserção
-- quando AUTOINCREMENT é usado, mas para manter a consistência
-- com o dump original, ele foi mantido aqui.
-- Alternativa: INSERT INTO alunos (nome_aluno, data_horario) VALUES ('Victor', '2025-11-17 14:28:28');