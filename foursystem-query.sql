CREATE DATABASE system4team;
USE system4team;

-- Tabela de empresas
CREATE TABLE empresas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cnpj VARCHAR(14) UNIQUE NOT NULL,
    endereco VARCHAR(255),
    telefone VARCHAR(15),
    email VARCHAR(100)
);

-- Tabela de cargos
CREATE TABLE cargos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

-- Tabela de funcionários
CREATE TABLE funcionarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cargo INT,
    email VARCHAR(100),
    telefone VARCHAR(15),
    id_empresa INT,
    FOREIGN KEY (cargo) REFERENCES cargos(id),
    FOREIGN KEY (id_empresa) REFERENCES empresas(id)
);

-- Tabela de clientes
CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    endereco VARCHAR(255),
    telefone VARCHAR(15),
    email VARCHAR(100),
    id_empresa INT,
    FOREIGN KEY (id_empresa) REFERENCES empresas(id)
);

-- Tabela de produtos
CREATE TABLE produtos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    preco DECIMAL(10, 2) NOT NULL,
    id_empresa INT,
    FOREIGN KEY (id_empresa) REFERENCES empresas(id)
);

-- Tabela de vendas
CREATE TABLE vendas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT,
    id_funcionario INT,
    id_produto INT,
    id_empresa INT,
    data_venda DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id),
    FOREIGN KEY (id_funcionario) REFERENCES funcionarios(id),
    FOREIGN KEY (id_produto) REFERENCES produtos(id),
    FOREIGN KEY (id_empresa) REFERENCES empresas(id)
);

-- Tabela de pedidos
CREATE TABLE pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT,
    id_produto INT,
    id_funcionario INT,
    quantidade INT NOT NULL,
    preco_total DECIMAL(10, 2) NOT NULL,
    data_pedido DATETIME DEFAULT CURRENT_TIMESTAMP,
    id_empresa INT,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id),
    FOREIGN KEY (id_produto) REFERENCES produtos(id),
    FOREIGN KEY (id_funcionario) REFERENCES funcionarios(id),
    FOREIGN KEY (id_empresa) REFERENCES empresas(id)
);

-- Tabela de usuários
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(255) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    cargo INT,
    imagem VARCHAR(255),
    id_funcionario INT,
    FOREIGN KEY (cargo) REFERENCES cargos(id),
    FOREIGN KEY (id_funcionario) REFERENCES funcionarios(id)
);
