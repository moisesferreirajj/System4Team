-- --------------------------------------------------------
-- Servidor:                     127.0.0.1
-- Versão do servidor:           10.4.22-MariaDB - mariadb.org binary distribution
-- OS do Servidor:               Win64
-- HeidiSQL Versão:              12.8.0.6908
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Copiando estrutura do banco de dados para system4team
CREATE DATABASE IF NOT EXISTS `system4team` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE `system4team`;

-- Copiando estrutura para tabela system4team.cargos
CREATE TABLE IF NOT EXISTS `cargos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;

-- Copiando dados para a tabela system4team.cargos: ~5 rows (aproximadamente)
DELETE FROM `cargos`;
INSERT INTO `cargos` (`id`, `nome`) VALUES
	(1, 'Tech-Lead'),
	(2, 'Senior'),
	(3, 'CEO'),
	(4, 'CTO'),
	(5, 'Cliente');

-- Copiando estrutura para tabela system4team.clientes
CREATE TABLE IF NOT EXISTS `clientes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(255) NOT NULL,
  `cpf` varchar(14) NOT NULL,
  `endereco` varchar(255) DEFAULT NULL,
  `telefone` varchar(15) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `id_empresa` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cpf` (`cpf`),
  KEY `id_empresa` (`id_empresa`),
  CONSTRAINT `clientes_ibfk_1` FOREIGN KEY (`id_empresa`) REFERENCES `empresas` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Copiando dados para a tabela system4team.clientes: ~0 rows (aproximadamente)
DELETE FROM `clientes`;

-- Copiando estrutura para tabela system4team.empresas
CREATE TABLE IF NOT EXISTS `empresas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(255) NOT NULL,
  `cnpj` varchar(14) NOT NULL,
  `endereco` varchar(255) DEFAULT NULL,
  `telefone` varchar(15) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cnpj` (`cnpj`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

-- Copiando dados para a tabela system4team.empresas: ~0 rows (aproximadamente)
DELETE FROM `empresas`;
INSERT INTO `empresas` (`id`, `nome`, `cnpj`, `endereco`, `telefone`, `email`) VALUES
	(1, 'SystemForTeam', '11111111111111', 'Rua Inexistente 147, Joinville SC', '47991270120', 'nubmoises321@gmail.com');

-- Copiando estrutura para tabela system4team.funcionarios
CREATE TABLE IF NOT EXISTS `funcionarios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(255) NOT NULL,
  `cargo` int(11) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `telefone` varchar(15) DEFAULT NULL,
  `id_empresa` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cargo` (`cargo`),
  KEY `id_empresa` (`id_empresa`),
  CONSTRAINT `funcionarios_ibfk_1` FOREIGN KEY (`cargo`) REFERENCES `cargos` (`id`),
  CONSTRAINT `funcionarios_ibfk_2` FOREIGN KEY (`id_empresa`) REFERENCES `empresas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

-- Copiando dados para a tabela system4team.funcionarios: ~0 rows (aproximadamente)
DELETE FROM `funcionarios`;
INSERT INTO `funcionarios` (`id`, `nome`, `cargo`, `email`, `telefone`, `id_empresa`) VALUES
	(1, 'Moises João Ferreira', 1, 'nubmoises@gmail.com', '47991270120', 1);

-- Copiando estrutura para tabela system4team.pedidos
CREATE TABLE IF NOT EXISTS `pedidos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_cliente` int(11) DEFAULT NULL,
  `id_produto` int(11) DEFAULT NULL,
  `id_funcionario` int(11) DEFAULT NULL,
  `quantidade` int(11) NOT NULL,
  `preco_total` decimal(10,2) NOT NULL,
  `data_pedido` datetime DEFAULT current_timestamp(),
  `id_empresa` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_cliente` (`id_cliente`),
  KEY `id_produto` (`id_produto`),
  KEY `id_funcionario` (`id_funcionario`),
  KEY `id_empresa` (`id_empresa`),
  CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id`),
  CONSTRAINT `pedidos_ibfk_2` FOREIGN KEY (`id_produto`) REFERENCES `produtos` (`id`),
  CONSTRAINT `pedidos_ibfk_3` FOREIGN KEY (`id_funcionario`) REFERENCES `funcionarios` (`id`),
  CONSTRAINT `pedidos_ibfk_4` FOREIGN KEY (`id_empresa`) REFERENCES `empresas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

-- Copiando dados para a tabela system4team.pedidos: ~1 rows (aproximadamente)
DELETE FROM `pedidos`;
INSERT INTO `pedidos` (`id`, `id_cliente`, `id_produto`, `id_funcionario`, `quantidade`, `preco_total`, `data_pedido`, `id_empresa`) VALUES
	(1, NULL, NULL, NULL, 1, 220.00, '2024-10-31 15:56:02', NULL);

-- Copiando estrutura para tabela system4team.produtos
CREATE TABLE IF NOT EXISTS `produtos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(255) NOT NULL,
  `descricao` text DEFAULT NULL,
  `preco` decimal(10,2) NOT NULL,
  `id_empresa` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_empresa` (`id_empresa`),
  CONSTRAINT `produtos_ibfk_1` FOREIGN KEY (`id_empresa`) REFERENCES `empresas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

-- Copiando dados para a tabela system4team.produtos: ~1 rows (aproximadamente)
DELETE FROM `produtos`;
INSERT INTO `produtos` (`id`, `nome`, `descricao`, `preco`, `id_empresa`) VALUES
	(1, 'Site', 'Um site desenvolvido', 1000.00, 1);

-- Copiando estrutura para tabela system4team.usuarios
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usuario` varchar(255) NOT NULL,
  `senha` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `cargo` int(11) DEFAULT NULL,
  `imagem` varchar(255) DEFAULT NULL,
  `id_funcionario` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cargo` (`cargo`),
  KEY `id_funcionario` (`id_funcionario`),
  CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`cargo`) REFERENCES `cargos` (`id`),
  CONSTRAINT `usuarios_ibfk_2` FOREIGN KEY (`id_funcionario`) REFERENCES `funcionarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;

-- Copiando dados para a tabela system4team.usuarios: ~5 rows (aproximadamente)
DELETE FROM `usuarios`;
INSERT INTO `usuarios` (`id`, `usuario`, `senha`, `email`, `cargo`, `imagem`, `id_funcionario`) VALUES
	(1, 'moises', '$2b$12$Vccc7Rwb1x4C5RnjvRHXIeUSJ57.n1Gl/wGcdGlUvxN.B/uJBlEe6', 'nubmoises@gmail.com', 1, NULL, 1),
	(2, 'igor', '$2b$12$Vccc7Rwb1x4C5RnjvRHXIeUSJ57.n1Gl/wGcdGlUvxN.B/uJBlEe6', 'igor@gmail.com', 2, NULL, NULL),
	(3, 'mark', '$2b$12$Vccc7Rwb1x4C5RnjvRHXIeUSJ57.n1Gl/wGcdGlUvxN.B/uJBlEe6', 'mark@gmail.com', 2, NULL, NULL),
	(4, 'yohan', '$2b$12$wouY5sgcHGuw9b7oKGJ9aurC/iYBkA6f53GK5DUSC1d00BlY4p9cS', 'yohan@gmail.com', NULL, NULL, NULL),
	(5, 'senhorinha', '$2b$12$R4AFjGq1m/p6fqUSY2hIxekvKKrNHOyUIGizntzEfzjMpFewaBJ/e', 'marciosenhorinha@gmail.com', NULL, NULL, NULL);

-- Copiando estrutura para tabela system4team.vendas
CREATE TABLE IF NOT EXISTS `vendas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_cliente` int(11) DEFAULT NULL,
  `id_funcionario` int(11) DEFAULT NULL,
  `id_produto` int(11) DEFAULT NULL,
  `id_empresa` int(11) DEFAULT NULL,
  `data_venda` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `id_cliente` (`id_cliente`),
  KEY `id_funcionario` (`id_funcionario`),
  KEY `id_produto` (`id_produto`),
  KEY `id_empresa` (`id_empresa`),
  CONSTRAINT `vendas_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id`),
  CONSTRAINT `vendas_ibfk_2` FOREIGN KEY (`id_funcionario`) REFERENCES `funcionarios` (`id`),
  CONSTRAINT `vendas_ibfk_3` FOREIGN KEY (`id_produto`) REFERENCES `produtos` (`id`),
  CONSTRAINT `vendas_ibfk_4` FOREIGN KEY (`id_empresa`) REFERENCES `empresas` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Copiando dados para a tabela system4team.vendas: ~0 rows (aproximadamente)
DELETE FROM `vendas`;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
