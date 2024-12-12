-- Criar o banco de dados
CREATE DATABASE treinamento;

-- Criar o usuário com uma senha
CREATE USER aplicacao WITH PASSWORD 'teste123';

-- Conceder privilégios de acesso total ao banco de dados 'treinamento'
GRANT CONNECT ON DATABASE treinamento TO aplicacao;
GRANT ALL PRIVILEGES ON DATABASE treinamento TO aplicacao;
GRANT USAGE ON SCHEMA public TO aplicacao;
GRANT ALL PRIVILEGES ON TABLE cliente TO novo_usuario;

-- Tornar o usuário o dono do banco de dados (opcional)
ALTER DATABASE treinamento OWNER TO aplicacao;